package game;

import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.FancyGroundFactory;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.World;
import edu.monash.fit2099.engine.weapons.Weapon;
import game.enemies.Bowser;
import game.items.Coin;
import game.items.PowerStar;
import game.items.SuperMushroom;
import game.items.Wrench;
import game.npc.PrincessPeach;
import game.npc.Toad;
import game.player.Luigi;
import game.player.Mario;
import game.player.Player;
import game.world.*;
import game.world.fountain.HealthFountain;
import game.world.fountain.MiracleFountain;
import game.world.fountain.PowerFountain;
import game.world.tree.Sprout;

import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

/**
 * Class that handles the Input/Output part of the code
 *
 * @author Nethmini Botheju
 * @version 1.0
 */
public class MainMenu {
    FancyGroundFactory groundFactory = new FancyGroundFactory(new Dirt(), new Wall(), new Floor(), new Sprout(), new Lava(), new HealthFountain(), new PowerFountain(), new MiracleFountain(),new WarpPipe());

    List<String> map = Arrays.asList(
            "..........................................##..........+...................C.....",
            "..C.........+............+..................#...................................",
            "............................................#...................................",
            ".............................................##......................+..........",
            ".....................................C.........#................................",
            "................................................#...............................",
            ".................+................................#.............................",
            "................................................##..............................",
            "................................................##..............................",
            ".........+........................H.....+#____####..C..............+............",
            ".......................................+#_____###++.............................",
            ".......................................+#______###..............................",
            "..................................A.....+#_____###..............................",
            "....C...................+........................##.............+...............",
            "...........................................V.......#............................",
            "...................................C................#...........................",
            "...................+.................................#..........................",
            "......................................................#.................C.......",
            "..........C............................................##.......................");

    List<String> lavaMap = Arrays.asList(
            "..C............LLL.........LLLLLLLLLLL...........LLLLLLLLLLLLLLL......LLL.......",
            "................LLLLLL.........LLL......................................LL......",
            "LLLL..............LLLL.............LLLL...........LLLLL.........................",
            "LLLLL...............LLL...............LLL..............LLLLLLL...........LL#####",
            "LLLLLLL...........LL.....................................................L#.....",
            "................................LLLL............................................",
            ".......................##....#................LLLLLLLLLLLL...............L#.....",
            "......LLLLLL...........#......#...................LLLLL..................LL#####",
            "............LLLL........#....##..LLL..........LLLLL........LLLL.................");

    /**
     * mathod that displays the main menu and selection options for the player.
     *
     * @return player object depending on which player is selected by the user
     */
    public Player displayTitleScreen() {
        System.out.println("|==============================================================================|");
        System.out.println("|..............................................................................|");
        System.out.println("|.......$$$...$...$..$$$...$$$..$$$......$......$....$....$$$...$....$$........|");
        System.out.println("|......$......$...$..$..$..$....$..$.....$$....$$...$.$...$..$..$...$..$.......|");
        System.out.println("|.......$$$...$...$..$$$$..$$$..$$$......$.$..$.$..$$$$$..$$$...$..$....$......|");
        System.out.println("|..........$..$...$..$.....$....$.$......$.$..$.$..$...$..$.$...$...$..$.......|");
        System.out.println("|.......$$$....$$$...$.....$$$..$..$.....$..$$..$..$...$..$..$..$....$$........|");
        System.out.println("|..............................................................................|");
        System.out.println("|............................SELECT MAIN PLAYER:...............................|");
        System.out.println("|........................(1)..............SUPER.MARIO..........................|");
        System.out.println("|........................(2)..............SUPER.LUIGI..........................|");
        System.out.println("|........................(3)...............EXIT.GAME...........................|");
        System.out.println("|..............................................................................|");
        System.out.println("|==============================================================================|");
        Scanner selectedPlayer = new Scanner(System.in);
        System.out.print("Select a player: ");
        Player player;
        int playerInt = Integer.parseInt(selectedPlayer.nextLine());
        int selection;
            selection = playerInt;
        switch (selection) {
            case 1 -> {
                player = new Mario();
                return player;
            }
            case 2 -> {
                player = new Luigi();
                return player;
            }
            case 3 -> {
                System.out.println("You exited the game!");
                System.exit(0);
            }
        }
        return null;
    }

