import { Shape } from "./GameClasses/index.js";

export class CanvasDragHandler {
  private activeShape: Shape | null = null;
  private dragOffset = { x: 0, y: 0 };

  private readonly handleMouseDown = (event: MouseEvent): void => {
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

  private readonly handleMouseMove = (event: MouseEvent): void => {
    if (!this.activeShape) {
      return;
    }

    const point = this.getCanvasPoint(event);
    this.activeShape.position.x = point.x - this.dragOffset.x;
    this.activeShape.position.y = point.y - this.dragOffset.y;
  };

  private readonly handleMouseUp = (): void => {
    this.activeShape = null;
  };

  constructor(
    private readonly canvas: HTMLCanvasElement,
    private readonly objects: Shape[]
  ) {
    this.canvas.addEventListener("mousedown", this.handleMouseDown);
    this.canvas.addEventListener("mousemove", this.handleMouseMove);
    window.addEventListener("mouseup", this.handleMouseUp);
  }

  private getCanvasPoint(event: MouseEvent): { x: number; y: number } {
    const rect = this.canvas.getBoundingClientRect();

    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
  }
}

