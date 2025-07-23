import random
import csv
import os

def generate_and_save_hv_data(num_samples=5000, filename="Backend/data/hv_data_5000_samples.csv"):
    """
    Generates synthetic data for Hydrogen Vehicle (HV) range prediction
    and saves it to a CSV file.
    """
    headers = [
        'hydrogen_percentage', 'fuel_cell_age_years', 'fuel_cell_efficiency',
        'ambient_temp', 'terrain_slope', 'speed_avg_kmph', 'acceleration_level',
        'hvac_on', 'driving_mode', 'drive_type', 'cargo_volume_liters',
        'top_speed_kmph', 'total_power_kw', 'total_torque_nm', 'range_in_km'
    ]

    ambient_temps = ['cold', 'mild', 'hot']
    hvac_options = ['yes', 'no']
    driving_modes = ['normal', 'sport', 'eco']
    drive_types = ['FWD', 'RWD', 'AWD']

    data = []
    for _ in range(num_samples):
        # Generate input features
        hydrogen_percentage = round(random.uniform(10.0, 100.0), 2)
        fuel_cell_age_years = round(random.uniform(0.0, 15.0), 2)
        fuel_cell_efficiency = round(random.uniform(40.0, 65.0), 2)
        ambient_temp = random.choice(ambient_temps) # Categorical
        terrain_slope = round(random.uniform(-5.0, 5.0), 2)
        speed_avg_kmph = round(random.uniform(20.0, 120.0), 2)
        acceleration_level = round(random.uniform(0.0, 1.0), 2)
        hvac_on = random.choice(hvac_options) # Categorical
        driving_mode = random.choice(driving_modes) # Categorical
        drive_type = random.choice(drive_types) # Categorical
        cargo_volume_liters = round(random.uniform(100.0, 2000.0), 2)
        top_speed_kmph = round(random.uniform(150.0, 300.0), 2)
        total_power_kw = round(random.uniform(50.0, 250.0), 2)
        total_torque_nm = round(random.uniform(100.0, 1000.0), 2)

        # Simulate range_in_km based on plausible relationships
        range_km = 400.0 # Base range

        # Positive impacts
        range_km += hydrogen_percentage * 1.5
        range_km += fuel_cell_efficiency * 2.0
        range_km += (total_power_kw / 10) * 5.0

        # Negative impacts
        if speed_avg_kmph > 80:
            range_km -= (speed_avg_kmph - 80) * 1.5
        elif speed_avg_kmph < 40:
            range_km -= (40 - speed_avg_kmph) * 1.0

        range_km -= abs(terrain_slope) * 5.0
        range_km -= acceleration_level * 50.0
        range_km -= (cargo_volume_liters / 100) * 2.0

        if hvac_on == 'yes':
            range_km -= 30.0 # HV AC usage penalty

        if driving_mode == 'sport':
            range_km -= 20.0
        elif driving_mode == 'eco':
            range_km += 15.0

        if drive_type == 'AWD':
            range_km -= 10.0 # AWD penalty

        # Age impact
        range_km -= fuel_cell_age_years * 5.0

        # Add random noise
        range_km += random.uniform(-20.0, 20.0)

        # Ensure range is non-negative
        range_km = max(0.0, round(range_km, 2))

        data.append([
            hydrogen_percentage, fuel_cell_age_years, fuel_cell_efficiency,
            ambient_temp, terrain_slope, speed_avg_kmph, acceleration_level,
            hvac_on, driving_mode, drive_type, cargo_volume_liters,
            top_speed_kmph, total_power_kw, total_torque_nm, range_km
        ])

    # Save to CSV file
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"Successfully generated and saved {num_samples} samples to '{filename}'")
    except IOError as e:
        print(f"Error saving file '{filename}': {e}")

if __name__ == "__main__":
    # Call the function to generate and save 5000 samples
    generate_and_save_hv_data(num_samples=5000, filename="Backend/data/hv.csv")