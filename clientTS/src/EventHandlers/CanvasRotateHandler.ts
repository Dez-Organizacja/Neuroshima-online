import { CanvasEventHandler } from "./CanvasEventHandler.js";
import {Shape} from "../GameClasses/index.js";

export class CanvasRotateHandler extends CanvasEventHandler{
  private activeShape: Shape | null = null;
  private intialAngle: number = 0;

  private readonly handleMouseDown = (event: MouseEvent): void => {
      const point = this.getCanvasPoint(event);

      for (let i = this.objects.length - 1; i >= 0; i -= 1) {
          const object = this.objects[i];
          if (object.rotable && object.detectClick(point.x, point.y)) {
              this.activeShape = object;
              this.intialAngle = Math.atan2(point.y - object.position.y, point.x - object.position.x) - object.rotation * (Math.PI / 180);
              break;
          }
      }

  };

  private readonly handleMouseMove = (event: MouseEvent): void => {
        if (!this.activeShape) {
            return;
        }

        const point = this.getCanvasPoint(event);
        const angle = Math.atan2(point.y - this.activeShape.position.y, point.x - this.activeShape.position.x) - this.intialAngle;
        this.activeShape.setRotation(angle * (180 / Math.PI));

  }

  private readonly handleMouseUp = (): void => {
      if(this.activeShape === null){
          return;
      }
      this.activeShape.rotable = false;
      this.activeShape.dragable = true;
      this.activeShape = null;
  }

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
