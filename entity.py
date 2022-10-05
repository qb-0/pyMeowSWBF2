import pyMeow as pm
from misc import Offsets, world_to_screen, ColorClass


class Entity:
    def __init__(self, addr):
        self.addr = addr
        self.team = 0
        self.health = 0
        self.max_health = 0
        self.height = 0.0
        self.distance = 0.0
        self.pos3d = None
        self.pos2d = None
        self.head_pos3d = None
        self.head_pos2d = None
        self.visible = False
        self.alive = False
        self.head = 0
        self.width = 0
        self.center = 0
        self.name = None
        self.box_color = None

    def read(self, proc, view_matrix=None):
        try:
            controlled = pm.r_int64(proc, self.addr + Offsets.ControlledControllable)
            health_comp = pm.r_int64(proc, controlled + Offsets.HealthComponent)
            self.height = pm.r_float(proc, controlled + Offsets.Height)
            self.health = pm.r_float(proc, health_comp + Offsets.Health)
            self.max_health = pm.r_float(proc, health_comp + Offsets.MaxHealth)
            self.alive = self.health > 0.0
            if not self.alive:
                return False
            soldier = pm.r_int64(proc, controlled + Offsets.SoldierPrediction)
            self.pos3d = pm.r_vec3(proc, soldier + Offsets.Position)
            self.head_pos3d = pm.vec3(self.pos3d["x"], self.pos3d["y"] + self.height - 18.5, self.pos3d["z"])
            if view_matrix:
                self.pos2d = world_to_screen(self.pos3d, view_matrix)
                self.head_pos2d = world_to_screen(self.head_pos3d, view_matrix)
                self.head = self.pos2d["y"] - self.head_pos2d["y"]
                self.width = self.head / 2
                self.center = self.width / 2
            self.team = pm.r_int(proc, self.addr + Offsets.Team)
            self.visible = pm.r_byte(proc, controlled + Offsets.Occluded) == 0
            self.name = pm.r_string(proc, pm.r_int64(proc, self.addr + Offsets.NameClass))
        except:
            return False
        return True

    def draw_box(self, color, visible_color, alpha):
        self.box_color = visible_color if self.visible else color
        pm.draw_rectangle(
            self.head_pos2d["x"] - self.center,
            self.head_pos2d["y"] - self.center / 2,
            self.width,
            self.head + self.center / 2,
            pm.fade_color(self.box_color, alpha),
        )
        pm.draw_rectangle_lines(
            self.head_pos2d["x"] - self.center,
            self.head_pos2d["y"] - self.center / 2,
            self.width,
            self.head + self.center / 2,
            self.box_color,
            1.2,
        )

    def draw_snapline(self, color, visible_color, alpha, thick, start_pos):
        c = visible_color if self.visible else color
        pm.draw_line(
            start_pos[0],
            start_pos[1],
            self.head_pos2d["x"] - self.center,
            self.head_pos2d["y"] - self.center / 2,
            pm.fade_color(c, alpha),
            thick,
        )

    def draw_health(self):
        end_pos = pm.vec2(self.head_pos2d["x"] + self.center, self.head_pos2d["y"] - self.width)
        pm.draw_line(
            self.head_pos2d["x"] + self.width - self.center,
            self.head_pos2d["y"] - self.center / 2,
            end_pos["x"],
            end_pos["y"],
            self.box_color,
            1.2,
        )
        pm.draw_circle_sector(
            end_pos["x"],
            end_pos["y"],
            self.center / 3 + 2,
            0,
            360,
            0,
            ColorClass.black,
        )
        pm.draw_circle_sector(
            end_pos["x"],
            end_pos["y"],
            self.center / 3,
            0,
            360,
            0,
            ColorClass.red,
        )
        pm.draw_circle_sector(
            end_pos["x"],
            end_pos["y"],
            self.center / 3,
            0,
            360 / self.max_health * self.health,
            0,
            ColorClass.green,
        )

    def draw_info(self, distance, color):
        end_pos = pm.vec2(
            self.head_pos2d["x"] + self.center + self.width - self.center / 2, self.head_pos2d["y"] - self.center / 2
        )
        pm.draw_line(
            self.head_pos2d["x"] + self.width - self.center,
            self.head_pos2d["y"] - self.center / 2,
            end_pos["x"],
            end_pos["y"],
            self.box_color,
            1.2,
        )
        pm.draw_font(0, self.name, end_pos["x"], end_pos["y"], 13, 0, color)
        pm.draw_font(0, f"D: {distance}", end_pos["x"], end_pos["y"] + 13, 13, 0, color)
        pm.draw_font(
            0, f"H: {int(self.health)} / {int(self.max_health)}", end_pos["x"], end_pos["y"] + 26, 13, 0, color
        )
