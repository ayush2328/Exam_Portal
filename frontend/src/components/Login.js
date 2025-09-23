// import React, { useState } from "react";

// function Login({ onLoginSuccess }) {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");

//   const handleLogin = (e) => {
//     e.preventDefault();
//     if (username === "admin" && password === "1234") {
//       onLoginSuccess();
//     } else {
//       alert("Invalid Credentials");
//     }
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "100px" }}>
//       <h2>Admin Login</h2>
//       <form onSubmit={handleLogin}>
//         <input
//           type="text"
//           placeholder="Username"
//           value={username}
//           onChange={(e) => setUsername(e.target.value)}
//         />
//         <br />
//         <input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//         />
//         <br />
//         <button type="submit">Login</button>
//       </form>
//     </div>
//   );
// }

// export default Login;
import React, { useState, useEffect } from "react";
import "./Login.css"; // ✅ yeh import zaroor karna hai

function Login({ onLoginSuccess }) {
  const [netId, setNetId] = useState("");
  const [password, setPassword] = useState("");
  const [captcha, setCaptcha] = useState("");
  const [generatedCaptcha, setGeneratedCaptcha] = useState("");

  // Captcha generate karne ka function
  const generateCaptcha = () => {
    const chars =
      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let captchaText = "";
    for (let i = 0; i < 6; i++) {
      captchaText += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setGeneratedCaptcha(captchaText);
  };

  useEffect(() => {
    generateCaptcha();
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (
      netId === "admin" &&
      password === "1234" &&
      captcha === generatedCaptcha
    ) {
      onLoginSuccess();
    } else {
      alert("Invalid Credentials or Captcha");
      generateCaptcha();
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Left */}
        <div className="login-left">
          <h2>Dear Student,</h2>
          <p>
            Welcome to SRMIST STUDENT PORTAL. <br />
            Dynamic Admit Card Admin Page.
          </p>
          <p>
            SRMIST students can login with credentials. <br />

          </p>
        </div>

        {/* Right */}
        <div className="login-right">
          <h3 className="portal-header">Student Portal</h3>
          <form className="login-form" onSubmit={handleLogin}>
            <div className="input-group">
              <input
                type="text"
                placeholder="Admin ID"
                value={netId}
                onChange={(e) => setNetId(e.target.value)}
              />
            </div>

            <div className="input-group">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <p className="forgot-password">Forgot Password?</p>

            <div className="captcha-row">
              <div className="captcha-box">
                <input
                  type="text"
                  placeholder="Captcha"
                  value={captcha}
                  onChange={(e) => setCaptcha(e.target.value)}
                />
              </div>
              <span className="captcha-text">{generatedCaptcha}</span>
              <span className="captcha-refresh" onClick={generateCaptcha}>
                🔄
              </span>
            </div>

            <button className="login-btn" type="submit">
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
