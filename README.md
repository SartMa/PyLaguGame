# In Search of a Lost Artifact

## Introduction
Welcome to "In Search of a Lost Artifact," an exciting platformer game that combines combat, exploration, and a captivating storyline. As a young knight, your mission is to retrieve a magical helmet now possessed by evil spirits. Embark on a journey through the ruins of your old capital, facing enemies, collecting keys, and ultimately confronting the golem to reclaim the powerful artifact.

## How to Run
1. Ensure you have Python3 and pygame installed.
2. Download the game zip file from this GitHub repository.
3. Extract the files at your desired location.
4. In Linux, open a terminal and navigate to the code section of project folder(using `cd download_location/PyLagu/code`).
5. In Windows, navigate to code folder in extracted file (location should look like `download_location/PyLagu/code`) and open command prompt(make sure to run it as administrator).
6. Run the game using the command: `python3 main.py`.

## Gameplay Instructions
- Move Right/Left: Arrow keys
- Jump: Arrow key (Up)
- Attack: Space
- Grab Ladder: D
- Climb Up/Down Ladder: W/S
- Collect Key: K

## Game Overview
At its core, our game is a platformer with elements of combat and exploration. The theme revolves around the quest to recover a magical helmet, now inhabited by evil spirits. The path to the golem's lair is blocked by enemies, and you must find 7 keys to reach the lair, defeat the golem, and retrieve the helmet.

## Development Journey
We started with no prior knowledge of pygame but were determined to create a platformer. After learning the basics from a tutorial, we implemented additional features using our own logic. These include a combat system, pushable blocks, ladders, and chests with collectible keys.

### Combat System
The combat system involves enemies attacking when the player is within their radius. Implementing this required careful management of player and enemy states using booleans. The boss can only be attacked during its idle state.

### Pushable Blocks
Pushable blocks can be stood upon or pushed horizontally by the player. Collision logic determines the player's interaction with the blocks. If a block collides with a wall, it stops moving.

### Ladders
Players can climb up and down ladders, with gravity disabled while grabbing a ladder. The onrope boolean tracks whether the player is on a ladder.

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

## Conclusion
Enjoy your adventurous journey in "In Search of a Lost Artifact"! Thank you for playing and celebrating our 1st anniversary with us. Here's to many more gaming experiences!

**Happy 1st Anniversary! 🎉**
