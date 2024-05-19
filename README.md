**Hungry Elephant**
-----------------

Welcome to Hungry Elephant! Meet Ariana our elephant, who loves to eat apples. In this game, you must help Ariana eat all the apples that drop from the sky in order for her not to meet game over. Play alone or with friends to see how many apples we can help Ariana eat! Sometimes there are golden pears as well, which are worth 3 apples, what a delicacy! However, you must watch out for bombs that appear at the same time as golden pears. They move at a higher speed than pears and make Ariana lose 3 apples, which may result in her starvation. Don't worry though, if you are not able to obtain a golden pear the game will continue on, unlike if you don't obtain an apple. Good luck, and bon appetit!

*Features*
----------

Added features are:
- Golden pears, which increase the score by 3 and have a 1/5 chance of appearing.
- Bombs, that appear only at the same time as golden pears which decrease the score by 3. (You are only able to obtain the benefits of golden pears if you are able to dodge the bombs.)
- Special sound when golden pear is obtained, a "yuh" sound.
- Special sound when bomb is obtained a "so sorry girl" sound.
- Score does not go negative, and only ends when an apple is not obtained.
- Increased speed, to make it easier to obtain apples.

*File with array implemented*
-----------------------------

[Uploadingimport greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.Random;

/**
 * The Elephant, our hero.
 * 
 * @author Michelle
 * @version 2024
 */
public class Elephant extends Actor
{
    GreenfootSound elephantSound = new GreenfootSound("elephantcub.mp3");
    GreenfootSound arianaSound = new GreenfootSound("yuh.mp3");
    GreenfootSound sorrySound = new GreenfootSound("sorry.mp3");
    GreenfootImage[] idleRight = new GreenfootImage[8];
    GreenfootImage[] idleLeft = new GreenfootImage[8];
    
    //Direction the elephant is facing
    String facing = "right";
    SimpleTimer animationTimer = new SimpleTimer();
    
    /**
     * Constructor - The code that gets run one time when object is created
     */
    public Elephant()
    {
        for(int i = 0; i<idleRight.length; i++)
        {
            idleRight[i] = new GreenfootImage("images/elephant_idle/idle" + i + ".png");
            idleRight[i].scale(100, 100);
        }
        
        for(int i=0; i<idleLeft.length; i++)
        {
            idleLeft[i] = new GreenfootImage("images/elephant_idle/idle" + i + ".png");
            idleLeft[i].mirrorHorizontally();
            idleLeft[i].scale(100, 100);
        }
        
        animationTimer.mark();
        
        setImage(idleRight[0]);
    }
    
    /**
     * Animate the elephant
     */
    int imageIndex = 0;
    public void animateElephant()
    {
        if(animationTimer.millisElapsed()<150)
        {
            return;
        }
        animationTimer.mark();
        
        if(facing.equals("right"))
        {
            setImage(idleRight[imageIndex]);
            imageIndex = (imageIndex + 1) % idleRight.length;
        }
        else
        {
            setImage(idleLeft[imageIndex]);
            imageIndex = (imageIndex + 1) % idleLeft.length;
        }
    }
    
    public void act()
    {
        if(Greenfoot.isKeyDown("left"))
        {
            move(-5);
            facing = "left";
        }
        else if(Greenfoot.isKeyDown("right"))
        {
            move(5);
            facing = "right";
        }

        //Remove apple if elephant eats it
        eat();
        eatPear();
        getBomb();
        
        //Animate the elephant
        animateElephant();
    }
    
    /**
     * Eat the apple and spawn new apple if an apple is eaten
     */
    public void eat()
    {
        if(isTouching(Apple.class))
        {
            removeTouching(Apple.class);
            MyWorld world = (MyWorld) getWorld();
            
            Random rand = new Random();
            if(rand.nextInt(3)==2)
            {
                world.createPear();
            }
            else
            {
                world.createApple();
            }
            world.increaseScore();
            elephantSound.play();
        }
    }
    
    public void eatPear()
    {
        if(isTouching(goldenpear.class))
        {
            removeTouching(goldenpear.class);
            MyWorld world = (MyWorld) getWorld();
            Random random = new Random();
            if(random.nextInt(5)==2)
            {
                world.createPear();
            }
            else
            {
                world.createApple();
            }
            world.increaseScore();
            world.increaseScore();
            world.increaseScore();
            arianaSound.play();
        }
    }
    
    public void getBomb()
    {
        if(isTouching(bomb.class))
        {
            removeTouching(bomb.class);
            MyWorld world = (MyWorld) getWorld();
            world.decreaseScore();
            world.decreaseScore();
            world.decreaseScore();
            sorrySound.play();
        }
    }
}
 Elephant.java…]()

