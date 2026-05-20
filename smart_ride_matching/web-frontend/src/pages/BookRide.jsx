import React, { useState, useEffect } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { MapPin, Navigation, Clock, Shield, Star, CheckCircle2, Car } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';

const SHIVAMOGGA_CENTER = [13.9299, 75.5681]; // Shivamogga, Karnataka

const LOCATIONS = [
  "Shivamogga Railway Station",
  "Bus Stand",
  "BH Road",
  "Vinobanagar",
  "Gandhi Park",
  "Jayanagar"
];

const LOCATION_COORDS = {
  "Shivamogga Railway Station": [13.9310, 75.5690],
  "Kuvempu Road": [13.9330, 75.5710],
  "Vinobanagar": [13.9350, 75.5750],
  "Savalanga Road": [13.9400, 75.5800],
  "Gopala": [13.9250, 75.5650],
  "Gandhi Park": [13.9280, 75.5720],
  "BH Road": [13.9300, 75.5760],
  "Bus Stand": [13.9320, 75.5780],
  "Jayanagar": [13.9200, 75.5600],
  "Shimoga Airport": [13.8500, 75.6300]
};

// Default driver start for animation
const MOCK_DRIVER_START = [13.9200, 75.5600];

const BookRide = () => {
  const [step, setStep] = useState(1); // 1: Search, 2: Matching, 3: Confirmed
  const [pickup, setPickup] = useState("");
  const [dropoff, setDropoff] = useState("");
  
  const [pickupCoords, setPickupCoords] = useState(null);
  const [dropoffCoords, setDropoffCoords] = useState(null);
  const [driverPos, setDriverPos] = useState(MOCK_DRIVER_START);
  
  const [fare, setFare] = useState({ auto: 0, plus: 0 });
  const [eta, setEta] = useState(0);

  // Suggestions state
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredLocations, setFilteredLocations] = useState(LOCATIONS);
  
  const [showPickupSuggestions, setShowPickupSuggestions] = useState(false);
  const [filteredPickupLocations, setFilteredPickupLocations] = useState(LOCATIONS);

  useEffect(() => {
    if (step === 3 && pickupCoords) {
      // Very simple animation for the driver moving towards pickup
      const interval = setInterval(() => {
        setDriverPos(prev => {
          const newLat = prev[0] + (pickupCoords[0] - prev[0]) * 0.1;
          const newLng = prev[1] + (pickupCoords[1] - prev[1]) * 0.1;
          return [newLat, newLng];
        });
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [step, pickupCoords]);

  const handleBook = async () => {
    try {
      await fetch('http://localhost:5000/api/book-ride', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: 'Amulya', // Mocking logged in user
          pickup,
          destination: dropoff,
          fare: fare.auto,
          eta,
          rideType: 'SafeHer Auto'
        })
      });
    } catch (err) {
      console.error("Failed to book ride:", err);
    }
    
    setStep(2);
    setTimeout(() => {
      setStep(3);
    }, 3000);
  };

  const handleSOS = () => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;
        
        try {
          const res = await fetch('http://localhost:5000/api/emergency/alert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              username: 'Amulya', 
              lat: latitude, 
              lng: longitude, 
              location: pickup || 'Unknown Location' 
            })
          });
          
          const data = await res.json();
          if (data.success) {
            alert(`🚨 Emergency alert sent! Contacting help...\n\nLocation: ${pickup || 'Unknown Location'}`);
            
            setTimeout(() => {
              alert('📞 Calling emergency contact...');
            }, 1500);
            
            setTimeout(() => {
              alert('📍 Live Location shared successfully.');
            }, 3000);
          }
        } catch (err) {
          console.error('SOS Failed:', err);
          alert('Failed to connect to server. Please dial emergency services directly!');
        }
      }, (error) => {
        alert("🚨 Could not access GPS. Please ensure location services are enabled!");
      });
    } else {
      alert("🚨 Geolocation is not supported by your browser.");
    }
  };

  const handlePickupChange = (val) => {
    setPickup(val);
    setShowPickupSuggestions(true);
    setFilteredPickupLocations(LOCATIONS.filter(l => l.toLowerCase().includes(val.toLowerCase())));
  };

  const selectPickupLocation = (loc) => {
    setPickup(loc);
    setShowPickupSuggestions(false);
    calculateRoute(loc, dropoff);
  };

  const handleLocationChange = (val) => {
    setDropoff(val);
    setShowSuggestions(true);
    setFilteredLocations(LOCATIONS.filter(l => l.toLowerCase().includes(val.toLowerCase())));
  };

  const calculateRoute = (pickupLoc, dropoffLoc) => {
    const pCoords = LOCATION_COORDS[pickupLoc];
    const dCoords = LOCATION_COORDS[dropoffLoc];
    
    if (pCoords) setPickupCoords(pCoords);
    if (dCoords) setDropoffCoords(dCoords);
    
    if (pCoords && dCoords) {
      // Calculate simple euclidean distance in roughly km
      const dist = Math.sqrt(Math.pow(pCoords[0] - dCoords[0], 2) + Math.pow(pCoords[1] - dCoords[1], 2)) * 111;
      
      const distanceKm = Math.max(1, dist);
      setFare({
        auto: Math.round(30 + distanceKm * 15),
        plus: Math.round(50 + distanceKm * 25)
      });
      setEta(Math.round(distanceKm * 3));
    }
  };

  const selectLocation = (loc) => {
    setDropoff(loc);
    setShowSuggestions(false);
    calculateRoute(pickup, loc);
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-[calc(100vh-8rem)]">
      {/* Left Panel - Booking Controls */}
      <div className="w-full lg:w-1/3 flex flex-col gap-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Book a Ride</h1>
        
        {step === 1 && (
          <Card className="p-6 flex-1 flex flex-col gap-6 overflow-visible">
            <div className="space-y-4">
              <div className="relative z-20">
                <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Input 
                  value={pickup} 
                  onChange={(e) => handlePickupChange(e.target.value)}
                  onFocus={() => setShowPickupSuggestions(true)}
                  onBlur={() => setTimeout(() => setShowPickupSuggestions(false), 200)}
                  placeholder="Where are you?" 
                  className="pl-12" 
                />
                
                {/* Pickup Autocomplete Dropdown */}
                {showPickupSuggestions && pickup.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-48 overflow-y-auto">
                    {filteredPickupLocations.map(loc => (
                      <div 
                        key={loc} 
                        className="px-4 py-2 hover:bg-pink-50 cursor-pointer text-gray-700"
                        onMouseDown={(e) => { e.preventDefault(); selectPickupLocation(loc); }}
                      >
                        {loc}
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <div className="relative z-10">
                <Navigation className="absolute left-4 top-1/2 -translate-y-1/2 text-[#EC4899] w-5 h-5" />
                <Input 
                  placeholder="Where to in Shivamogga?" 
                  className="pl-12" 
                  value={dropoff}
                  onChange={(e) => handleLocationChange(e.target.value)}
                  onFocus={() => setShowSuggestions(true)}
                  onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                />
                
                {/* Autocomplete Dropdown */}
                {showSuggestions && dropoff.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-48 overflow-y-auto">
                    {filteredLocations.map(loc => (
                      <div 
                        key={loc} 
                        className="px-4 py-2 hover:bg-pink-50 cursor-pointer text-gray-700"
                        onMouseDown={(e) => { e.preventDefault(); selectLocation(loc); }}
                      >
                        {loc}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {dropoffCoords && (
              <div className="border-t border-gray-100 pt-6">
                <h3 className="font-semibold text-gray-900 mb-4">Available Options</h3>
                <div className="space-y-3">
                  <div className="p-4 rounded-xl border-2 border-[#F9A8D4] bg-pink-50 flex justify-between items-center cursor-pointer transition-all">
                    <div className="flex items-center gap-4">
                      <img src="/girl_scooter.png" alt="Scooter" className="w-12 h-12 object-contain" />
                      <div>
                        <p className="font-bold text-gray-900">SafeHer Auto</p>
                        <p className="text-sm text-gray-500">2 mins away • 1 seat</p>
                      </div>
                    </div>
                    <p className="font-bold text-lg">₹{fare.auto}</p>
                  </div>
                  
                  <div className="p-4 rounded-xl border border-gray-200 hover:border-[#F9A8D4] flex justify-between items-center cursor-pointer transition-all">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
                        <Shield className="w-6 h-6 text-gray-400" />
                      </div>
                      <div>
                        <p className="font-bold text-gray-900">SafeHer Plus</p>
                        <p className="text-sm text-gray-500">5 mins away • 4 seats</p>
                      </div>
                    </div>
                    <p className="font-bold text-lg">₹{fare.plus}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="mt-auto">
              <Button className="w-full" size="lg" onClick={handleBook} disabled={!dropoffCoords}>
                Request SafeHer Auto
              </Button>
            </div>
          </Card>
        )}

        {step === 2 && (
          <Card className="p-8 flex-1 flex flex-col items-center justify-center text-center gap-6">
            <div className="relative w-24 h-24">
              <div className="absolute inset-0 border-4 border-pink-100 rounded-full border-t-[#EC4899] animate-spin"></div>
              <div className="absolute inset-2 bg-pink-50 rounded-full flex items-center justify-center">
                <Shield className="w-8 h-8 text-[#EC4899]" />
              </div>
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Finding your safe ride...</h2>
              <p className="text-gray-500">Scanning verified drivers in Shivamogga using AI metrics.</p>
            </div>
          </Card>
        )}

        {step === 3 && (
          <Card className="p-6 flex-1 flex flex-col gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-8 h-8 text-green-600" />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Driver Assigned!</h2>
              <p className="text-gray-500 text-sm">Arriving in 2 mins</p>
            </div>

            <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-sm font-bold text-[#EC4899] border border-pink-100">
                  S
                </div>
                <div>
                  <p className="font-bold text-gray-900">Sneha Patel</p>
                  <div className="flex items-center text-sm text-gray-500 gap-1">
                    <Star className="w-3 h-3 text-yellow-400 fill-current" /> 4.9 • <Shield className="w-3 h-3 text-green-500" /> Verified
                  </div>
                </div>
              </div>
              <div className="text-right">
                <p className="font-bold text-gray-900 bg-gray-200 px-2 py-1 rounded text-sm">KA 14 AB 1234</p>
                <p className="text-sm text-gray-500 mt-1">White Honda Activa</p>
              </div>
            </div>

            <div className="bg-red-50 p-4 rounded-xl border border-red-100 flex items-center justify-between">
              <div>
                <p className="font-semibold text-red-900">Emergency SOS</p>
                <p className="text-xs text-red-700">Share live location with contacts</p>
              </div>
              <Button variant="danger" size="sm" onClick={handleSOS}>Activate</Button>
            </div>

            <div className="mt-auto">
              <Button className="w-full" size="lg" onClick={() => setStep(1)}>Cancel Ride</Button>
            </div>
          </Card>
        )}
      </div>

      {/* Right Panel - Real Leaflet Map */}
      <div className="flex-1 bg-gray-200 rounded-3xl overflow-hidden relative shadow-inner z-0 border border-gray-200">
        <MapContainer 
          center={SHIVAMOGGA_CENTER} 
          zoom={14} 
          style={{ height: '100%', width: '100%', zIndex: 0 }}
          zoomControl={false}
        >
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {pickupCoords && (
            <Marker position={pickupCoords}>
              <Popup>Pickup Location</Popup>
            </Marker>
          )}

          {step >= 1 && dropoffCoords && (
            <>
              <Marker position={dropoffCoords}>
                <Popup>Dropoff Location</Popup>
              </Marker>
              <Polyline 
                positions={[pickupCoords, dropoffCoords]} 
                color="#EC4899" 
                dashArray="10, 10" 
                weight={4}
              />
            </>
          )}

          {step === 3 && (
            <Marker position={driverPos}>
              <Popup>Driver</Popup>
            </Marker>
          )}

        </MapContainer>

        {/* Floating ETA */}
        {step === 3 && (
          <div className="absolute top-6 right-6 bg-white/90 backdrop-blur-md p-4 rounded-xl shadow-lg border border-pink-100 flex items-center gap-3 z-10">
            <Clock className="text-[#EC4899] w-5 h-5" />
            <div>
              <p className="text-xs text-gray-500 font-bold uppercase">Est. Travel Time</p>
              <p className="font-bold text-gray-900 text-lg">{eta} mins</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BookRide;
