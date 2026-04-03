import { Shape } from "./GameClasses/index.js";

export class CanvasClickHandler {
  private readonly handleClick = (event: MouseEvent): void => {
    const point = this.getCanvasPoint(event);

    for(const object of this.objects) {
      if(object.clickable && object.detectClick(point.x, point.y)) {
        object.fillColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
      }
    }
  };

  constructor(
    private readonly canvas: HTMLCanvasElement,
    private readonly objects: Shape[]
  ) {
    this.canvas.addEventListener("click", this.handleClick);
  }

  private getCanvasPoint(event: MouseEvent): { x: number; y: number } {
    const rect = this.canvas.getBoundingClientRect();

    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
  }
}

