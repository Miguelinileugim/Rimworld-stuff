import xml.etree.ElementTree as ET
import csv
from pathlib import Path

# -------- CONFIG --------
RIMWORLD_FOLDER = "C:\\Applications\\RimWorld"
# --------


# Classes
class plantsEntry:
    def __init__(self):
        # Base stats
        self.parent = ""
        self.name = ""
        self.harvestNutrition = 0
        self.lifespanDaysPerGrowDays = ""
        self.fertilityMin = 0
        self.fertilitySensitivity = 0
        self.sowWork = ""
        self.sowMinSkill = ""
        self.harvestWork = ""
        self.harvestedThingDef = ""
        self.harvestYield = 0
        self.hydroponic = ""
        self.growDays = 0
        # Derived stats
        self.daytimeGrowDays = ""
        self.yieldSand = ""
        self.yieldDirt = ""
        self.yieldSoil = ""
        self.yieldRich = ""
        self.yieldHydroponics = ""
        self.yieldEcosystem = ""
        # Nutrition per day
        self.nutritionYieldSand = ""
        self.nutritionYieldDirt = ""
        self.nutritionYieldSoil = ""
        self.nutritionYieldRich = ""
        self.nutritionYieldHydroponics = ""
        self.nutritionYieldEcosystem = ""


def scanFiles(rimworldFolderPath):
    XMLFilePathList = []
    defIndex = {}
    # Excludes older versions
    excludedKeywords = ["1.0", "1.1", "1.2", "1.3", "1.4"]
    # Exports every single xml into a single variable
    for XMLFilePath in Path(rimworldFolderPath).rglob("**/*.xml"):
        if not any(keyword in str(XMLFilePath) for keyword in excludedKeywords):
            XMLFilePathList.append(XMLFilePath)
            try:
                tree = ET.parse(XMLFilePath)
                root = tree.getroot()
                for element1 in root:
                    for element2 in element1:
                        if element2.tag == "defName":
                            defIndex[element2.text] = XMLFilePath
            except Exception:
                pass
    return (XMLFilePathList, defIndex)


# Figures out harvest nutrition from a harvestable's def
def getHarvestableNutrition(defIndex, harvestableDef):
    harvestNutrition = 0
    ingestible = False
    harvestNutritionSpecified = False
    tree = ET.parse(defIndex[harvestableDef])
    root = tree.getroot()
    for element1 in root:  # ThingDef
        for element2 in element1:  # e.g defName, statBase
            if element2.text == harvestableDef:
                for element2 in element1:  # e.g defName, statBase
                    match element2.tag:
                        case "statBases":
                            for element3 in element2:
                                if element3.tag == "Nutrition":
                                    harvestNutrition = element3.text
                                    harvestNutritionSpecified = True
                        case "ingestible":
                            ingestible = True
    harvestNutrition = (
        0.05 if ingestible and not harvestNutritionSpecified else harvestNutrition
    )
    return harvestNutrition


def yieldCalculator(entry, type, soil):
    soilFertility = 0
    match soil:
        case "sand":
            soilFertility = 0.1
        case "dirt":
            soilFertility = 0.7
        case "soil":
            soilFertility = 1
        case "rich":
            soilFertility = 1.4
        case "hydroponics":
            soilFertility = 2.8
        case "ecosystem":
            soilFertility = 3.5

    fertileGrowth = float(entry.fertilitySensitivity) * soilFertility
    infertileGrowth = 1 - float(entry.fertilitySensitivity)
    growthRate = fertileGrowth + infertileGrowth

    match type:
        case "base":
            return float(entry.harvestYield) * growthRate
        case "nutrition":
            return (
                float(entry.harvestYield) * float(entry.harvestNutrition) * growthRate
            )


