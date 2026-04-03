export class CanvasDragHandler {
    constructor(canvas, objects) {
        this.canvas = canvas;
        this.objects = objects;
        this.activeShape = null;
        this.dragOffset = { x: 0, y: 0 };
        this.handleMouseDown = (event) => {
            const point = this.getCanvasPoint(event);
            for (let i = this.objects.length - 1; i >= 0; i -= 1) {
                const object = this.objects[i];
                if (object.dragable && object.detectClick(point.x, point.y)) {
                    this.activeShape = object;
                    this.dragOffset = {
                        x: point.x - object.position.x,
                        y: point.y - object.position.y,
                    };
                    break;
                }
            }
        };
        this.handleMouseMove = (event) => {
            if (!this.activeShape) {
                return;
            }
            const point = this.getCanvasPoint(event);
            this.activeShape.position.x = point.x - this.dragOffset.x;
            this.activeShape.position.y = point.y - this.dragOffset.y;
        };
        this.handleMouseUp = () => {
            this.activeShape = null;
        };
        this.canvas.addEventListener("mousedown", this.handleMouseDown);
        this.canvas.addEventListener("mousemove", this.handleMouseMove);
        window.addEventListener("mouseup", this.handleMouseUp);
    }
    getCanvasPoint(event) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top,
        };
    }
}
