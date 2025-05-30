import csv
from Functions.XMLFinder import XMLFinder

# -------- CONFIG --------
RIMWORLD_FOLDER = "C:\\Applications\\RimWorld"
DEFS_EXPORT_FOLDER = "C:\\Projects\\Rimworld stuff\\Defs"
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
        self.hydroponic = False
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
    # Get the filepath to every XML file
    XMLFilePaths = XMLFinder(RIMWORLD_FOLDER)

    # Export every def into a separate file
    exportDefs(RIMWORLD_FOLDER, DEFS_EXPORT_FOLDER)

    # Patch every def as to account for inheritance
    patchDefs(DEFS_EXPORT_FOLDER)

    # Extract every def
    # for XMLFilePath in XMLFilePathList:
    # extractDef(XMLFilePath, defIndex, sheets)

    for sheetName in sheets.keys():
        sheet = sheets[sheetName]
        # Process defs to get more info
        processDefs(sheet, sheets)

        # Write the CSVs
        with open(
            "\\CSVs" + sheetName + ".csv", "w", newline="", encoding="utf-8"
        ) as csvf:
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
