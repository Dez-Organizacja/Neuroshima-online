import { CanvasClickHandler } from "./CanvasClickHandler.js";
import { CanvasDragHandler } from "./CanvasDragHandler.js";
import { Hexagon, Rectangle } from "./GameClasses/index.js";
const canvasElement = document.getElementById("app-canvas");
const buttonElement = document.getElementById("add-element");
if (!(canvasElement instanceof HTMLCanvasElement)) {
    throw new Error("Nie znaleziono elementu canvas o id 'app-canvas'.");
}
if (!(buttonElement instanceof HTMLButtonElement)) {
    throw new Error("Nie znaleziono elementu button o id 'add-element'.");
}
const canvas = canvasElement;
const button = buttonElement;
const contextValue = canvas.getContext("2d");
if (!contextValue) {
    throw new Error("Nie udalo sie pobrac kontekstu 2D dla canvas.");
}
const context = contextValue;
const shapes = [
    new Hexagon({ x: 360, y: 180 }, 55, false, false, "#123456", "#e2e8f0"),
];
new CanvasClickHandler(canvas, shapes);
new CanvasDragHandler(canvas, shapes);
function fu() {
    shapes.push(new Rectangle({
        x: Math.random() * canvas.clientWidth,
        y: Math.random() * canvas.clientHeight,
    }, 50, 50, true, true, `#${Math.floor(Math.random() * 16777215).toString(16)}`, "#e2e8f0"));
}
button.addEventListener("click", fu);
function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.floor(rect.width * dpr);
    canvas.height = Math.floor(rect.height * dpr);
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
}
function draw() {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    context.clearRect(0, 0, width, height);
    context.fillStyle = "#e2e8f0";
    context.font = "16px system-ui, sans-serif";
    context.fillText("TypeScript + Canvas", 16, 28);
    shapes.forEach((shape) => shape.draw(context));
}
function loop() {
    draw();
    requestAnimationFrame(loop);
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();
requestAnimationFrame(loop);
