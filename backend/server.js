const express = require('express');
const cors = require('cors');
const PDFDocument = require('pdfkit');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: [
    'http://localhost:5173',
    'http://localhost:3000',
    /\.vercel\.app$/,
    process.env.FRONTEND_URL
  ].filter(Boolean),
  credentials: true
}));
app.use(express.json());

// --- IN-MEMORY DATA STORAGE ---
// Keeps the backend simple without needing a database. Data resets on server restart.
let users = [];
let rides = [];
let emergencyContacts = [];
let emergencyAlerts = [];
let paymentMethods = [
  { id: 'pm_1', type: 'VISA', last4: '4242', exp: '12/28', isDefault: true },
  { id: 'pm_2', type: 'UPI', upiId: 'amulya@ybl', provider: 'Google Pay', isDefault: false }
];
let wallet = { balance: 3540 };

// ==========================================
// 1. AUTHENTICATION
// ==========================================

app.post('/api/signup', (req, res) => {
  const { name, email, password, username, gender } = req.body;
  const userIdentifier = username || email;

  if (!userIdentifier || !password) {
    return res.status(400).json({ detail: 'Username/Email and password are required.' });
  }

  // Check if user already exists
  if (users.find(u => u.username === userIdentifier)) {
    return res.status(400).json({ detail: 'User already exists.' });
  }

  const newUser = {
    id: Date.now().toString(),
    username: userIdentifier,
    password, // Storing in plain text only because this is a simple mock backend
    name: name || userIdentifier,
    phone: '',
    gender: gender || 'female', // Default to female for the SafeHer platform if not provided
    createdAt: new Date()
  };

  users.push(newUser);
  res.json({ success: true, message: 'Account created successfully!' });
});

app.post('/api/login', (req, res) => {
  const { email, password, username } = req.body;
  const userIdentifier = username || email;

  if (!userIdentifier || !password) {
    return res.status(400).json({ detail: 'Username/Email and password are required.' });
  }

  const user = users.find(u => u.username === userIdentifier && u.password === password);
  
  if (!user) {
    return res.status(401).json({ detail: 'Invalid username or password.' });
  }

  res.json({ 
    success: true, 
    message: 'Login successful!',
    token: `mock-jwt-token-${user.id}`
  });
});

// ==========================================
// 2. RIDE BOOKING
// ==========================================

app.post('/api/book-ride', (req, res) => {
  const { username, pickup, destination, fare, eta, rideType } = req.body;
  
  if (!pickup || !destination) {
    return res.status(400).json({ detail: 'Pickup and destination are required.' });
  }

  const ride = {
    id: `RIDE-${Date.now()}`,
    username: username || 'guest',
    pickup,
    destination,
    fare: fare || 0,
    eta: eta || 0,
    rideType: rideType || 'SafeHer Auto',
    status: 'Confirmed',
    timestamp: new Date()
  };

  rides.push(ride);
  res.json({ success: true, message: 'Ride booked successfully', ride });
});

app.get('/api/rides', (req, res) => {
  const { username } = req.query;
  
  // If a username is provided, filter rides for that user, otherwise return all rides
  const result = username ? rides.filter(r => r.username === username) : rides;
  res.json({ success: true, rides: result });
});

// ==========================================
// 3. PROFILE MANAGEMENT
// ==========================================

app.get('/api/profile', (req, res) => {
  const { username } = req.query;
  const user = users.find(u => u.username === username);
  
  if (!user) return res.status(404).json({ detail: 'User not found' });
  
  // Return user without password
  const { password, ...safeUser } = user;
  res.json({ success: true, profile: safeUser });
});

app.put('/api/profile', (req, res) => {
  const { username, name, phone } = req.body;
  const userIndex = users.findIndex(u => u.username === username);
  
  if (userIndex === -1) return res.status(404).json({ detail: 'User not found' });
  
  if (name) users[userIndex].name = name;
  if (phone) users[userIndex].phone = phone;
  
  res.json({ success: true, message: 'Profile updated successfully', profile: users[userIndex] });
});

// ==========================================
// 4. EMERGENCY CONTACTS
// ==========================================

app.post('/api/emergency', (req, res) => {
  const { username, contactName, contactPhone, relation } = req.body;
  
  if (!contactName || !contactPhone) {
    return res.status(400).json({ detail: 'Contact name and phone are required' });
  }

  const newContact = {
    id: Date.now().toString(),
    username: username || 'guest',
    contactName,
    contactPhone,
    relation: relation || 'Family'
  };

  emergencyContacts.push(newContact);
  res.json({ success: true, message: 'Emergency contact added', contact: newContact });
});

