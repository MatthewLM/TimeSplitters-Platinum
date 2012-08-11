TimeSplitters-Platinum
======================

Code for an incomplete TimeSplitters fan game. Includes a 3D Monkey Curling and Anaconda minigame, a mapmaker and a basic game engine.

The game is written primarily in Python but contains C++ extensions and a Objective-C version of some of the code. Many of the images are placeholders. For isntance the guns are just rectangles with numbers on them.

It is perhaps best if the game was reqritten in another programming language more suitable for games such as C.

**Permission has been granted by Crytek for the use of TimeSplitters trademarks and copyright providing the game remains non-commercial. Do not make any commercial adaptations without removing all TimeSplitters references first.**

See each file for respective software licenses.

Files and Directories
=====================

* __./Cocoa Scalelib/Scalelib Cocoa Framework :__ Objective-C code using Cocoa for the general GUI code. Can be linked to python with PyObjC.
* __./docs/Anaconda A2 Computing Project Document.doc :__ Some explaination of the code from a write-up for a A2 computing piece of coursework. The Anaconda minigame was used as an A2 Computing project. This is not the final document but contains information nonetheless.
* __./Python/C++ Extensions :__ Contains C++ code linked in with the python code via dynamic libraries to extend the python code with faster equivilents.
* __./Python/characters :__ Contains numbered folders for character data.
* __./Python/fonts :__ Fonts used by the game.
* __./Python/images/curling_textures :__ Textures used in the 3D Monkey Curling mini-game.
* __./Python/images/items :__ Images for items in levels.
* __./Python/images/mapmaker_images :__ Images used in the mapmaker. Only a magnifying glass.
* __./Python/images/menu_images :__ A monkey and Harry Tipper used in the menu.
* __./Python/images/misc :__ Other images.
* __./Python/levels :__ Empty directory where level data should go.
* __./Python/music/anaconda.ogg :__ Music for the Anaconda minigame.
* __./Python/music/menu.ogg :__ Music for the menu.
* __./Python/music/game :__ Music for playing the game.
* __./Python/sounds :__ Various sound effects
* __./Python/weapons :__ Weapon images and sound effects.
* __./Python/main.py :__ The main game code. Very large python file. Would be best broken down into seperate files. Even better if converted to a more suitable language.
* __./Python/menulib.py :__ Python classes for easily making menus. This could easilly be seperated from the project and be used in many projects.
* __./Python/scalelib.py :__ Code for a graphics interface with a scalable window.
* __./Python/textrect.py :__ Code for rendering text with pygame.
* __./theme_music_versions/ :__ Various versions of the TimeSplitters Platinum theme derived from the TimeSplitters Future Perfect theme.