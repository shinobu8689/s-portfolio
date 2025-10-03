export { initialState, reduceState }

import { SpawnProp, Body, Constants, State, Block, Tick, RotateCW, RotateCCW, Left, Down, Right, Restart, Drop} from "./types"
import { Axis , randValueRange } from "./util"

/**
   * create a new single block
   *
   * @param x : axis coordinate in grid value 0 - 9
   * @param y : axis coordinate in grid value 0 - 19
   * @param style: block colour in string 'fill: _____', where _____ is the colour
   * @param relativeLocation: for tetromino rotation, see doRotateCW() / doRotateCCW()
   * @return block Body
   */
const createBlock = (x: number) => (y: number) => (style: string) => (relativeLocation: number): Body => 
    ({
        viewType: 'block',
        axis: new Axis(x * Block.WIDTH, y * Block.HEIGHT),
        style: style,
        relativeLocation: relativeLocation
    })

/**
   * create different tetromino shapes: O, T, J, L, S, Z, I
   *
   * @param x : axis coordinate in grid value 0 - 9
   * @param y : axis coordinate in grid value 0 - 19
   * @param rng: random number from rngStream for random tetromino generation
   * @return array of block
   */
const createShape = (x: number = 0) => (y: number = 0) => (rng: number = 1): Array<Body> => 
    rng === 1 ? 
        [createBlock(x + 1)(y)('fill: yellow')(0),  // O
        createBlock(x + 2)(y)('fill: yellow')(0), 
        createBlock(x + 1)(y + 1)('fill: yellow')(0),
        createBlock(x + 2)(y + 1)('fill: yellow')(0)] :
    rng === 2 ? 
        [createBlock(x + 1)(y)('fill: purple')(8),  // T
        createBlock(x)(y + 1)('fill: purple')(4), 
        createBlock(x + 1)(y + 1)('fill: purple')(5),
        createBlock(x + 2)(y + 1)('fill: purple')(6)] :
    rng === 3 ? 
        [createBlock(x)(y)('fill: blue')(7),        // J
        createBlock(x)(y + 1)('fill: blue')(4), 
        createBlock(x + 1)(y + 1)('fill: blue')(5),
        createBlock(x + 2)(y + 1)('fill: blue')(6)] :
    rng === 4 ? 
        [createBlock(x + 2)(y)('fill: orange')(9),  // L
        createBlock(x)(y + 1)('fill: orange')(4), 
        createBlock(x + 1)(y + 1)('fill: orange')(5),
        createBlock(x + 2)(y + 1)('fill: orange')(6)] :
    rng === 5 ? 
        [createBlock(x + 1)(y)('fill: green')(8),   // S
        createBlock(x + 2)(y)('fill: green')(9), 
        createBlock(x)(y + 1)('fill: green')(4),
        createBlock(x + 1)(y + 1)('fill: green')(5)] :
    rng === 6 ? 
        [createBlock(x)(y)('fill: red')(7),         // Z
        createBlock(x + 1)(y)('fill: red')(8),
        createBlock(x + 1)(y + 1)('fill: red')(5),
         createBlock(x + 2)(y + 1)('fill: red')(6)] :
 // rng === 7 ?
        [createBlock(x)(y)('fill: cyan')(11),       // I
        createBlock(x + 1)(y)('fill: cyan')(12), 
        createBlock(x + 2)(y)('fill: cyan')(13),
        createBlock(x + 3)(y)('fill: cyan')(14)]

/////////////// INITIAL STATE ////////////////////
const initialState = (score: number = 0): State => ({
        clearedRow: 0,
        currBlock: createShape(SpawnProp.SPAWN_X)(SpawnProp.SPAWN_Y)(4),
        blocks: [],
        gameOver: false,
        score: 0,
        next: createShape(SpawnProp.SPAWN_X)(SpawnProp.SPAWN_Y)(2),
        highScore: score,
        level: 0
});

