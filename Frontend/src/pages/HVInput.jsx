// src/pages/HVInput.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import axios from 'axios';

export default function HVInput() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    hydrogen_percentage: "",
    fuel_cell_age_years: "",
    fuel_cell_efficiency: "",
    ambient_temp: "mild",
    terrain_slope: "",
    speed_avg_kmph: "",
    acceleration_level: "",
    hvac_on: false,
    driving_mode: "normal",
    drive_type: "FWD",
    cargo_volume_liters: "",
    top_speed_kmph: "",
    total_power_kw: "",
    total_torque_nm: ""
  });

  const inputConfig = [
    { name: "hydrogen_percentage", placeholder: "Hydrogen Tank %", min: 0, max: 100, type: "number" },
    { name: "fuel_cell_age_years", placeholder: "Fuel Cell Age (years)", min: 0, type: "number" },
    { name: "fuel_cell_efficiency", placeholder: "Fuel Cell Efficiency", min: 0, max: 100, step: "0.01", type: "number" },
    { name: "speed_avg_kmph", placeholder: "Avg Speed (km/h)", min: 0, type: "number" },
    { name: "acceleration_level", placeholder: "Acceleration (0–1)", min: 0, max: 1, step: "0.01", type: "number" },
    { name: "cargo_volume_liters", placeholder: "Cargo Volume (liters)", min: 0, type: "number" },
    { name: "top_speed_kmph", placeholder: "Top Speed (km/h)", min: 0, type: "number" },
    { name: "total_power_kw", placeholder: "Total Power (kW)", min: 0, type: "number" },
    { name: "total_torque_nm", placeholder: "Total Torque (Nm)", min: 0, type: "number" },
  ];

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [hvSuggestions, setHvSuggestions] = useState([]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    let newValue = value;

    if (type === "number") {
      newValue = value.replace(",", ".");
    }

    setFormData(prevData => ({
      ...prevData,
      [name]: type === "checkbox" ? checked : newValue,
    }));
  };

  const validate = () => {
    const newErrors = {};
    if (formData.hydrogen_percentage !== "" && (parseFloat(formData.hydrogen_percentage) < 0 || parseFloat(formData.hydrogen_percentage) > 100)) newErrors.hydrogen_percentage = "Hydrogen % must be between 0 and 100.";
    if (formData.acceleration_level !== "" && (parseFloat(formData.acceleration_level) < 0 || parseFloat(formData.acceleration_level) > 1)) newErrors.acceleration_level = "Acceleration must be between 0 and 1.";
    if (formData.speed_avg_kmph !== "" && parseFloat(formData.speed_avg_kmph) < 0) newErrors.speed_avg_kmph = "Speed must be a positive value.";
    if (formData.fuel_cell_age_years !== "" && parseFloat(formData.fuel_cell_age_years) < 0) newErrors.fuel_cell_age_years = "Age must be a positive value.";
    if (formData.fuel_cell_efficiency !== "" && (parseFloat(formData.fuel_cell_efficiency) < 0 || parseFloat(formData.fuel_cell_efficiency) > 100)) newErrors.fuel_cell_efficiency = "Efficiency must be between 0 and 100.";
    if (formData.terrain_slope !== "" && isNaN(parseFloat(formData.terrain_slope)))
        newErrors.terrain_slope = "Terrain Slope must be a valid number.";
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Sending formData:", formData);

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    setErrors({});
    setHvSuggestions([]);

    const formattedPayload = {
      acceleration_level: parseFloat(formData.acceleration_level),
      ambient_temp: formData.ambient_temp,
      cargo_volume_liters: parseFloat(formData.cargo_volume_liters),
      drive_type: formData.drive_type,
      driving_mode: formData.driving_mode,
      fuel_cell_age_years: parseFloat(formData.fuel_cell_age_years),
      fuel_cell_efficiency: parseFloat(formData.fuel_cell_efficiency),
      hvac_on: formData.hvac_on ? "yes" : "no",
      hydrogen_percentage: parseFloat(formData.hydrogen_percentage),
      speed_avg_kmph: parseFloat(formData.speed_avg_kmph),
      terrain_slope: parseFloat(formData.terrain_slope),
      top_speed_kmph: parseFloat(formData.top_speed_kmph),
      total_power_kw: parseFloat(formData.total_power_kw),
      total_torque_nm: parseFloat(formData.total_torque_nm),
    };

    let predictedRange = null;
    let predictionSuccess = false;

    try {
      // 1. Fetch Prediction
      const predictionResponse = await axios.post("http://localhost:8000/predict/hv", formattedPayload, {
        headers: { "Content-Type": "application/json" },
      });

      predictedRange = predictionResponse.data.predicted_range_km; // Access .data.predicted_range_km
      
      if (typeof predictedRange === 'number' && !isNaN(predictedRange) && isFinite(predictedRange)) {
          predictionSuccess = true;
          console.log('HV Prediction successful:', predictedRange);
      } else {
          console.error('HV Prediction successful but value is invalid:', predictedRange);
          alert('Failed to get a valid range prediction. Please check your inputs.');
      }

    } catch (error) {
      console.error("Prediction request failed:", error);
      alert("Failed to predict range. Please try again.");
    }

    // 2. Fetch Suggestions (always attempt, regardless of prediction success)
    let fetchedSuggestions = [];
    try {
      const suggestionsResponse = await fetch('http://localhost:8000/suggest/hv/suggestions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedPayload),
      });

      if (suggestionsResponse.ok) {
        const suggestionsData = await suggestionsResponse.json();
        fetchedSuggestions = suggestionsData.suggestions;
        setHvSuggestions(fetchedSuggestions);
        console.log('HV Suggestions fetched:', fetchedSuggestions);
      } else {
        const errorData = await suggestionsResponse.json();
        console.error('Failed to fetch HV suggestions:', errorData.detail || 'Unknown error');
      }
    } catch (suggestionError) {
      console.error('Error fetching HV suggestions:', suggestionError);
    }

    // Only navigate if prediction was successful AND valid
    if (predictionSuccess) {
      navigate("/results", {
        state: {
          type: "hv",
          prediction: predictedRange,
          inputData: formData,
          suggestions: fetchedSuggestions
        },
      });
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#010c0e] text-white flex flex-col items-center px-4 py-12">
      {/* Hero Section */}
      <div className="w-full max-w-6xl flex flex-col-reverse md:flex-row items-center justify-between mb-12 gap-8">
        <div className="text-center md:text-left space-y-4 w-full md:w-1/2">
          <h1 className="text-4xl md:text-5xl font-extrabold leading-tight text-blue-400">
            Predict Your Hydrogen Range
          </h1>
          <p className="text-gray-300 text-lg">
            Enter vehicle and driving parameters to estimate how far your Hydrogen Vehicle can go.
          </p>
          <button
            onClick={() => navigate("/")}
            className="mt-4 px-4 py-2 cursor-pointer bg-blue-700 hover:bg-blue-800 rounded-lg text-white text-sm shadow"
          >
            ← Back to Home
          </button>
        </div>
        <div className="w-full md:w-1/2 flex justify-center">
          <DotLottieReact
            src="https://lottie.host/ecfdba0a-044a-4878-b527-9244b06cd553/rB8Pxmpwhc.lottie"
            loop
            autoplay
            speed={1}
            className="w-full max-w-sm md:max-w-md"
          />
        </div>
      </div>

      {/* Form Section */}
      <form onSubmit={handleSubmit} className="w-full max-w-4xl bg-[#0f1a1c] p-8 rounded-3xl shadow-2xl space-y-6 border border-blue-800">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {inputConfig.map(({ name, placeholder, step, min, max, type }) => (
            <div key={name}>
              <input
                className="input appearance-none w-full"
                type={type}
                name={name}
                placeholder={placeholder}
                step={step || "any"}
                min={min}
                max={max}
                value={formData[name]}
                onChange={handleChange}
                onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                required
              />
              {errors[name] && <p className="text-red-500 text-sm mt-1">{errors[name]}</p>}
            </div>
          ))}

          {/* Specific input for terrain_slope, ensure type="number" */}
          <div>
            <input
              type="number"
              inputMode="decimal"
              pattern="^-?\d*\.?\d*$"
              name="terrain_slope"
              placeholder="Terrain Slope"
              value={formData.terrain_slope}
              onChange={handleChange}
              onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
              required
            />
            {errors.terrain_slope && (
              <p className="text-red-500 text-sm mt-1">{errors.terrain_slope}</p>
            )}
          </div>

          <select className="input bg-[#0f1a1c]" name="ambient_temp" onChange={handleChange} value={formData.ambient_temp}>
            <option value="cold">Cold</option>
            <option value="mild">Mild</option>
            <option value="hot">Hot</option>
          </select>

          <select className="input bg-[#0f1a1c]" name="driving_mode" onChange={handleChange} value={formData.driving_mode}>
            <option value="eco">Eco</option>
            <option value="normal">Normal</option>
            <option value="sport">Sport</option>
          </select>

          <select className="input bg-[#0f1a1c]" name="drive_type" onChange={handleChange} value={formData.drive_type}>
            <option value="FWD">FWD</option>
            <option value="RWD">RWD</option>
            <option value="AWD">AWD</option>
          </select>
        </div>

        <label className="flex items-center gap-3 text-blue-300">
          <input
            type="checkbox"
            name="hvac_on"
            checked={formData.hvac_on}
            onChange={handleChange}
            className="accent-blue-500"
          />
          HVAC On
        </label>

        <button
          type="submit"
          disabled={loading}
          className="mt-4 w-full py-3 rounded-xl bg-gradient-to-r cursor-pointer from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 text-white font-semibold shadow-xl"
        >
          {loading ? 'Predicting...' : '🚗 Predict Range'}
        </button>
      </form>

      {/* NEW SECTION: Display HV Suggestions */}
      {hvSuggestions.length > 0 && (
        <div className="w-full max-w-4xl mt-8 p-6 bg-[#0f1a1c] rounded-3xl shadow-xl border border-blue-700">
          <h3 className="text-xl font-bold text-blue-400 mb-4">Suggestions for Optimization:</h3>
          <ul className="list-disc list-inside text-gray-300 space-y-2">
            {hvSuggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
      {/* END NEW SECTION */}
    </div>
  );
}