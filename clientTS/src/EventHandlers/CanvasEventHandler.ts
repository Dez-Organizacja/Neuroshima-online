import { Shape } from "../GameClasses/index.js";

export class CanvasEventHandler{

    constructor(
        protected readonly canvas: HTMLCanvasElement,
        protected readonly objects: Shape[]
      ){}

    protected getCanvasPoint(event: MouseEvent): { x: number; y: number } {
    const rect = this.canvas.getBoundingClientRect();

    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
  }
}