//////////////// STATE UPDATES //////////////////////
                 
    const totalRows = [...Array(Constants.GRID_HEIGHT).keys()] // 0 - 19
    const totalCols = [...Array(Constants.GRID_WIDTH).keys()] // 0 - 9
    const lvlUpRow = 5  // the number of rows cleared to level up & increase difficulty

 /**
   * clear the given row in blocks
   *
   * @param blocks : array of blocks to be filtered
   * @param row : the row to be cleared in blocks
   * @return array without the blocks that in given row
   */
    const rowToClear = (blocks: Array<Body>) => (row: number): Array<Body> => 
        blocks.filter((b: Body) => b.axis.y != row * Block.HEIGHT)



    // check given row inside blocks is full or not (10 blocks)
    const fullRow = (blocks: Array<Body>) => (row: number): boolean =>
        blocks.filter((b: Body) => b.axis.y === row * Block.HEIGHT).length === 10

    // return a list of rows that are full
    const fullRows = (blocks: Array<Body>): Array<number> =>
        totalRows.filter((e) => fullRow(blocks)(e) )
           

    // check is the current Block overlapped with all the blocks
    const overlapped = (currBlock: Array<Body>) => (blocks: Array<Body>) =>
        currBlock.some((e) => blocks.some( (another) =>
            e.axis.x === another.axis.x && e.axis.y === another.axis.y
        ))

    // when level up and currBlock goes down and get overlapped
    // this is should no be counted as gameOver, so auto correct currBlock location to not overlap
    const seperateOverlap = (currBlock: Array<Body>) => (blocks: Array<Body>): Array<Body> => 
        overlapped(currBlock)(blocks) ? 
            currBlock.map((b: Body) => ({...b, axis: b.axis.ascend()})) : currBlock

    const bottomTouchGround = (b: Body): boolean => (b.axis.y >= (Constants.GRID_HEIGHT - 1) * Block.HEIGHT)



    const handleCollisions = (s: State) => (randValue: number): State => {

        // has that single block landed on existing block yet
        const bottomTouchBlock = (a: Body): boolean => s.blocks.some((b: Body) => 
            a.axis.x === b.axis.x &&                    // only collided on top and buttom
            a.axis.y + Block.HEIGHT >= b.axis.y &&      // blockA top past blockB bottom
            a.axis.y <= b.axis.y + Block.HEIGHT )       // blockA bottom past blockB top
            
        const rowThatsFull = fullRows(s.blocks)
        const currBlockLandedOnSth = s.currBlock.some((e) => bottomTouchGround(e) || bottomTouchBlock(e)) 
            
        // clear each full row form all blocks
        const removeFullRow = (blocks: Array<Body>): Array<Body> => 
            rowThatsFull.reduce((acc, e) => rowToClear(acc)(e), blocks)
            
        // lower all blocks thats above the cleared row
        const collapseRow = (blocks: Array<Body>): Array<Body> => 
            rowThatsFull.reduce( (acc, e) => 
                acc.map((b: Body) => (b.axis.y < e * Block.HEIGHT) ? {...b, axis: b.axis.descend()} : b ),
            removeFullRow(blocks))

        return {
            ...s,
            clearedRow: s.clearedRow + rowThatsFull.length,
            score: s.score + rowThatsFull.length * 10,
            highScore: (s.score + rowThatsFull.length * 10) > s.highScore ? s.score : s.highScore,
            blocks: currBlockLandedOnSth ?
            collapseRow([...s.blocks].concat(seperateOverlap(s.currBlock)(s.blocks))):
            collapseRow([...s.blocks]),
            currBlock: currBlockLandedOnSth ? s.next : s.currBlock,
            // game over when currBlock spawn and overlapped existing blocks
            // or existing blocks exceeds the frame
            gameOver: (overlapped(s.next)(s.blocks)) || s.blocks.some((e) => e.axis.y < 0 ) ?
                    true : s.gameOver,
            level: s.clearedRow >= lvlUpRow ? s.level + 1 : s.level,
            next: currBlockLandedOnSth ?
                createShape(SpawnProp.SPAWN_X)(SpawnProp.SPAWN_Y)(randValueRange(randValue)(1)(7)):
                s.next
        }
    }
    
    

    /** rotation rules to map to rotated location
    *  0 no effect by rotation, belongs to no where or O shape, 
    *  1 - 9 for 3x3 according to numpad
    *  11 - 14 L=>R for I beam
    *  21 - 24 T=>B for I beam
    *  */
    const doRotateCW = (currBlock: Array<Body>): Array<Body> => 
        currBlock.map( (b: Body) => 
            b.relativeLocation === 1 ? createBlock(b.axis.x / Block.WIDTH)(b.axis.y / Block.HEIGHT - 2)(b.style)(7) :
            b.relativeLocation === 2 ? createBlock(b.axis.x / Block.WIDTH - 1)(b.axis.y / Block.HEIGHT - 1)(b.style)(4) :
            b.relativeLocation === 3 ? createBlock(b.axis.x / Block.WIDTH - 2)(b.axis.y / Block.HEIGHT)(b.style)(1) :
            b.relativeLocation === 4 ? createBlock(b.axis.x / Block.WIDTH + 1)(b.axis.y / Block.HEIGHT - 1)(b.style)(8) :
            b.relativeLocation === 6 ? createBlock(b.axis.x / Block.WIDTH - 1)(b.axis.y / Block.HEIGHT + 1)(b.style)(2) :
            b.relativeLocation === 7 ? createBlock(b.axis.x / Block.WIDTH + 2)(b.axis.y / Block.HEIGHT)(b.style)(9) :
            b.relativeLocation === 8 ? createBlock(b.axis.x / Block.WIDTH + 1)(b.axis.y / Block.HEIGHT + 1)(b.style)(6) :
            b.relativeLocation === 9 ? createBlock(b.axis.x / Block.WIDTH)(b.axis.y / Block.HEIGHT + 2)(b.style)(3) :
            b.relativeLocation > 10 ? doRotateI(b) :    // I beam
            b
        )

    const doRotateCCW = (currBlock: Array<Body>): Array<Body> => 
        currBlock.map( (b: Body) => 
            b.relativeLocation === 1 ? createBlock(b.axis.x / Block.WIDTH + 2)(b.axis.y / Block.HEIGHT)(b.style)(3) :
            b.relativeLocation === 2 ? createBlock(b.axis.x / Block.WIDTH + 1)(b.axis.y / Block.HEIGHT - 1)(b.style)(6) :
            b.relativeLocation === 3 ? createBlock(b.axis.x / Block.WIDTH)(b.axis.y / Block.HEIGHT - 2)(b.style)(9) :
            b.relativeLocation === 4 ? createBlock(b.axis.x / Block.WIDTH + 1)(b.axis.y / Block.HEIGHT + 1)(b.style)(2) :
            b.relativeLocation === 6 ? createBlock(b.axis.x / Block.WIDTH - 1)(b.axis.y / Block.HEIGHT - 1)(b.style)(8) :
            b.relativeLocation === 7 ? createBlock(b.axis.x / Block.WIDTH)(b.axis.y / Block.HEIGHT + 2)(b.style)(1) :
            b.relativeLocation === 8 ? createBlock(b.axis.x / Block.WIDTH - 1)(b.axis.y / Block.HEIGHT + 1)(b.style)(4) :
            b.relativeLocation === 9 ? createBlock(b.axis.x / Block.WIDTH - 2)(b.axis.y / Block.HEIGHT)(b.style)(7) :
            b.relativeLocation > 10 ? doRotateI(b) : // I beam
            b
        )
    
    const doRotateI = (b: Body): Body => 
        b.relativeLocation === 11 ? createBlock(b.axis.x / Block.WIDTH + 2)(b.axis.y / Block.HEIGHT - 2)(b.style)(21) :
        b.relativeLocation === 12 ? createBlock(b.axis.x / Block.WIDTH + 1)(b.axis.y / Block.HEIGHT - 1)(b.style)(22) :
        b.relativeLocation === 14 ? createBlock(b.axis.x / Block.WIDTH - 1)(b.axis.y / Block.HEIGHT + 1)(b.style)(24) :
        b.relativeLocation === 21 ? createBlock(b.axis.x / Block.WIDTH - 2)(b.axis.y / Block.HEIGHT + 2)(b.style)(11) :
        b.relativeLocation === 22 ? createBlock(b.axis.x / Block.WIDTH - 1)(b.axis.y / Block.HEIGHT + 1)(b.style)(12) :
        b.relativeLocation === 24 ? createBlock(b.axis.x / Block.WIDTH + 1)(b.axis.y / Block.HEIGHT - 1)(b.style)(14) :
        b

        
    /** 
     * interval tick: shape drop
     * @param s old State
     * @param tick object with elapsed time
     * @returns new State
     */
    const tick = (s: State) => (t: Tick): State => 
        s.gameOver? s :
        handleCollisions({
            ...s,
            clearedRow: (s.clearedRow >= lvlUpRow) ? s.clearedRow - lvlUpRow : s.clearedRow, 
            blocks: addDummyRow(t.value)(s.blocks)(s.clearedRow >= lvlUpRow),
            currBlock: currMoveDown(s.currBlock)(s.blocks)
        })(t.value)
    
    // add white blocks to increase diff
    const addDummyRow = (rng: number) => (blocks: Array<Body>) => (levelUp: boolean): Array<Body> =>
        levelUp ?
        totalCols.reduce((acc: Array<Body>, col: number) => 
            Math.floor(Math.abs(rng) * (10)) != col ?        
                // add dummy block to all except a random col                       
                acc.concat([createBlock(col)(19)('fill: grey')(0)]) : acc,    
                blocks.map((e: Body) =>     // move all current block go up 1
                    ({...e, axis: new Axis(e.axis.x, e.axis.y - Block.HEIGHT)})
                )
        ) : blocks

    // chk currBlock touching any existing blocks on the left / right / bottom
    const collidedLeft = (currBlock: Array<Body>) => (blocks: Array<Body>): boolean => 
        (currBlock.some((e) => blocks.some((another) => 
            e.axis.y === another.axis.y && e.axis.x === another.axis.x + Block.WIDTH
        )))
        
    const collidedRight = (currBlock: Array<Body>) => (blocks: Array<Body>): boolean => 
        (currBlock.some((e) => blocks.some((another) => 
            e.axis.y === another.axis.y && e.axis.x + Block.WIDTH === another.axis.x
        )))
        
    const collidedBottom = (currBlock: Array<Body>) => (blocks: Array<Body>): boolean => 
        (currBlock.some((e) => blocks.some((another) => 
            e.axis.x === another.axis.x && e.axis.y + Block.HEIGHT === another.axis.y
        ))) 
        
    
    // currBlock Moves
    const straightDown = (currBlock: Array<Body>) => (blocks: Array<Body>): Array<Body> => 
        !collidedBottom(currBlock)(blocks) && 
            currBlock.every((e) => e.axis.y < (Constants.GRID_HEIGHT - 1) * Block.HEIGHT) ?
        straightDown(currMoveDown(currBlock)(blocks))(blocks) : currBlock

    const currMoveDown = (currBlock: Array<Body>) => (blocks: Array<Body>): Array<Body> =>
        currBlock.map((b: Body) => !collidedBottom(currBlock)(blocks) && 
            currBlock.every((e: Body) => e.axis.y < (Constants.GRID_HEIGHT - 1) * Block.HEIGHT) ?
            {...b, axis: b.axis.descend()} : b )

    const currMoveLeft = (currBlock: Array<Body>) => (blocks: Array<Body>): Array<Body> =>
        currBlock.map((b: Body) => !collidedLeft(currBlock)(blocks) &&
            currBlock.every((e: Body) => e.axis.x > 0 ) ?
            {...b, axis: b.axis.left()} : b )   
    
    const currMoveRight = (currBlock: Array<Body>) => (blocks: Array<Body>): Array<Body> =>
        currBlock.map((b: Body) => !collidedRight(currBlock)(blocks) &&
            currBlock.every((e: Body) => e.axis.x < (Constants.GRID_WIDTH - 1) * Block.WIDTH) ?
            {...b, axis: b.axis.right()} : b )   
                    
    // if currBlock out of bound while rotation, pull in back to the frame 
    const overlapToDir = 
        (currBlock: Array<Body>) => 
        (blocks: Array<Body>) => 
        (currMoveDir: (a: Array<Body>) => (b: Array<Body>) => Array<Body>)
        : Array<Body> =>
            currBlock.some((e) => (e.axis.x < 0 || e.axis.x >= Constants.GRID_WIDTH * Block.WIDTH)) ?
                overlapToDir(currMoveDir(currBlock)(blocks))(blocks)(currMoveDir) : currBlock

    /**
     * state transducer
     * @param s input State
     * @param action type of action to apply to the State
     * @returns a new State 
     */
    const reduceState = (s: State, action: RotateCW | RotateCCW | Restart | Left | Right | Down | Tick | Drop) =>
        action instanceof RotateCW ? {
            ...s, currBlock:
            // if rotated will out of bound (right frame)
            doRotateCW(s.currBlock).some((e) => e.axis.x >= Constants.GRID_WIDTH * Block.WIDTH) ? 
                overlapToDir(doRotateCW(s.currBlock))(s.blocks)(currMoveLeft) : 
            // if rotated will out of bound (left frame)
            doRotateCW(s.currBlock).some((e) => e.axis.x < 0) ? 
                overlapToDir(doRotateCW(s.currBlock))(s.blocks)(currMoveRight) : 
            // if rotated will overlap (not enough space to rotate)
            !overlapped(doRotateCW(s.currBlock))(s.blocks) ?
                doRotateCW(s.currBlock) :
                s.currBlock
        }
        : action instanceof RotateCCW ? {
            ...s, currBlock:
            // if rotated will out of bound (right frame)
            doRotateCCW(s.currBlock).some((e) => e.axis.x >= Constants.GRID_WIDTH * Block.WIDTH) ? 
                overlapToDir(doRotateCCW(s.currBlock))(s.blocks)(currMoveLeft) : 
            // if rotated will out of bound (left frame)
            doRotateCCW(s.currBlock).some((e) => e.axis.x < 0) ? 
                overlapToDir(doRotateCCW(s.currBlock))(s.blocks)(currMoveRight) :
            // if rotated will overlap (not enough space to rotate)
            !overlapped(doRotateCCW(s.currBlock))(s.blocks) ?
                doRotateCCW(s.currBlock) :
                s.currBlock
        }
        : action instanceof Left ? {
            ...s, currBlock: currMoveLeft(s.currBlock)(s.blocks)
        }
        : action instanceof Right ? {
            ...s, currBlock: currMoveRight(s.currBlock)(s.blocks)  
        }
        : action instanceof Down ? handleCollisions({
            ...s, currBlock: currMoveDown(s.currBlock)(s.blocks)
        })(action.value)
        : action instanceof Drop ? handleCollisions({
            ...s, currBlock: straightDown(s.currBlock)(s.blocks)
        })(action.value)
        : action instanceof Restart ? initialState(s.highScore)
        : tick(s)(action);