package edu.monash.fit2099.demo.BugHunt;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;

public class BreakAction extends Action {
    private Breakable breakable;
    private Location breakableLocation;
    private String direction;

    public BreakAction(Breakable breakable, Location breakableLocation, String direction){
        this.breakable = breakable;
        this.breakableLocation = breakableLocation;
        this.direction = direction;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        return breakable.broken(actor, breakableLocation);
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " breaks the " + breakable + " to the " + direction;
    }
}
