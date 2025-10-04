package game;

import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.player.Player;


/**
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public interface Maskable {
    Integer range = 7;
    char fogChar = ' ';

    static void masking(GameMap map, Location location, Maskable maskableObject){
        // search the whole map
        for (int x = 0; x <= map.getXRange().max(); x++) {
            for (int y = 0; y <= map.getYRange().max(); y++) {
                // find the location that has player with Status.BLIND
                if (map.at(x, y).containsAnActor() && map.at(x, y).getActor() instanceof Player && map.at(x, y).getActor().hasCapability(Status.BLIND)) {
                    // Calculate is this inside the range of player radius
                    if (Utils.distance(map.at(x, y), location) > Maskable.range) {
                        maskableObject.setMaskedChar();
                    } else {
                        maskableObject.setDefaultChar();
                    }
                }
            }
        }
    }

    /**
     * show itself when unmasking
     */
    void setDefaultChar();

    /**
     * mask to fogChar when player is too far
     */
    void setMaskedChar();

}
