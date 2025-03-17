from pathlib import Path
from typing import List, Optional
from main import hw_info, system_lang
from graphic import screen_resolutions
from language import Translator
from anbernic import Anbernic
import graphic as gr
import input
import sys
import time
import json
import config as cf
from set import Set

ver="v1.2"
translator = Translator(system_lang)
selected_position = 0
menu_selected_position = 0
opt_selected_position = 0
selected_menu = ""
current_window = "menu"
help_txt = ""
skip_input_check = False
an = Anbernic()
set = Set()

x_size, y_size, max_elem = screen_resolutions.get(hw_info, (640, 480, 7))

button_x = x_size - 110
button_y = y_size - 30
ratio = y_size / x_size


def start() -> None:
    print("Starting Backup & Restore Tool...")
    gr.draw_log(
        f"{translator.translate('welcome')}", fill=gr.colorBlue, outline=gr.colorBlueD1
    )
    gr.draw_paint()
    time.sleep(1)
    load_menu_menu()


def update() -> None:
    global current_window, \
            selected_position, \
            skip_input_check

    if skip_input_check:
        input.reset_input()
        skip_input_check = False
    else:
        input.check()

    if input.key("MENUF"):
        gr.draw_end()
        print("Exiting Backup & Restore Tool...")
        sys.exit()

    if current_window == "menu":
        load_menu_menu()
    elif current_window == "options":
        load_options_menu()
    else:
        load_menu_menu()


def load_menu_menu() -> None:
    global \
        menu_selected_position, \
        selected_menu, \
        current_window, \
        skip_input_check

    all_menu = set.get_all_menus()

    if not all_menu:
        gr.draw_text((x_size/2, y_size/2), translator.translate('menu.empty'), font=17, anchor='mm')
        gr.draw_paint()
        time.sleep(2)
        current_window = "menu"
        return

    if all_menu:
        if input.key("DY"):
            menu_selected_position += input.value
            if menu_selected_position < 0:
                menu_selected_position = len(all_menu) - 1
            elif menu_selected_position >= len(all_menu):
                menu_selected_position = 0
        elif input.key("A"):
            current_window = "options"
            selected_menu = all_menu[menu_selected_position]
            skip_input_check = True
            return

    gr.draw_clear()

    gr.draw_rectangle_r([10, 40, x_size - 10, y_size - 40], 15, fill=gr.colorGrayD2, outline=None)
    gr.draw_text((x_size / 2, 20), f"{translator.translate('Backup & Restore Tool')} {ver}", font=17, anchor="mm")

    start_idx = int(menu_selected_position / max_elem) * max_elem
    end_idx = start_idx + max_elem
    for i, system in enumerate(all_menu[start_idx:end_idx]):
        row_list(
            translator.translate(system), (20, 50 + (i * 35)), x_size - 40, i == (menu_selected_position % max_elem)
        )

    help_txt = set.get_menu_help(all_menu[menu_selected_position])
    gr.draw_help(
        f"{translator.translate(help_txt)}", fill=None, outline=gr.colorBlue
    )

    button_circle((30, button_y), "A", f"{translator.translate('Select')}")
    button_circle((button_x, button_y), "M", f"{translator.translate('Exit')}")

    gr.draw_paint()


def load_options_menu() -> None:
    global \
        current_window, \
        skip_input_check, \
        selected_menu, \
        opt_selected_position

    exit_menu = False
    if selected_menu == "menu.back":
        cur_color = gr.colorBlueD1
    else:
        cur_color = gr.colorRed
    opt_list = set.get_menu_option(selected_menu)

    if len(opt_list) < 1:
        current_window = "menu"
        gr.draw_log(
            f"{translator.translate('No available settings found.')}", fill=gr.colorBlue, outline=gr.colorBlueD1
        )
        gr.draw_paint()
        time.sleep(2)
        exit_menu = True

    if input.key("B"):
        exit_menu = True
    elif input.key("A"):
        gr.draw_log(
            f"{translator.translate('Executing...')}", fill=gr.colorBlue, outline=gr.colorBlueD1
        )
        gr.draw_paint()
        selected_operation = set.get_menu_operation(opt_selected_position, selected_menu)
        command = set.get_menu_operation(opt_selected_position, selected_menu)
        storage_path = an.get_sd_storage_path()
        success, output, file = set.execute_command(command, storage_path)
        if success:
            status_msg = f"<{translator.translate('Done')}> {translator.translate(output)}\n{file}"
            status_color = gr.colorBlue
        else:
            status_msg = f"<{translator.translate('Error')}> {translator.translate(output)}\n{file}"
            status_color = gr.colorRed
        
        gr.draw_log(f"{status_msg}", fill=status_color, outline=status_color, font=13)
        gr.draw_paint()
        time.sleep(3)

    elif input.key("DY"):
        opt_selected_position += input.value
        if opt_selected_position < 0:
            opt_selected_position = len(opt_list) - 1
        elif opt_selected_position >= len(opt_list):
            opt_selected_position = 0

    elif input.key("Y"):
        an.switch_sd_storage()

    if exit_menu:
        current_window = "menu"
        gr.draw_clear()
        opt_selected_position = 0
        skip_input_check = True
        return

    gr.draw_clear()

    gr.draw_rectangle_r([10, 40, x_size - 10, y_size - 40], 15, fill=gr.colorGrayD2, outline=None)
    gr.draw_text(
        (x_size / 2, 20),
        f"{translator.translate(selected_menu)} - {translator.translate('options')} {opt_selected_position + 1} {translator.translate('of')} {len(opt_list)}",
        font=17, anchor="mm",
    )

    start_idx = int(opt_selected_position / max_elem) * max_elem
    end_idx = start_idx + max_elem
    for i, para in enumerate(opt_list[start_idx:end_idx]):
        row_list(
            f"{translator.translate(para)}",
            (20, 50 + (i * 35)),
            x_size -40,
            i == (opt_selected_position % max_elem),
        )

    help_txt = set.get_opt_help(opt_selected_position, selected_menu)
    gr.draw_help(
        f"{translator.translate(help_txt)}",
        fill=cur_color, outline=gr.colorBlueD1
    )

    button_circle((30, button_y), "A", f"{translator.translate('Select')}")
    button_circle((150, button_y), "B", f"{translator.translate('Back')}")
    button_circle((270, button_y), "Y", f"{translator.translate('Save in')} TF: {an.get_sd_storage()}")
    button_circle((button_x, button_y), "M", f"{translator.translate('Exit')}")

    gr.draw_paint()

def row_list(text: str, pos: tuple[int, int], width: int, selected: bool) -> None:
    gr.draw_rectangle_r(
        [pos[0], pos[1], pos[0] + width, pos[1] + 32],
        5,
        fill=(gr.colorBlue if selected else gr.colorGrayL1),
    )
    gr.draw_text((pos[0] + 5, pos[1] + 5), text)


def button_circle(pos: tuple[int, int], button: str, text: str) -> None:
    gr.draw_circle(pos, 25, fill=gr.colorBlueD1)
    gr.draw_text((pos[0] + 12, pos[1] + 12), button, anchor="mm")
    gr.draw_text((pos[0] + 30, pos[1] + 12), text, font=13, anchor="lm")


def button_rectangle(pos: tuple[int, int], button: str, text: str) -> None:
    gr.draw_rectangle_r(
        (pos[0], pos[1], pos[0] + 60, pos[1] + 25), 5, fill=gr.colorGrayL1
    )
    gr.draw_text((pos[0] + 30, pos[1] + 12), button, anchor="mm")
    gr.draw_text((pos[0] + 65, pos[1] + 12), text, font=13, anchor="lm")
