import React from 'react';
import StatusChart from './components/StatusChart';
import MetricCard from './components/MetricCard';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Top Chart Section */}
        <div className="mb-8">
          <StatusChart />
        </div>

        {/* Calls Section */}
        <h2 className="text-lg font-bold text-gray-700 mb-4">Calls</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard title="Total calls" value="32" label="Calls" />
          <MetricCard title="Total call minutes" value="71" label="Duration" />
          <MetricCard title="Avg call duration" value="2m 14s" label="Efficiency" />
        </div>

        {/* Emails Section */}
        <h2 className="text-lg font-bold text-gray-700 mb-4">Emails</h2>
        <div className="w-1/3">
          <MetricCard title="Total Emails" value="0" label="Emails" />
        </div>
      </div>
    </div>
  );
}