# Extracts defs
def extractDef(defFilePath, defIndex, sheets):
    sheetName = "undefined"

    try:
        tree = ET.parse(defFilePath)
        root = tree.getroot()
        for element in root.iter(tag="ThingDef"):
            print(element.tag)
    except Exception:
        pass

    match sheetName:
        case "plants":
            for element in root:  # ThingDef
                entry = plantsEntry()
                for element2 in element:  # e.g label
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
