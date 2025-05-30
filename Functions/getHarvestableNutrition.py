import xml.etree.ElementTree as ET


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
