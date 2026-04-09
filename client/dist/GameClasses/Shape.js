export class Shape {
    constructor(position, clickable = false, dragable = false, fillColor = "#0ea5e9", strokeColor = "#e2e8f0") {
        this.position = position;
        this.clickable = clickable;
        this.dragable = dragable;
        this.fillColor = fillColor;
        this.strokeColor = strokeColor;
    }
}
