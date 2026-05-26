const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("api", {

    saveAction: (data) =>
        ipcRenderer.invoke("save-action", data)
});