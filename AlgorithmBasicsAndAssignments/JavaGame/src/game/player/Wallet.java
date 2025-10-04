package game.player;

/**
 * Class that creates a wallet for the player to store coins
 *
 * @author Neth Botheju
 * @version 1.0
 * @see game.player.Player
 */
public class Wallet {
    private int value;

    /**
     * constructor to create new instance of the wallet class
     *
     * @param value the amount of money in the wallet
     */
    public Wallet(int value){
        this.value = value;
    }

    /**
     * getter for the amount of money in the wallet
     *
     * @return the amount of money currently in the wallet
     */
    public int getWalletAmount(){
        return this.value;
    }

    /**
     * adds coin values into the player's wallet
     *
     * @param coinValue the value of the coin picked up
     * @return the total amount of money in the wallet after the coin value added
     */
    protected int addCoin(Integer coinValue) {
        return this.value += coinValue;
    }

    /**
     * subtracts the amount from wallet during a trade
     *
     * @param amount the price of the iteam being traded
     * @return the total amount of money in the wallet after trade deducated
     */
    protected int subtract(int amount) {
        return this.value -= amount;
    }
}
