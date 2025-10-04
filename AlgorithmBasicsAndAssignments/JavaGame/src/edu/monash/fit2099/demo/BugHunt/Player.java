package edu.monash.fit2099.demo.BugHunt;
import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.displays.Menu;
import edu.monash.fit2099.engine.positions.GameMap;

public class Player extends Actor {
    private Menu menu;

    public Player(String name, char displayChar, int hitPoints){
        super(name, displayChar,hitPoints);
        menu = new Menu();
    }

    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        return menu.showMenu(this,actions,display);

    }
}
