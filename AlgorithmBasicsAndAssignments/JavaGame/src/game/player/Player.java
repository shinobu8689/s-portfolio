package game.player;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.displays.Menu;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.*;
import game.actions.DizzyAction;
import game.actions.QuitGameAction;
import game.actions.ReplayAction;
import game.actions.ResetAction;
import game.items.Bottle;
import game.world.Lava;

import java.util.ArrayList;
import java.util.List;

import static java.lang.Math.abs;

/**
 * Class representing the Player.
 */
public abstract class Player extends BaseActor implements Resettable {

	private final Menu menu = new Menu();

	private Wallet wallet;
	private Bottle bottle;

	private Boolean resetStatus;
	private Integer burntCounter;
	private Integer dizzyCounter;
	private Integer invincibleCounter;
	private Integer blessedCounter;
	public Lives lives;
	private Location spawnPoint;
	private int hitpoints;

	/**
	 * Constructor.
	 *
	 * @param name        Name to call the player in the UI
	 * @param displayChar Character to represent the player in the UI
	 * @param hitPoints   Player's starting number of hitpoints
	 */
	public Player(String name, char displayChar, int hitPoints, int lives) {
		super(name, displayChar, hitPoints);
		this.hitpoints = hitPoints;
		this.wallet = new Wallet(0);
		this.bottle = null;
		this.resetStatus = false;
		this.addCapability(Status.HOSTILE_TO_ENEMY);
		this.addCapability(Status.CAN_TRADE);
		this.addCapability(Status.PLAYABLE);
		this.lives = new Lives(lives);
		setDefault();
		registerInstance();
	}

	/**
	 * Figure out what to do next.
	 * @see Actor#playTurn(ActionList, Action, GameMap, Display)
	 */
	@Override
	public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {

		// update capability counter
		processDizzy();
		processBlessed();
		processInvincible();
		Boolean onLava = processBurnt(map);

		// Handle multi-turn Actions
		if (lastAction.getNextAction() != null)
			return lastAction.getNextAction();

		// if player is dying or dizzy
		if ( this.hasCapability(Status.DIZZY) ) {
			actions.clear();
			actions.add(new DizzyAction());
		}

		// check has player reset yet
		if (!resetStatus) { actions.add(new ResetAction()); }

		if (lives.checksLives(this, map)) {
			actions.clear();
			actions.add(new ReplayAction());
			actions.add(new QuitGameAction());
		}

		getPlayerStatus(display, onLava);


		// return/print the console menu

	return menu.showMenu(this, actions, display);
	}

	public Location getSpawnPoint() {
		return spawnPoint;
	}

	public void setSpawnPoint(Location spawnPoint) {
		this.spawnPoint = spawnPoint;
	}

	/**
	 * update Burnt status counter
	 */
	public Boolean processBurnt(GameMap map){
		// Handle lava and Burnt status
		if (!this.hasCapability(Status.INVINCIBLE) && this.isConscious()){
			if (map.locationOf(this).getGround() instanceof Lava) {
				return true;
			} else {
				// burnt will only hurt if player is not on lava, since player already get hurt on lava
				if (burntCounter > 0) {
					this.hurt(burntCounter);
					burntCounter -= 1;
					if (burntCounter == 0) {
						this.removeCapability(Status.BURNT);
					}
				}
			}

		}
		return false;
	}

	/**
	 * update Dizzy status counter
	 */
	public void processDizzy() {
		if (this.hasCapability(Status.DIZZY)){
			this.dizzyCounter += 1;
		}
		if (this.dizzyCounter >= 5) {
			this.removeCapability(Status.DIZZY);
		}
	}

	/**
	 * update Invincible status counter
	 */
	public void processInvincible() {
		// Handle INVINCIBLE effect tick
		if (this.invincibleCounter > 0) {
			this.invincibleCounter -= 1;
		} else if (this.invincibleCounter <= 0) {
			this.removeCapability(Status.INVINCIBLE);
		}
	}

	/**
	 * update Blessed status counter
	 */
	public void processBlessed() {
		if (this.hasCapability(Status.BLESSED)) {
			this.blessedCounter += 1;
		}

		if (this.blessedCounter >= 5) {
			this.removeCapability(Status.BLESSED);
			this.blessedCounter = 0;
		}
	}

	public Lives getLives() {
		return lives;
	}

	public int getHitpoints(){
		return hitpoints;
	}

	@Override
	public char getDisplayChar(){
		return this.hasCapability(Status.TALL) ? Character.toUpperCase(super.getDisplayChar()): super.getDisplayChar();
	}


