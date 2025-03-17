import os
import binascii
import base64
from pathlib import Path
import ssl
from systems import systems
from anbernic import Anbernic
import subprocess
import textwrap
import sys
import config as cf

an = Anbernic()


class Set:
    def __init__(self):
        self.user = ""

    def execute_command(self, command, storage_path):
        if command.startswith('back:'):
            code = command[5:]
            if code == "sys":
                backup_file = f"{storage_path}/system.tar.gz"
                output = "System settings backup to:"
                files = [
                    "/mnt/data/.wifi",
                    "/mnt/data/dmenu/",
                    "/mnt/data/misc/",
                    "/mnt/mod/ctrl/configs/*.cfg",
                    "/mnt/mod/ctrl/configs/*.txt",
                    "/mnt/vendor/bin/arcade-plus.csv",
                    "/mnt/vendor/bin/default.ttf"
                ]
            elif code == "emu":
                backup_file = f"{storage_path}/emulator.tar.gz"
                output = "Emulator settings backup to:"
                files = [
                    "/.config/retroarch/retroarch.cfg",
                    "/mnt/mmc/Roms/OPENBOR/Saves/",
                    "/mnt/mmc/anbernic/autocores/",
                    "/mnt/mmc/anbernic/custom/",
                    "/mnt/mmc/openbor/Saves/",
                    "/mnt/vendor/deep/drastic-modify/res/config/",
                    "/mnt/vendor/deep/drastic-modify/res/resources/settings.json",
                    "/mnt/vendor/deep/drastic/config/",
                    "/mnt/vendor/deep/ppsspp/PSP/SYSTEM/",
                    "/mnt/vendor/deep/retro/config/",
                    "/mnt/vendor/deep/retro/remaps/"
                ]
            elif code == "save":
                backup_file = f"{storage_path}/save.tar.gz"
                output = "Save files backup to:"
                files = [
                    "/mnt/mmc/.config/ppsspp/PSP/PPSSPP_STATE/",
                    "/mnt/mmc/.config/ppsspp/PSP/SAVEDATA/",
                    "/mnt/mmc/.pcsx/memcards/",
                    "/mnt/mmc/.pcsx/sstates/",
                    "/mnt/mmc/.pixel_reader_store/",
                    "/mnt/mmc/openbor/Saves/",
                    "/mnt/mmc/save/",
                    "/mnt/mmc/save_nds/",
                    "/mnt/mmc/saves_RA/",
                    "/mnt/mmc/states_RA/",
                    "/mnt/vendor/deep/drastic-modify/res/backup/",
                    "/mnt/vendor/deep/drastic-modify/res/savestates/",
                    "/mnt/vendor/deep/retro/system/dc/*.bin"
                ]
            elif code == "theme":
                backup_file = f"{storage_path}/theme.tar.gz"
                output = "Theme files backup to:"
                files = [
                    "/mnt/vendor/res1/",
                    "/mnt/vendor/res2/"
                ]
            backup_dir = os.path.dirname(backup_file)
            os.makedirs(backup_dir, exist_ok=True)
            files_to_compress = []
            for file in files:
                if os.path.exists(file):
                    files_to_compress.append(file)
            run_command = f"tar -zcvf {backup_file} {' '.join(files_to_compress)}"
        elif command.startswith('restore:'):
            code = command[8:]
            if code == "sys":
                backup_file = f"{storage_path}/system.tar.gz"
                output = "Recovered System settings backup file:"
            elif code == "emu":
                backup_file = f"{storage_path}/emulator.tar.gz"
                output = "Backup file for restored Emulator settings:"
            elif code == "save":
                backup_file = f"{storage_path}/save.tar.gz"
                output = "Recovered Saved files:"
            elif code == "theme":
                backup_file = f"{storage_path}/theme.tar.gz"
                output = "Recovered theme files:"
            if os.path.exists(backup_file):
                run_command = f"tar -zxvf {backup_file} -C /"
            else:
                return False, "No backup files exist!", backup_file
        try:
            result = subprocess.run(
                run_command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=10
            )
            return True, output, backup_file
        except subprocess.CalledProcessError as e:
            return False, e.stdout.decode('utf-8'), backup_file
        except Exception as e:
            return False, str(e), backup_file

    def get_all_menus(self) -> list[str]:
        all_menu = [system["menu"] for system in systems]
        return all_menu

    def get_menu_help(self, menu_name: str) -> list[str]:
        for system in systems:
            if system["menu"] == menu_name:
                return system["menu_help"]

    def get_menu_option(self, menu_name: str) -> list[str]:
        for system in systems:
            if system["menu"] == menu_name:
                return system["options"]
        return []

    def get_opt_help(self, opt_select, menu_name: str) -> list[str]:
        for system in systems:
            if system["menu"] == menu_name:
                help_list=system["opt_help"]
                return help_list[opt_select]
        return []

    def get_menu_operation(self, opt_select, menu_name: str) -> list[str]:
        for system in systems:
            if system["menu"] == menu_name:
                operation_list=system["operations"]
                return operation_list[opt_select]
        return []
