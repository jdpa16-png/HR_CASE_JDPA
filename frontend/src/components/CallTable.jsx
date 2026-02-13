import React from 'react';

export default function CallTable({ logs }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
        <h2 className="font-semibold text-slate-800">Recent Call Logs</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/50">
              {["Date", "Carrier", "Route", "Negotiation", "Status", "Final Rate"].map((header) => (
                <th key={header} className="px-6 py-3 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {logs.map((log) => (
              <tr key={log.Run_ID} className="hover:bg-slate-50 transition-colors group">
                {/* Date */}
                <td className="px-6 py-4 text-sm text-slate-600 whitespace-nowrap">
                  {new Date(log.date_time).toLocaleDateString()}
                </td>
                
                {/* Carrier */}
                <td className="px-6 py-4">
                  <div className="text-sm font-medium text-slate-900">{log.Carrier_Legal_Name || "N/A"}</div>
                  <div className="text-xs text-slate-400">{log.mc_number}</div>
                </td>

                {/* Route */}
                <td className="px-6 py-4 text-sm text-slate-600">
                  {log.Origin} → {log.destination}
                </td>

                {/* Turns/Negotiation */}
                <td className="px-6 py-4 text-sm text-slate-600 text-center">
                  <span className="bg-slate-100 px-2 py-1 rounded text-xs font-mono">
                    {log.turns} turns
                  </span>
                </td>

                {/* Status Badge */}
                <td className="px-6 py-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                    log.flag_closed_deal 
                      ? 'bg-emerald-100 text-emerald-700' 
                      : 'bg-rose-100 text-rose-700'
                  }`}>
                    {log.flag_closed_deal ? 'Closed' : 'Failed'}
                  </span>
                </td>

                {/* Financials */}
                <td className="px-6 py-4 text-sm font-semibold text-slate-900">
                  ${log.final_rate || log.original_rate}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}