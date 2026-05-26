import React from "react";
import { useState } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import DevBoardApp from "./DevBoardApp";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {/* <App/> */}
    <DevBoardApp />
  </React.StrictMode>
);
