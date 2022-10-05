import os
import sys
import pyMeow as pm

from configparser import ConfigParser

from entity import Entity
from misc import Offsets, ColorClass

# Globals
proc = render_view = game_context = player_manager = client_array = None
Config = ConfigParser()
Colors = ColorClass()


def load_config():
    with open("config.ini") as f:
        Config.read_file(f)


def apply_patches():
    def nop_code(address, n):
        pm.w_bytes(proc, address, [0x90] * n)

    # No Recoil
    nop_code(Offsets.RecoilPatch, 5)
    # No Spread
    nop_code(Offsets.SpreadPatch, 5)


def init():
    if os.name == "posix":
        # 'comm' and 'status' file in linux save the process name as 'starwarsbattlef'
        process_name = "starwarsbattlef"
    elif os.name == "nt":
        process_name = "starwarsbattlefrontii.exe"
    else:
        sys.exit("Only Windows and Linux are supported.")

    try:
        global proc, render_view, game_context, player_manager, client_array, Config
        load_config()
        Colors.parse_colors(Config)
        proc = pm.open_process(processName=process_name)
        render_view = pm.r_int(proc, pm.r_int(proc, Offsets.GameRenderer) + Offsets.RenderView)
        game_context = pm.r_int(proc, Offsets.ClientGameContext)
        player_manager = pm.r_int(proc, game_context + Offsets.PlayerManager)
        client_array = pm.r_int(proc, player_manager + Offsets.ClientArray)
        apply_patches()
        pm.overlay_init(
            fps=Config.getint("Main", "FPS"),
            target="STAR WARS Battlefront II",
            title="SWBF2 pyMeow",
        )
        pm.load_font("assets/soloist1.ttf", 0)
    except Exception as e:
        sys.exit(e)


def ent_loop():
    if client_array:
        clients = pm.r_ints64(proc, client_array, 64)
        view_matrix = pm.r_floats(proc, render_view + Offsets.ViewProj, 16)
        for ent_addr in clients:
            if ent_addr:
                ent = Entity(ent_addr)
                if ent.read(proc, view_matrix):
                    yield ent


def main():
    while pm.overlay_loop():
        pm.begin_drawing()
        if Config.getboolean("Main", "DrawFPS"):
            pm.draw_fps(10, pm.get_screen_height() - 30)

        # Init Local
        local_player = pm.r_int64(proc, player_manager + Offsets.LocalPlayer)
        local_player = Entity(local_player)
        if not local_player.read(proc):
            pm.end_drawing()
            continue

        # Entity loop
        for ent in ent_loop():
            if ent.addr == local_player.addr:
                continue

            same_team = ent.team == local_player.team
            if not Config.getboolean("Main", "TeamESP") and same_team:
                continue

            # Boxes
            ent.draw_box(
                Colors.team_box if same_team else Colors.enemy_box,
                Colors.team_box_visible if same_team else Colors.enemy_box_visible,
                Colors.team_box_alpha if same_team else Colors.enemy_box_alpha,
            )

            # Snaplines
            if Config.getboolean("Main", "DrawSnaplines"):
                pos = (pm.get_screen_width() / 2, pm.get_screen_height())
                if Config["Main"]["SnaplinesPosition"].lower() == "top":
                    pos = (pm.get_screen_width() / 2, 0)
                elif Config["Main"]["SnaplinesPosition"].lower() == "mid":
                    pos = (pm.get_screen_width() / 2, pm.get_screen_height() / 2)
                ent.draw_snapline(
                    Colors.team_snaplines if same_team else Colors.enemy_snaplines,
                    Colors.team_snaplines_visible if same_team else Colors.enemy_snaplines_visible,
                    Colors.team_snaplines_alpha if same_team else Colors.enemy_snaplines_alpha,
                    Config.getfloat("Main", "SnaplinesThickness"),
                    pos,
                )

            # Health
            if Config.getboolean("Main", "DrawHealth"):
                ent.draw_health()

            # Info
            if Config.get("Main", "DrawInfo"):
                ent.draw_info(int(pm.vec3_distance(local_player.pos3d, ent.pos3d)), Colors.info)

        pm.end_drawing()


if __name__ == "__main__":
    init()
    main()
