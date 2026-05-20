import React, { useState, useEffect } from 'react';
import { Card } from '../components/ui/Card';
import { Shield, Activity, Users, AlertCircle, RefreshCw, AlertTriangle } from 'lucide-react';

const AdminDashboard = () => {
  const [alerts, setAlerts] = useState([]);

  const fetchAlerts = () => {
    fetch('http://localhost:5000/api/emergency/alerts')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setAlerts(data.alerts);
        }
      })
      .catch(console.error);
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(() => {
      fetchAlerts();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">System Admin</h1>
        <button onClick={fetchAlerts} className="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg font-medium text-sm flex items-center gap-2 hover:bg-gray-50">
          <RefreshCw className="w-4 h-4" /> Refresh Data
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'Active Nodes', value: '42', icon: Activity, color: 'text-blue-500' },
          { label: 'AI Health', value: '99.8%', icon: Shield, color: 'text-green-500' },
          { label: 'System Load', value: '24%', icon: Activity, color: 'text-purple-500' },
          { label: 'Errors/hr', value: '0.01', icon: AlertCircle, color: 'text-red-500' }
        ].map((stat, i) => (
          <Card key={i} className="p-4 flex items-center justify-between bg-gray-900 text-white border-gray-800">
            <div>
              <p className="text-gray-400 text-sm">{stat.label}</p>
              <h3 className="text-2xl font-bold">{stat.value}</h3>
            </div>
            <stat.icon className={`w-8 h-8 ${stat.color} opacity-80`} />
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><Users className="text-[#EC4899]" /> Recent Onboarding</h2>
          <div className="space-y-4 text-sm">
            {[
              { id: 1, name: 'Amulya', status: 'Confirmed' },
              { id: 2, name: 'Priya Sharma', status: 'Pending' },
              { id: 3, name: 'Ananya Rao', status: 'Pending' },
              { id: 4, name: 'Sneha Reddy', status: 'Pending' },
              { id: 5, name: 'Kavya Nair', status: 'Pending' },
              { id: 6, name: 'Pooja Verma', status: 'Pending' }
            ].map((driver) => (
              <div key={driver.id} className="flex justify-between items-center p-3 hover:bg-gray-50 rounded-lg transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-pink-100 text-[#EC4899] font-bold flex items-center justify-center rounded-full">{driver.name.charAt(0)}</div>
                  <div>
                    <p className="font-semibold text-gray-900">{driver.name}</p>
                    <p className="text-gray-500">{driver.status === 'Confirmed' ? 'Verified Rider' : 'Awaiting Verification'}</p>
                  </div>
                </div>
                {driver.status === 'Confirmed' ? (
                  <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-bold">CONFIRMED</span>
                ) : (
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs font-bold">PENDING</span>
                )}
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6 border-red-100">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-red-600"><AlertTriangle /> Emergency SOS Alerts</h2>
          <div className="space-y-4 overflow-y-auto max-h-[300px] pr-2">
            {alerts.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <Shield className="w-12 h-12 mx-auto text-green-500 mb-2 opacity-50" />
                <p>No active emergencies. System is safe.</p>
              </div>
            ) : (
              alerts.slice().reverse().map((alert, idx) => (
                <div key={alert.id} className={`p-4 rounded-xl border ${idx === 0 ? 'bg-red-50 border-red-300 shadow-sm' : 'bg-white border-gray-200'}`}>
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-red-100 text-red-600 font-bold flex items-center justify-center rounded-full">
                        {alert.username.charAt(0)}
                      </div>
                      <div>
                        <span className="font-bold text-gray-900 block">{alert.username}</span>
                        <span className="text-xs text-gray-500">{new Date(alert.time).toLocaleTimeString()}</span>
                      </div>
                    </div>
                    {alert.status === 'Active' ? (
                      <span className="px-2 py-1 bg-red-500 text-white rounded text-xs font-bold animate-pulse">ACTIVE</span>
                    ) : (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs font-bold">{alert.status}</span>
                    )}
                  </div>
                  <div className="text-sm text-gray-700 space-y-1 bg-white/50 p-2 rounded">
                    <p className="flex items-center gap-1"><strong className="text-gray-900">Pickup:</strong> {alert.location}</p>
                    {alert.lat && alert.lng && (
                      <p className="flex items-center gap-1"><strong className="text-gray-900">GPS:</strong> {alert.lat.toFixed(4)}, {alert.lng.toFixed(4)}</p>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;
