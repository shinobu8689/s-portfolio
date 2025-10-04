package game.world.tree;

import edu.monash.fit2099.engine.positions.Location;
import game.Utils;
import game.enemies.Koopa;
import game.enemies.FlyingKoopa;

import java.util.*;
import edu.monash.fit2099.engine.positions.Exit;
import game.world.Dirt;

public class Mature extends Tree {

    public Mature() {
        super('T');
        registerInstance();
    }

    /**
     * Lets Mature trees experience the flow of time
     * @param location location of tree
     */
    public void tick(Location location) {
        this.age = this.age + 1;
        // Every five ticks after it grows to mature, will attempt to grow a sprout next to it
        if (this.age > 0 && this.age % 5 == 0) {
            growNewTree(location);
        }
        // Sets the tree to be killed with a 20% chance every tick
        if (Utils.randomChance(20)) {
            this.dead = true;
        }
        // Spawns either a Koopa or Flying Koopa on the tree with a 15% chance every tick
        if (Utils.randomChance(15) && !location.containsAnActor()) {
            if (Utils.randomChance(50)) {
                location.addActor(new Koopa());
            } else {
                location.addActor(new FlyingKoopa());
            }
        }
        killTree(location);
        super.tick(location);
    }
    /**
     * Grows a new sprout adjacent to the tree at @param location if there is fertile ground (dirt)
     * @param location location of original tree
     */
    private void growNewTree(Location location) {
        // Gets the locations adjacent to the original tree
        List<Exit> exits = location.getExits();
        List<Location> locs = new ArrayList<>();
        // Checks each adjacent location to determine if it is fertile
        // If it is, the location is added to the list of locs 
        for (Exit temp : exits) {
            Location tempDest = temp.getDestination();
            if (tempDest.getGround() instanceof Dirt) {
                locs.add(tempDest);
            }

        }
        // Randomly picks a location from locs and grows the new sprout there. 
            locs.get(Utils.randomPick(locs.size())).setGround(new Sprout());
    }
}
