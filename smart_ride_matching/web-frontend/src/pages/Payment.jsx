import React, { useState, useEffect } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { CreditCard, Wallet, Receipt } from 'lucide-react';

const Payment = () => {
  const [methods, setMethods] = useState([]);
  const [balance, setBalance] = useState(0);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/payment/methods')
      .then(res => res.json())
      .then(data => data.success && setMethods(data.methods))
      .catch(console.error);
      
    fetch('http://localhost:5000/api/wallet')
      .then(res => res.json())
      .then(data => data.success && setBalance(data.wallet.balance))
      .catch(console.error);

    fetch('http://localhost:5000/api/payment/transactions')
      .then(res => res.json())
      .then(data => data.success && setTransactions(data.transactions))
      .catch(console.error);
  }, []);

  const handleAddMethod = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/payment/add-method', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'VISA', provider: 'HDFC Bank' })
      });
      const data = await res.json();
      if (data.success) setMethods([...methods, data.method]);
    } catch (err) {
      console.error(err);
    }
  };

  const handleTopUp = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/wallet/topup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: 500 })
      });
      const data = await res.json();
      if (data.success) setBalance(data.balance);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDownloadInvoice = async (rideId) => {
    if (!rideId) return alert('No transaction selected');
    try {
      const response = await fetch(`http://localhost:5000/api/payment/invoice/${rideId}`);
      if (!response.ok) throw new Error('Failed to download invoice');
      
      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `invoice.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download error:', err);
      alert('Error downloading invoice. Please try again.');
    }
  };

  const latestTransaction = transactions.length > 0 ? transactions[transactions.length - 1] : null;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Payment & Billing</h1>
      
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <Card className="p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <CreditCard className="text-[#EC4899]" /> Payment Methods
            </h2>
            
            <div className="space-y-4">
              {methods.map((method, index) => (
                <div key={method.id || index} className={`p-4 rounded-xl ${method.isDefault ? 'border-2 border-[#F9A8D4] bg-pink-50' : 'border border-gray-200 hover:border-pink-200'} flex items-center justify-between cursor-pointer transition-colors`}>
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-8 rounded flex items-center justify-center font-bold text-xs ${method.type === 'VISA' ? 'bg-white border border-gray-200 text-blue-900 italic' : 'bg-black text-white'}`}>
                      {method.type}
                    </div>
                    <div>
                      {method.type === 'VISA' || method.type === 'Card' ? (
                        <>
                          <p className="font-bold text-gray-900">•••• •••• •••• {method.last4}</p>
                          <p className="text-sm text-gray-500">Expires {method.exp}</p>
                        </>
                      ) : (
                        <>
                          <p className="font-semibold text-gray-900">{method.upiId}</p>
                          <p className="text-sm text-gray-500">{method.provider}</p>
                        </>
                      )}
                    </div>
                  </div>
                  {method.isDefault && <span className="text-[#EC4899] font-semibold text-sm">Default</span>}
                </div>
              ))}

              <Button variant="secondary" className="w-full border-dashed border-2" onClick={handleAddMethod}>
                + Add New Payment Method
              </Button>
            </div>
          </Card>
          
          <Card className="p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Wallet className="text-[#EC4899]" /> Wallet Balance
            </h2>
            <div className="flex items-center justify-between p-6 bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl text-white shadow-lg">
              <div>
                <p className="text-gray-400 font-medium mb-1">Available Balance</p>
                <h3 className="text-4xl font-bold">₹{balance}</h3>
              </div>
              <Button onClick={handleTopUp} className="bg-white text-gray-900 hover:bg-gray-100 shadow-none border-none">
                Top Up
              </Button>
            </div>
          </Card>
        </div>
        
        <div className="space-y-6">
          <Card className="p-6 bg-[#FDF2F8] border-none shadow-sm">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Receipt className="text-[#EC4899]" /> Recent Transaction
            </h2>
            
            {latestTransaction ? (
              <div className="space-y-4 text-sm">
                <div className="flex justify-between text-gray-600">
                  <span>Trip ID</span>
                  <span className="font-medium text-gray-900">{latestTransaction.id}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Date</span>
                  <span className="font-medium text-gray-900">{new Date(latestTransaction.date).toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Distance</span>
                  <span className="font-medium text-gray-900">{latestTransaction.distance}</span>
                </div>
                <div className="w-full h-px bg-gray-200 my-2"></div>
                <div className="flex justify-between text-gray-600">
                  <span>Base Fare</span>
                  <span className="font-medium text-gray-900">₹{latestTransaction.baseFare}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Distance Fare</span>
                  <span className="font-medium text-gray-900">₹{latestTransaction.distanceFare}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Safety Premium</span>
                  <span className="font-medium text-green-600 text-xs px-2 py-0.5 bg-green-100 rounded">Included</span>
                </div>
                <div className="w-full h-px bg-gray-200 my-2"></div>
                <div className="flex justify-between items-center">
                  <span className="font-bold text-gray-900 text-lg">Total</span>
                  <span className="font-bold text-[#EC4899] text-xl">₹{latestTransaction.total}</span>
                </div>
                <Button className="w-full mt-6" variant="primary" onClick={() => handleDownloadInvoice(latestTransaction.id)}>
                  Download Invoice
                </Button>
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                No recent transactions found. Book a ride to see it here!
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Payment;
