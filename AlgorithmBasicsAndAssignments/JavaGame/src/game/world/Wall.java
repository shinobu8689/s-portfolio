package game.world;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.items.Coin;
import game.player.Player;

public class Wall extends JumpableGround {

	public Wall() {
		super('#');
	}
	
	/**
	 * if player is invincible they could destroy a wall and move to that location, $5 per wall
	 * @param location The location of the Ground
	 */
	@Override
	public void tick(Location location){
		super.tick(location);
		if (location.containsAnActor()){
			if (location.getActor() instanceof Player && location.getActor().hasCapability(Status.INVINCIBLE)){
				location.setGround(new Dirt());
				location.addItem(new Coin("Coin", '$', true, 5));
			}
		}
	}

	
	@Override
	public boolean blocksThrownObjects() {
		return true;
	}
}
