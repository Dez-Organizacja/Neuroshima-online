const hasLoginScreen = Boolean(
  document.getElementById("login-button") ?? document.getElementById("login-button")
);
const hasGameCanvas = Boolean(document.getElementById("app-canvas"));

if (hasLoginScreen) {
  void import("./LoginScreen/main.js");
}

if (hasGameCanvas) {
  void import("./game/main.js");
}
