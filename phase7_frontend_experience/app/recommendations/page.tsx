'use client';

import { useEffect, useState } from 'react';
import { Star, MapPin, Bookmark, Share2, Sparkles, Loader2 } from 'lucide-react';

interface Restaurant {
  title: string;
  subtitle: string;
  rating: number;
  estimated_cost: number;
  cuisine: string;
  location: string;
  explanation: string;
}

interface RecommendationData {
  profile: {
    location: string;
    budget: string;
    cuisine: string;
    min_rating: number;
  };
  summary: string;
  cards: Restaurant[];
  explanation_lines: string[];
}

export default function RecommendationsPage() {
  const [data, setData] = useState<RecommendationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        // Get preferences from localStorage
        const preferencesStr = localStorage.getItem('preferences');
        const preferences = preferencesStr ? JSON.parse(preferencesStr) : {
          location: 'Bangalore',
          budget: 'medium',
          cuisine: 'Chinese',
          min_rating: 3.8,
        };

        // Call the API
        const response = await fetch('/api/v1/recommendations', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            location: preferences.location || 'Bangalore',
            budget: preferences.budget || 'medium',
            cuisine: preferences.cuisine || 'Chinese',
            min_rating: preferences.minRating || 3.8,
            optional_tags: preferences.diningOptions || [],
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to fetch recommendations');
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  const getRatingColor = (rating: number) => {
    if (rating >= 4.5) return 'bg-rating-high';
    if (rating >= 3.5) return 'bg-rating-medium';
    return 'bg-rating-low';
  };

  const getRankBadge = (index: number) => {
    const ranks = ['#1', '#2', '#3'];
    return ranks[index] || `#${index + 1}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-primary animate-spin mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-secondary">Finding the best restaurants for you...</h2>
          <p className="text-secondary-light mt-2">Our AI is analyzing thousands of options</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-xl font-semibold text-secondary mb-2">Something went wrong</h2>
          <p className="text-secondary-light">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!data || !data.cards || data.cards.length === 0) {
    return (
      <div className="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🔍</div>
          <h2 className="text-xl font-semibold text-secondary">No recommendations found</h2>
          <p className="text-secondary-light mt-2">Try adjusting your preferences</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FAFAFA]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-secondary mb-2">Top Picks For You</h1>
          <p className="text-secondary-light">
            {data.cards.length} {data.profile?.cuisine} restaurants in {data.profile?.location} within {data.profile?.budget} budget
          </p>
        </div>

        {/* Restaurant Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.cards.slice(0, 6).map((restaurant, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl overflow-hidden shadow-card card-hover animate-fade-in flex flex-col"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Header Section with Rank and Rating */}
              <div className="relative bg-gradient-to-br from-gray-100 to-gray-200 p-4 flex-shrink-0">
                <div className="flex items-center justify-between">
                  <span className="bg-secondary/80 text-white text-xs font-bold px-2 py-1 rounded">
                    Rank {getRankBadge(index)}
                  </span>
                  <div className={`${getRatingColor(restaurant.rating)} text-white px-2 py-1 rounded flex items-center gap-1`}>
                    <span className="text-sm font-bold">{restaurant.rating}</span>
                    <Star className="w-3 h-3 fill-white" />
                  </div>
                </div>
              </div>

              {/* Content Section - grows to fill space */}
              <div className="p-5 flex flex-col flex-grow">
                <h3 className="text-lg font-bold text-secondary mb-1">{restaurant.title}</h3>
                <div className="flex items-center gap-2 text-sm text-secondary-light mb-3">
                  <MapPin className="w-4 h-4" />
                  <span>{restaurant.location}</span>
                  <span>•</span>
                  <span>₹{restaurant.estimated_cost}</span>
                </div>

                {/* Why Recommended - grows to fill available space */}
                <div className="bg-primary/5 border-l-4 border-primary p-3 rounded-r-lg mb-4 flex-grow">
                  <div className="flex items-start gap-2">
                    <Sparkles className="w-4 h-4 text-primary flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-xs font-bold text-primary uppercase mb-1">Why Recommended</p>
                      <p className="text-sm text-secondary">{restaurant.explanation}</p>
                    </div>
                  </div>
                </div>

                {/* Actions - always at bottom */}
                <div className="flex items-center gap-2 mt-auto flex-shrink-0">
                  <button className="flex-1 bg-primary text-white py-2 rounded-lg font-medium hover:bg-primary-dark transition-colors text-sm">
                    VIEW DETAILS
                  </button>
                  <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                    <Bookmark className="w-4 h-4 text-secondary-light" />
                  </button>
                  <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                    <Share2 className="w-4 h-4 text-secondary-light" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Load More */}
        {data.cards.length > 6 && (
          <div className="mt-8 text-center">
            <button className="px-8 py-3 border-2 border-primary text-primary font-medium rounded-lg hover:bg-primary hover:text-white transition-all">
              LOAD MORE RECOMMENDATIONS
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