app.get('/api/emergency', (req, res) => {
  const { username } = req.query;
  const contacts = username ? emergencyContacts.filter(c => c.username === username) : emergencyContacts;
  res.json({ success: true, contacts });
});

app.delete('/api/emergency', (req, res) => {
  const { id } = req.query;
  const initialLength = emergencyContacts.length;
  
  emergencyContacts = emergencyContacts.filter(c => c.id !== id);
  
  if (emergencyContacts.length === initialLength) {
    return res.status(404).json({ detail: 'Contact not found' });
  }
  
  res.json({ success: true, message: 'Contact deleted successfully' });
});

// ==========================================
// 5. ADMIN
// ==========================================

app.get('/api/admin/users', (req, res) => {
  // Strip passwords for admin view and filter ONLY female users
  const safeUsers = users
    .filter(u => u.gender === 'female')
    .map(u => {
      const { password, ...safeUser } = u;
      return safeUser;
    });
  
  res.json({ success: true, users: safeUsers });
});

app.get('/api/admin/rides', (req, res) => {
  res.json({ success: true, rides });
});

// ==========================================
// 6. PAYMENT, WALLET, & INVOICE
// ==========================================

app.post('/api/payment/add-method', (req, res) => {
  const { type, last4, exp, upiId, provider } = req.body;
  const newMethod = {
    id: `pm_${Date.now()}`,
    type: type || 'Card',
    last4: last4 || Math.floor(1000 + Math.random() * 9000).toString(),
    exp: exp || '12/29',
    upiId,
    provider,
    isDefault: paymentMethods.length === 0
  };
  paymentMethods.push(newMethod);
  res.json({ success: true, method: newMethod });
});

app.get('/api/payment/methods', (req, res) => {
  res.json({ success: true, methods: paymentMethods });
});

app.get('/api/payment/transactions', (req, res) => {
  // Use rides as transactions, generating some mock ones if empty
  const transactions = rides.map(r => ({
    id: r.id,
    date: r.timestamp,
    distance: `${Math.max(1, Math.round(r.eta / 3))} km`,
    baseFare: Math.round(r.fare * 0.4),
    distanceFare: Math.round(r.fare * 0.6),
    total: r.fare
  }));
  res.json({ success: true, transactions });
});

app.get('/api/wallet', (req, res) => {
  res.json({ success: true, wallet });
});

app.post('/api/wallet/topup', (req, res) => {
  const { amount } = req.body;
  if (!amount) return res.status(400).json({ detail: 'Amount required' });
  wallet.balance += parseInt(amount, 10);
  res.json({ success: true, balance: wallet.balance });
});

app.get('/api/payment/invoice/:rideId', (req, res) => {
  const { rideId } = req.params;
  const ride = rides.find(r => r.id === rideId);
  
  if (!ride) {
    return res.status(404).json({ detail: 'Ride not found' });
  }

  const doc = new PDFDocument();
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', `attachment; filename=invoice.pdf`);
  
  doc.pipe(res);
  
  doc.fontSize(25).text('Smart Ride Invoice', { align: 'center' });
  doc.moveDown();
  doc.fontSize(14).text(`Trip ID: ${ride.id}`);
  doc.text(`Date: ${new Date(ride.timestamp).toLocaleString()}`);
  doc.text(`Pickup: ${ride.pickup}`);
  doc.text(`Destination: ${ride.destination}`);
  doc.moveDown();
  doc.text(`Distance: ${Math.max(1, Math.round(ride.eta / 3))} km`);
  doc.text(`Total Amount: INR ${ride.fare}`);
  
  doc.end();
});

// ==========================================
// 7. EMERGENCY SOS
// ==========================================

app.post('/api/emergency/alert', (req, res) => {
  const { username, lat, lng, location } = req.body;
  
  const newAlert = {
    id: `SOS-${Date.now()}`,
    username: username || 'guest',
    lat: lat || null,
    lng: lng || null,
    location: location || 'unknown',
    time: new Date(),
    status: 'Active'
  };
  
  emergencyAlerts.push(newAlert);
  
  console.log(`\n===========================================`);
  console.log(`🚨 EMERGENCY ALERT TRIGGERED BY ${newAlert.username.toUpperCase()}!`);
  console.log(`📍 Location: ${newAlert.location}`);
  console.log(`🧭 GPS: Lat ${newAlert.lat}, Lng ${newAlert.lng}`);
  console.log(`===========================================\n`);
  
  res.json({ success: true, message: 'Alert sent' });
});

app.get('/api/emergency/alerts', (req, res) => {
  res.json({ success: true, alerts: emergencyAlerts });
});

// Global Error Handler for invalid JSON requests
app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({ detail: 'Invalid JSON payload' });
  }
  next();
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
