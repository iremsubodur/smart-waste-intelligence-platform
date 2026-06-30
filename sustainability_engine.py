# =========================================================
# SUSTAINABILITY ENGINE
# =========================================================

CO2_FACTORS = {

    "glass": 0.315,
    "metal": 1.80,
    "paper": 0.90,
    "plastic": 0.45
}

ENERGY_FACTORS = {

    "glass": 0.12,
    "metal": 2.5,
    "paper": 1.3,
    "plastic": 0.55
}

LANDFILL_FACTORS = {

    "glass": 0.40,
    "metal": 0.95,
    "paper": 0.70,
    "plastic": 0.60
}

def calculate_environmental_impact(counts):

    total_co2 = 0
    total_energy = 0
    landfill_saved = 0

    for waste_type, amount in counts.items():

        total_co2 += amount * CO2_FACTORS[waste_type]

        total_energy += amount * ENERGY_FACTORS[waste_type]

        landfill_saved += amount * LANDFILL_FACTORS[waste_type]

    eco_score = min(
        100,
        int((total_co2 / 150) * 100)
    )

    return {

        "co2_saved": round(total_co2, 2),

        "energy_saved": round(total_energy, 2),

        "landfill_saved": round(landfill_saved, 2),

        "eco_score": eco_score
    }