import React, { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

import AdmitCardPreview from "./components/AdmitCardPreview";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [admitCardData, setAdmitCardData] = useState(null);

  return (
    <div>
      {isLoggedIn ? (
        admitCardData ? (
          <AdmitCardPreview data={admitCardData} onBack={() => setAdmitCardData(null)} />
        ) : (
          <Dashboard
            onLogout={() => setIsLoggedIn(false)}
            setAdmitCardData={setAdmitCardData}
          />
        )
      ) : (
        <Login onLoginSuccess={() => setIsLoggedIn(true)} />
      )}
    </div>
  );
}
// export default Dashboard;

export default App;
