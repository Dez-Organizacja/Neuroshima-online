export interface Point {
  x: number;
  y: number;
}

export abstract class Shape {
  public clickable: boolean = false;
  public dragable: boolean = false;
  public rotable: boolean = false;
  public rotation: number = 0;
  public fillColor: string = "#0ea5e9";
  public strokeColor: string = "#e2e8f0";

  constructor(
    public position: Point,
    clickable: boolean = false,
    dragable: boolean = false,
    rotable: boolean = false,
    rotation: number = 0,
    fillColor: string = "#0ea5e9",
    strokeColor: string = "#e2e8f0"
  ) {
    this.clickable = clickable;
    this.dragable = dragable;
    this.rotable = rotable;
    this.rotation = rotation;
    this.fillColor = fillColor;
    this.strokeColor = strokeColor;
  }

  abstract draw(context: CanvasRenderingContext2D): void;

  abstract detectClick(x: number, y: number): boolean;

  setRotation(angle: number): void {
    this.rotation = angle % 360;
  }
}
