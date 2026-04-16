import { Shape } from "./Shape.js";

export class Rectangle extends Shape {
  constructor(
    position: { x: number; y: number },
    public width: number,
    public height: number,
    clickable: boolean = false,
    dragable: boolean = false,
    fillColor: string = "#0ea5e9",
    strokeColor: string = "#e2e8f0"
  ) {
    super(position, clickable, dragable, false, 0, fillColor, strokeColor);
  }

  draw(context: CanvasRenderingContext2D): void {
    context.fillStyle = this.fillColor;
    context.strokeStyle = this.strokeColor;

    const centerX = this.position.x + this.width / 2;
    const centerY = this.position.y + this.height / 2;
    const angleRad = (this.rotation * Math.PI) / 180;

    context.save();
    context.translate(centerX, centerY);
    context.rotate(angleRad);
    context.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
    context.strokeRect(-this.width / 2, -this.height / 2, this.width, this.height);
    context.restore();
  }

  detectClick(x: number, y: number): boolean {
    const minX = Math.min(this.position.x, this.position.x + this.width);
    const maxX = Math.max(this.position.x, this.position.x + this.width);
    const minY = Math.min(this.position.y, this.position.y + this.height);
    const maxY = Math.max(this.position.y, this.position.y + this.height);

    return x >= minX && x <= maxX && y >= minY && y <= maxY;
  }
}
