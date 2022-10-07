# pyMeow SWBF2
A configurable cross platform Starwars Battlefront 2 ESP created with [pyMeow](https://github.com/qb-0/pyMeow).

<img src="https://github.com/qb-0/pyMeowSWBF2/raw/master/screenshots/screenshot.png" alt="alt text" width="800" height="600">

## Features
- FPS control
- Box ESP
- Snaplines
- Entity ESP
- No Recoil
- No Spread
- Ingame Menu

## Installation
- Install Python (64bit)
- Install pyMeow [pyMeow](https://github.com/qb-0/pyMeow)
- Clone this repository and run the main script:
  - Windows: `python main.py`
  - Linux: `sudo python3 main.py`
  
## Instructions
Run SWBF2 in windowed or windowed fullscreen mode.

### Menu
The ingame menu can be opened by pressing `INSERT`:<br>
![alt text](https://github.com/qb-0/pyMeowSWBF2/raw/master/screenshots/menu.png)
### config.ini
You can change various colors by editing the config file:
```ini
[Main]
fps = 240
drawfps = True
teamesp = True
drawsnaplines = True
snaplinesthickness = 1.0
snaplinesposition = mid
drawhealth = True
drawinfo = True
infocolor = white

[EnemyColor]
box = orange
boxvisible = lime
boxalpha = 0.3
snaplines = orange
snaplinesvisible = lime
snaplinesalpha = 0.3

[TeamColor]
box = silver
boxvisible = white
boxalpha = 0.3
snaplines = silver
snaplinesvisible = silver
snaplinesalpha = 0.3
```

