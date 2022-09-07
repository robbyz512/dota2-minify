import os
import vpk
import shutil
import webbrowser
import urllib.error
from urllib.request import urlopen

workshop_installed = False

# ---------------------------------------------------------------------------- #
#                                   Warnings                                   #
# ---------------------------------------------------------------------------- #
# Output can be passed  here to display as warnings at the end of patching.

warnings = []

def handleWarnings(logs_dir):
    global warnings

    if len(warnings) != 0:
        with open(os.path.join(logs_dir, 'warnings.txt'), 'w') as file:
            for line in warnings:
                file.write(line + "\n")
        if len(warnings) == 1:
            print(f"{len(warnings)} error occured. Check logs\\warnings.txt for details.")
        elif len(warnings) >= 2:
            print(f"{len(warnings)} errors occured. Check logs\\warnings.txt for details.")
# ---------------------------------------------------------------------------- #
#                               Gameinfo Patcher                               #
# ---------------------------------------------------------------------------- #
l0 = "Game_LowViolence	dota_lv"
l1 = "			Game				dota_minify\n"
l2 = "			Mod				    dota_minify\n"

def patchGameInfo(gameinfo_dir):
    with open(gameinfo_dir, "r") as file:
        contents = file.readlines()
        for index, line in enumerate(contents):
            if l0 in line:
                match_index = index
                contents.insert(match_index+1, l1)
                contents.insert(match_index+2, l2)
                with open(gameinfo_dir, "w") as file:
                    file.writelines(contents)
                break
# ---------------------------------------------------------------------------- #
#                                   GUI                                        #
# ---------------------------------------------------------------------------- #
def disableWorkshopMods(mods_dir, mods_folders, checkboxes):
    for folder in mods_folders:
        mod_path = os.path.join(mods_dir, folder)
        styling_txt = os.path.join(mod_path, 'styling.txt') 

        for box in checkboxes:
            if checkboxes[box] == folder:
                if os.stat(styling_txt).st_size != 0:
                    box.configure(state='disable')

def toggleFrameOn(frame_checkbox, frame_buttons, mods_dir, mods_folders, checkboxes):
    for widget in frame_checkbox.winfo_children():
        widget.configure(state='normal')

    for widget in frame_buttons.winfo_children():
        if widget.cget('text') == 'Patch':
            widget.configure(state='normal')
        if widget.cget('text') == 'Uninstall':
            widget.configure(state='normal')

    if workshop_installed == False:
        disableWorkshopMods(mods_dir, mods_folders, checkboxes)

def toggleFrameOff(frame_checkbox, frame_buttons):
    for widget in frame_checkbox.winfo_children():
        widget.configure(state='disable')

    for widget in frame_buttons.winfo_children():
        if widget.cget('text') == 'Patch':
            widget.configure(state='disable')
        if widget.cget('text') == 'Uninstall':
            widget.configure(state='disable')

def getAppHeight(mods_folders):
    height = 465

    num_of_mods = len(mods_folders)
    i = 10

    while (i < num_of_mods):
        i += 1
        height += 30

    return height
# ---------------------------------------------------------------------------- #

def cleanFolders(build_dir, logs_dir, content_dir, game_dir, minify_dir):
    shutil.rmtree(build_dir, ignore_errors=True)

    for root, dirs, files in os.walk(logs_dir):
        for filename in files:
            open(os.path.join(root, filename), 'w').close()
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            os.remove(os.path.join(root, filename))
    for root, dirs, files in os.walk(game_dir):
        for filename in files:
            os.remove(os.path.join(root, filename))
    os.makedirs(os.path.join(minify_dir, 'build'))

def urlDispatcher(url):
    webbrowser.open(url)

def getBlankFileExtensions(blank_files_dir):
    extensions = []
    for file in os.listdir(blank_files_dir): extensions.append(os.path.splitext(file)[1])
    return extensions

def vpkExtractor(path, pak01_dir, build_dir):
    pak1 = vpk.open(pak01_dir)
    fullPath = os.path.join(build_dir, path)
    if not os.path.exists(fullPath): # extract files from VPK only once
        print("        extracting: " + path)
        path = path.replace(os.sep,'/')
        pakfile = pak1.get_file(path)
        pakfile.save(os.path.join(fullPath))

def urlValidator(url):
    content = []
    url = url.replace('@@', '')

    try: 
        for line in urlopen(url):
            try: 
                line = line.decode('utf-8').split()
                line = ''.join(line)
            except UnicodeDecodeError as exception:
                warnings.append("[{}]".format(type(exception).__name__) + " Cannot decode -> " + str(line) + " Make sure your URL is using a 'utf-8' charset")

            content.append(line)

    except urllib.error.HTTPError as exception:
        warnings.append("[{}]".format(type(exception).__name__) + f" Could not connect to -> " + url)
        
    except ValueError as exception:
        warnings.append("[{}]".format(type(exception).__name__) + f" Invalid URL -> " + url)
    
    except urllib.error.URLError as exception:
        warnings.append("[{}]".format(type(exception).__name__) + f" Invalid URL -> " + url)

    return content

def processBlacklistDir(index, line, folder, pak01_dir):
    data = []
    line = line.replace('>>', '')
    line = line.replace(os.sep,'/')
    pak1 = vpk.open(pak01_dir)
    
    for filepath in pak1:
        if filepath.startswith(line):
            data.append(filepath)

    if not data:
        warnings.append(f"[Directory Not Found] Could not find '{line}' in pak01_dir.vpk -> mods\\{folder}\\blacklist.txt [line: {index+1}]")
    
    return data

def processBlackList(index, line, folder, blank_file_extensions, pak01_dir):
    data = []

    if line.startswith("@@"):
        content = urlValidator(line)

        for line in content:

            if line.startswith("#"):
                continue

            if line.startswith(">>"):
                for path in processBlacklistDir(index, line, folder, pak01_dir):
                    data.append(path)
                continue

            try:
                if line.endswith(tuple(blank_file_extensions)):
                    data.append(line)
                else:
                    warnings.append(f"[Invalid Extension] '{line}' in 'mods\\{folder}\\blacklist.txt' [line: {index+1}] does not end in one of the valid extensions -> {blank_file_extensions}")

            except TypeError as exception:
                warnings.append("[{}]".format(type(exception).__name__) + " Invalid data type in line -> " + str(line))

    return data