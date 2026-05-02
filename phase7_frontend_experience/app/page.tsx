'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { MapPin, Utensils, Star, Sparkles } from 'lucide-react';

const cities = ['Koramangala', 'Indiranagar', 'BTM', 'Jayanagar', 'JP Nagar', 'HSR Layout', 'Whitefield', 'MG Road', 'Marathahalli'];
const cuisines = ['Chinese', 'Italian', 'Indian', 'Mexican', 'Thai', 'Japanese', 'Continental'];
const diningOptions = [
  { id: 'quick', label: 'Quick Service', icon: '⚡' },
  { id: 'fine', label: 'Fine Dining', icon: '🍽️' },
  { id: 'outdoor', label: 'Outdoor Seating', icon: '🌿' },
];

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    location: '',
    budget: '',
    cuisine: '',
    minRating: 4.0,
    diningOptions: [] as string[],
  });

  const handleCitySelect = (city: string) => {
    setFormData({ ...formData, location: city });
  };

  const handleCuisineSelect = (cuisine: string) => {
    setFormData({ ...formData, cuisine });
  };

  const handleBudgetSelect = (budget: string) => {
    setFormData({ ...formData, budget });
  };

  const handleDiningToggle = (option: string) => {
    setFormData({
      ...formData,
      diningOptions: formData.diningOptions.includes(option)
        ? formData.diningOptions.filter((o) => o !== option)
        : [...formData.diningOptions, option],
    });
  };

  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    // Validate required fields
    if (!formData.location) {
      setError('Please select a location');
      return;
    }
    if (!formData.cuisine) {
      setError('Please select a cuisine');
      return;
    }
    if (!formData.budget) {
      setError('Please select a budget');
      return;
    }
    
    setIsLoading(true);
    
    // Store preferences in localStorage for the results page
    localStorage.setItem('preferences', JSON.stringify(formData));
    
    // Navigate to recommendations page
    router.push('/recommendations');
  };

  const budgetOptions = [
    { value: 'low', label: 'Low', symbol: '₹' },
    { value: 'medium', label: 'Medium', symbol: '₹₹' },
    { value: 'high', label: 'High', symbol: '₹₹₹' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FFF5F5] to-[#FEF2F2]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Left Side - Hero Content */}
          <div className="space-y-6">
            <div className="space-y-4">
              <h1 className="text-4xl md:text-5xl font-bold text-secondary leading-tight">
                Tell Us What You&apos;re Craving
              </h1>
              <p className="text-lg text-secondary-light max-w-md">
                Help our AI understand your mood. We&apos;ll curate a personalized selection of restaurants based on your location, budget, and culinary tastes.
              </p>
              <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1.5 rounded-full text-sm font-medium">
                <MapPin className="w-4 h-4" />
                Currently serving Bangalore only (51,717 restaurants)
              </div>
            </div>

            {/* Hero Image Card */}
            <div className="relative rounded-2xl overflow-hidden shadow-card">
              <div className="aspect-[4/3] bg-gradient-to-br from-gray-100 to-gray-200 relative">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-6xl mb-4">🍜</div>
                    <p className="text-secondary-light">Delicious food awaits</p>
                  </div>
                </div>
                <div className="absolute bottom-4 left-4">
                  <span className="bg-primary text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                    Personalized Pick
                  </span>
                </div>
                <div className="absolute bottom-4 right-4">
                  <p className="text-white text-sm font-medium drop-shadow-lg">
                    Discovery awaits you.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Form */}
          <div className="bg-white rounded-2xl shadow-card p-8">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Location */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-secondary uppercase tracking-wider">
                  Your Current Location
                </label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-primary" />
                  <input
                    type="text"
                    placeholder="Search neighborhood or city..."
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
                <div className="flex flex-wrap gap-2">
                  {cities.map((city) => (
                    <button
                      key={city}
                      type="button"
                      onClick={() => handleCitySelect(city)}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                        formData.location === city
                          ? 'bg-primary/10 text-primary border border-primary'
                          : 'bg-gray-100 text-secondary-light hover:bg-gray-200 border border-transparent'
                      }`}
                    >
                      {city}
                    </button>
                  ))}
                </div>
              </div>

              {/* Budget */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-secondary uppercase tracking-wider">
                  Planned Budget
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {budgetOptions.map((option) => (
                    <button
                      key={option.value}
                      type="button"
                      onClick={() => handleBudgetSelect(option.value)}
                      className={`py-3 px-4 rounded-xl border-2 font-medium transition-all ${
                        formData.budget === option.value
                          ? 'border-primary bg-primary/5 text-primary'
                          : 'border-gray-200 text-secondary-light hover:border-gray-300'
                      }`}
                    >
                      <span className="block text-lg">{option.symbol}</span>
                      <span className="text-sm">{option.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Cuisine */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-secondary uppercase tracking-wider flex items-center gap-2">
                  <Utensils className="w-4 h-4" />
                  Favorite Cuisines
                </label>
                <div className="flex flex-wrap gap-2">
                  {cuisines.map((cuisine) => (
                    <button
                      key={cuisine}
                      type="button"
                      onClick={() => handleCuisineSelect(cuisine)}
                      className={`px-4 py-2 rounded-full text-sm font-medium transition-all border-2 ${
                        formData.cuisine === cuisine
                          ? 'bg-primary text-white border-primary'
                          : 'bg-white text-secondary border-gray-200 hover:border-primary/50'
                      }`}
                    >
                      {cuisine}
                    </button>
                  ))}
                </div>
              </div>

              {/* Rating */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-secondary uppercase tracking-wider flex items-center gap-2">
                  <Star className="w-4 h-4" />
                  Minimum Rating
                </label>
                <div className="space-y-2">
                  <input
                    type="range"
                    min="0"
                    max="5"
                    step="0.1"
                    value={formData.minRating}
                    onChange={(e) => setFormData({ ...formData, minRating: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-secondary-light">Any rating</span>
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-primary fill-primary" />
                      <span className="font-bold text-secondary">{formData.minRating.toFixed(1)}+</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Dining Experience */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-secondary uppercase tracking-wider">
                  Dining Experience
                </label>
                <div className="flex flex-wrap gap-2">
                  {diningOptions.map((option) => (
                    <button
                      key={option.id}
                      type="button"
                      onClick={() => handleDiningToggle(option.id)}
                      className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all border-2 ${
                        formData.diningOptions.includes(option.id)
                          ? 'bg-primary text-white border-primary'
                          : 'bg-white text-secondary border-gray-200 hover:border-primary/50'
                      }`}
                    >
                      <span>{option.icon}</span>
                      <span>{option.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-primary text-white font-semibold py-4 rounded-xl hover:bg-primary-dark transition-all flex items-center justify-center gap-2 disabled:opacity-70"
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Analyzing with AI...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    FIND MY RESTAURANTS
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
