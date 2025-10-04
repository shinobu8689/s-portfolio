package game.world.tree;

import edu.monash.fit2099.engine.positions.Location;
import game.Utils;
import game.enemies.Goomba;

public class Sprout extends Tree {
    public Sprout() {
        super('+');
        registerInstance();
    }
    /**
     * Lets sprout objects experience time. 
     * @param location the location of the sprout
     */
    @Override
    public void tick(Location location) {
        // Calls the tree tick method

        // Increase age of tree
        this.age = this.age + 1;
        // If age of tree is 10, it grows into a Sapling
        if (this.age >= 10) {
            location.setGround(new Sapling());
        }
        // Spawns a Goomba on its location with a 10% chance every tick
        if (Utils.randomChance(10) && !(location.containsAnActor())) {
            location.addActor(new Goomba());
        }
        super.tick(location);
    }

}
