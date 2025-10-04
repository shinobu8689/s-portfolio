package game;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.positions.World;
import game.player.Player;
import game.world.LavaMap;

import java.util.ArrayList;
import java.util.List;

public class WarpMapManager {
    static List<LavaMap> warpableMaps = new ArrayList<>();
    private static World world;
    private static WarpMapManager instance;
    private Location warpLocations;
    private Location oldWarpLocation;
    public static Location newWarpLocation;

    /**
     * Creates an instance of the WarpMapManager class
     *
     * @return instance - the instance of the WarpMapManager
     */
    public static WarpMapManager getInstance(){
        if(instance == null){
            instance = new WarpMapManager();
        }
        return instance;
    }

    /**
     * Creates the world to add the maps
     *
     * @return world new object of the World class
     */
    public static World createWorld(){
        world = new World(new Display());
        return world;
    }

    /**
     * Adds a warp map to the world and adds it to an array that saves all Warp Maps added
     *
     * @param map game map that needs to be added to the array
     */
    public void addWarpMap(GameMap map){
        warpableMaps.add((LavaMap) map);
        this.world.addGameMap(map);
    }

    /**
     * Retrieves the warp map from the warp map array
     *
     * @param mapName String of the name the map was saved in the array as
     * @return map which the user has called for
     */
    public static GameMap getWarpableMap(String mapName) {
        GameMap map = null;
        for(int i = 0; i < warpableMaps.size(); i++){
            if (warpableMaps.get(i).getName() == mapName){
                map = warpableMaps.get(i);
            }
        }
        return map;
    }

    /**
     * Allows the player to warp to a new location
     *
     * @param currentMap the map the player is currently standing on
     * @param newMap the map that is to be warped to
     * @param player the player that is warping
     * @return string that declares the player has warped
     */
    public String newWarpLocation(GameMap currentMap, GameMap newMap, Player player){

        if(!(currentMap instanceof LavaMap)) {
            this.oldWarpLocation = currentMap.locationOf(player);
        }

        this.newWarpLocation = getWarpLocation(newMap);
        if(newWarpLocation.containsAnActor())
        {
            Actor plant =  newMap.getActorAt(newWarpLocation);
            if(!(plant.hasCapability(Status.PLAYABLE))) {
                newMap.removeActor(plant);
            }
        }

        if(currentMap instanceof LavaMap){
            currentMap.moveActor(player,oldWarpLocation);
            return player + " returns to Main Map!";

        } else {
            currentMap.moveActor(player, newWarpLocation);
            return player + " warps to New World: Lava Dome!";
        }
    }

    /**
     * Gets the location of the warp pipes in the map
     *
     * @param map the map that the warp pipes are on
     * @return location of the warp pipes
     */
    public Location getWarpLocation(GameMap map){
        for (int i = 0; i < map.getXRange().max(); i++) {
            for (int j = 0; j < map.getYRange().max(); j++) {
                if (map.at(i,j).getGround().hasCapability(Status.WARPABLE)) {
                    warpLocations = map.at(i,j);
                }
            }
        }
        return warpLocations;
    }
}


