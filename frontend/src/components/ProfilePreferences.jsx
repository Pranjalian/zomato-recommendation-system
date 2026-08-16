import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useStore from '../store/useStore';
import { getProfile, updateProfile } from '../services/api';
import { ArrowLeft, Save } from 'lucide-react';

export default function ProfilePreferences() {
  const userId = useStore((state) => state.userId);
  const logout = useStore((state) => state.logout);
  const navigate = useNavigate();

  const [diet, setDiet] = useState('none');
  const [allergies, setAllergies] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!userId) {
      navigate('/login');
      return;
    }
    const fetchProfile = async () => {
      try {
        const data = await getProfile(userId);
        if (data.explicit_preferences) {
          setDiet(data.explicit_preferences.diet || 'none');
          setAllergies(data.explicit_preferences.allergies?.join(', ') || '');
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchProfile();
  }, [userId, navigate]);

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const allergyList = allergies.split(',').map(s => s.trim()).filter(Boolean);
      await updateProfile(userId, { diet, allergies: allergyList });
      setMessage('Preferences saved successfully!');
    } catch (err) {
      setMessage('Failed to save preferences.');
      console.error(err);
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="p-4 flex justify-between items-center bg-surface/80 backdrop-blur-md sticky top-0 z-10 border-b border-surface-variant">
        <button 
          onClick={() => navigate('/')}
          className="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-surface-container transition-colors"
        >
          <ArrowLeft size={24} />
        </button>
        <span className="font-heading font-semibold text-lg text-on-surface">Preferences</span>
        <div className="w-10"></div> {/* Spacer for centering */}
      </header>

      <main className="flex-1 p-4">
        <div className="max-w-[448px] mx-auto w-full space-y-6 mt-4">
          
          <div className="bg-surface-container-low p-6 rounded-2xl shadow-sm border border-surface-variant">
            <h2 className="text-xl font-heading font-bold text-on-surface mb-1">Dietary Profile</h2>
            <p className="text-on-surface-variant text-sm mb-6">Tell us what you can and can't eat so we recommend the right places.</p>

            <form onSubmit={handleSave} className="space-y-5">
              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-on-surface">Diet</label>
                <select 
                  value={diet} 
                  onChange={(e) => setDiet(e.target.value)}
                  className="px-4 py-3 rounded-lg border border-surface-variant bg-surface-container focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent appearance-none"
                >
                  <option value="none">No specific diet</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                  <option value="gluten_free">Gluten Free</option>
                  <option value="keto">Keto</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-on-surface">Allergies</label>
                <input 
                  type="text" 
                  value={allergies}
                  onChange={(e) => setAllergies(e.target.value)}
                  placeholder="e.g. peanuts, shellfish"
                  className="px-4 py-3 rounded-lg border border-surface-variant bg-surface-container focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <button 
                type="submit" 
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 mt-4 py-3 rounded-xl bg-on-surface text-inverse-on-surface font-semibold hover:bg-inverse-surface transition-colors disabled:opacity-70"
              >
                <Save size={18} />
                {loading ? 'Saving...' : 'Save Preferences'}
              </button>

              {message && (
                <p className="text-green-600 text-sm font-medium text-center">{message}</p>
              )}
            </form>
          </div>

          <div className="flex justify-center mt-8">
            <button 
              onClick={handleLogout}
              className="px-6 py-2 text-error font-semibold hover:bg-error-container rounded-full transition-colors"
            >
              Log out
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
