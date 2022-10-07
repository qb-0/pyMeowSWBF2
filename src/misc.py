import pyMeow as pm


class Offsets:
    GameRenderer = 0x143FFBE10
    RenderView = 0x538
    ViewProj = 0x430
    ClientGameContext = 0x143DD7948
    PlayerManager = 0x58
    LocalPlayer = 0x568
    ClientArray = 0x768
    Team = 0x58
    ControlledControllable = 0x210
    HealthComponent = 0x2C8
    Height = 0x470
    SoldierPrediction = 0x758
    Occluded = 0xA58
    Health = 0x20
    MaxHealth = 0x24
    Position = 0x20
    NameClass = 0x18
    RecoilPatch = 0x0147EEE11E
    SpreadPatch = 0x0147EE6A39


class ColorClass:
    black = pm.get_color("black")
    white = pm.get_color("white")
    green = pm.get_color("lightgreen")
    red = pm.get_color("orangered")

    def __init__(self):
        self.enemy_box = None
        self.enemy_box_visible = None
        self.enemy_box_alpha = None
        self.enemy_snaplines = None
        self.enemy_snaplines_visible = None
        self.enemy_snaplines_alpha = None
        self.team_box = None
        self.team_box_visible = None
        self.team_box_alpha = None
        self.team_snaplines = None
        self.team_snaplines_visible = None
        self.team_snaplines_alpha = None
        self.info = None

    def parse_colors(self, config):
        self.enemy_box = pm.get_color(config["EnemyColor"]["Box"])
        self.enemy_box_visible = pm.get_color(config["EnemyColor"]["BoxVisible"])
        self.enemy_box_alpha = config.getfloat("EnemyColor", "BoxAlpha")
        self.enemy_snaplines = pm.get_color(config["EnemyColor"]["Snaplines"])
        self.enemy_snaplines_visible = pm.get_color(config["EnemyColor"]["SnaplinesVisible"])
        self.enemy_snaplines_alpha = config.getfloat("EnemyColor", "SnaplinesAlpha")
        self.team_box = pm.get_color(config["TeamColor"]["Box"])
        self.team_box_visible = pm.get_color(config["TeamColor"]["BoxVisible"])
        self.team_box_alpha = config.getfloat("TeamColor", "BoxAlpha")
        self.team_snaplines = pm.get_color(config["TeamColor"]["Snaplines"])
        self.team_snaplines_visible = pm.get_color(config["TeamColor"]["SnaplinesVisible"])
        self.team_snaplines_alpha = config.getfloat("TeamColor", "SnaplinesAlpha")
        self.info = pm.get_color(config["Main"]["InfoColor"])


def world_to_screen(pos, vm):
    w = vm[3] * pos["x"] + vm[7] * pos["y"] + vm[11] * pos["z"] + vm[15]
    if w < 0.3:
        raise Exception("Out of bounds")
    x = vm[0] * pos["x"] + vm[4] * pos["y"] + vm[8] * pos["z"] + vm[12]
    y = vm[1] * pos["x"] + vm[5] * pos["y"] + vm[9] * pos["z"] + vm[13]

    return pm.vec2(
        pm.get_screen_width() / 2 + pm.get_screen_width() / 2 * x / w,
        pm.get_screen_height() / 2 - pm.get_screen_height() / 2 * y / w,
    )
