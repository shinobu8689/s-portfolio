package game.water;

import game.Status;

/**
 * water base that makes different water
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public abstract class StandardWater {

    private String name;
    protected Status status;

    public StandardWater(String name,Status status){
        this.name = name;
        this.status = status;
    }

    @Override
    public String toString(){
        return name;
    }

    public Status getStatus(){
        return status;
    }

}
