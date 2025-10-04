package edu.monash.fit2099.demo.BugHunt;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.FancyGroundFactory;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.World;

import java.util.Arrays;
import java.util.List;

public class ApplicationBugHunt {
    public static void main(String[] args) {
        World world = new World(new Display());
        FancyGroundFactory groundFactory = new FancyGroundFactory(new Dirt(), new Bush(), new Crate(), new Chest());
        List<String> map = Arrays.asList(
                "......#................................=....",
                "........................=...................",
                ".........*.............................*....",
                "..............=................=............",
                ".......*............*....................*..",
                ".............................*..............",
                "............................................",
                ".........*........#.........................",
                ".....#..........................*.......#...");
        GameMap gameMap = new GameMap(groundFactory, map);
        world.addGameMap(gameMap);
        Actor player = new Player("Player", 'ඞ', 100);
        world.addPlayer(player, gameMap.at(22, 0));
        world.run();
    }
}