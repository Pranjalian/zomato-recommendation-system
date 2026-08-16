import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useStore from '../store/useStore';
import { getRecommendations, sendFeedback } from '../services/api';
import { ArrowLeft, Sparkles, MapPin, Star } from 'lucide-react';

export default function CuratedMatches() {
  const query = useStore((state) => state.query);
  const recommendations = useStore((state) => state.recommendations);
  const setRecommendations = useStore((state) => state.setRecommendations);
  const userId = useStore((state) => state.userId);
  const navigate = useNavigate();

  useEffect(() => {
    if (!query) {
      navigate('/');
      return;
    }

    const fetchRecs = async () => {
      try {
        if (recommendations.length === 0) {
          const data = await getRecommendations(userId, query);
          setRecommendations(data);
        }
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    };

    fetchRecs();
  }, [query, navigate, userId, recommendations.length, setRecommendations]);

  const handleOrder = async (restaurantId) => {
    try {
      await sendFeedback(userId, 'click', restaurantId);
      alert(`Feedback logged! Navigating to restaurant ${restaurantId}...`);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-surface-container-low flex flex-col">
      <header className="p-4 flex flex-col gap-4 bg-surface/80 backdrop-blur-md sticky top-0 z-10 border-b border-surface-variant shadow-sm">
        <div className="flex items-center justify-between">
          <button 
            onClick={() => navigate('/')}
            className="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <div className="flex items-center gap-1.5 px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-semibold">
            <Sparkles size={16} />
            AI Curated
          </div>
          <div className="w-10"></div> {/* Spacer */}
        </div>
        
        <div className="px-2">
          <h2 className="text-sm font-medium text-on-surface-variant">Your Craving:</h2>
          <p className="text-lg font-heading font-bold text-on-surface leading-tight mt-1">"{query}"</p>
        </div>
      </header>

      <main className="flex-1 p-4 pb-20">
        <div className="max-w-[576px] mx-auto w-full flex flex-col gap-6">
          
          {recommendations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-center px-4">
              <div className="w-16 h-16 rounded-full bg-surface-variant flex items-center justify-center mb-4">
                <Sparkles size={32} className="text-on-surface-variant" />
              </div>
              <h3 className="text-xl font-heading font-bold text-on-surface">Working magic...</h3>
              <p className="text-on-surface-variant mt-2">Finding the perfect spots for you.</p>
              {/* In the future we will fetch from API here, so we show loading state */}
            </div>
          ) : (
            recommendations.map((match, index) => (
              <div key={match.restaurant_id || index} className="bg-surface-container-lowest rounded-[24px] overflow-hidden shadow-sm border border-surface-variant relative">
                {/* Image Placeholder */}
                <div className="h-48 bg-surface-variant w-full relative">
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                  
                  {index === 0 && (
                    <div className="absolute top-4 right-4 bg-gradient-to-r from-primary to-[#ff416c] text-white text-xs font-bold px-3 py-1.5 rounded-full flex items-center gap-1 shadow-lg">
                      <Sparkles size={14} /> Top Match
                    </div>
                  )}
                  
                  <div className="absolute bottom-4 left-4 right-4 text-white">
                    <h3 className="text-2xl font-heading font-bold">{match.name}</h3>
                    <div className="flex items-center gap-3 text-sm mt-1 opacity-90">
                      <span className="flex items-center gap-1"><Star size={14} className="fill-tertiary-container text-tertiary-container" /> {match.score.toFixed(1)}</span>
                      <span>•</span>
                      <span className="truncate">{match.cuisines}</span>
                    </div>
                  </div>
                </div>

                {/* AI Explanation */}
                <div className="p-5">
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 mt-1">
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                        <Sparkles size={16} className="text-primary" />
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-on-surface mb-1">Why this fits:</h4>
                      <p className="text-on-surface-variant text-sm leading-relaxed">
                        {match.explanation}
                      </p>
                    </div>
                  </div>
                  
                  <div className="mt-5 flex gap-3">
                    <button 
                      onClick={() => handleOrder(match.restaurant_id)}
                      className="flex-1 py-3 rounded-xl bg-surface-container hover:bg-surface-variant text-on-surface font-semibold text-sm transition-colors"
                    >
                      View Menu
                    </button>
                    <button 
                      onClick={() => handleOrder(match.restaurant_id)}
                      className="flex-1 py-3 rounded-xl bg-gradient-to-r from-primary to-[#ff416c] text-white font-semibold text-sm shadow-md hover:shadow-lg transition-all active:scale-95"
                    >
                      Order Now
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}
