import { Shape } from "./Shape.js";
export class Rectangle extends Shape {
    constructor(position, width, height, clickable, dragable, fillColor, strokeColor) {
        super(position, clickable, dragable, fillColor, strokeColor);
        this.width = width;
        this.height = height;
    }
    draw(context) {
        context.fillStyle = this.fillColor;
        context.strokeStyle = this.strokeColor;
        context.fillRect(this.position.x, this.position.y, this.width, this.height);
        context.strokeRect(this.position.x, this.position.y, this.width, this.height);
    }
    detectClick(x, y) {
        const minX = Math.min(this.position.x, this.position.x + this.width);
        const maxX = Math.max(this.position.x, this.position.x + this.width);
        const minY = Math.min(this.position.y, this.position.y + this.height);
        const maxY = Math.max(this.position.y, this.position.y + this.height);
        return x >= minX && x <= maxX && y >= minY && y <= maxY;
    }
}
