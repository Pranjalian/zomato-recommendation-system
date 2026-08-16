import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import UserLogin from './components/UserLogin';
import HomeConcierge from './components/HomeConcierge';
import ProfilePreferences from './components/ProfilePreferences';
import CuratedMatches from './components/CuratedMatches';
import useStore from './store/useStore';

// Protected Route wrapper
function ProtectedRoute({ children }) {
  const userId = useStore((state) => state.userId);
  if (!userId) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<UserLogin />} />
        
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <HomeConcierge />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/profile" 
          element={
            <ProtectedRoute>
              <ProfilePreferences />
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/matches" 
          element={
            <ProtectedRoute>
              <CuratedMatches />
            </ProtectedRoute>
          } 
        />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
