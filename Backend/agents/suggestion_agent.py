# Backend/agents/suggestion_agent.py

from typing import List, Dict, Any

# These imports assume the input data will be passed as a dictionary
# directly from the validated Pydantic models.

# --- Rule-based agent for EV suggestions ---
def get_ev_suggestions(input_data: Dict[str, Any]) -> List[str]:
    suggestions = []

    # Accessing input data (ensure keys match EVInput schema)
    battery_percentage = input_data.get('battery_percentage')
    battery_age_years = input_data.get('battery_age_years')
    ambient_temp = input_data.get('ambient_temp')
    speed_avg_kmph = input_data.get('speed_avg_kmph')
    hvac_on = input_data.get('hvac_on') # This will be boolean due to schema
    driving_mode = input_data.get('driving_mode')

    # Example Rules for EV
    if battery_percentage is not None and battery_percentage < 20:
        suggestions.append("Your battery is low. Consider finding a charging station soon.")
    if battery_age_years is not None and battery_age_years > 5:
        suggestions.append("Your battery is aging. Regular check-ups can help maintain performance.")
    if ambient_temp is not None and ambient_temp.lower() == 'cold' and hvac_on:
        suggestions.append("In cold weather, pre-conditioning your EV while plugged in can save significant range.")
    if speed_avg_kmph is not None and speed_avg_kmph > 100 and driving_mode.lower() == 'normal':
        suggestions.append("High speeds reduce range. Consider engaging 'Eco' mode for better efficiency on highways.")
    if hvac_on:
        suggestions.append("Turning off HVAC when not essential can significantly extend your EV's range.")

    if not suggestions:
        suggestions.append("No specific suggestions at this moment, keep driving safely!")

    return suggestions

# --- Rule-based agent for HV suggestions ---
def get_hv_suggestions(input_data: Dict[str, Any]) -> List[str]:
    suggestions = []

    # Accessing input data (ensure keys match HVInput schema)
    hydrogen_percentage = input_data.get('hydrogen_percentage')
    fuel_cell_age_years = input_data.get('fuel_cell_age_years')
    fuel_cell_efficiency = input_data.get('fuel_cell_efficiency')
    terrain_slope = input_data.get('terrain_slope')
    acceleration_level = input_data.get('acceleration_level')
    driving_mode = input_data.get('driving_mode')

    # Example Rules for HV
    if hydrogen_percentage is not None and hydrogen_percentage < 15:
        suggestions.append("Your hydrogen tank is low. Plan for a refuel soon.")
    if fuel_cell_age_years is not None and fuel_cell_age_years > 7:
        suggestions.append("Your fuel cell is aging. Regular inspections are recommended for optimal performance.")
    if fuel_cell_efficiency is not None and fuel_cell_efficiency < 60:
        suggestions.append("Consider a fuel cell system check-up to improve efficiency.")
    if terrain_slope is not None and terrain_slope > 10 and acceleration_level is not None and acceleration_level > 0.5:
        suggestions.append("Aggressive acceleration on steep slopes consumes more hydrogen. Try a gentler approach.")
    if driving_mode is not None and driving_mode.lower() == 'sport':
        suggestions.append("Sport mode prioritizes power over efficiency. For better range, switch to 'Normal' or 'Eco' mode.")

    if not suggestions:
        suggestions.append("No specific suggestions at this moment, enjoy your drive!")

    return suggestions