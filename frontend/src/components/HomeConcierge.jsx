import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useStore from '../store/useStore';
import { Search, MapPin, Navigation } from 'lucide-react';

export default function HomeConcierge() {
  const [localQuery, setLocalQuery] = useState('');
  const setQuery = useStore((state) => state.setQuery);
  const setRecommendations = useStore((state) => state.setRecommendations);
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (localQuery.trim()) {
      setQuery(localQuery.trim());
      setRecommendations([]);
      navigate('/matches');
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="p-4 flex justify-between items-center bg-surface/80 backdrop-blur-md sticky top-0 z-10 border-b border-surface-variant">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-[#ff416c] flex items-center justify-center shadow-md">
            <span className="text-white font-bold text-lg">Z</span>
          </div>
          <span className="font-heading font-bold text-xl text-on-surface">Cravematch AI</span>
        </div>
        <button 
          onClick={() => navigate('/profile')}
          className="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center text-on-surface-variant hover:bg-surface-variant transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </button>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col px-4 pt-12 pb-24">
        <div className="max-w-[576px] mx-auto w-full flex flex-col gap-8">
          
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-heading font-bold tracking-tight text-on-surface">
              What are you <br/>
              <span className="magic-gradient-text">craving right now?</span>
            </h1>
            <p className="text-on-surface-variant text-lg">
              Tell me what you're in the mood for. The more details, the better the magic.
            </p>
          </div>

          <form onSubmit={handleSearch} className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-primary via-[#ff416c] to-[#ff4b2b] rounded-2xl blur opacity-30 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative flex items-center bg-surface-container-lowest rounded-2xl shadow-lg border border-surface-variant overflow-hidden">
              <div className="pl-4 text-primary">
                <Search size={24} />
              </div>
              <input
                type="text"
                value={localQuery}
                onChange={(e) => setLocalQuery(e.target.value)}
                placeholder="e.g. A quiet place for spicy Thai food..."
                className="w-full px-4 py-5 bg-transparent focus:outline-none text-on-surface text-lg placeholder:text-on-surface-variant/50"
              />
              <button 
                type="submit"
                className="mx-2 px-6 py-3 bg-on-surface text-inverse-on-surface font-semibold rounded-xl hover:bg-inverse-surface transition-colors whitespace-nowrap"
              >
                Find Magic
              </button>
            </div>
          </form>

          {/* Context Override Mock (for prototype) */}
          <div className="mt-8 flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
            <button className="flex items-center gap-2 px-4 py-2 rounded-full border border-surface-variant bg-surface-container text-on-surface text-sm whitespace-nowrap hover:border-primary transition-colors">
              <MapPin size={16} className="text-primary" />
              Current Location
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded-full border border-surface-variant bg-surface-container text-on-surface text-sm whitespace-nowrap hover:border-primary transition-colors">
              <Navigation size={16} className="text-secondary" />
              Within 5km
            </button>
          </div>
          
        </div>
      </main>
    </div>
  );
}
