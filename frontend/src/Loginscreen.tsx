import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import { Login } from "./features/auth/Login";
import { imagesByName } from "./Images";
import "./styles/Auth.css";
import { apiUrl } from "./config";

type LoginScreenProps = {
  onSwitchToRegister: () => void;
  onAcceptedLogin: () => void;
};

const factionInsignia = ["borgo", "moloch", "posterunek", "hegemonia"];

export default function LoginScreen({
  onSwitchToRegister,
  onAcceptedLogin,
}: LoginScreenProps) {
  const [username, setName] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  
  async function handleLogin() {
    if (!username.trim() || !password || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      const data = await Login(username.trim(), password, apiUrl("/api/auth/login"));
      if (data.token) {
        const normalizedUsername = username.trim();
        const previousUsername = localStorage.getItem("username");

        // Room/game ids belong to the account that created them.
        if (
          previousUsername &&
          previousUsername.toLocaleLowerCase() !==
            normalizedUsername.toLocaleLowerCase()
        ) {
          localStorage.removeItem("room");
          localStorage.removeItem("gameId");
          localStorage.removeItem("clientID");
        }

        localStorage.setItem("token", data.token);
        localStorage.setItem("username", normalizedUsername);

        if (typeof data.expiresAt === "string") {
          localStorage.setItem("tokenExpiresAt", data.expiresAt);
        } else {
          localStorage.removeItem("tokenExpiresAt");
        }

        onAcceptedLogin();
      } else {
        setError("The command network did not return an access token.");
      }
    } catch (loginError) {
      setError(
        loginError instanceof Error
          ? loginError.message
          : "Access denied. Check your credentials and try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-screen auth-screen--login">
      <div className="auth-screen__noise" aria-hidden="true" />
      <div className="auth-screen__grid" aria-hidden="true" />

      <div className="auth-shell">
        <header className="auth-header">
          <div className="auth-brand">
            <div className="auth-brand__mark" aria-hidden="true">
              <span>NH</span>
            </div>

            <div>
              <p className="auth-eyebrow">Neuroshima Hex</p>
              <h1>Command network</h1>
            </div>
          </div>

          <div className="auth-network-status" aria-label="Secure network">
            <span className="auth-network-status__signal" aria-hidden="true" />
            <div>
              <span>System status</span>
              <strong>Secure channel</strong>
            </div>
          </div>
        </header>

        <section className="auth-console" aria-labelledby="login-title">
          <aside className="auth-briefing">
            <div>
              <p className="auth-section-number">Access / 01</p>
              <h2>Return to the battlefield</h2>
              <p className="auth-briefing__copy">
                Authenticate your commander profile to enter the deployment
                network and reconnect with your battle rooms.
              </p>
            </div>

            <div className="auth-insignia" aria-hidden="true">
              {factionInsignia.map((factionName) => (
                <span className="auth-insignia__hex" key={factionName}>
                  <img
                    src={imagesByName[`${factionName}/sztab`]}
                    alt=""
                  />
                </span>
              ))}
            </div>

            <div className="auth-briefing__footer">
              <span className="auth-briefing__line" aria-hidden="true" />
              <p>Four armies. One command channel. No retreat.</p>
            </div>
          </aside>

          <div className="auth-form-panel">
            <div className="auth-form-heading">
              <p className="auth-section-number">Commander verification</p>
              <h2 id="login-title">Log in</h2>
              <p>Enter your assigned credentials to continue.</p>
            </div>

            <div className="auth-fields">
              <label className="auth-field" htmlFor="login-username">
                <span className="auth-field__label">Commander name</span>
                <span className="auth-field__control">
                  <TextInput
                    id="login-username"
                    name="username"
                    className="auth-input"
                    value={username}
                    onChange={(value) => {
                      setName(value);
                      setError("");
                    }}
                    placeholder="Enter username"
                    autoComplete="username"
                    disabled={isSubmitting}
                  />
                  <span className="auth-field__corner" aria-hidden="true" />
                </span>
              </label>

              <label className="auth-field" htmlFor="login-password">
                <span className="auth-field__label">Access key</span>
                <span className="auth-field__control">
                  <TextInput
                    id="login-password"
                    name="password"
                    className="auth-input"
                    type="password"
                    value={password}
                    onChange={(value) => {
                      setPassword(value);
                      setError("");
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        void handleLogin();
                      }
                    }}
                    placeholder="Enter password"
                    autoComplete="current-password"
                    disabled={isSubmitting}
                  />
                  <span className="auth-field__corner" aria-hidden="true" />
                </span>
              </label>
            </div>

            <div
              className={`auth-feedback${error ? " is-error" : ""}`}
              role={error ? "alert" : "status"}
            >
              <span className="auth-feedback__icon" aria-hidden="true">
                {error ? "!" : "i"}
              </span>
              <span>
                {error || "Credentials are required to access the network."}
              </span>
            </div>

            <Button
              className="auth-submit-button"
              onClick={handleLogin}
              disabled={!username.trim() || !password || isSubmitting}
              text={
                <>
                  <span>{isSubmitting ? "Authenticating…" : "Enter network"}</span>
                  <span aria-hidden="true">→</span>
                </>
              }
            />

            <div className="auth-switch">
              <div>
                <span>New commander?</span>
                <strong>Create a profile before deployment.</strong>
              </div>
              <Button
                className="auth-switch-button"
                onClick={onSwitchToRegister}
                disabled={isSubmitting}
                text={
                  <>
                    <span>Register</span>
                    <span aria-hidden="true">+</span>
                  </>
                }
              />
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}