import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
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
            move(-3);
            facing = "left";
        }
        else if(Greenfoot.isKeyDown("right"))
        {
            move(3);
            facing = "right";
        }
        
        //Remove apple if elephant eats it
        eat();
        eatPear();
        
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
            if(random.nextInt(4)==2)
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
