package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Location;
import game.actions.ConsumeItemAction;
import game.player.Player;
import game.water.HealthWater;
import game.water.PowerWater;
import game.water.StandardWater;

import java.util.Collections;
import java.util.List;
import java.util.Stack;

/**
 * a magical bottle that could store different water with power ups
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class Bottle extends Item implements Consumable {

    /**
     * the content(water) of the bottle
     */
    private final Stack<StandardWater> content = new Stack<>();
    /**
     * limit the action to drink from this bottle only (only one bottle allowed)
     */
    private ConsumeItemAction action = new ConsumeItemAction(this);

    /***
     * Constructor.
     * @param name the name of this Item
     * @param displayChar the character to use to represent this item if it is on the ground
     * @param portable true if and only if the Item can be picked up
     */
    public Bottle(String name, char displayChar, boolean portable) {
        super(name, displayChar, portable);
    }

    public void addWater(StandardWater water){
            content.push(water);
    }

    public StandardWater drinkWater(){
            return content.pop();
    }

    /**
     * Inform a carried Item of the passage of time.
     *
     * This method is called once per turn, if the Item is being carried.
     * @param currentLocation The location of the actor carrying this Item.
     * @param actor The actor carrying this Item.
     */
    public void tick(Location currentLocation, Actor actor) {
        // only can drink when there is water inside
        if (content.size() > 0) {
            if ( !(getAllowableActions().contains(action)) ){
                this.addAction(action);
            }
        } else {
            this.removeAction(action);
        }
    }

    public List getContent(){
        return Collections.unmodifiableList(content);
    }

    @Override
    public String toString(){
        if (content.size() > 0) {
            return super.toString() + " " + getContent();
        } else {
            return super.toString() + " [Empty]";
        }

    }

    /**
     * determine which type of water the player drink and give the correct effect
     * @param player
     */
    public void consumeBy(Player player){
        StandardWater water = player.getBottle().drinkWater();
        if (water instanceof HealthWater){
            player.drinkHealthWater();
        } else if (water instanceof PowerWater) {
            player.drinkPowerWater();
        } else {
            player.addCapability(water.getStatus());
        }
    }

}
