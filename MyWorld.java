import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * The World our hero lives in.
 * 
 * @author Michelle 
 * @version April 2024
 */
public class MyWorld extends World
{

    /**
     * Constructor for objects of class MyWorld.
     * 
     */
    public MyWorld()
    {    
        // Create a new world with 600x400 cells with a cell size of 1x1 pixels.
        super(600, 400, 1);
        
        Elephant elephant = new Elephant();
        addObject(elephant, 300, 200);
        
        Apple apple = new Apple();
        addObject(apple, 300, 0);
    }
}
