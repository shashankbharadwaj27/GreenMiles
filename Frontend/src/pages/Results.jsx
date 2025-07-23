import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Results = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state;

  if (!state) {
    navigate('/');
    return null;
  }

  const { type, result, inputData } = state;

  const title =
    type === 'ev' ? 'Estimated EV Range' : 'Estimated Hydrogen Vehicle Range';
  const icon = type === 'ev' ? '🔋' : '🚗💨';
  const predictedRange = result ? result : 'N/A';

  const onBack = () => {
    navigate(type === 'ev' ? '/ev/predict' : '/hv/predict');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 py-10 bg-gray-100 dark:bg-gray-900">
      <div className="max-w-2xl w-full bg-white dark:bg-gray-800 shadow-lg rounded-xl p-6">
        <h1 className="text-3xl font-bold text-center text-green-600 dark:text-green-400 mb-4">
          {title}
        </h1>

        <p className="text-center text-5xl font-semibold text-gray-800 dark:text-white my-6">
          {icon} {predictedRange} km
        </p>

        {/* Caution section */}
        <div className="mt-6 bg-yellow-100 dark:bg-yellow-300/20 border-l-4 border-yellow-400 dark:border-yellow-300 text-yellow-800 dark:text-yellow-200 p-4 rounded-md">
          <p className="font-medium">⚠️ Caution:</p>
          <p className="text-sm mt-1">
            This is a model-based estimated range. Real-world performance may vary based on factors like driving habits,
            traffic conditions, battery health, terrain, and weather. Always plan your journey with extra buffer.
          </p>
        </div>

        <div className="mt-8 text-center">
          <button
            onClick={onBack}
            className="px-6 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white dark:bg-blue-500 dark:hover:bg-blue-600 transition"
          >
            Predict Again
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;
