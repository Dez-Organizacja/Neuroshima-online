import { Shape } from "../GameClasses/index.js";
import { CanvasEventHandler } from "./CanvasEventHandler.js";

export class CanvasClickHandler extends CanvasEventHandler {
  private readonly handleClick = (event: MouseEvent): void => {
    const point = this.getCanvasPoint(event);

    for(const object of this.objects) {
      if(object.clickable && object.detectClick(point.x, point.y)) {
        object.fillColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
      }
    }
  };

  constructor(
    protected readonly canvas: HTMLCanvasElement,
    protected readonly objects: Shape[]
  ) {
    super(canvas, objects);
    this.canvas.addEventListener("click", this.handleClick);
  }
}

