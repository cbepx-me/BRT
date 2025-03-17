# Backup & Restore Tool
A simple backup & restore tool for modified stock os for your Anbernic RG??xx devices

## Inspired by
https://github.com/Julioevm/tiny-scraper

## Features
### The following files can be backed up and restored:
- System settings: including system settings, favorites, history, wifi settings, arcade name files, and default fonts, etc
- Emulator settings: including Retroarch and standalone Emulator settings
- Game save: including game progress of the "Game room" and "Ra game" emulator, even if saved, etc
- System theme: Theme resources of the current system

## Supported Devices
All released Anbernic h700 handheld devices

## Installation
To install Bezel Custom Manager on your Anbernic device, follow these steps:

1. Download the Latest Release:

  - Navigate to the Releases page and download the latest version of brt.zip.

2. Transfer to Device:

  - Extract and copy the content of the downloaded zip to the APPS directory of your Anbernic. You can copy it in /mnt/sdcard/Roms/APPS if you want the app on the SD2 or /mnt/mmc/Roms/APPS for the SD1.
Setup config

3. Start Backup & Restore Tool:
  - From the main menu, go to App Center, select Apps and launch Backup_&_Restore_Tool.

## Troubleshooting
Old version of stock OS might cause issues. V 1.0.3 (20240511) hs been reported to miss some necessary libraries: No module named 'PIL' try to update in this case.

Any issue should be logged in the log.txt file inside the tiny_scraper folder. Open an issue and share its contents for help!
