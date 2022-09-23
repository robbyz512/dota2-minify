import os
import winreg
import traceback
from urllib.request import urlopen

try:
    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
except Exception as exception:
    hkey = None
    with open(os.path.join(os.getcwd(), 'logs\\registry.txt'), 'w') as file:
        file.write(traceback.format_exc())

try:
    steam_path = winreg.QueryValueEx(hkey, "InstallPath")
except:
    steam_path = None
    with open(os.path.join(os.getcwd(), 'logs\\registry_query.txt'), 'w') as file:
        file.write(traceback.format_exc())

try:
    steam_dir = steam_path[0]
except:
    steam_dir = ""

# when dota2 is not inside Steam folder then set new steam directory from 'dota2path_minify.txt
# this text file is created and set by the user in validatefiles.py during startup
if not os.path.exists(os.path.join(steam_dir, 'common\dota 2 beta\game\bin\win64\dota2.exe')):
    documents = os.path.join(os.path.expanduser('~'), 'Documents')
    path_file   = os.path.join(documents, 'dota2path_minify.txt')

    # make sure the text file exists
    if not os.path.exists(path_file):
        with open(path_file,'a+') as file:
            file.write('')
    
    # load the path from text file
    with open(path_file, 'r') as file:
        for line in file:
            steam_dir = line.strip()

# minify project paths
minify_dir = os.getcwd()
bin_dir = os.path.join(minify_dir, "bin")
blank_files_dir = os.path.join(bin_dir, "blank-files")
build_dir = os.path.join(minify_dir, "build")
mods_dir = os.path.join(minify_dir, "mods")
logs_dir = os.path.join(minify_dir, "logs")

# configure urls remotely
urls = []
for line in urlopen('https://raw.githubusercontent.com/robbyz512/dota2-minify/master/bin/modpaths/urls.txt'):
    line = line.decode('utf-8').strip().split('=')
    urls.append(line)

update_url  = urls[0][1]
discord_url = urls[1][1]
patreon_url = urls[2][1]
help_url    = urls[3][1]
latest_version_url = urls[4][1]
dev_version = urls[5][1]

# dota2 paths
content_dir = os.path.join(steam_dir, "steamapps\\common\\dota 2 beta\\content\\dota_addons\\minify")
game_dir = os.path.join(steam_dir, "steamapps\\common\\dota 2 beta\\game\\dota_addons\\minify")
dota_minify = os.path.join(steam_dir, "steamapps\\common\\dota 2 beta\\game\\dota_minify")
resource_compiler = os.path.join(steam_dir, "steamapps\\common\\dota 2 beta\\game\\bin\\win64\\resourcecompiler.exe")
gameinfo_dir = os.path.join(steam_dir, "steamapps\\common\\dota 2 beta\\game\\dota\\gameinfo.gi")
pak01_dir = os.path.join(steam_dir, "steamapps\\common\\dota 2 beta\\game\\dota\\pak01_dir.vpk")

# exclude invalid mods
enabled_mods = ['Auto Accept Match',
                'Dark Terrain',
                'Default Menu Background',
                'Ink Shader',
                'Minify HUD',
                'Minify Spells & Items',
                'Misc Optimization',
                'Remove Battlepass Sounds', 
                'Remove Foilage', 
                'Remove Pinging', 
                'Remove Sprays',
                'Terrain - Sanctum of the Divine',
                'Tree Mod',
                ]

patreon_mods = ['Terrain - Sanctum of the Divine']

mods_folders = []
for mod in os.listdir(mods_dir): mods_folders.append(mod)
mods_folders = [p for p in mods_folders if p in enabled_mods]