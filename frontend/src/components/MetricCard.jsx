import React from 'react';

export default function MetricCard({ title, value, label }) {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex flex-col">
        {/* The primary KPI number */}
        <span className="text-3xl font-bold text-slate-900 tracking-tight">
          {value}
        </span>
        
        {/* The short description or unit */}
        <span className="text-sm font-medium text-slate-500 mt-1 uppercase tracking-wider">
          {label}
        </span>
        
        {/* The semantic title of the card */}
        <div className="mt-4 pt-4 border-t border-slate-100">
          <h3 className="text-sm font-semibold text-slate-700">
            {title}
          </h3>
        </div>
      </div>
    </div>
  );
}