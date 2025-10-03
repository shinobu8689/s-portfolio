export { Axis, RNG, randValueRange }
import { Block } from "./types";

abstract class RNG {
    // LCG using GCC's constants
    private static m = 0x80000000; // 2**31
    private static a = 1103515245;
    private static c = 12345;

    /**
     * Call `hash` repeatedly to generate the sequence of hashes.
     * @param seed 
     * @returns a hash of the seed
     */
    public static hash = (seed: number) => (RNG.a * seed + RNG.c) % RNG.m;

    /**
     * Takes hash value and scales it to the range [-1, 1]
     */
    public static scale = (hash: number) => (2 * hash) / (RNG.m - 1) - 1;
}

class Axis {
    constructor(public readonly x: number = 0, public readonly y: number = 0) { }
    // move the block to each direction
    public descend = () => new Axis( this.x, this.y + 1 * Block.HEIGHT )
    public left = () => new Axis( this.x - 1 * Block.WIDTH, this.y )
    public right = () => new Axis( this.x + 1 * Block.WIDTH, this.y )
    public ascend = () => new Axis( this.x, this.y - 1 * Block.HEIGHT )
}

// return a random number between min - max with given random RNG value
const randValueRange = (random: number) => (min: number) => (max: number): number => 
        Math.floor(Math.abs(random) * (max) + min)
