import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { Button } from '../components/ui/Button';
import { Shield, MapPin, Zap, Star } from 'lucide-react';

const Landing = () => {
  return (
    <div className="min-h-screen bg-[#FDF2F8] font-sans">
      <Navbar isAuthenticated={false} />
      
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 relative overflow-hidden">
        <div className="absolute top-[-10%] left-[-5%] w-96 h-96 bg-[#F9A8D4]/30 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-[-10%] right-[-5%] w-96 h-96 bg-[#EC4899]/20 rounded-full blur-3xl pointer-events-none"></div>
        
        <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
          <div className="space-y-8 text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 border border-pink-200 text-[#EC4899] font-medium text-sm backdrop-blur-sm">
              <Shield className="w-4 h-4" />
              <span>AI-Powered Women's Safe Mobility</span>
            </div>
            <h1 className="text-5xl lg:text-7xl font-extrabold text-gray-900 leading-tight">
              Ride Safely, <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#F9A8D4] to-[#EC4899]">
                Travel Proudly.
              </span>
            </h1>
            <p className="text-lg text-gray-600 max-w-lg mx-auto lg:mx-0">
              Smart Ride Matching connects you with verified drivers using AI-driven safety scoring, ensuring every journey is secure and comfortable.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link to="/login">
                <Button size="lg" className="w-full sm:w-auto">Get Started</Button>
              </Link>
              <Link to="/login">
                <Button variant="secondary" size="lg" className="w-full sm:w-auto">Become a Driver</Button>
              </Link>
            </div>
          </div>
          
          <div className="relative mx-auto w-full max-w-lg aspect-square lg:max-w-none">
            <div className="absolute inset-0 bg-gradient-to-tr from-[#F9A8D4] to-[#EC4899] rounded-full opacity-20 blur-3xl"></div>
            <img src="/girl_scooter.png" alt="Hero illustration" className="relative z-10 w-full h-full object-contain drop-shadow-2xl hover:scale-105 transition-transform duration-700" />
            
            {/* Floating Badges */}
            <div className="absolute top-10 left-0 bg-white/80 backdrop-blur-md p-4 rounded-2xl shadow-xl border border-white flex items-center gap-3 animate-bounce" style={{ animationDuration: '3s' }}>
              <div className="bg-green-100 p-2 rounded-full text-green-600">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-500 font-bold uppercase tracking-wider">Verified</p>
                <p className="font-bold text-gray-900">Drivers</p>
              </div>
            </div>
            
            <div className="absolute bottom-10 right-0 bg-white/80 backdrop-blur-md p-4 rounded-2xl shadow-xl border border-white flex items-center gap-3 animate-bounce" style={{ animationDuration: '4s', animationDelay: '1s' }}>
              <div className="bg-purple-100 p-2 rounded-full text-purple-600">
                <Star className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-500 font-bold uppercase tracking-wider">Safety Rating</p>
                <p className="font-bold text-gray-900">4.9/5.0</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Why Choose Smart Ride?</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">Experience the premium standard in ride-matching, built exclusively with safety and comfort in mind.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Shield, title: 'AI Safety Scoring', desc: 'Every driver is evaluated continuously to ensure the highest safety standards.' },
              { icon: MapPin, title: 'Smart Routing', desc: 'Real-time optimized routes that avoid unsafe zones and minimize ETA.' },
              { icon: Zap, title: 'Instant Matching', desc: 'Our advanced algorithm connects you with the perfect driver in seconds.' }
            ].map((feat, i) => (
              <div key={i} className="p-8 rounded-3xl bg-pink-50/50 border border-pink-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center shadow-sm mb-6 text-[#EC4899]">
                  <feat.icon className="w-7 h-7" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feat.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Footer Placeholder */}
      <footer className="bg-gray-900 text-gray-300 py-12 px-6">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Shield className="text-[#F9A8D4]" />
            <span className="font-bold text-white text-xl">Smart Ride</span>
          </div>
          <p className="text-sm">© 2026 Smart Ride Matching. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
