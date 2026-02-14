import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar , Legend
} from 'recharts';
import MetricCard from './components/MetricCard';
import CallTable from './components/CallTable';

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL;
        const headers = { 'x-api-key': import.meta.env.VITE_INTERNAL_API_KEY };

        const [analyticsRes, logsRes] = await Promise.all([
          axios.get(`${apiUrl}/call_analytics`, { headers }),
          axios.get(`${apiUrl}/all_call_extractions`, { headers })
        ]);

        setData({
          ...analyticsRes.data,
          raw_logs: logsRes.data
        });
      } catch (err) {
        console.error("Fetch Error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-20 text-center text-slate-500">Loading Dashboard...</div>;
  
  if (!data || !data.summary) {
    return <div className="p-20 text-center">Data loaded but summary is missing. Check backend.</div>;
  }

  const evolutionData = data.evolution 
  ? Object.entries(data.evolution)
      .map(([date, stats]) => ({
        date,
        // Success Rate (%)
        rate: parseFloat(((stats.closed / stats.total) * 100).toFixed(1)),
        // Total Loads (#)
        totalLoads: stats.total, 
        timestamp: new Date(date).getTime() 
      }))
      .sort((a, b) => a.timestamp - b.timestamp) 
  : [];

  const originData = data.origin_success ? Object.entries(data.origin_success).map(([name, stats]) => ({
    name,
    rate: ((stats.closed / stats.total) * 100).toFixed(1)
  })) : [];

  const sentimentData = data.sentiment_distribution ? Object.entries(data.sentiment_distribution).map(([name, value]) => ({ 
    name, 
    value 
  })) : [];

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-10 font-sans">
      <h1 className="text-2xl font-bold mb-8">Logistics Dashboard</h1>

      {/* Metric Cards - Using ?. to prevent crashes */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <MetricCard title="Success Rate" value={`${data.summary?.success_rate}%`} label="Closed/Total" />
        <MetricCard title="Rate Efficiency" value={`${data.summary?.rate_efficiency_ratio}%`} label="Final vs Initial" />
        <MetricCard title="Avg Turns" value={data.summary?.avg_negotiation_turns} label="Turns" />
        <MetricCard title="Total Calls" value={data.summary?.total_calls} label="Total Volume" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
        {/* Evolution Chart */}
        <div className="bg-white p-6 rounded-xl border h-80">
          <h2 className="font-semibold mb-4">Evolution</h2>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={evolutionData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(str) => new Date(str).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              
              {/* Left Axis: Total Loads (#) */}
              <YAxis 
                yAxisId="left" 
                orientation="left" 
                stroke="#94a3b8" 
                tick={{ fontSize: 11 }} 
                label={{ value: 'Total Loads', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fill: '#94a3b8', fontSize: 12 } }}
              />
              
              {/* Right Axis: Success Rate (%) */}
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                domain={[0, 100]} 
                stroke="#3b82f6" 
                tick={{ fontSize: 11 }} 
                unit="%"
                label={{ value: 'Success Rate', angle: 90, position: 'insideRight', style: { textAnchor: 'middle', fill: '#3b82f6', fontSize: 12 } }}
              />

              <Tooltip />
              <Legend verticalAlign="top" height={36}/>

              {/* Total Loads - Left Axis */}
              <Line 
                yAxisId="left"
                type="monotone" 
                dataKey="totalLoads" 
                stroke="#94a3b8" 
                strokeWidth={2} 
                name="Total Loads (#)"
                dot={{ r: 4 }}
              />

              {/* Success Rate - Right Axis */}
              <Line 
                yAxisId="right"
                type="monotone" 
                dataKey="rate" 
                stroke="#3b82f6" 
                strokeWidth={3} 
                name="Success Rate (%)"
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Origin Chart */}
        <div className="bg-white p-6 rounded-xl border h-80">
          <h2 className="font-semibold mb-4">Success by Origin</h2>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={originData} layout="vertical">
              <XAxis type="number" hide />
              <YAxis dataKey="name" type="category" width={80} />
              <Tooltip />
              <Bar dataKey="rate" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <CallTable logs={data.raw_logs || []} />
    </div>
  );
}