# Extracts defs
def extractDef(defFilePath, defIndex, sheets):
    sheetName = "undefined"

    try:
        tree = ET.parse(defFilePath)
        root = tree.getroot()
        for element1 in root:  # ThingDef
            for element2 in element1:  # e.g label
                match element2.tag:
                    case "plant":
                        sheetName = "plants"
    except Exception:
        pass

    match sheetName:
        case "plants":
            for element1 in root:  # ThingDef
                entry = plantsEntry()
                for element2 in element1:  # e.g label
                    match element2.tag:
                        case "label":
                            entry.name = element2.text
                        case "plant":
                            for element3 in element2:
                                match element3.tag:
                                    case "fertilitySensitivity":
                                        entry.fertilitySensitivity = element3.text
                                    case "harvestedThingDef":
                                        entry.harvestedThingDef = element3.text
                                        entry.harvestNutrition = (
                                            getHarvestableNutrition(
                                                defIndex, element3.text
                                            )
                                        )
                                    case "harvestYield":
                                        entry.harvestYield = element3.text
                                    case "sowTags":
                                        for element4 in element3:
                                            match element4.text:
                                                case "Hydroponic":
                                                    entry.hydroponic = True
                                    case "growDays":
                                        entry.growDays = element3.text
                # Derived stats
                entry.daytimeGrowDays = float(entry.growDays) / (13 / 24)
                entry.yieldSand = yieldCalculator(entry, "base", "sand")
                entry.yieldDirt = yieldCalculator(entry, "base", "dirt")
                entry.yieldSoil = yieldCalculator(entry, "base", "soil")
                entry.yieldRich = yieldCalculator(entry, "base", "rich")
                entry.yieldHydroponics = yieldCalculator(entry, "base", "hydroponics")
                entry.yieldEcosystem = yieldCalculator(entry, "base", "ecosystem")
                entry.nutritionYieldSand = yieldCalculator(entry, "nutrition", "sand")
                entry.nutritionYieldDirt = yieldCalculator(entry, "nutrition", "dirt")
                entry.nutritionYieldSoil = yieldCalculator(entry, "nutrition", "soil")
                entry.nutritionYieldRich = yieldCalculator(entry, "nutrition", "rich")
                entry.nutritionYieldHydroponics = yieldCalculator(
                    entry, "nutrition", "hydroponics"
                )
                entry.nutritionYieldEcosystem = yieldCalculator(
                    entry, "nutrition", "ecosystem"
                )
                sheets[sheetName].append(entry)


# Processes defs
def processDefs(sheet, sheets):
    pass


# Defines variables for each sheet
sheets = {
    "plants": [],
    "materials": [],
    "weapons": [],
    "armors": [],
    "animals": [],
    "vehicles": [],
}

# Code execution starts here
if __name__ == "__main__":
    # Get XML and def
    XMLFilePathList, defIndex = scanFiles(RIMWORLD_FOLDER)
    # print(defIndex)

    # Extract every def
    for XMLFilePath in XMLFilePathList:
        extractDef(XMLFilePath, defIndex, sheets)

    for sheetName in sheets.keys():
        sheet = sheets[sheetName]
        # Process defs to get more info
        processDefs(sheet, sheets)

        # Write the CSVs
        with open(sheetName + ".csv", "w", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)
            writer.writerow(
                [
                    "Name",
                    "Harvest Nutrition",
                    "Fertility min",
                    "Fertility Sensitivity",
                    "Harvest Yield",
                    "Hydroponic",
                    "Grow Days",
                    "Daytime Grow Days",
                    # Yield per day
                    "yieldSand",
                    "yieldDirt",
                    "yieldSoil",
                    "yieldRich",
                    "yieldHydroponics",
                    "yieldEcosystem",
                    # Nutrition per day
                    "nutritionYieldSand",
                    "nutritionYieldDirt",
                    "nutritionYieldSoil",
                    "nutritionYieldRich",
                    "nutritionYieldHydroponics",
                    "nutritionYieldEcosystem",
                ]
            )
            for entry in sheet:
                writer.writerow(
                    [
                        entry.name,
                        entry.harvestNutrition,
                        entry.fertilityMin,
                        entry.fertilitySensitivity,
                        entry.harvestYield,
                        entry.hydroponic,
                        entry.growDays,
                        entry.daytimeGrowDays,
                        entry.yieldSand,
                        entry.yieldDirt,
                        entry.yieldSoil,
                        entry.yieldRich,
                        entry.yieldHydroponics,
                        entry.yieldEcosystem,
                        entry.nutritionYieldSand,
                        entry.nutritionYieldDirt,
                        entry.nutritionYieldSoil,
                        entry.nutritionYieldRich,
                        entry.nutritionYieldHydroponics,
                        entry.nutritionYieldEcosystem,
                    ]
                )
