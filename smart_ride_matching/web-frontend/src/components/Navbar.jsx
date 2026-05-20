import React from 'react';
import { Link } from 'react-router-dom';
import { Shield } from 'lucide-react';

const Navbar = ({ isAuthenticated = false }) => {
  return (
    <nav className="fixed top-0 left-0 w-full z-20 px-6 py-4 flex justify-between items-center bg-white/80 backdrop-blur-md border-b border-pink-100 shadow-[0_4px_30px_rgba(249,168,212,0.1)]">
      <Link to="/" className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-[#F9A8D4] to-[#EC4899] rounded-xl flex items-center justify-center shadow-md">
          <Shield className="w-6 h-6 text-white" />
        </div>
        <span className="text-xl font-bold text-gray-900 hidden sm:block tracking-tight">
          Smart Ride
        </span>
      </Link>
      
      <div className="flex items-center gap-6">
        {!isAuthenticated && (
          <>
            <Link to="#" className="hidden md:block text-sm font-medium text-gray-600 hover:text-[#EC4899] transition-colors">
              Drive with us
            </Link>
            <Link to="#" className="hidden md:block text-sm font-medium text-gray-600 hover:text-[#EC4899] transition-colors">
              Safety
            </Link>
            <Link to="/login" className="text-sm font-semibold text-[#EC4899] hover:text-[#be185d] transition-colors">
              Log in
            </Link>
            <Link to="/login" className="bg-[#F9A8D4] hover:bg-[#EC4899] text-white px-5 py-2.5 rounded-full text-sm font-semibold transition-all shadow-md hover:shadow-lg active:scale-95">
              Sign up
            </Link>
          </>
        )}
        {isAuthenticated && (
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-pink-100 flex items-center justify-center border-2 border-white shadow-sm">
              <span className="text-sm font-bold text-[#EC4899]">US</span>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
