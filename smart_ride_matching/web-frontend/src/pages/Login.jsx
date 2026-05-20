import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [loginMethod, setLoginMethod] = useState('phone'); // 'phone' or 'email'
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    
    if (!identifier || !password) {
      setErrorMessage('Please fill in all fields.');
      return;
    }
    
    setIsLoading(true);
    
    try {
      const endpoint = isLoginMode ? '/api/login' : '/api/signup';
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: identifier, password }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }
      
      if (isLoginMode) {
        // Redirect to React Dashboard using React Router
        navigate('/dashboard');
      } else {
        setIsLoginMode(true);
        setErrorMessage('Signup successful! Please log in.'); // Will show in green temporarily
        setPassword('');
      }
    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col lg:flex-row font-sans">
      
      {/* Left Panel - Hero Section */}
      <div className="lg:flex-1 bg-[#F9A8D4] relative overflow-hidden flex flex-col justify-center items-center p-12 text-center lg:text-left pt-24 lg:pt-12">
        {/* Decorative background elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] bg-white opacity-10 rounded-full blur-3xl"></div>
          <div className="absolute top-[60%] -right-[10%] w-[60%] h-[60%] bg-[#EC4899] opacity-20 rounded-full blur-3xl"></div>
        </div>

        <div className="relative z-10 max-w-lg w-full flex flex-col items-center lg:items-start">
          <h1 className="text-4xl lg:text-6xl font-extrabold text-gray-900 mb-6 leading-tight">
            Fast, Safe & <br className="hidden lg:block"/> Affordable Ride Matching.
          </h1>
          <p className="text-lg lg:text-xl text-gray-800 font-medium mb-12 opacity-90 max-w-md">
            Join thousands of verified riders and drivers. Experience seamless mobility built for you.
          </p>

          {/* Abstract Illustration */}
          <div className="w-full max-w-md aspect-video bg-white/20 rounded-2xl border-2 border-white/30 flex items-center justify-center backdrop-blur-sm shadow-xl relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-tr from-white/10 to-transparent"></div>
            <img src="/girl_scooter.png" alt="Girl on scooter" className="object-cover w-full h-full opacity-90 group-hover:scale-105 transition-transform duration-500" />
          </div>
        </div>
      </div>

      {/* Right Panel - Auth Section */}
      <div className="lg:flex-1 bg-white flex flex-col justify-center items-center p-6 lg:p-12 relative pt-12 lg:pt-0 shadow-[-20px_0_40px_-10px_rgba(0,0,0,0.05)] z-0 lg:z-10">
        <div className="w-full max-w-md">
          
          <div className="mb-8 text-center lg:text-left">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {isLoginMode ? 'Welcome Back' : 'Create an Account'}
            </h2>
            <p className="text-gray-500">
              {isLoginMode ? 'Log in to your Smart Ride account' : 'Join Smart Ride today'}
            </p>
          </div>

          <div className="bg-white lg:shadow-xl lg:border border-gray-100 rounded-2xl lg:p-8">
            
            {/* Method Tabs - Only show in Login mode for logic simplicity */}
            {isLoginMode && (
              <div className="flex bg-gray-100 p-1 rounded-lg mb-6">
                <button 
                  onClick={() => setLoginMethod('phone')}
                  className={`flex-1 py-2 text-sm font-semibold rounded-md transition-all ${loginMethod === 'phone' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
                >
                  Phone Number
                </button>
                <button 
                  onClick={() => setLoginMethod('email')}
                  className={`flex-1 py-2 text-sm font-semibold rounded-md transition-all ${loginMethod === 'email' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
                >
                  Email / Username
                </button>
              </div>
            )}

            {errorMessage && (
              <div className={`mb-4 p-3 rounded text-sm font-medium ${errorMessage.includes('successful') ? 'bg-green-100 text-green-700' : 'bg-red-50 text-red-600'}`}>
                {errorMessage}
              </div>
            )}

            <form className="space-y-5" onSubmit={handleSubmit}>
              
              {isLoginMode && loginMethod === 'phone' ? (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Mobile Number</label>
                  <div className="flex">
                    <span className="inline-flex items-center px-4 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500 sm:text-sm font-medium">
                      +91
                    </span>
                    <input 
                      type="text" 
                      className="flex-1 min-w-0 block w-full px-4 py-3 rounded-none rounded-r-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#F9A8D4] focus:border-transparent transition-all duration-200" 
                      placeholder="99999 99999"
                      value={identifier}
                      onChange={(e) => setIdentifier(e.target.value)}
                    />
                  </div>
                </div>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Username / Email</label>
                  <input 
                    type="text" 
                    className="input-field" 
                    placeholder="Enter your username" 
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                  />
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input 
                  type="password" 
                  className="input-field" 
                  placeholder="••••••••" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              {isLoginMode && (
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input id="remember-me" type="checkbox" className="h-4 w-4 text-[#EC4899] focus:ring-[#F9A8D4] border-gray-300 rounded" />
                    <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-600">
                      Remember me
                    </label>
                  </div>
                  <div className="text-sm">
                    <a href="#" className="font-semibold text-gray-900 hover:text-[#EC4899] transition-colors">
                      Forgot password?
                    </a>
                  </div>
                </div>
              )}

              <button 
                type="submit" 
                className={`btn-primary mt-2 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
                disabled={isLoading}
              >
                {isLoading ? 'Processing...' : (isLoginMode ? 'Continue' : 'Sign Up')}
              </button>
            </form>

            <div className="mt-8">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-200"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">Or continue with</span>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-2 gap-4">
                <button className="btn-social">
                  <svg className="w-5 h-5" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                  </svg>
                  <span className="hidden sm:inline">Google</span>
                </button>
                <button className="btn-social">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.04 2.26-.79 3.55-.79 2.05.08 3.55.97 4.54 2.45-1.78 1.05-1.46 3.5.21 4.51-.55 1.61-1.39 3.33-3.38 5.25M12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25"/>
                  </svg>
                  <span className="hidden sm:inline">Apple</span>
                </button>
              </div>
            </div>
            
            <p className="mt-8 text-center text-xs text-gray-500">
              By clicking "Continue", you agree to our <br className="hidden sm:block"/>
              <a href="#" className="underline hover:text-gray-900">Terms of Service</a> and <a href="#" className="underline hover:text-gray-900">Privacy Policy</a>.
            </p>

          </div>

          <p className="mt-6 text-center text-sm text-gray-600">
            {isLoginMode ? "Don't have an account? " : "Already have an account? "}
            <button 
              onClick={() => {
                setIsLoginMode(!isLoginMode);
                setErrorMessage('');
              }} 
              className="font-bold text-gray-900 hover:text-[#EC4899] hover:underline"
            >
              {isLoginMode ? "Sign up" : "Log in"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
