package game.items;

import game.player.Player;

public interface Tradeable {
    boolean calculateTrade(Player player);
    int getPrice();
}
