import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

FEMALE_NAMES = [
    "Aanya", "Bela", "Chetna", "Dhara", "Elina", "Farha", "Gita", "Himani", "Ila", "Jhanvi",
    "Kanika", "Lata", "Mansi", "Naina", "Ojasvi", "Payal", "Qudsia", "Rani", "Sanya", "Tara",
    "Urvi", "Vani", "Wahida", "Yashvi", "Zoya", "Amrita", "Bindu", "Charu", "Damini", "Eesha",
    "Fiza", "Garima", "Hiral", "Ishita", "Juhi", "Keya", "Lisha", "Mitali", "Navya", "Ojaswi",
    "Pihu", "Rachna", "Shreya", "Tanya", "Ujjwala", "Varsha", "Wisha", "Yukta", "Zainab", "Arya",
    "Bhakti", "Chandni", "Darshana", "Eva", "Falak", "Gunjan", "Honey", "Iti", "Jagriti", "Kamya",
    "Lavanya", "Mahika", "Nidhi", "Omisha", "Pari", "Rhea", "Simran", "Trisha", "Urvashi", "Vidhi",
    "Yami", "Zaira", "Aparna", "Bhoomi", "Chanda", "Dipti", "Eshani", "Farheen", "Ganika", "Harsha",
    "Ivana", "Jasleen", "Komal", "Leela", "Myra", "Nisha", "Oprah", "Poonam", "Rashi", "Sakshi",
    "Tithi", "Unnati", "Veda", "Wani", "Yuvika", "Zaina", "Alisha", "Bani", "Chahat", "Durga",
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

riders = []

for i in range(1, 101):

    pickup, destination = random.sample(LOCATION_POINTS, 2)

    rider = {
        "rider_id": f"R{i}",
        "name": random.choice(FEMALE_NAMES),
        "pickup_x": pickup[0],
        "pickup_y": pickup[1],
        "destination_x": destination[0],
        "destination_y": destination[1],
        "priority_level": random.choices(
            ["normal", "high", "urgent"],
            weights=[70, 20, 10]
        )[0],
    }

    riders.append(rider)

df = pd.DataFrame(riders)
df.to_csv("data/riders.csv", index=False)

print(f"riders.csv generated: {len(df)} female riders")
print(f"Normal: {len(df[df['priority_level'] == 'normal'])}")
print(f"High: {len(df[df['priority_level'] == 'high'])}")
print(f"Urgent: {len(df[df['priority_level'] == 'urgent'])}")