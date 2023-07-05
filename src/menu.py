import os
import pyMeow as pm

from time import sleep


class Menu:
    def __init__(self):
        self.draw = False
        self.prevState = False
        # Insert
        self.menu_key = 0x2D
        if os.name == "posix":
            self.menu_key = 0xff63

    def draw_menu(self, config):
        window_box = pm.gui_window_box(
            posX=0,
            posY=0,
            width=400,
            height=210,
            title="pyMeow SWBF2"
        )
        if window_box:
            self.draw = False
            pm.toggle_mouse()

        config["Main"]["DrawFPS"] = str(pm.gui_check_box(
            posX=10, posY=30,
            width=20, height=20,
            text="Draw FPS",
            checked=config.getboolean("Main", "DrawFPS")
        ))

        fps_choices = [0, 30, 60, 120, 144, 240]
        config["Main"]["FPS"] = str(fps_choices[
            pm.gui_dropdown_box(
                posX=120, posY=30,
                width=80, height=20,
                text="Max;30;60;120;144;240",
                id=0
            )
        ])
        if pm.gui_button(posX=210, posY=30, width=50, height=20, text="Set FPS"):
            pm.set_fps(int(config["Main"]["FPS"]))

        config["Main"]["TeamESP"] = str(pm.gui_check_box(
            posX=10, posY=60,
            width=20, height=20,
            text="Draw Team ESP",
            checked=config.getboolean("Main", "TeamESP")
        ))

        config["Main"]["DrawSnaplines"] = str(pm.gui_check_box(
            posX=10, posY=90,
            width=20, height=20,
            text="Draw Snaplines",
            checked=config.getboolean("Main", "DrawSnaplines")
        ))

        snapline_positions = ["mid", "top", "bottom"]
        config["Main"]["SnaplinesPosition"] = snapline_positions[
            pm.gui_dropdown_box(
                posX=120, posY=90,
                width=80, height=20,
                text="#64#Mid;#121#Top;#120#Bottom",
                id=1
            )
        ]

        config["Main"]["SnapLinesThickness"] = str(pm.gui_slider(
            posX=265, posY=90,
            width=80, height=20,
            textLeft="Thickness", textRight=str(config["Main"]["SnapLinesThickness"]),
            value=config.getfloat("Main", "SnapLinesThickness"), minValue=0.1, maxValue=10.0
        ))

        config["Main"]["DrawHealth"] = str(pm.gui_check_box(
            posX=10, posY=120,
            width=20, height=20,
            text="Draw Health",
            checked=config.getboolean("Main", "DrawHealth")
        ))

        config["Main"]["DrawInfo"] = str(pm.gui_check_box(
            posX=10, posY=150,
            width=20, height=20,
            text="Draw Information",
            checked=config.getboolean("Main", "DrawInfo")
        ))

        if pm.gui_button(posX=10, posY=180, width=380, height=20, text="Safe Config"):
            pm.set_fps(int(config["Main"]["FPS"]))
            with open("config.ini", "w") as f:
                config.write(f)

        return config

    def check_key(self):
        state = pm.key_pressed(self.menu_key)
        if state and not self.prevState:
            self.draw = not self.draw
            pm.toggle_mouse()
        self.prevState = state
