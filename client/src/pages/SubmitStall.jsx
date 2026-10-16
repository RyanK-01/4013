import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FormInput, FormTextarea, Button, Card, ToggleGroup } from '../components/ui';
import api from '../services/api';
import toast from 'react-hot-toast';

const DIETARY_TAGS = ['Halal', 'Vegetarian', 'Seafood', 'Nuts', 'Beef'];

export default function SubmitStall() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: '',
    description: '',
    address: '',
    cuisine_type: '',
    price_range_min: '',
    price_range_max: '',
    dietary_tags: [],
    menu_items: [{ name: '', price: '', description: '' }],
  });

  if (!user) {
    navigate('/login');
    return null;
  }

  const addMenuItem = () => {
    setForm((f) => ({ ...f, menu_items: [...f.menu_items, { name: '', price: '', description: '' }] }));
  };

  const updateMenuItem = (idx, field, value) => {
    setForm((f) => {
      const items = [...f.menu_items];
      items[idx] = { ...items[idx], [field]: value };
      return { ...f, menu_items: items };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.address) {
      toast.error('Name and address are required');
      return;
    }
    setLoading(true);
    try {
      await api.post('/stalls/submit', {
        ...form,
        price_range_min: form.price_range_min ? Number(form.price_range_min) : null,
        price_range_max: form.price_range_max ? Number(form.price_range_max) : null,
        menu_items: form.menu_items
          .filter((m) => m.name)
          .map((m) => ({ ...m, price: m.price ? Number(m.price) : null })),
      });
      toast.success('Stall submitted! Pending admin approval.');
      navigate('/');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Submission failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto pb-4">
      <h1 className="text-xl font-bold mb-4">Submit New Stall</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Card className="space-y-3">
          <FormInput
            label="Stall Name *"
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
          <FormInput
            label="Address *"
            type="text"
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
            required
          />
          <FormTextarea
            label="Description"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            rows={2}
          />
          <FormInput
            label="Cuisine Type"
            type="text"
            value={form.cuisine_type}
            onChange={(e) => setForm({ ...form, cuisine_type: e.target.value })}
            placeholder="e.g. Chinese Cuisine"
          />
          <div className="grid grid-cols-2 gap-3">
            <FormInput
              label="Min Price ($)"
              type="number"
              value={form.price_range_min}
              onChange={(e) => setForm({ ...form, price_range_min: e.target.value })}
              step="0.5"
            />
            <FormInput
              label="Max Price ($)"
              type="number"
              value={form.price_range_max}
              onChange={(e) => setForm({ ...form, price_range_max: e.target.value })}
              step="0.5"
            />
          </div>
        </Card>

        <Card>
          <label className="block text-sm font-medium mb-2">Dietary Tags</label>
          <ToggleGroup
            options={DIETARY_TAGS}
            value={form.dietary_tags}
            onChange={(tags) => setForm((f) => ({ ...f, dietary_tags: tags }))}
            multiple
            activeColor="bg-green-500 text-white"
          />
        </Card>

        <Card>
          <label className="block text-sm font-medium mb-2">Menu Items</label>
          {form.menu_items.map((item, idx) => (
            <div key={idx} className="grid grid-cols-3 gap-2 mb-2">
              <input type="text" placeholder="Item name" value={item.name} onChange={(e) => updateMenuItem(idx, 'name', e.target.value)} className="border rounded-lg px-2 py-1.5 text-sm" />
              <input type="number" placeholder="Price" value={item.price} onChange={(e) => updateMenuItem(idx, 'price', e.target.value)} className="border rounded-lg px-2 py-1.5 text-sm" step="0.1" />
              <input type="text" placeholder="Description" value={item.description} onChange={(e) => updateMenuItem(idx, 'description', e.target.value)} className="border rounded-lg px-2 py-1.5 text-sm" />
            </div>
          ))}
          <button type="button" onClick={addMenuItem} className="text-sm text-orange-500 hover:underline">+ Add menu item</button>
        </Card>

        <Button type="submit" loading={loading} loadingText="Submitting..." fullWidth>
          Submit Stall for Review
        </Button>
        <p className="text-xs text-gray-400 text-center">Your submission will be reviewed by an admin before being published.</p>
      </form>
    </div>
  );
}
