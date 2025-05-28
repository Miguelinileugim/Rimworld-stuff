import os
import xml.etree.ElementTree as ET
import csv

# -------- CONFIG --------
RIMWORLD_FOLDER = "C:\\Applications\\RimWorld"
DEFPATHTYPE_1 = "1.5\\Defs"
DEFPATHTYPE_2 = "v1.5\\Defs"
DEFPATHTYPE_3 = "Defs"
# --------


# Classes
class plant:
    name = "undefinedPlant"
    plantHarvestYield = 0


# Process defs
def extractDef(defFilePath, sheets):
    defName = os.path.basename(defFilePath)
    print("test")
    # Plants
    # if root.thingDef.plant --> If this exists then it is a plant!
    defSearchKey = "Plants_"
    if defName.find(defSearchKey) != -1:
        tree = ET.parse(defFilePath)
        root = tree.getroot()
        print(root)


# Returns a list with every def path
def getDefPaths():
    defFilePathList = []
    defPathTypes = [
        RIMWORLD_FOLDER + "\\Data"
        DEFPATHTYPE_1,
        DEFPATHTYPE_2,
        DEFPATHTYPE_3]

    for defPathType in defPathTypes:
        defsFolderPath = os.path.join(RIMWORLD_FOLDER, defPathType)
        print(os.path.exists(defsFolderPath))
        if os.path.exists(defsFolderPath):
            for defFolderPath in os.listdir(defsFolderPath):
                for defSubfolderPath in os.listdir(defFolderPath):
                    defFilePath = os.path.join(defFolderPath, defSubfolderPath)
                    if os.path.isdir(defFilePath):
                        for defFile in os.listdir(defFilePath):
                            defPath = os.path.join(defFilePath, defFile)
                            defFilePathList.append(defPath)

    # Returns the filelist
    return defFilePathList


# Writes CSVs
def write_csv(sheets):
    for sheet in sheets:
        with open(sheet + ".csv", "w", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)
            for rowNumber in range(len(sheet)):
                row = sheet[rowNumber]
                writer.writerows(row)


# Defines variables for each sheet
sheets = {
    "harvestables": [],
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
    defFilePathList = getDefPaths()

    # Extract every def
    for defFilePath in defFilePathList:
        extractDef(defFilePath, sheets)

    # Write the CSVs
    for sheet in sheets:
        write_csv(sheet)
