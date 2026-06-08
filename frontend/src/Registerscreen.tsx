import { useState } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import { Register } from "./features/auth/Register";
import { imagesByName } from "./Images";
import "./styles/Auth.css";

type RegisterScreenProps = {
  onSwitchToLogin: () => void;
};

const factionInsignia = ["borgo", "moloch", "posterunek", "hegemonia"];

export default function RegisterScreen({
  onSwitchToLogin,
}: RegisterScreenProps) {
  const url = "http://localhost:8080/api/auth/register";
  const [username, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const passwordsMatch = password === confirmPassword;
  const canSubmit =
    Boolean(username.trim()) &&
    Boolean(password) &&
    Boolean(confirmPassword) &&
    passwordsMatch &&
    !isSubmitting;

  async function handleRegister() {
    if (!canSubmit) {
      if (password && confirmPassword && !passwordsMatch) {
        setError("The access keys do not match.");
      }
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      await Register(username.trim(), password, url);
      onSwitchToLogin();
    } catch (registerError) {
      setError(
        registerError instanceof Error
          ? registerError.message
          : "Profile creation failed. Try another commander name.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  function clearError() {
    if (error) {
      setError("");
    }
  }

  return (
    <main className="auth-screen auth-screen--register">
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

          <div className="auth-network-status" aria-label="Recruitment channel">
            <span className="auth-network-status__signal" aria-hidden="true" />
            <div>
              <span>System status</span>
              <strong>Recruitment open</strong>
            </div>
          </div>
        </header>

        <section className="auth-console" aria-labelledby="register-title">
          <aside className="auth-briefing">
            <div>
              <p className="auth-section-number">Enlistment / 02</p>
              <h2>Join the command network</h2>
              <p className="auth-briefing__copy">
                Establish a commander identity, secure your access key, and
                prepare to lead one of the armies of the wasteland.
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
              <p>Your callsign will identify you in every battle room.</p>
            </div>
          </aside>

          <div className="auth-form-panel">
            <div className="auth-form-heading">
              <p className="auth-section-number">New commander profile</p>
              <h2 id="register-title">Register</h2>
              <p>Create the credentials used for future deployments.</p>
            </div>

            <div className="auth-fields">
              <label className="auth-field" htmlFor="register-username">
                <span className="auth-field__label">Commander name</span>
                <span className="auth-field__control">
                  <TextInput
                    id="register-username"
                    name="username"
                    className="auth-input"
                    value={username}
                    onChange={(value) => {
                      setName(value);
                      clearError();
                    }}
                    placeholder="Choose username"
                    autoComplete="username"
                    disabled={isSubmitting}
                  />
                  <span className="auth-field__corner" aria-hidden="true" />
                </span>
              </label>

              <label className="auth-field" htmlFor="register-password">
                <span className="auth-field__label">Access key</span>
                <span className="auth-field__control">
                  <TextInput
                    id="register-password"
                    name="password"
                    className="auth-input"
                    type="password"
                    value={password}
                    onChange={(value) => {
                      setPassword(value);
                      clearError();
                    }}
                    placeholder="Create password"
                    autoComplete="new-password"
                    disabled={isSubmitting}
                  />
                  <span className="auth-field__corner" aria-hidden="true" />
                </span>
              </label>

              <label className="auth-field" htmlFor="register-password-confirm">
                <span className="auth-field__label">Confirm access key</span>
                <span className="auth-field__control">
                  <TextInput
                    id="register-password-confirm"
                    name="password-confirm"
                    className={`auth-input${
                      confirmPassword && !passwordsMatch ? " is-invalid" : ""
                    }`}
                    type="password"
                    value={confirmPassword}
                    onChange={(value) => {
                      setConfirmPassword(value);
                      clearError();
                    }}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        void handleRegister();
                      }
                    }}
                    placeholder="Repeat password"
                    autoComplete="new-password"
                    disabled={isSubmitting}
                  />
                  <span className="auth-field__corner" aria-hidden="true" />
                </span>
              </label>
            </div>

            <div
              className={`auth-feedback${
                error || (confirmPassword && !passwordsMatch) ? " is-error" : ""
              }`}
              role={error ? "alert" : "status"}
            >
              <span className="auth-feedback__icon" aria-hidden="true">
                {error || (confirmPassword && !passwordsMatch) ? "!" : "i"}
              </span>
              <span>
                {error ||
                  (confirmPassword && !passwordsMatch
                    ? "The access keys do not match."
                    : "Use a unique commander name and a secure access key.")}
              </span>
            </div>

            <Button
              className="auth-submit-button"
              onClick={handleRegister}
              disabled={!canSubmit}
              text={
                <>
                  <span>{isSubmitting ? "Creating profile…" : "Create profile"}</span>
                  <span aria-hidden="true">→</span>
                </>
              }
            />

            <div className="auth-switch">
              <div>
                <span>Already enlisted?</span>
                <strong>Return to commander verification.</strong>
              </div>
              <Button
                className="auth-switch-button"
                onClick={onSwitchToLogin}
                disabled={isSubmitting}
                text={
                  <>
                    <span>Log in</span>
                    <span aria-hidden="true">↳</span>
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