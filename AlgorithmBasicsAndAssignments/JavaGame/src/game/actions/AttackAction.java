package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.weapons.Weapon;
import game.*;
import game.items.SuperMushroom;
import game.player.Player;
import game.world.Fire;
import game.enemies.Enemy;
import game.enemies.Koopa;

/**
 * Special Action for attacking other Actors.
 *
 * @author Yin Lam Lo
 * @version 2.0
 */
public class AttackAction extends Action {

	/**
	 * The Actor that is to be attacked
	 */
	protected BaseActor target;

	/**
	 * The direction of incoming attack.
	 */
	protected String direction;

	/**
	 *  the chance that the shield effect could block a hit
	 */
	protected final Integer shieldBlockChance = 90;

	/**
	 *  the chance that get dizzy when player get hit
	 */
	protected final Integer getDizzyChance = 30;

	/**
	 * Constructor for player's attack
	 * 
	 * @param target the Actor to attack
	 */
	public AttackAction(Actor target, String direction) {
		this.target = (BaseActor) target;
		this.direction = direction;
	}

	/**
	 * Constructor for enemies' attack
	 *
	 * @param target the Actor to attack
	 */
	public AttackAction(Actor target) {
		this.target = (BaseActor) target;
		this.direction = null;
	}

	/**
	 * @see Action#execute(Actor, GameMap)
	 * @param actor The actor performing the action.
	 * @param map The map the actor is on.
	 * @return a suitable description to display in the UI
	 */
	@Override
	public String execute(Actor actor, GameMap map) {

		BaseActor baseActor = (BaseActor) actor;
		Weapon weapon = baseActor.getWeapon();

		if (Utils.randomChance(100 - weapon.chanceToHit())) { return baseActor + " misses " + target + "."; }

		Integer damage = getDamage(weapon, baseActor);

		String result = baseActor + " " + weapon.verb() + " " + target + " for " + damage + " damage.";

		//if player get hit with positive damages
		if (target instanceof Player && damage > 0) {
			target.removeCapability(Status.TALL);
		}

		if (!target.isConscious()) {
			dropItems(actor, map);
			result += shouldActorDie(actor, map);
		}

		if(target instanceof Player){
			((Player) target).getLives().checksLives(target, map);
		}

		// if the weapon used has the flamethrower ability, set the target ground to fire
		if (actor.hasCapability(WeaponEffect.FLAMETHROWER)) {
			map.locationOf(target).setGround(new Fire());;
		}

		return result;
	}

	/**
	 * determine the damage and effect and attack while checking on both character's capabilities.
	 * @param weapon
	 * @return the damage deal depends on actor capabilities
	 */
	public Integer getDamage(Weapon weapon, BaseActor baseActor){
		// if player is invincible, take no damage
		// if player is blessed, take less damage
		// if player has shield effect, shieldBlockChance% chance takes no damage
		int damage;
		if (target.hasCapability(Status.INVINCIBLE)) {
			damage = 0;
		} else if (target.hasCapability(Status.SHIELD) && Utils.randomChance(shieldBlockChance) ){
			damage = 0;
			target.removeCapability(Status.SHIELD);
		} else if (target.hasCapability(Status.BLESSED)){
			damage = Math.round(weapon.damage() / 2);
			// getDizzy();
		} else {
			damage = weapon.damage();
			// getDizzy();
		}

		// instant kill target, if the one who is hitting is invincible
		if (baseActor.hasCapability(Status.INVINCIBLE)){
			damage = target.instantKill();
		} else {
			target.hurt(damage);
		}

		return damage;
	}

	/**
	 * Check enemies type to determine it should drop a mushroom, or it should be dead
	 * @param map
	 * @return result
	 */
	public String shouldActorDie(Actor actor, GameMap map){
		// if player is not invincible and koopa has no hp, koopa turn into dormant mode
		if (target instanceof Koopa && !actor.hasCapability(Status.INVINCIBLE)){
			target.addCapability(Status.DORMANT);
			((Enemy) target).becomeDormant();
			return System.lineSeparator() + target + " hides in its shell.";
		} else {
			// if player is invincible, koopa is dead and spawn mushroom
			if (target instanceof Koopa) {
				map.locationOf(target).addItem(new SuperMushroom("Super Mushroom", '^',true));
			}
			if (target instanceof Enemy){
				map.removeActor(target);
			}
			return System.lineSeparator() + target + " is killed.";
		}
	}

	/**
	public void getDizzy(){
		if (Utils.randomChance(getDizzyChance)) {
			target.addCapability(Status.DIZZY);
		}
	} **/

	public void dropItems(Actor actor, GameMap map){
		ActionList dropActions = new ActionList();
		// drop all items
		for (Item item : target.getInventory())
			dropActions.add(item.getDropAction(actor));
		for (Action drop : dropActions)
			drop.execute(target, map);
	}

	/**
	 * Describe the action in a format suitable for displaying in the menu.
	 * @param actor The actor performing the action.
	 * @return a string, e.g. "Player picks up the rock"
	 */
	@Override
	public String menuDescription(Actor actor) {
		return actor + " attacks " + target + " at " + direction;
	}

}
