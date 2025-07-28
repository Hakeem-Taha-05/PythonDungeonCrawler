# 🎮 ASCII Action Game

A terminal-based action game built in Python featuring player movement, enemy AI with pathfinding, projectile combat, and ASCII art graphics.

## 🚀 Features

- **👤 Player Character**: Move around the map and shoot projectiles
- **🤖 Intelligent Enemies**: AI-controlled enemies with BFS pathfinding algorithm  
- **💥 Combat System**: Shoot bullets in four directions with limited ammo
- **🗺️ Level Loading**: Load custom levels from text files
- **🎯 Range Detection**: Enemies can detect and chase the player within range
- **💖 Health System**: Take damage from enemy collisions
- **🏆 Win/Lose Conditions**: Eliminate all enemies to win, avoid dying

## 🛠️ Technologies Used

- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.x**
- 🧮 **Math Module**: For distance calculations and positioning
- 📁 **File I/O**: For level loading from text files
- 🔍 **BFS Algorithm**: Breadth-First Search for enemy pathfinding
- 🎨 **ASCII Art**: Text-based graphics and sprites

## 📦 Project Structure

```
game/
├── main.py          # Main game loop and level loading
├── classes.py       # Entity classes (Player, Enemy, Projectile)
├── sprites.py       # ASCII art sprites for characters
├── globals.py       # Global variables and game state
└── levels/          # Level files (user-created)
    ├── level1.txt
    └── level2.txt
```

## 🎮 How to Play

### Controls
- **W/A/S/D**: Move player up/left/down/right
- **F**: Fire projectile in facing direction
- **Enter**: Confirm input

### Game Elements

| Symbol | Description |
|--------|-------------|
| `O/` `\|` `/\` | Player character |
| `X` `/\|\` `/\` | Enemy character |
| `->` `<-` `^\|` `\|V` | Projectiles (bullets) |
| `#` | Wall/obstacle |
| `+` | Wall/obstacle |
| `'` | Enemy range indicator |
| `o` | Enemy entity marker |

### Objective
- Eliminate all enemies on the level to win
- Avoid taking damage and dying (health reaches 0)
- Manage your limited ammunition (5 bullets)

## 🚀 Installation & Setup

1. **Clone or download** the game files
2. **Ensure Python 3.x** is installed on your system
3. **Create level files** (see Level Format section)
4. **Run the game**:
   ```bash
   python main.py
   ```

## 🗺️ Level Format

Create custom levels using text files with this format:

```
MAP [rows] [cols]
########
#P    ^#
#      #
#   V  #
#      #
########
```

### Level Characters
- `P` - Player starting position
- `^` `V` `<` `>` - Enemies (facing direction)
- `#` - Walls
- `+` - Alternative wall type
- ` ` - Empty walkable space

## 🎯 Game Mechanics

### Enemy AI
- **Patrol Behavior**: Enemies move back and forth in their facing direction
- **Player Detection**: When player enters range (10 tiles), enemy switches to chase mode
- **Pathfinding**: Uses BFS algorithm to find optimal path to player
- **Collision**: Enemies deal 1 damage when touching the player

### Combat System
- **Directional Shooting**: Bullets travel in the direction player is facing
- **Limited Ammo**: Start with 5 bullets per level
- **Collision Detection**: Bullets destroy on impact with walls or enemies
- **One-Hit Elimination**: Enemies are destroyed by single bullet hit

### Player Stats Display
The game shows real-time information:
- Current health
- Remaining ammo
- Facing direction
- Enemies remaining
- Status messages

## 🔧 Code Architecture

### Class Hierarchy
```
Entity (base class)
├── Player
├── Enemy
└── Projectile
```

### Key Components
- **Entity System**: Base class for all game objects with collision detection
- **Movement System**: Direction-based movement with collision checking
- **Rendering System**: ASCII-based display update and drawing
- **AI System**: BFS pathfinding for intelligent enemy behavior

## 🐛 Known Issues & Limitations

- Game runs in terminal/console only
- No save/load game functionality
- Limited to single-player experience
- ASCII graphics may not display properly on all terminals
- No sound effects or music

## 🎨 Customization

### Adding New Sprites
Edit `sprites.py` to modify character appearances:
```python
custom_enemy = [
    " ☠ ",
    "/|\\",
    "/ \\"
]
```

### Creating New Enemy Types
Extend the `Enemy` class in `classes.py` for different behaviors.

### Level Design Tips
- Ensure adequate space for player movement
- Place enemies strategically for challenging gameplay
- Use walls to create interesting pathfinding scenarios
- Test levels for appropriate difficulty

## 🤝 Contributing

Feel free to contribute by:
- Creating new levels
- Adding new enemy types
- Improving AI algorithms
- Enhancing graphics/UI
- Fixing bugs

## 📄 License

This project is open source and available under standard educational use.

---

**Enjoy the game!** 🎮 Challenge yourself with custom levels and see how long you can survive against the intelligent enemy AI!