	/**
	 * adds to coin picked up by player into wallet
	 *
	 * @param value the value of the coin picked up
	 */
	public void pickUpCoins(Integer value){ wallet.addCoin(value); }

	/**
	 * gets the amount of money currently in player wallet
	 *
	 * @return the wallet amount integer
	 */
	public int getWallet(){
		return wallet.getWalletAmount();
	}

	/**
	 * minuses the trade amount from player wallet
	 *
	 * @param amount the amount being deducted
	 *
	 */
	public void subTradeWallet(int amount){
		wallet.subtract(amount);
	}


	/**
	 * print player status
	 * @param display
	 */
	public void getPlayerStatus(Display display, Boolean onLava){
		display.println(this + "(" + getDisplayChar() + ")" + " : HP" + printHp() + " | Lives: " + lives.getLivesStr() + " | Wallet: $" + getWallet() + " | Weapon: " + getWeapon() + " [" + getWeapon().damage() + " Damage]");
		display.println("Inventory: " + getFormattedInventory());
		if (hasBottle()) { display.println("Bottle   : " + getBottle().getContent()); }
		if (capabilitiesList().size() > 2) {
			display.println("Capabilities:");
			if (this.hasCapability(Status.SHIELD)){
				display.println(this + " is well prepared for a hit!");
			}
			if (this.hasCapability(Status.INVINCIBLE)) {
				display.println(this + " is INVINCIBLE!" + " - Remaining " + invincibleCounter + " turns");
			}
			if (this.hasCapability(Status.BURNT)) {
				display.println(this + " has burnt!" + " - Remaining " + burntCounter + " turns");
			}
			if (this.hasCapability(Status.BLESSED)) {
				display.println(this + " is blessed!" + " - Remaining " + (5 - blessedCounter + 1) + " turns");
			}
			if (this.hasCapability(Status.DIZZY)) {
				display.println(this + " is dizzy!");
			}
			if (this.hasCapability(Status.BLIND)) {
				display.println(this + " has limited vision!");
			}
		}
		if (onLava) { display.println(this + " has been damaged by lava"); }
		display.println("================================================");
	}

	/**
	 * Get a copy of this Actor's inventory list without Bottle for better display.
	 * @return An unmodifiable wrapper of the inventory.
	 */
	public List<Item> getFormattedInventory() {
		List<Item> formattedInv = new ArrayList<>();
		for (Item item : super.getInventory()) {
			if (!(item instanceof Bottle)) {
				formattedInv.add(item);
			}
		}
		return formattedInv;
	}


	/**
	 * @return check if player owns a bottle or not
	 */
	public Boolean hasBottle(){
		for (Item item : super.getInventory()){
			if (item instanceof Bottle) {
				this.bottle = (Bottle) item;
				return true;
			}
		}
		return false;
	}

	/**
	 * @return bottle object
	 */
	public Bottle getBottle(){ return bottle; }


	/**
	 * Creates and returns an intrinsic weapon.
	 *
	 * By default, the Actor 'punches' for 5 damage. Override this method to create
	 * an Actor with more interesting descriptions and/or different damage.
	 * Player hits harder with more power water drunk.
	 *
	 * @return a freshly-instantiated IntrinsicWeapon
	 */
	@Override
	protected IntrinsicWeapon getIntrinsicWeapon() {
		return new IntrinsicWeapon(5 + 15 * powerGauge, "punches");
	}


	public void getBurnt(){
		this.addCapability(Status.BURNT);
		this.burntCounter += 1;
	}

	/**
	 * setup the duration of PowerStar effect
	 * @param turn
	 */
	public void setInvincibleCounter(Integer turn){ this.invincibleCounter = turn; }

	/**
	 * setup the counter for different effects
	 */
	public void setDefault(){
		this.invincibleCounter = 0;
		this.powerGauge = 0;
		this.burntCounter = 0;
		this.blessedCounter = 0;
		this.dizzyCounter = 0;
	}

	@Override
	public void resetInstance(Actor actor, GameMap map) {
		this.resetStatus = true;
		this.resetMaxHp(getHitpoints());
		this.removeCapability(Status.TALL);
		this.removeCapability(Status.INVINCIBLE);
		this.removeCapability(Status.BURNT);
		this.removeCapability(Status.BLESSED);
		this.removeCapability(Status.SHIELD);
		this.removeCapability(Status.DIZZY);
		this.setDefault();
	}

	@Override
	public void registerInstance() { Resettable.super.registerInstance(); }

}


