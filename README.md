# Aetherial Pursuit

## Introduction
Welcome to "Aetherial Pursuit," an exciting platformer game that combines combat, exploration, and a captivating storyline. As a young knight, your mission is to retrieve a magical helmet now possessed by evil spirits. Embark on a journey through the ruins of your old capital, facing enemies, collecting keys, and ultimately confronting the golem to reclaim the powerful artifact.

## How to Run
1. Ensure you have Python3 and pygame installed.
2. Download the game zip file from this GitHub repository.
3. Extract the files at your desired location.
4. In Linux, open a terminal and navigate to the code section of project folder(using `cd download_location/PyLagu/code`).
5. It is strongly recommended to run it in Linux, as there are some bugs when the program is being run in Windows.
6. Run the game using the command: `python3 main.py`.

## Gameplay Instructions
- Move Right/Left: Arrow keys
- Space: Attack the enemy
- Jump: Arrow key (Up)
- Attack: Space
- Grab Ladder: Hold D
- Climb Up/Down Ladder: W/S
- Collect Key: K

## Game Overview
At its core, our game is a platformer with elements of combat and exploration. The theme revolves around the quest to recover a magical helmet which was stolen from your vault, now under the possession of an evil golem. The path to the golem's lair is blocked by enemies, and you must find 7 keys to reach the lair, defeat the golem, and retrieve the helmet.

## Development Journey
We started with no prior knowledge of pygame but were determined to create a platformer. After learning the basics from a tutorial, we implemented all additional features using our own logic. These include a combat system, pushable blocks, ladders, and chests with collectible keys.

### Combat System
The combat system involves enemies attacking when the player is within their radius. Implementing this required careful management of player and enemy states using booleans. Enemies can only be attacked during thier idle state, which they enter after they have finished attacking you.

### Pushable Blocks
The pushable blocks are initially in their enabled state. If the player collides with them on the y axis, the player can stand on them. If he collides with them on the x axis, he can push the block. This we did by simply setting the left of the rect to the right of the player when he is contact with the blcok(and vice-versa for the reverse direction). If the block collides with a wall, it stops moving and its enable state becomes zero, since it cannot now move. We no longer check for x collisions for this block. We also no longer apply gravity to this  block. This allowed us to easily implement blocks that are initially static but fall after the playeer stands on them, simply by changing their initial enable state. Pushable/falling blocks are red in colour.

### Ladders
The ladders can be climbed up/down on. When the player is grabbing a ladder we don’t apply gravity and only move the rect of the player up or down based on the input. We track if he is grabbing a ladder or not using the onrope boolean (we’ve called it a rope in the code but changed the sprite to a ladder in the end).

## Assets and Credits
- Most assets sourced from [itch.io](https://itch.io/).
- Background tileset obtained from [opengameart.org](https://opengameart.org/).
- Level map created using Tiled.

## Classes
- **Player Class:** Manages player actions and interactions.
- **Enemy Class:** Parent class for three enemy types with unique attributes.
- **Tile Classes:** Includes static and animated tiles for level design.
- **Healthbar Class:** Manages health bars for players and enemies.
- **Level Class:** Represents the game level; a new instance is created upon player loss, effectively resetting the level.

