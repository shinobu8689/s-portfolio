package game.world;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.GroundFactory;

import java.io.IOException;
import java.util.List;

/**
 * New map with lava
 *
 * @author Neth Botheju
 * @version 1.0
 */
public class LavaMap extends GameMap implements WarpableMaps {
    private final String name;

    /**
     * Constructor for creating the map.
     * Uses parameters from GameMap superclass
     */
    public LavaMap(String mapName, GroundFactory groundFactory, char groundChar, int width, int height) {
        super(groundFactory, groundChar, width, height);
        this.name = mapName;
    }

    /**
     * Constructor for creating the map.
     * Uses parameters from GameMap superclass
     */
    public LavaMap(String mapName, GroundFactory groundFactory, List<String> lines) {
        super(groundFactory, lines);
        this.name = mapName;
    }

    /**
     * Constructor for creating the map.
     * Uses parameters from GameMap superclass
     */
    public LavaMap(String mapName, GroundFactory groundFactory, String mapFile) throws IOException {
        super(groundFactory, mapFile);
        this.name = mapName;
    }

    /**
     * getter for the name of the map
     * @return string of the name
     */
    public String getName() {
        return name;
    }

}
