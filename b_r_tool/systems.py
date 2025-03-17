from pathlib import Path
import json

try:
    config_path = Path(__file__).parent / 'lang' / 'menu_config.json'
    systems = json.loads(config_path.read_text(encoding='utf-8'))['systems']
except Exception as e:
    print(f"Error loading menu config: {e}")
    systems = [{
        "menu": "default.menu",
        "menu_help": "default.help",
        "options": [],
        "opt_help": [],
        "operations": []
    }] # 默认菜单配置

