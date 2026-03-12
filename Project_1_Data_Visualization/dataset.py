# dataset.py — Simulated dataset based on publicly reported figures
# Sources: OCHA, WHO, UNRWA reports (2023–2024)

import pandas as pd
import numpy as np

def load_casualty_data():
    months = [
        "Oct '23", "Nov '23", "Dec '23", "Jan '24", "Feb '24",
        "Mar '24", "Apr '24", "May '24", "Jun '24", "Jul '24",
        "Aug '24", "Sep '24", "Oct '24"
    ]
    killed      = [3500, 6000, 9000, 10500, 12500, 14500, 16500, 18000, 19500, 21000, 23000, 25000, 27000]
    injured     = [8000, 14000, 20000, 24000, 29000, 33000, 37000, 41000, 44000, 47000, 51000, 55000, 60000]
    children    = [1200, 2500, 3800, 4500, 5400, 6200, 7100, 7900, 8600, 9300, 10200, 11000, 11900]
    women       = [800,  1700, 2500, 3000, 3600, 4200, 4800, 5300, 5700, 6200, 6800,  7400,  8000 ]
    return pd.DataFrame({
        "month": months, "killed": killed, "injured": injured,
        "children_killed": children, "women_killed": women
    })

def load_infrastructure_data():
    categories = [
        "Hospitals\nDamaged/Destroyed",
        "Schools\nDamaged/Destroyed",
        "Mosques\nDamaged/Destroyed",
        "Residential\nBuildings Destroyed",
        "Water/Sanitation\nFacilities Damaged",
        "Roads &\nBridges Damaged"
    ]
    counts = [35, 350, 230, 17000, 90, 75]
    pct_destroyed = [60, 65, 70, 55, 80, 50]
    return pd.DataFrame({"category": categories, "count": counts, "pct_destroyed": pct_destroyed})

def load_displacement_data():
    phases = ["Pre-conflict\nPopulation", "Internally\nDisplaced", "Fled to\nEgypt/Abroad", "Sheltering\nUNRWA Sites"]
    values = [2300000, 1900000, 100000, 1400000]
    colors = ["#c4451c", "#e07b5a", "#f0a882", "#d4614a"]
    return pd.DataFrame({"phase": phases, "people": values, "color": colors})

def load_aid_data():
    months = ["Oct '23", "Nov '23", "Dec '23", "Jan '24", "Feb '24",
              "Mar '24", "Apr '24", "May '24", "Jun '24", "Jul '24"]
    trucks_needed  = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
    trucks_entered = [20,  65,  100, 75,  80,  120, 90,  140, 110, 130]
    return pd.DataFrame({"month": months, "needed": trucks_needed, "entered": trucks_entered})

