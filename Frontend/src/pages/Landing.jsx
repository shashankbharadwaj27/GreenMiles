import { useNavigate } from "react-router-dom";
import vehicleImage from "../assets/vehicle.png";

const buttonConfigs = [
  {
    name: "🔋 Electric Vehicle",
    link: "/ev/predict",
    gradient: {
      outer: "from-green-400 via-green-600 to-green-800",
      inner: "from-green-300/20 via-green-500/10 to-green-800/20",
      text: "from-green-200 to-green-400",
      glow: "shadow-[inset_0_0_40px_rgba(34,197,94,0.3)]",
      hover: "from-green-400/20 via-green-500/10 to-green-600/20",
    },
  },
  {
    name: "💧 Hydrogen Vehicle",
    link: "/hv/predict",
    gradient: {
      outer: "from-blue-400 via-blue-600 to-blue-800",
      inner: "from-blue-300/20 via-blue-500/10 to-blue-800/20",
      text: "from-blue-200 to-blue-400",
      glow: "shadow-[inset_0_0_40px_rgba(59,130,246,0.3)]",
      hover: "from-blue-400/20 via-blue-500/10 to-blue-600/20",
    },
  },
];

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen w-full bg-[#010c0e] text-white flex flex-col">
      {/* Main Hero Section */}
      <main className="flex flex-col-reverse md:flex-row items-center justify-between px-8 flex-1">
        {/* Text Section */}
        <div className="w-full md:w-1/2 text-center md:text-left py-8 space-y-6">
          <p className="text-sm text-green-400 tracking-wider uppercase">
            Smarter Driving Starts Here
          </p>

          <h1 className="text-4xl md:text-5xl font-extrabold leading-tight">
            Increase Accuracy,
            <br />
            <span className="text-green-400">Predict Your Range</span>
          </h1>

          <p className="text-gray-300 max-w-md mx-auto md:mx-0 text-lg">
            AI-powered prediction for Electric and Hydrogen Vehicles.
            Know how far you can go, before you even start.
          </p>

          {/* Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            {buttonConfigs.map((btn) => (
              <button
                key={btn.name}
                onClick={() => navigate(btn.link)}
                className="relative h-12 px-8 rounded-lg overflow-hidden transition-all duration-500 group"
              >
                {/* Outer Border */}
                <div className={`absolute inset-0 rounded-lg p-[2px] bg-gradient-to-b ${btn.gradient.outer}`}>
                  <div className="absolute inset-0 bg-black rounded-lg opacity-90" />
                </div>

                {/* Inner Layers */}
                <div className="absolute inset-[2px] bg-black rounded-lg opacity-95" />
                <div className="absolute inset-[2px] bg-gradient-to-r from-black via-gray-900 to-black rounded-lg opacity-90" />
                <div className={`absolute inset-[2px] bg-gradient-to-b ${btn.gradient.inner} rounded-lg opacity-80`} />
                <div className={`absolute inset-[2px] ${btn.gradient.glow} rounded-lg`} />

                {/* Button Text */}
                <div className="relative flex items-center justify-center gap-2">
                  <span
                    className={`text-lg font-normal bg-gradient-to-b ${btn.gradient.text} bg-clip-text text-transparent drop-shadow-[0_0_12px_rgba(0,0,0,0.4)] tracking-tighter`}
                  >
                    {btn.name}
                  </span>
                </div>

                {/* Hover Overlay */}
                <div
                  className={`absolute inset-[2px] opacity-0 transition-opacity duration-300 bg-gradient-to-r ${btn.gradient.hover} group-hover:opacity-100 rounded-lg`}
                />
              </button>
            ))}
          </div>
        </div>

        {/* Image Section */}
        <div className="w-full md:w-1/2 flex justify-end mb-12 md:mb-0">
          <img
            src={vehicleImage}
            alt="Top view of electric/hydrogen vehicle"
            className="w-screen max-w-md object-contain"
          />
        </div>
      </main>
    </div>
  );
}
