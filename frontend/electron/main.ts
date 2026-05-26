import { app, BrowserWindow, screen, ipcMain } from "electron";
import path from "path";

// // app.disableHardwareAcceleration();

// // app.commandLine.appendSwitch("disable-gpu");
// // app.commandLine.appendSwitch("disable-software-rasterizer");
// // app.commandLine.appendSwitch("disable-accelerated-video-decode");
// // app.commandLine.appendSwitch("disable-features", "VaapiVideoDecoder,VaapiVideoDecodeLinuxGL");

// function createWindow() {
//   const win = new BrowserWindow({
//     width: 1800,
//     height: 1000,
//   });

//   // Load Vite dev server
//   win.loadURL("http://localhost:5173");
// }

// app.whenReady().then(createWindow);

// const { app, BrowserWindow } = require("electron");

let mainWindow;

function createWindow() {
  const primaryDisplay = screen.getPrimaryDisplay();
  const { width, height } = primaryDisplay.workAreaSize;

  const mainWindow = new BrowserWindow({
    width,
    height,
    minWidth: 800,
    minHeight: 600,
    // webPreferences: {
    //   preload: path.join(__dirname, "preload.js"),
    // },
  });

  mainWindow.loadURL("http://localhost:5173");
  mainWindow.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});