package game;

import game.player.Player;

/**
 * The main class for the Mario World game.
 *
 */
public class Application {

	public static void main(String[] args) {
		MainMenu mainMenu = new MainMenu();
		Player player = mainMenu.displayTitleScreen();
		Boolean fogOfWar = mainMenu.chooseFogOfWarEffect();
		mainMenu.startGame(player,fogOfWar);
	}
}
