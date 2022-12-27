## TODO:
 - Get camera working
   - Figure out why the camera class is smooth stepping width and height
   - Get camera to follow player
     - Fix pose update system
       - Make poses update after each game update, not after each frame
     - Give drawables an internal tracker so they only update when they need to and not every frame since the pose will still say it is updated
   - Change drawable object to accept a camera to draw using that perspective
   - Change window size to be able to be different from game grid size