    public Boolean chooseFogOfWarEffect(){
        System.out.println("|==============================================================================|");
        System.out.println("|..............................................................................|");
        System.out.println("|.......$$$...$...$..$$$...$$$..$$$......$......$....$....$$$...$....$$........|");
        System.out.println("|......$......$...$..$..$..$....$..$.....$$....$$...$.$...$..$..$...$..$.......|");
        System.out.println("|.......$$$...$...$..$$$$..$$$..$$$......$.$..$.$..$$$$$..$$$...$..$....$......|");
        System.out.println("|..........$..$...$..$.....$....$.$......$.$..$.$..$...$..$.$...$...$..$.......|");
        System.out.println("|.......$$$....$$$...$.....$$$..$..$.....$..$$..$..$...$..$..$..$....$$........|");
        System.out.println("|..............................................................................|");
        System.out.println("|...........................ADD.FOG.OF.WAR.EFFECT?.............................|");
        System.out.println("|........................(1)......................YES..........................|");
        System.out.println("|........................(2).......................NO..........................|");
        System.out.println("|..............................................................................|");
        System.out.println("|..............................................................................|");
        System.out.println("|==============================================================================|");
        Scanner choice = new Scanner(System.in);
        System.out.print("Add fog of war effects? (Makes the game harder): ");
        int choiceInt = Integer.parseInt(choice.nextLine());
        int selection;
        selection = choiceInt;
        switch (selection) {
            case 1 -> {
                return true;
            }
            case 2 -> {
                return false;
            }
        }
        return null;
    }

    /**
     * The main method that creates the world and starts the game
     *
     * @param player the player that was chosen by the user to iniate the game
     */
    public void startGame(Player player, Boolean fogOfWar) {
        WarpMapManager warpMapManager = new WarpMapManager();
        World world = WarpMapManager.createWorld();
        GameMap gameMap = new GameMap(groundFactory, map);
        LavaMap lavaGameMap = new LavaMap("LavaMap", groundFactory, lavaMap);
        world.addGameMap(gameMap);
        warpMapManager.addWarpMap(lavaGameMap);

        player.setSpawnPoint(gameMap.at(42,10));
        if (fogOfWar) { player.addCapability(Status.BLIND); };
        world.addPlayer(player, player.getSpawnPoint());

        Bowser bowser = new Bowser();
        bowser.setBowserSpawnPoint(lavaGameMap.at(74,5));
        lavaGameMap.addActor(bowser, bowser.getBowserSpawnPoint());


        lavaGameMap.at(77, 5).addActor(new PrincessPeach());

        SuperMushroom superMushroom = new SuperMushroom("Super Mushroom", '^', true);
        gameMap.at(44, 10).addItem(superMushroom);
        lavaGameMap.at(10, 1).addItem(superMushroom);
        lavaGameMap.at(27, 2).addItem(superMushroom);

        PowerStar powerStar1 = new PowerStar("Power Star", '*', true, 10, 10);
        gameMap.at(44, 11).addItem(powerStar1);

        Weapon wrench = new Wrench("Wrench", 'w', 50, "wreck", 80);
        gameMap.at(44, 9).addItem((Item) wrench);
        lavaGameMap.at(77, 1).addItem((Item) wrench);

        Item coin = new Coin("Coin", '$', true);
        gameMap.at(44, 12).addItem(coin);
        lavaGameMap.at(56, 7).addItem(coin);
        lavaGameMap.at(45, 1).addItem(coin);

        gameMap.at(43, 10).addActor(new Toad());
        
        world.run();

    }


}
