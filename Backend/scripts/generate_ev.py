import random
import csv
import os

def generate_and_save_ev_data(num_samples=5000, filename="Backend/data/ev_data.csv"):
    """
    Generates synthetic data for Electric Vehicle (EV) range prediction
    and saves it to a CSV file.
    """
    headers = [
        'battery_percentage', 'battery_age_years', 'ambient_temp',
        'terrain_slope', 'speed_avg_kmph', 'acceleration_level', 'hvac_on',
        'driving_mode', 'drive_type', 'top_speed_kmph', 'total_power_kw',
        'total_torque_nm', 'battery_capacity_kwh',
        # Derived features that your model expects
        'battery_per_kWh', # Derived: battery_percentage / battery_capacity_kwh
        'battery_remaining_kWh', # Derived: battery_capacity_kwh * battery_percentage / 100
        'electric_range_km' # Target variable
    ]

    ambient_temps = ['cold', 'mild', 'hot']
    hvac_options = ['yes', 'no']
    driving_modes = ['Normal', 'Sport', 'Eco']
    drive_types = ['FWD', 'RWD']

    data = []
    for _ in range(num_samples):
        # Generate base input features
        battery_percentage = round(random.uniform(10.0, 100.0), 2)
        battery_age_years = round(random.uniform(0.0, 10.0), 2)
        ambient_temp = random.choice(ambient_temps)
        terrain_slope = round(random.uniform(-5.0, 5.0), 2)
        speed_avg_kmph = round(random.uniform(20.0, 130.0), 2)
        acceleration_level = round(random.uniform(0.0, 1.0), 2)
        hvac_on = random.choice(hvac_options)
        driving_mode = random.choice(driving_modes)
        drive_type = random.choice(drive_types)
        top_speed_kmph = round(random.uniform(120.0, 250.0), 2)
        total_power_kw = round(random.uniform(50.0, 200.0), 2)
        total_torque_nm = round(random.uniform(100.0, 600.0), 2)
        battery_capacity_kwh = round(random.uniform(30.0, 100.0), 2)

        # Calculate derived features (ensuring consistency with train_ev.py and ev_preprocess.py)
        battery_per_kWh = round(battery_percentage / battery_capacity_kwh if battery_capacity_kwh != 0 else 0.0, 2)
        battery_remaining_kWh = round(battery_capacity_kwh * battery_percentage / 100.0, 2)

        # Simulate electric_range_km based on plausible relationships
        base_range = 300.0

        range_km = base_range
        range_km += (battery_percentage / 100.0) * battery_capacity_kwh * 4.0
        range_km -= battery_age_years * 5.0

        if ambient_temp == 'cold':
            range_km -= 40.0
        elif ambient_temp == 'hot':
            range_km -= 20.0

        if speed_avg_kmph > 90:
            range_km -= (speed_avg_kmph - 90) * 0.8
        elif speed_avg_kmph < 50:
            range_km -= (50 - speed_avg_kmph) * 0.5

        range_km -= abs(terrain_slope) * 3.0
        range_km -= acceleration_level * 40.0

        if hvac_on == 'yes':
            range_km -= 25.0

        if driving_mode == 'Sport':
            range_km -= 15.0
        elif driving_mode == 'Eco':
            range_km += 10.0
            
        range_km -= (total_power_kw / 100) * 5.0 

        range_km += random.uniform(-15.0, 15.0)

        electric_range_km = max(0.0, round(range_km, 2))

        data.append([
            battery_percentage, battery_age_years, ambient_temp,
            terrain_slope, speed_avg_kmph, acceleration_level, hvac_on,
            driving_mode, drive_type, top_speed_kmph, total_power_kw,
            total_torque_nm, battery_capacity_kwh,
            battery_per_kWh, battery_remaining_kWh, electric_range_km
        ])

    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Successfully generated and saved {num_samples} samples to '{filename}'")
    except IOError as e:
        print(f"Error saving file '{filename}': {e}")

if __name__ == "__main__":
    generate_and_save_ev_data(num_samples=5000, filename="Backend/data/ev_data.csv")