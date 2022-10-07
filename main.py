import os
import sys
import pyMeow as pm

from configparser import ConfigParser

from entity import Entity
from misc import Offsets, ColorClass
from menu import Menu


class PyMeowSWBF2:
    def __init__(self):
        if os.name == "posix":
            # 'comm' and 'status' file in linux save the process name as 'starwarsbattlef'
            process_name = "starwarsbattlef"
        elif os.name == "nt":
            process_name = "starwarsbattlefrontii.exe"
        else:
            sys.exit("Only Windows and Linux are supported.")

        self.colors = ColorClass()
        self.config = ConfigParser()
        self.menu = Menu()
        self.local_player = None

        try:
            with open("config.ini") as f:
                self.config.read_file(f)
            self.colors.parse_colors(self.config)
            self.proc = pm.open_process(processName=process_name)
            self.render_view = pm.r_int(self.proc, pm.r_int(self.proc, Offsets.GameRenderer) + Offsets.RenderView)
            self.game_context = pm.r_int(self.proc, Offsets.ClientGameContext)
            self.player_manager = pm.r_int(self.proc, self.game_context + Offsets.PlayerManager)
            self.client_array = pm.r_int(self.proc, self.player_manager + Offsets.ClientArray)
            self.patches()
            pm.overlay_init(
                fps=self.config.getint("Main", "FPS"),
                target="STAR WARS Battlefront II",
                title="SWBF2 pyMeow",
            )
            pm.load_font("assets/soloist1.ttf", 0)
        except Exception as e:
            sys.exit(e)

    def patches(self):
        # No Recoil
        pm.w_bytes(self.proc, Offsets.RecoilPatch, [0x90] * 5)
        # No Spread
        pm.w_bytes(self.proc, Offsets.SpreadPatch, [0x90] * 5)

    def entity_loop(self):
        clients = pm.r_ints64(self.proc, self.client_array, 64)
        view_matrix = pm.r_floats(self.proc, self.render_view + Offsets.ViewProj, 16)
        for ent_addr in clients:
            if ent_addr:
                ent = Entity(ent_addr)
                if ent.read(self.proc, view_matrix):
                    yield ent

    def main_loop(self):
        while pm.overlay_loop():
            pm.begin_drawing()

            # FPS
            if self.config.getboolean("Main", "DrawFPS"):
                pm.gui_progress_bar(
                    posX=26, posY=pm.get_screen_height() - 30,
                    width=200, height=20,
                    textLeft="FPS ", textRight=f" {pm.get_fps()}",
                    value=pm.get_fps(), minValue=0,
                    maxValue=600 if self.config.getfloat("Main", "FPS") == 0 else self.config.getfloat("Main", "FPS")
                )

            # Menu
            self.menu.check_key()
            if self.menu.draw:
                self.config = self.menu.draw_menu(self.config)

            # Init Local
            local_addr = pm.r_int64(self.proc, self.player_manager + Offsets.LocalPlayer)
            self.local_player = Entity(local_addr)
            if not self.local_player.read(self.proc):
                # No local player
                pm.end_drawing()
                continue

            # Entity loop
            for ent in self.entity_loop():
                if ent.addr == self.local_player.addr:
                    continue

                same_team = ent.team == self.local_player.team
                if not self.config.getboolean("Main", "TeamESP") and same_team:
                    continue

                # Boxes
                ent.draw_box(
                    self.colors.team_box if same_team else self.colors.enemy_box,
                    self.colors.team_box_visible if same_team else self.colors.enemy_box_visible,
                    self.colors.team_box_alpha if same_team else self.colors.enemy_box_alpha,
                )

                # Snaplines
                if self.config.getboolean("Main", "DrawSnaplines"):
                    pos = (pm.get_screen_width() / 2, pm.get_screen_height())
                    if self.config["Main"]["SnaplinesPosition"].lower() == "top":
                        pos = (pm.get_screen_width() / 2, 0)
                    elif self.config["Main"]["SnaplinesPosition"].lower() == "mid":
                        pos = (pm.get_screen_width() / 2, pm.get_screen_height() / 2)
                    ent.draw_snapline(
                        self.colors.team_snaplines if same_team else self.colors.enemy_snaplines,
                        self.colors.team_snaplines_visible if same_team else self.colors.enemy_snaplines_visible,
                        self.colors.team_snaplines_alpha if same_team else self.colors.enemy_snaplines_alpha,
                        self.config.getfloat("Main", "SnaplinesThickness"),
                        pos,
                    )

                # Health
                if self.config.getboolean("Main", "DrawHealth"):
                    ent.draw_health()

                # Info
                if self.config.getboolean("Main", "DrawInfo"):
                    ent.draw_info(int(pm.vec3_distance(self.local_player.pos3d, ent.pos3d)), self.colors.info)

            pm.end_drawing()


if __name__ == "__main__":
    run = PyMeowSWBF2()
    run.main_loop()
