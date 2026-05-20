import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

FEMALE_NAMES = [
    "Aadhya", "Ananya", "Diya", "Isha", "Kavya", "Meera", "Nisha", "Priya", "Riya", "Saanvi",
    "Anika", "Avni", "Bhavna", "Charvi", "Deepika", "Esha", "Fatima", "Gauri", "Hema", "Indu",
    "Jaya", "Kiran", "Lakshmi", "Mala", "Neha", "Pallavi", "Radha", "Seema", "Tanvi", "Uma",
    "Vidya", "Wafa", "Yamini", "Zara", "Aditi", "Bhumi", "Chitra", "Divya", "Ekta", "Falguni",
    "Geeta", "Harini", "Ira", "Janvi", "Kriti", "Latika", "Madhuri", "Nandini", "Oviya", "Pooja",
]

# Shimoga mapped locations only
LOCATION_POINTS = [
    (2, 3),   # Shimoga Bus Stand
    (4, 5),   # Railway Station
    (6, 7),   # Gopi Circle
    (8, 10),  # Vinobanagar
    (10, 12), # Durgigudi
    (12, 14), # Savalanga Road
    (14, 16), # B.H. Road
    (16, 18), # KU Campus
    (5, 15),  # Ameer Ahmed Circle
    (9, 9)    # City Center Mall
]

drivers = []

for i in range(1, 51):

    location = random.choice(LOCATION_POINTS)

    driver = {
        "driver_id": f"W{i}",
        "name": random.choice(FEMALE_NAMES),
        "x": location[0],
        "y": location[1],
        "status": random.choice(["available", "available", "available", "busy"]),
        "verification_status": random.choices(
            ["verified", "pending"],
            weights=[85, 15]
        )[0],
        "safety_rating": round(random.uniform(3.5, 5.0), 1),
    }

    drivers.append(driver)

df = pd.DataFrame(drivers)
df.to_csv("data/drivers.csv", index=False)

print(f"drivers.csv generated: {len(df)} female drivers")
print(f"Verified: {len(df[df['verification_status'] == 'verified'])}")
print(f"Available: {len(df[df['status'] == 'available'])}")
print(f"Avg safety rating: {df['safety_rating'].mean():.2f}")