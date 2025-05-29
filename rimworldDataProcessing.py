import xml.etree.ElementTree as ET
import csv
from pathlib import Path

# -------- CONFIG --------
RIMWORLD_FOLDER = "C:\\Applications\\RimWorld"
# --------


# Classes
class PlantBaseNonEdible:
    def __init__(self):
        self.parent = "undefined"
        self.name = "undefinedPlant"
        self.nutrition = 0
        self.lifespanDaysPerGrowDays = 0
        self.fertilityMin = 0.7
        self.fertilitySensitivity = 1
        self.sowWork = 170
        self.sowMinSkill = 0
        self.harvestWork = 200
        self.harvestedThingDef = "undefined"
        self.harvestYield = 0
        self.hydroponic = False
        self.growDays = 0


class PlantBase:
    def __init__(self):
        self.parent = "undefined"
        self.name = "undefinedPlant"
        self.nutrition = 0
        self.lifespanDaysPerGrowDays = 0
        self.fertilityMin = 0.7
        self.fertilitySensitivity = 1
        self.sowWork = 170
        self.sowMinSkill = 0
        self.harvestWork = 200
        self.harvestedThingDef = "undefined"
        self.harvestYield = 0
        self.hydroponic = False
        self.growDays = 0


class BushBase:
    def __init__(self):
        self.parent = "undefined"
        self.name = "undefinedPlant"
        self.nutrition = 0.5
        self.lifespanDaysPerGrowDays = 0
        self.fertilityMin = 0.7
        self.fertilitySensitivity = 0.5
        self.sowWork = 170
        self.sowMinSkill = 0
        self.harvestWork = 200
        self.harvestedThingDef = "undefined"
        self.harvestYield = 0
        self.hydroponic = False
        self.growDays = 3


class TreeBase:
    def __init__(self):
        self.parent = "undefined"
        self.name = "undefinedPlant"
        self.nutrition = 2
        self.lifespanDaysPerGrowDays = 9
        self.fertilityMin = 0.7
        self.fertilitySensitivity = 0.5
        self.sowWork = 4000
        self.sowMinSkill = 6
        self.harvestWork = 800
        self.harvestedThingDef = "undefined"
        self.harvestYield = 25
        self.hydroponic = False
        self.growDays = 0


class DeciduousTreeBase:
    def __init__(self):
        self.parent = "undefined"
        self.name = "undefinedPlant"
        self.nutrition = 2
        self.lifespanDaysPerGrowDays = 9
        self.fertilityMin = 0.7
        self.fertilitySensitivity = 0.5
        self.sowWork = 4000
        self.sowMinSkill = 6
        self.harvestWork = 800
        self.harvestedThingDef = "undefined"
        self.harvestYield = 25
        self.hydroponic = False
        self.growDays = 0


class CavePlantBase:
    def __init__(self):
        self.parent = "undefined"
        self.name = "undefinedPlant"
        self.nutrition = 0
        self.lifespanDaysPerGrowDays = 0
        self.fertilityMin = 0.7
        self.fertilitySensitivity = 1
        self.sowWork = 170
        self.sowMinSkill = 0
        self.harvestWork = 200
        self.harvestedThingDef = "undefined"
        self.harvestYield = 0
        self.hydroponic = False
        self.growDays = 0


# Process defs
def extractDef(defFilePath, sheets):
    sheetName = "undefined"
    entry = "undefined"

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
                try:
                    parentName = element1.attrib["ParentName"]
                except Exception:
                    break
                match parentName:
                    case "PlantBaseNonEdible":
                        entry = PlantBaseNonEdible()
                    case "PlantBase":
                        entry = PlantBase()
                    case "BushBase":
                        entry = BushBase()
                    case "TreeBase":
                        entry = TreeBase()
                    case "DeciduousTreeBase":
                        entry = DeciduousTreeBase()
                    case "CavePlantBase":
                        entry = CavePlantBase()
                    case "VEE_Flower":
                        entry = VEE_Flower()
                    case "StumpChoppedBase":
                        break
                    case "StumpSmashedBase":
                        break
                    case _:
                        print("Missing plant base:" + parentName)

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
                                    case "harvestYield":
                                        entry.harvestYield = element3.text
                                    case "sowTags":
                                        for element4 in element3:
                                            match element4.text:
                                                case "hydroponic":
                                                    entry.hydroponic = True
                                    case "growDays":
                                        entry.growDays = element3.text
                sheets[sheetName].append(entry)


# Returns a list with every def path
def getXMLFilePaths():
    # Returns the filelist
    XMLFilePaths = []
    excludedKeywords = ["1.0", "1.1", "1.2", "1.3", "1.4"]
    for XMLFile in Path(RIMWORLD_FOLDER).rglob("**/*.xml"):
        if not any(keyword in str(XMLFile) for keyword in excludedKeywords):
            XMLFilePaths.append(XMLFile)
    return XMLFilePaths


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
    # Get a list with every def path
    XMLFilePathList = getXMLFilePaths()

    # Extract every def
    for XMLFilePath in XMLFilePathList:
        extractDef(XMLFilePath, sheets)

    # Write the CSVs
    for sheetName in sheets.keys():
        sheet = sheets[sheetName]
        with open(sheetName + ".csv", "w", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)
            writer.writerow(
                [
                    "Parent",
                    "Name",
                    "Fertility Sensitivity",
                    "Harvest Yield",
                    "Hydroponic",
                    "Grow Days",
                ]
            )
            for entry in sheet:
                writer.writerow(
                    [
                        entry.parent,
                        entry.name,
                        entry.fertilitySensitivity,
                        entry.harvestYield,
                        entry.hydroponic,
                        entry.growDays,
                    ]
                )
