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
