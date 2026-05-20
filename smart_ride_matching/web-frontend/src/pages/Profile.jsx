import React, { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { User, Shield, Bell, Lock, Trash2, Edit2, Check, X } from 'lucide-react';

const Profile = () => {
  const [contacts, setContacts] = useState([
    { id: 1, name: 'Mom', phone: '+91 99999 88888' }
  ]);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ name: '', phone: '' });
  const [isAdding, setIsAdding] = useState(false);
  const [newContact, setNewContact] = useState({ name: '', phone: '' });

  const handleDelete = (id) => {
    setContacts(contacts.filter(c => c.id !== id));
  };

  const startEdit = (contact) => {
    setEditingId(contact.id);
    setEditForm({ name: contact.name, phone: contact.phone });
  };

  const saveEdit = () => {
    if (!editForm.name || !editForm.phone) return;
    setContacts(contacts.map(c => c.id === editingId ? { ...c, ...editForm } : c));
    setEditingId(null);
  };

  const handleAdd = () => {
    if (!newContact.name || !newContact.phone) return;
    setContacts([...contacts, { id: Date.now(), ...newContact }]);
    setNewContact({ name: '', phone: '' });
    setIsAdding(false);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Profile Settings</h1>
      
      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-1 space-y-4">
          <Card className="p-6 text-center">
            <div className="w-24 h-24 bg-pink-100 rounded-full mx-auto mb-4 flex items-center justify-center border-4 border-white shadow-lg relative">
              <User className="w-10 h-10 text-[#EC4899]" />
              <div className="absolute bottom-0 right-0 bg-green-500 w-6 h-6 rounded-full border-2 border-white flex items-center justify-center">
                <Shield className="w-3 h-3 text-white" />
              </div>
            </div>
            <h2 className="font-bold text-xl text-gray-900">Amulya</h2>
            <p className="text-sm text-gray-500 mb-4">amulya@example.com</p>
            <div className="inline-flex items-center gap-1 bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold">
              <Shield className="w-3 h-3" /> Identity Verified
            </div>
          </Card>
          
          <div className="space-y-1">
            <button className="w-full text-left px-4 py-3 bg-pink-50 text-[#EC4899] font-medium rounded-xl flex items-center justify-between">
              <span>Personal Info</span>
              <User className="w-4 h-4" />
            </button>
            <button className="w-full text-left px-4 py-3 text-gray-600 hover:bg-gray-50 hover:text-gray-900 font-medium rounded-xl flex items-center justify-between transition-colors">
              <span>Security & Safety</span>
              <Shield className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <div className="md:col-span-2 space-y-6">
          <Card className="p-8">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Personal Information</h3>
            <form className="space-y-5">
              <div className="grid grid-cols-2 gap-5">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-700">First Name</label>
                  <Input defaultValue="Amulya" />
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-700">Last Name</label>
                  <Input defaultValue="Doe" />
                </div>
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium text-gray-700">Phone Number</label>
                <Input defaultValue="+91 98765 43210" />
              </div>
              <div className="pt-4">
                <Button>Save Changes</Button>
              </div>
            </form>
          </Card>
          
          <Card className="p-8 border-red-100 bg-red-50/30">
            <h3 className="text-xl font-bold text-red-900 mb-2">Emergency Contacts</h3>
            <p className="text-sm text-red-700 mb-6">These contacts will be notified immediately if you trigger the SOS alert during a ride.</p>
            
            <div className="space-y-3">
              {contacts.map((contact) => (
                <div key={contact.id} className="flex items-center justify-between p-3 bg-white rounded-lg border border-red-100">
                  {editingId === contact.id ? (
                    <div className="flex-1 flex items-center gap-2 mr-2">
                      <Input value={editForm.name} onChange={(e) => setEditForm({...editForm, name: e.target.value})} className="h-8 py-1 px-2" />
                      <Input value={editForm.phone} onChange={(e) => setEditForm({...editForm, phone: e.target.value})} className="h-8 py-1 px-2" />
                      <button onClick={saveEdit} className="p-1 text-green-600 hover:bg-green-50 rounded"><Check className="w-5 h-5"/></button>
                      <button onClick={() => setEditingId(null)} className="p-1 text-gray-500 hover:bg-gray-100 rounded"><X className="w-5 h-5"/></button>
                    </div>
                  ) : (
                    <>
                      <div>
                        <p className="font-semibold text-gray-900">{contact.name}</p>
                        <p className="text-sm text-gray-500">{contact.phone}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <button onClick={() => startEdit(contact)} className="p-2 text-blue-500 hover:bg-blue-50 rounded-full transition-colors"><Edit2 className="w-4 h-4" /></button>
                        <button onClick={() => handleDelete(contact.id)} className="p-2 text-red-500 hover:bg-red-50 rounded-full transition-colors"><Trash2 className="w-4 h-4" /></button>
                      </div>
                    </>
                  )}
                </div>
              ))}
              
              {isAdding ? (
                <div className="flex items-center gap-2 p-3 bg-white rounded-lg border border-red-200">
                  <Input placeholder="Name" value={newContact.name} onChange={(e) => setNewContact({...newContact, name: e.target.value})} className="h-9 py-1 px-3" />
                  <Input placeholder="Phone (e.g. +91...)" value={newContact.phone} onChange={(e) => setNewContact({...newContact, phone: e.target.value})} className="h-9 py-1 px-3" />
                  <Button onClick={handleAdd} size="sm" className="h-9 px-3 shrink-0">Add</Button>
                  <Button onClick={() => setIsAdding(false)} variant="ghost" size="sm" className="h-9 px-2 shrink-0"><X className="w-4 h-4"/></Button>
                </div>
              ) : (
                <Button onClick={() => setIsAdding(true)} variant="secondary" className="w-full text-red-600 border-red-200 hover:bg-red-50">+ Add Emergency Contact</Button>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Profile;
