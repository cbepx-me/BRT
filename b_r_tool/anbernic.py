import os
from pathlib import Path


class Anbernic:
    
    def __init__(self):
        self.__sd1_rom_storage_path = "/mnt/mmc/anbernic/backup"
        self.__sd2_rom_storage_path = "/mnt/sdcard/anbernic/backup"
        self.__current_sd = 2


    def get_sd1_storage_path(self):
        return self.__sd1_rom_storage_path

    def get_sd2_storage_path(self):
        return self.__sd2_rom_storage_path
    
    def get_sd1_storage_console_path(self, console):
        return os.path.join(self.__sd1_rom_storage_path, self.__rom_folder_mapping[console])

    def get_sd2_storage_console_path(self, console):
        return os.path.join(self.__sd2_rom_storage_path, self.__rom_folder_mapping[console])
    
    def set_sd_storage(self, sd):
        if sd == 1 or sd == 2:
            self.__current_sd = sd
    
    def get_sd_storage(self):
        if self.__current_sd == 2 and not any(Path("/mnt/sdcard").iterdir()):
            self.__current_sd = 1
        return self.__current_sd
    
    def switch_sd_storage(self):
        if self.__current_sd == 1 and any(Path("/mnt/sdcard").iterdir()):
            self.__current_sd = 2
        else:
            self.__current_sd = 1
    
    def get_sd_storage_path(self):
        if self.__current_sd == 1 or not any(Path("/mnt/sdcard").iterdir()):
            self.__current_sd = 1
            return self.get_sd1_storage_path()
        else:
            return self.get_sd2_storage_path()
