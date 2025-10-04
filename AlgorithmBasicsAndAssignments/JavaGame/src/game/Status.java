package game;

/**
 * Use this enum class to give `buff` or `debuff`.
 * It is also useful to give a `state` to abilities or actions that can be attached-detached.
 */
public enum Status {
    HOSTILE_TO_ENEMY, // use this status to be considered hostile towards enemy (e.g., to be attacked by enemy)
    TALL, // use this status to tell that current instance has "grown".
    INVINCIBLE, // use this to tell that current instance is invincible
    DORMANT, // use this for koopa shell mode ;
    CAN_TRADE, // Use this to check if actor is player and can buy
    BURNT, // use this when actor gets fire damage
    BLESSED, // use this for miracle water effect
    SHIELD, // use this for miracle water effect
    DIZZY, // use this for player get hit real hard
    BLIND, // enable fog of war
    WARPABLE, // shows the ground is able to be warped to
    PLAYABLE, // shows that these characters are playable
    FLYING, // when the actor is flying and so can traverse any high terrain
    FINAL_BOSS
}