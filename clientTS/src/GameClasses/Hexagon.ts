import { Shape } from "./Shape.js";

export class Hexagon extends Shape {
  constructor(
    position: { x: number; y: number },
    public radius: number,
    clickable: boolean = false,
    dragable: boolean = false,
    fillColor: string = "#0ea5e9",
    strokeColor: string = "#e2e8f0"
  ) {
    super(position, clickable, dragable, false, 0, fillColor, strokeColor);
  }

  draw(context: CanvasRenderingContext2D): void {
    context.beginPath();

    for (let i = 0; i < 6; i += 1) {
      const angle = (Math.PI / 3) * i;
      const x = this.position.x + this.radius * Math.cos(angle);
      const y = this.position.y + this.radius * Math.sin(angle);

      if (i === 0) {
        context.moveTo(x, y);
      } else {
        context.lineTo(x, y);
      }
    }

    context.closePath();
    context.fillStyle = this.fillColor;
    context.strokeStyle = this.strokeColor;
    context.fill();
    context.stroke();
  }

  detectClick(x: number, y: number): boolean {
    let approx : number = 0.97;
    return (x-this.position.x) ** 2 + (y-this.position.y) ** 2 <= (this.radius*approx) ** 2;
  }
}
