package game.world.tree;

import edu.monash.fit2099.engine.positions.Location;
import game.items.Coin;
import game.Utils;

public class Sapling extends Tree {

    public Sapling() {
        super('t');
        registerInstance();
    }
   
    /**
     * Lets Sapling object experience the flow of time.
     * @param location location of tree
     */
    
   public void tick(Location location) {
       // Calls the tree class tick method, which will check if the player is invulnerable, 
       // and also kill the tree if need be

       // Increase age of tree each tick
       this.age = this.age + 1;
       // If the sapling is over 10 ticks old, it will grow to a mature tree
       if (this.age >= 10) {
           location.setGround(new Mature());
       }
       // Creates a coin object on its location with a 10% chance every tick
       if (Utils.randomChance(10) && location.getItems().isEmpty()) {
            location.addItem(new Coin("Coin", '$', true, 20));
       }
       super.tick(location);
   } 
}
