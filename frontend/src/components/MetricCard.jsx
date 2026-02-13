
import React from 'react';

export default function MetricCard({ title, value, label }) {
  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <div className="text-3xl font-bold text-gray-900">{value}</div>
      <div className="text-sm text-gray-500 mt-1">{label}</div>
      <div className="text-xs text-gray-400 mt-2 uppercase tracking-wider">{title}</div>
    </div>
  );
}   