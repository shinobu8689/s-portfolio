import "./style.css";

import { zip, fromEvent, interval, merge, Observable } from 'rxjs';
import { map, filter, scan } from "rxjs/operators";
import { Tick, Key, Event, Constants, Viewport, Block, Left, Right, Down, State, Restart, RotateCW, RotateCCW, Drop } from './types'
import { RNG} from './util';
import { initialState, reduceState } from './state';

/** Rendering (side effects) */

/**
 * Displays a SVG element on the canvas. Brings to foreground.
 * @param elem SVG element to display
 */
const show = (elem: SVGGraphicsElement) => {
  elem.setAttribute("visibility", "visible");
  elem.parentNode!.appendChild(elem);
};

/**
 * Hides a SVG element on the canvas.
 * @param elem SVG element to hide
 */
const hide = (elem: SVGGraphicsElement) =>
  elem.setAttribute("visibility", "hidden");

/**
 * Creates an SVG element with the given properties.
 *
 * See https://developer.mozilla.org/en-US/docs/Web/SVG/Element for valid
 * element names and properties.
 *
 * @param namespace Namespace of the SVG element
 * @param name SVGElement name
 * @param props Properties to set on the SVG element
 * @returns SVG element
 */
const createSvgElement = (
  namespace: string | null,
  name: string,
  props: Record<string, string> = {}
) => {
  const elem = document.createElementNS(namespace, name) as SVGElement;
  Object.entries(props).forEach(([k, v]) => elem.setAttribute(k, v));
  return elem;
};

// Create an observable of random number based on a seed, the one used in tute
function createRngStreamFromSource<T>(source$: Observable<T>) {
  return function createRngStream(
    seed: number = 0
  ): Observable<number> {
    // hash() a seed to generate a new value thats [-1, 1], use map to scale() it up 
    const randomNumberStream = source$.pipe(scan((acc) => RNG.hash(acc), seed), map((value) => RNG.scale(value)));
    return randomNumberStream;
  };
}


/**
 * This is the function called on page load. Your main game loop
 * should be called here.
 */
export function main() {

  // Canvas elements
  const svg = document.querySelector("#svgCanvas") as SVGGraphicsElement & HTMLElement;
  const preview = document.querySelector("#svgPreview") as SVGGraphicsElement & HTMLElement;
  const gameover = document.querySelector("#gameOver") as SVGGraphicsElement & HTMLElement;
  const container = document.querySelector("#main") as HTMLElement;
  
  svg.setAttribute("height", `${Viewport.CANVAS_HEIGHT}`);
  svg.setAttribute("width", `${Viewport.CANVAS_WIDTH}`);
  preview.setAttribute("height", `${Viewport.PREVIEW_HEIGHT}`);
  preview.setAttribute("width", `${Viewport.PREVIEW_WIDTH}`);

  // Text fields
  const levelText = document.querySelector("#levelText") as HTMLElement;
  const scoreText = document.querySelector("#scoreText") as HTMLElement;
  const highScoreText = document.querySelector("#highScoreText") as HTMLElement;

  // random number stream
  const rngStream = createRngStreamFromSource(interval(Constants.TICK_RATE_MS))(9527)

  // User input
  const key$ = fromEvent<KeyboardEvent>(document, "keypress");
  const fromKey = (keyCode: Key) => key$.pipe(filter(({ code }) => code === keyCode));
  const left$       = fromKey('KeyA').pipe(map(_ => new Left()))
  const right$      = fromKey('KeyD').pipe(map(_ => new Right()))
  const drop$       = zip(createRngStreamFromSource(interval(8))(9527), fromKey('KeyW')).pipe(map(([a, b]) => new Drop(a)))
  const down$       = zip(createRngStreamFromSource(interval(8))(9527), fromKey('KeyS')).pipe(map(([a, b]) => new Down(a)))
  const restart$    = fromKey('Enter').pipe(map(_ => new Restart()))
  const rotateCW$   = fromKey('KeyL').pipe(map(_ => new RotateCW()))
  const rotateCCW$  = fromKey('KeyK').pipe(map(_ => new RotateCCW()))

  /** Determines the rate of time steps */
  const tick$ = zip(rngStream, interval(Constants.TICK_RATE_MS)).pipe(
      map(([a, b]) => new Tick(a, b))
  );


  /**
   * Renders the current state to the canvas.
   *
   * In MVC terms, this updates the View using the Model.
   *
   * @param s Current state
   */
  const render = (s: State) => {
    
    // if getElement is null, exit function early without doing anything
    if (!svg) return

    // remove the existing rect
    svg.querySelectorAll("rect").forEach((e) => e.remove());
    preview.querySelectorAll("rect").forEach((e) => e.remove());

    // update score text
    if (scoreText) {scoreText.innerHTML = String(s.score);}
    if (highScoreText) {highScoreText.innerHTML = String(s.highScore);}
    if (levelText) {levelText.innerHTML = String(s.level);}

    // print all block in s.blocks in game frame
    s.blocks.forEach((e) => {
      const avgBlockSVG = createSvgElement(svg.namespaceURI, "rect",{
        height: `${Block.HEIGHT}`,
        width: `${Block.WIDTH}`,
        x: `${e.axis.x}`,
        y: `${e.axis.y}`,
        style: `${e.style}`
      });
      svg.appendChild(avgBlockSVG);
    })
    

    // print all block of current piece in game frame
    s.currBlock.forEach((e) => {
      const currBlockSVG = createSvgElement(svg.namespaceURI, "rect",{
        height: `${Block.HEIGHT}`,
        width: `${Block.WIDTH}`,
        x: `${e.axis.x}`,
        y: `${e.axis.y}`,
        style: `${e.style}`
      });
      svg.appendChild(currBlockSVG);
    })

    // Add the shape to the preview canvas
    s.next.forEach((e) => {
      const previewSVG = createSvgElement(preview.namespaceURI, "rect",{
        height: `${Block.HEIGHT}`,
        width: `${Block.WIDTH}`,
        x: `${e.axis.x}`,
        y: `${e.axis.y + Block.HEIGHT}`,
        style: `${e.style}`
      });
      preview.appendChild(previewSVG);
    })

  }

  const source$ = merge(tick$, left$, right$, down$, restart$, rotateCW$, rotateCCW$, drop$).pipe(
    scan( (s: State, action) => reduceState(s, action), initialState())
    ).subscribe((s: State) => {
      render(s);
      if (s.gameOver) {
        show(gameover);
      } else {
        hide(gameover);
      }
    });
}


// The following simply runs your main function on window load.  Make sure to leave it in place.
if (typeof window !== "undefined") {
  window.onload = () => {
    main();
  };
}
