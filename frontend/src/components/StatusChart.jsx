import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const data = [
  { name: '02/07', completed: 0, running: 0, failed: 0 },
  { name: '02/09', completed: 3, running: 1, failed: 0 },
  { name: '02/10', completed: 2, running: 0, failed: 1 },
  { name: '02/12', completed: 5, running: 2, failed: 0 },
];

export default function StatusChart() {
  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm h-80">
      <h2 className="text-lg font-semibold mb-4">Runs by Status</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="completed" stroke="#10b981" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="running" stroke="#3b82f6" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="failed" stroke="#ef4444" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
