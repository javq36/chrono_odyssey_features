import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import RedditScraper from "./reddit-scraper/reddit-scrapper.component";
import DashboardComponent from "./dashboard/dashboard.Component";
import Transcriber from "./transcriber/transcriber.component";

import "primereact/resources/themes/lara-light-indigo/theme.css"; // or your chosen theme
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css"; // Optional, but useful for layout

// If you have a global CSS file, ensure it's imported, e.g., import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Dashboard Layout Route */}
        <Route path="/" element={<DashboardComponent />}>
          {/* Index route for the dashboard: defaults to the transcriber */}
          <Route index element={<Navigate to="/transcriber" replace />} />

          {/* Feature routes rendered within the Dashboard's <Outlet /> */}
          <Route path="transcriber" element={<Transcriber />} />
          <Route path="reddit-scraper" element={<RedditScraper />} />
          {/* 
            Example for future components:
            <Route path="summarizer" element={<SummarizerComponent />} />
            <Route path="build-manager" element={<BuildManagerComponent />} /> 
          */}
        </Route>

        {/* Fallback route: if no other route matches, redirect to the dashboard's default */}
        <Route path="*" element={<Navigate to="/transcriber" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
