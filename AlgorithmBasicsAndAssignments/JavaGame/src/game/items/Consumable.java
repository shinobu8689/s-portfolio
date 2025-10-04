package game.items;

import game.player.Player;

/**
 * apply to items that could be eaten
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public interface Consumable {
    /**
     * process the effect after the player consumed/used the item
     * @param player
     */
    void consumeBy(Player player);
}
