import React, { useState, useEffect } from 'react';
import API_BASE from '../lib/api';
import { Card } from '../components/ui/Card';
import { Shield, Car, UserCheck, AlertTriangle } from 'lucide-react';

const Dashboard = () => {
  const [recentRides, setRecentRides] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/rides`)
      .then(res => res.json())
      .then(data => {
        if (data.success && data.rides) {
          setRecentRides(data.rides);
        }
      })
      .catch(err => console.error("Failed to fetch rides:", err));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Overview</h1>
        <div className="px-4 py-2 bg-green-100 text-green-700 rounded-full font-semibold text-sm flex items-center gap-2">
          <Shield className="w-4 h-4" /> System Secure
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Rides" value="1,284" icon={Car} color="bg-blue-100 text-blue-600" />
        <StatCard title="Verified Drivers" value="342" icon={UserCheck} color="bg-green-100 text-green-600" />
        <StatCard title="Avg Safety Score" value="4.8/5" icon={Shield} color="bg-purple-100 text-purple-600" />
        <StatCard title="Urgent Alerts" value="0" icon={AlertTriangle} color="bg-red-100 text-red-600" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 p-6">
          <h2 className="text-xl font-bold mb-4">Recent Ride Activity</h2>
          <div className="space-y-4">
            {recentRides.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No recent rides found.</p>
            ) : (
              recentRides.slice().reverse().map((trip) => (
                <div key={trip.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-pink-100 flex items-center justify-center font-bold text-[#EC4899]">
                      {trip.username ? trip.username.charAt(0).toUpperCase() : 'U'}
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">Trip to {trip.destination}</p>
                      <p className="text-sm text-gray-500">{new Date(trip.timestamp).toLocaleTimeString()}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-gray-900">₹{trip.fare}</p>
                    <p className="text-sm text-green-600">{trip.status}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>
        
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-4">Safety Profile</h2>
          <div className="flex flex-col items-center justify-center py-6 text-center">
            <div className="w-24 h-24 rounded-full border-4 border-[#F9A8D4] flex items-center justify-center mb-4 relative">
              <Shield className="w-10 h-10 text-[#EC4899]" />
              <div className="absolute -bottom-2 -right-2 bg-green-500 w-6 h-6 rounded-full border-2 border-white"></div>
            </div>
            <h3 className="font-bold text-lg">Amulya</h3>
            <p className="text-gray-500 text-sm">Rider Level: Gold</p>
            <div className="mt-6 w-full p-4 bg-pink-50 rounded-xl border border-pink-100">
              <p className="text-sm font-medium text-gray-700 mb-2">Profile Verification</p>
              <div className="w-full bg-white rounded-full h-2">
                <div className="bg-gradient-to-r from-[#F9A8D4] to-[#EC4899] h-2 rounded-full w-[80%]"></div>
              </div>
              <p className="text-xs text-right mt-1 text-gray-500">80% Complete</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon: Icon, color }) => (
  <Card className="p-6 flex items-center gap-4">
    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${color}`}>
      <Icon className="w-6 h-6" />
    </div>
    <div>
      <p className="text-gray-500 text-sm font-medium">{title}</p>
      <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
    </div>
  </Card>
);

export default Dashboard;
