import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export default function EVInput() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    battery_percentage: "",
    battery_age_years: "",
    battery_capacity_kwh: "",
    ambient_temp: "mild",
    terrain_slope: "",
    speed_avg_kmph: "",
    acceleration_level: "",
    hvac_on: false,
    driving_mode: "Normal",
    drive_type: "FWD",
    cargo_volume_liters: "",
    top_speed_kmph: "",
    total_power_kw: "",
    total_torque_nm: ""
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const validate = () => {
    const newErrors = {};
    if (formData.battery_percentage < 0 || formData.battery_percentage > 100)
      newErrors.battery_percentage = "Battery % must be between 0 and 100.";
    if (formData.acceleration_level < 0 || formData.acceleration_level > 1)
      newErrors.acceleration_level = "Acceleration must be between 0 and 1.";
    if (formData.speed_avg_kmph < 0)
      newErrors.speed_avg_kmph = "Speed must be a positive value.";
    if (formData.battery_age_years < 0)
      newErrors.battery_age_years = "Battery age must be a positive value.";
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/ev", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        navigate('/results', {
          state: {
            type: 'ev',
            result: result.predicted_range_km,
            inputData: formData
          }
        });
      } else {
        alert(`❌ Prediction failed: ${result.detail}`);
      }
    } catch (error) {
      console.error("❌ Error submitting form:", error);
      alert("❌ An error occurred during submission.");
    }
  };
  const inputConfig = [
    { name: "battery_percentage", placeholder: "Battery %", min: 0, max: 100 },
    { name: "battery_age_years", placeholder: "Battery Age (years)", min: 0 },
    { name: "battery_capacity_kwh", placeholder: "Battery Capacity (kWh)", min: 0 },
    // { name: "terrain_slope", placeholder: "Terrain Slope (%)", min: -100, max: 100 },
    { name: "speed_avg_kmph", placeholder: "Avg Speed (km/h)", min: 0 },
    { name: "acceleration_level", placeholder: "Acceleration (0–1)", step: "0.01", min: 0, max: 1 },
    { name: "cargo_volume_liters", placeholder: "Cargo Volume (liters)", min: 0 },
    { name: "top_speed_kmph", placeholder: "Top Speed (km/h)", min: 0 },
    { name: "total_power_kw", placeholder: "Total Power (kW)", min: 0 },
    { name: "total_torque_nm", placeholder: "Total Torque (Nm)", min: 0 },
  ];

  return (
    <div className="min-h-screen bg-[#010c0e] text-white flex flex-col items-center px-4 py-12">
      {/* Hero Section */}
      <div className="w-full max-w-6xl flex flex-col-reverse md:flex-row items-center justify-between mb-12 gap-8">
        <div className="text-center md:text-left space-y-4 w-full md:w-1/2">
          <h1 className="text-4xl md:text-5xl font-extrabold leading-tight text-green-400">
            Predict Your Electric Range
          </h1>
          <p className="text-gray-300 text-lg">
            Enter vehicle and driving parameters to estimate how far your EV can go.
          </p>
                    <button
            onClick={() => navigate("/")}
            className="mt-4 px-4 py-2 cursor-pointer bg-green-700 hover:bg-green-800 rounded-lg text-white text-sm shadow"
          >
            ← Back to Home
          </button>
        </div>
        <div className="w-full md:w-1/2 flex justify-center">
          <DotLottieReact
            src="https://lottie.host/d819043f-bc41-4208-8593-de0ab7c7746a/KkvfFdrKtD.lottie"
            loop
            autoplay
            speed={1.5}
            className="w-full max-w-sm md:max-w-md"
          />
        </div>
      </div>

      {/* Form Section */}
       <form
        onSubmit={handleSubmit}
        className="w-full max-w-4xl bg-[#0f1a1c] p-8 rounded-3xl shadow-2xl space-y-6 border border-green-800"
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {inputConfig.map(({ name, placeholder, step, min, max }) => (
            <div key={name}>
              <input
                className="input appearance-none w-full"
                type=""
                name={name}
                placeholder={placeholder}
                step={step || "any"}
                min={min}
                max={max}
                value={formData[name]}
                onChange={handleChange}
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                required
              />
              {errors[name] && (
                <p className="text-red-500 text-sm mt-1">{errors[name]}</p>
              )}
            </div>
          ))}
          <input
            type="text"
            inputMode="decimal"
            pattern="^-?\d*\.?\d*$"
            name="terrain_slope"
            placeholder="Terrain Slope"
            value={formData.terrain_slope}
            onChange={handleChange}
          />

          <select
            className="input bg-[#0f1a1c]"
            name="ambient_temp"
            onChange={handleChange}
            value={formData.ambient_temp}
          >
            <option value="cold">Cold</option>
            <option value="mild">Mild</option>
            <option value="hot">Hot</option>
          </select>

          <select
            className="input bg-[#0f1a1c]"
            name="driving_mode"
            onChange={handleChange}
            value={formData.driving_mode}
          >
            <option value="Eco">Eco</option>
            <option value="Normal">Normal</option>
            <option value="Sport">Sport</option>
          </select>

          <select
            className="input bg-[#0f1a1c]"
            name="drive_type"
            onChange={handleChange}
            value={formData.drive_type}
          >
            <option value="FWD">FWD</option>
            <option value="RWD">RWD</option>
          </select>
        </div>

        <label className="flex items-center gap-3 text-green-300">
          <input
            type="checkbox"
            name="hvac_on"
            checked={formData.hvac_on}
            onChange={handleChange}
            className="accent-green-500"
          />
          HVAC On
        </label>

        <button
          type="submit"
          className="mt-4 w-full py-3 rounded-xl bg-gradient-to-r cursor-pointer from-green-500 to-green-700 hover:from-green-600 hover:to-green-800 text-white font-semibold shadow-xl"
        >
          🚗 Predict Range
        </button>
      </form>
    </div>
  );
}
