export interface Point {
  x: number;
  y: number;
}

export abstract class Shape {
  constructor(
    public position: Point,
    public clickable: boolean = false,
    public dragable: boolean = false,
    public fillColor: string = "#0ea5e9",
    public strokeColor: string = "#e2e8f0"
  ) {}

  abstract draw(context: CanvasRenderingContext2D): void;

  abstract detectClick(x: number, y: number): boolean;
}
