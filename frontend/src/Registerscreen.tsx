import { useState, useCallback, useEffect } from "react";
import Button from "./components/Button";
import TextInput from "./components/TekstInput";
import { Register } from "./features/auth/Register";
import { imagesByName } from "./Images";
import { apiUrl } from "./config";
import "./styles/Auth.css";

type RegisterScreenProps = {
  onSwitchToLogin: () => void;
};

const factionInsignia = ["borgo", "moloch", "posterunek", "hegemonia"];

type RegistrationConfig = {
  registrationEnabled: boolean;
  captchaRequired: boolean;
};

type CaptchaResponse = {
  captchaId: string;
  image: string;
};

type ApiError = {
  error?: string;
};

export default function RegisterScreen({
  onSwitchToLogin,
}: RegisterScreenProps) {
  const [username, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const [isConfigLoading, setIsConfigLoading] = useState(true);
  const [registrationEnabled, setRegistrationEnabled] = useState(false);

  const [captchaRequired, setCaptchaRequired] = useState(false);
  const [captchaId, setCaptchaId] = useState("");
  const [captchaImage, setCaptchaImage] = useState("");
  const [captchaAnswer, setCaptchaAnswer] = useState("");
  const [isCaptchaLoading, setIsCaptchaLoading] = useState(false);

  const loadCaptcha = useCallback(async () => {
    
    setIsCaptchaLoading(true);
    setCaptchaId("");
    setCaptchaImage("");
    setCaptchaAnswer("");

    try {
      const response = await fetch(apiUrl("/api/auth/captcha"), {
        cache: "no-store",
      });

      const data = (await response.json()) as CaptchaResponse & ApiError;

      if (!response.ok) {
        throw new Error(data.error || "Could not load CAPTCHA.");
      }

      if (!data.captchaId || !data.image) {
        throw new Error("The server returned an invalid CAPTCHA response.");
      }

      setCaptchaId(data.captchaId);
      setCaptchaImage(data.image);
    } finally {
      setIsCaptchaLoading(false);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function initialiseRegistration() {
      setIsConfigLoading(true);

      try {
        const response = await fetch(apiUrl("/api/auth/registration-config"),{cache: "no-store"});

        const data = (await response.json()) as RegistrationConfig & ApiError;

        if (!response.ok) {
          throw new Error(data.error || "Could not read registration settings.");
        }

        if (cancelled) {
          return;
        }

        setRegistrationEnabled(data.registrationEnabled);
        setCaptchaRequired(data.captchaRequired);

        if (data.registrationEnabled && data.captchaRequired) {
          await loadCaptcha();
        }
      } catch (initialisationError) {
        if (!cancelled) {
          setError(
            initialisationError instanceof Error
              ? initialisationError.message
              : "Could not initialise registration.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsConfigLoading(false);
        }
      }
    }

    void initialiseRegistration();

    return () => {
      cancelled = true;
    };
  }, [loadCaptcha]);

  const passwordsMatch = password === confirmPassword;
  const captchaComplete =
    !captchaRequired ||
    (Boolean(captchaId) &&
      Boolean(captchaImage) &&
      Boolean(captchaAnswer.trim()));

  const canSubmit =
    Boolean(username.trim()) &&
    Boolean(password) &&
    Boolean(confirmPassword) &&
    passwordsMatch &&
    captchaComplete &&
    registrationEnabled &&
    !isConfigLoading &&
    !isCaptchaLoading &&
    !isSubmitting;

  async function handleRefreshCaptcha() {
    setError("");

    try {
      await loadCaptcha();
    } catch (captchaError) {
      setError(
        captchaError instanceof Error
          ? captchaError.message
          : "Could not load a new CAPTCHA.",
      );
    }
  }

  async function handleRegister() {
    if (!canSubmit) {
      if (password && confirmPassword && !passwordsMatch) {
        setError("The access keys do not match.");
      } else if (captchaRequired && !captchaAnswer.trim()) {
        setError("Enter the code shown in the CAPTCHA image.");
      }

      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      await Register(
        {
          username: username.trim(),
          password,
          ...(captchaRequired
            ? {
                captchaId,
                captchaAnswer: captchaAnswer.trim(),
              }
            : {}),
        },
        apiUrl("/api/auth/register"),
      );

      onSwitchToLogin();
    } catch (registerError) {
      setError(
        registerError instanceof Error
          ? registerError.message
          : "Profile creation failed. Try another commander name.",
      );
      if (captchaRequired) {
        try {
          await loadCaptcha();
        } catch {
        }
      }
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

              {captchaRequired && (
                <div className="auth-captcha">
                  <div className="auth-captcha__heading">
                    <span className="auth-field__label">
                      Security check
                    </span>

                    <Button
                      className="auth-captcha__refresh"
                      onClick={() => void handleRefreshCaptcha()}
                      disabled={isSubmitting || isCaptchaLoading}
                      text={isCaptchaLoading ? "Loading…" : "New code"}
                    />
                  </div>

                  <div className="auth-captcha__image-frame">
                    {captchaImage ? (
                      <img
                        className="auth-captcha__image"
                        src={captchaImage}
                        alt="CAPTCHA verification code"
                      />
                    ) : (
                      <span>
                        {isCaptchaLoading
                          ? "Generating security code…"
                          : "CAPTCHA unavailable"}
                      </span>
                    )}
                  </div>

                  <label
                    className="auth-field"
                    htmlFor="register-captcha"
                  >
                    <span className="auth-field__label">
                      Enter the code from the image
                    </span>

                    <span className="auth-field__control">
                      <TextInput
                        id="register-captcha"
                        name="captchaAnswer"
                        className="auth-input"
                        value={captchaAnswer}
                        onChange={(value) => {
                          setCaptchaAnswer(value);
                          clearError();
                        }}
                        onKeyDown={(event) => {
                          if (event.key === "Enter") {
                            void handleRegister();
                          }
                        }}
                        placeholder="Security code"
                        autoComplete="off"
                        disabled={
                          isSubmitting ||
                          isCaptchaLoading ||
                          !captchaImage
                        }
                      />

                      <span
                        className="auth-field__corner"
                        aria-hidden="true"
                      />
                    </span>
                  </label>
                </div>
              )}

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
                    : isConfigLoading
                      ? "Checking registration settings…"
                      : !registrationEnabled
                        ? "Registration is currently disabled."
                        : captchaRequired
                          ? "Complete the security check before creating the profile."
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