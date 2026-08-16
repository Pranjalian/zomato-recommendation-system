import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set) => ({
      userId: null,
      setUserId: (id) => set({ userId: id }),
      
      query: '',
      setQuery: (q) => set({ query: q }),
      
      recommendations: [],
      setRecommendations: (recs) => set({ recommendations: recs }),
      
      clearSession: () => set({ query: '', recommendations: [] }),
      logout: () => set({ userId: null, query: '', recommendations: [] })
    }),
    {
      name: 'cravematch-storage',
    }
  )
);

export default useStore;
