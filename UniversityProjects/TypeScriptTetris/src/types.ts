
export { Viewport, Constants, Block, SpawnProp, Tick, RotateCW, RotateCCW, Left, Right, Down, Restart, Drop }
export type { Body, State, ViewType, Key, Event }

import { Axis } from './util'

const Viewport = {
  CANVAS_WIDTH: 200,
  CANVAS_HEIGHT: 400,
  PREVIEW_WIDTH: 160,
  PREVIEW_HEIGHT: 80,
} as const;

const Constants = {
  TICK_RATE_MS: 500,
  GRID_WIDTH: 10,
  GRID_HEIGHT: 20,
} as const;

const Block = {
  WIDTH: Viewport.CANVAS_WIDTH / Constants.GRID_WIDTH,
  HEIGHT: Viewport.CANVAS_HEIGHT / Constants.GRID_HEIGHT,
};

// where the tetromino spawns
const SpawnProp = {
  SPAWN_X: 3,
  SPAWN_Y: 0
}


type Key = "KeyS" | "KeyA" | "KeyD" | "KeyW" | "KeyK" | "KeyL" | "Enter";

type Event = "keydown" | "keyup" | "keypress";

type ViewType = 'block';

class Tick { constructor(public readonly value: number, public readonly time: number) { } }
class RotateCW { constructor() { } }
class RotateCCW { constructor() { } }
class Left { constructor() { } }
class Right { constructor() { } }
class Drop { constructor(public readonly value: number) { } }
class Down { constructor(public readonly value: number) { } }
class Restart { constructor() { } }


interface IBody {
    viewType: ViewType,
    axis: Axis,
    style: string // block colouring
    relativeLocation: number  
    /** 0, belongs to no where or O shape, no effect by rotation
     *  1 - 9 for 3x3 according to numpad, 
     *  11 - 14 L=>R for I beam
     *  21 - 24 T=>B for I beam
     *  */ 
  }

type Body = Readonly<IBody>

type State = Readonly<{
    clearedRow: number,
    currBlock: Array<Body>,
    blocks: Array<Body>,
    gameOver: boolean,
    score: number,
    next: Array<Body>
    highScore: number,
    level: number
  }>