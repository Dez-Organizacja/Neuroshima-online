export class CanvasClickHandler {
    constructor(canvas, objects) {
        this.canvas = canvas;
        this.objects = objects;
        this.handleClick = (event) => {
            const point = this.getCanvasPoint(event);
            for (const object of this.objects) {
                if (object.clickable && object.detectClick(point.x, point.y)) {
                    object.fillColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
                }
            }
        };
        this.canvas.addEventListener("click", this.handleClick);
    }
    getCanvasPoint(event) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top,
        };
    }
}
