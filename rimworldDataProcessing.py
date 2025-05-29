import xml.etree.ElementTree as ET
import csv
from pathlib import Path

# -------- CONFIG --------
RIMWORLD_FOLDER = "C:\\Applications\\RimWorld"
# --------


# Classes
class plant:
    def __init__(self):
        self.name = "undefinedPlant"
        self.harvestYield = 0


# Process defs
def extractDef(defFilePath, sheets):
    sheetName = "undefined"
    entry = "undefined"

    try:
        tree = ET.parse(defFilePath)
        root = tree.getroot()
        for element1 in root:  # ThingDef
            for element2 in element1:  # e.g label
                if element2.tag == "plant":
                    sheetName = "plants"
    except Exception:
        pass

    match sheetName:
        case "plants":
            for element1 in root:  # ThingDef
                entry = plant()
                for element2 in element1:  # e.g label
                    match element2.tag:
                        case "label":
                            entry.name = element2.text
                        case "plant":
                            for element3 in element2:
                                match element3.tag:
                                    case "harvestYield":
                                        entry.harvestYield = element3.text
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
    XMLFilePathList = getXMLFilePaths()

    # Extract every def
    for XMLFilePath in XMLFilePathList:
        extractDef(XMLFilePath, sheets)

    # Write the CSVs
    for sheetName in sheets.keys():
        sheet = sheets[sheetName]
        with open(sheetName + ".csv", "w", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)
            writer.writerow(["Name", "Yield"])
            for entry in sheet:
                writer.writerow([entry.name, entry.harvestYield])
