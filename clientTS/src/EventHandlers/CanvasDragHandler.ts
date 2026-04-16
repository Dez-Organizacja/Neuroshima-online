import { Shape } from "../GameClasses/index.js";
import { CanvasEventHandler } from "./CanvasEventHandler.js";

export class CanvasDragHandler extends CanvasEventHandler {
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
    if(this.activeShape === null){
        return;
    }
    this.activeShape.dragable = false;
    this.activeShape.rotable = true;
    this.activeShape = null;
  };

  constructor(
    protected readonly canvas: HTMLCanvasElement,
    protected readonly objects: Shape[]
  ) {
    super(canvas, objects);
    this.canvas.addEventListener("mousedown", this.handleMouseDown);
    this.canvas.addEventListener("mousemove", this.handleMouseMove);
    window.addEventListener("mouseup", this.handleMouseUp);
  }
}

