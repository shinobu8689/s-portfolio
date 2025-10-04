package edu.monash.fit2099.demo.BugHunt;

import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;

public class Bush extends Ground {
    private int counter;

    public Bush(){
        super('*');
        counter = 0;
    }

    @Override
    public void tick(Location location){
        counter +=1;
        if(counter % 5 == 0 && !location.containsAnActor()){
            location.addActor(new Bug());
        }
    }
}
