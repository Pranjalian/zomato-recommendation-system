import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useStore from '../store/useStore';

export default function UserLogin() {
  const [selectedUser, setSelectedUser] = useState('');
  const setUserId = useStore((state) => state.setUserId);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (selectedUser.trim()) {
      setUserId(selectedUser.trim());
      navigate('/');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-background">
      <div className="glass-panel max-w-[384px] w-full p-8 rounded-2xl shadow-xl flex flex-col gap-6">
        <div className="text-center">
          <h1 className="text-3xl font-heading font-bold text-on-surface mb-2">Welcome</h1>
          <p className="text-on-surface-variant font-sans">Select a user to continue</p>
        </div>

        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-semibold text-on-surface">User ID</label>
            <input
              type="text"
              value={selectedUser}
              onChange={(e) => setSelectedUser(e.target.value)}
              placeholder="e.g. test_user_1"
              className="px-4 py-3 rounded-lg border border-surface-variant bg-surface-container focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            />
          </div>
          
          <div className="flex gap-2 text-sm text-on-surface-variant mt-2">
            <span className="font-semibold">Hints:</span>
            <button type="button" onClick={() => setSelectedUser('test_user_1')} className="underline hover:text-primary">test_user_1</button>,
            <button type="button" onClick={() => setSelectedUser('test_telemetry_user')} className="underline hover:text-primary">test_telemetry_user</button>
          </div>

          <button
            type="submit"
            className="mt-4 py-3 rounded-xl bg-gradient-to-r from-primary to-[#ff416c] text-white font-semibold shadow-lg shadow-primary/30 hover:shadow-primary/50 transition-all active:scale-95"
          >
            Continue
          </button>
        </form>
      </div>
    </div>
  );
}
