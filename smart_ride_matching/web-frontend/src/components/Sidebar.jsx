import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Home, MapPin, CreditCard, User, Shield, LogOut } from 'lucide-react';

const Sidebar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Mock logout
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', icon: Home, path: '/dashboard' },
    { name: 'Book a Ride', icon: MapPin, path: '/book' },
    { name: 'Payment', icon: CreditCard, path: '/payment' },
    { name: 'Profile', icon: User, path: '/profile' },
    { name: 'Admin', icon: Shield, path: '/admin' },
  ];

  return (
    <div className="h-screen w-64 bg-white border-r border-pink-100 flex flex-col fixed left-0 top-0 pt-20 z-10 shadow-[4px_0_24px_rgba(249,168,212,0.05)]">
      <div className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${
                isActive
                  ? 'bg-pink-50 text-[#EC4899]'
                  : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </div>
      
      <div className="p-4 border-t border-gray-100">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 w-full px-4 py-3 text-gray-500 hover:text-red-500 hover:bg-red-50 rounded-xl font-medium transition-all"
        >
          <LogOut className="w-5 h-5" />
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
