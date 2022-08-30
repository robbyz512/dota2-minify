#  __    __     __     __   __     __     ______   __  __    
# /\ "-./  \   /\ \   /\ "-.\ \   /\ \   /\  ___\ /\ \_\ \   
# \ \ \-./\ \  \ \ \  \ \ \-.  \  \ \ \  \ \  __\ \ \____ \  
#  \ \_\ \ \_\  \ \_\  \ \_/"\_\  \ \_\  \ \_\    \/\_____\ 
#   \/_/  \/_/   \/_/   \/_/ \/_/   \/_/   \/_/     \/_____/ 
# ---------------------------------------------------------- 

# This is the stable branch
# If you are interested in developing use the experimental branch (Url)

import os
import sys
import vpk
import shutil
import psutil
import traceback
import threading
import subprocess
import tkinter as tk
from idlelib.tooltip import Hovertip
from shutil import copytree, ignore_patterns

import mpaths
import validatefiles
import helper

version = "1.0"

# button size
btnXpad = 5
btnYpad = 10
btnW = 8

patching = False
checkboxes = {}
blacklist_dictionary = {}
styling_dictionary = {}

def welcomeMsg():
 print(r"""
 Welcome to Minify
 Github: https://github.com/robbyz512/dota2-minify
 -------------------------------------------------""")

class Extension:
    def __init__(self, path):
        self.path = path
        self.css = path + '.css'
        self.vcss_c = path + '.vcss_c'
        self.xml = path + '.xml'
        self.vxml_C = path + '.vxml_c'

class Path:
    def __init__(self, path, style):
        self.path = Extension(path)
        self.style = style

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal") 
        self.widget.insert("end", " " + str, (self.tag))
        self.widget.see('end')
        self.widget.configure(state="disabled")

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.setupGUI()
        self.setupSystem()
        self.setupButtonState()
        self.root.mainloop()

    def exit(self):
        self.root.destroy()

    def setupGUI(self):
        # ------------------------------ gui properties ------------------------------ #
        self.root.title("Minify Dota2")
        self.root.iconbitmap('bin/images/favicon.ico')
        self.root.resizable(False, False)
        self.app_width = 840
        self.app_height = helper.getAppHeight(mpaths.mods_folders)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.app_width / 2)
        self.y = (self.screen_height / 2) - (self.app_height / 2)
        self.root.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        # -------------------------------- widgets -------------------------------- #

        self.checkboxesFrame = tk.Frame(self.root)
        self.checkboxesFrame.grid(row=0, column=0, sticky='w')

        self.buttonsFrame = tk.Frame(self.root)
        self.buttonsFrame.grid(row=1, column=0, pady=13, sticky='nsew')
        
        self.consoleFrame = tk.Frame(self.root)
        self.consoleFrame.grid(row=0, column=1, rowspan=2, pady=5, padx=5, sticky='nsew')

        # Checkboxes
        for index in range(len(mpaths.mods_folders)):
            self.name = mpaths.mods_folders[index]
            self.current_var = tk.IntVar()
            self.current_box = tk.Checkbutton(self.checkboxesFrame, text=self.name, variable=self.current_var, takefocus=False, command=self.setupButtonState)
            self.current_box.var = self.current_var
            self.current_box.grid(row=index, column=0, sticky='w')
            checkboxes[self.current_box] = self.name  # so checkbutton object is the key and value is string

        # Buttons
        self.patchBtn = tk.Button(self.buttonsFrame, text='Patch', state=tk.NORMAL, width=btnW, takefocus=False, command=lambda:threading.Thread(target=self.patcher, daemon=True).start())
        self.patchBtn.grid(row=10, column=0, pady=btnYpad, padx=btnXpad)
        self.helpBtn = tk.Button(self.buttonsFrame, text='Help', state=tk.NORMAL, width=btnW, takefocus=False, command=lambda:threading.Thread(target=helper.urlDispatcher(mpaths.help_url), daemon=True).start())
        self.helpBtn.grid(row=10, column=1, pady=btnYpad, padx=btnXpad)
        self.updateBtn = tk.Button(self.buttonsFrame, text='Update', state=tk.NORMAL, width=btnW, takefocus=False, command=lambda:threading.Thread(target=helper.urlDispatcher(mpaths.update_url), daemon=True).start())
        self.updateBtn.grid(row=11, column=0, pady=btnYpad, padx=btnXpad)
        self.updateBtnTip = Hovertip(self.updateBtn, text='')
        self.exitBtn = tk.Button(self.buttonsFrame, text='Exit', width=btnW, takefocus=False, command=self.exit)
        self.exitBtn.grid(row=11, column=1, pady=btnYpad, padx=btnXpad)
        self.versionLabel = tk.Label(self.buttonsFrame, font=("None", 8), width=20)
        self.versionLabel.grid(row=12, column=0)
        self.patreonBtn = tk.Button(self.buttonsFrame, text='Patreon', width=btnW, takefocus=False, command=lambda:threading.Thread(target=helper.urlDispatcher(mpaths.patreon_url), daemon=True).start())
        self.patreonBtn.grid(row=14, column=0, pady=btnYpad, padx=btnXpad)
        self.discordBtn = tk.Button(self.buttonsFrame, text='Discord', width=btnW, takefocus=False, command=lambda:threading.Thread(target=helper.urlDispatcher(mpaths.discord_url), daemon=True).start())
        self.discordBtn.grid(row=14, column=1, pady=btnYpad, padx=btnXpad)

        # Other Widget
        self.consoleText = tk.Text(self.consoleFrame, wrap=tk.WORD, state=tk.DISABLED, width=78, borderwidth=2, bg="#FFFFF7", relief="groove")
        self.consoleText.grid(row=0,column=0)
        self.consoleText.configure(font=("Fixedsys"))
        self.devLabel = tk.Label(self.consoleFrame, font=("Tahoma", 8), width=40)
        self.devLabel.config(text=f"Want to create Dota2 mods with Minify?")
        self.devLabel.place(x=400,y=390)
        self.devbtn = tk.Button(self.consoleFrame, text='Download Developer Version', width=22, height=1, font=("None", 7), takefocus=False, command=lambda:threading.Thread(target=helper.urlDispatcher(mpaths.dev_version), daemon=True).start())
        self.devbtn.place(x=475,y=412)

        # redirects stdout and stderror to text box widget, which means print statements will not appear in the gui until these two lines are ran
        sys.stdout = TextRedirector(self.consoleText, "stdout")
        sys.stderr = TextRedirector(self.consoleText, "stderr")

        welcomeMsg()

    def setupSystem(self):
        x = validatefiles.MyClass(checkboxes)
        public_methods = [method for method in dir(x) if callable(getattr(x, method)) if not method.startswith('_')]  # private methods start with _
        try:
            for method in public_methods:
                getattr(x, method)()
                if x.toggle_flag == True:
                    helper.toggleFrameOff(self.checkboxesFrame, self.buttonsFrame)
                    break
        except Exception:
            with open(os.path.join(mpaths.logs_dir, 'crashlog.txt'), 'w') as file:
                file.write(traceback.format_exc())
                helper.toggleFrameOff(self.checkboxesFrame, self.buttonsFrame)
                print("Failed to start!")
                print("Check 'logs\\crashlog.txt' for more info.")

    def setupButtonState(self):  
        for box in checkboxes:
            if box.var.get() == 1:
                self.patchBtn.config(state='normal')
                break
            else:
                self.patchBtn.config(state='disabled')

        if helper.workshop_installed == False:
            helper.disableWorkshopMods(mpaths.mods_dir, mpaths.mods_folders, checkboxes)

        if version == version:
            self.updateBtn.config(state='disabled')
            self.versionLabel.config(fg="#0cb6b3")
            self.versionLabel.config(text=f"Latest version {version}")
            self.updateBtnTip.text = 'You are using the latest version'
            self.updateBtnTip.hover_delay = 250
        else:
            self.updateBtn.config(state='normal')
            self.versionLabel.config(fg="#DE3163")
            self.versionLabel.config(text="New version available!")
            self.updateBtnTip.text = ''
            self.updateBtnTip.hover_delay = 500000 # .text='' showing pixelated whitespace, just set hover delay to forever
    # ---------------------------------------------------------------------------- #
    #                                     Main                                     #
    # ---------------------------------------------------------------------------- #
    def patcher(self): 
        global patching
        
        if "dota2.exe" in (p.name() for p in psutil.process_iter()):
            print("Please close Dota 2 first and then patch.")
            return

        patching = True 
        helper.toggleFrameOff(self.checkboxesFrame, self.buttonsFrame)

        try: 
            # clean up previous patching data
            helper.cleanFolders(mpaths.build_dir, mpaths.logs_dir, mpaths.content_dir, mpaths.game_dir, mpaths.minify_dir)
            styling_dictionary = {}
            # blacklist_dictionary = {}
            helper.warnings = []

            blank_file_extensions = helper.getBlankFileExtensions(mpaths.blank_files_dir) # list of extensions in bin/blank-files
            blacklist_data = [] # path from every blacklist.txt
            styling_data = [] # path and style from every styling.txt
            
            for folder in mpaths.mods_folders:
                try:
                    mod_path = os.path.join(mpaths.mods_dir, folder)
                    files_total = sum([len(files) for r, d, files in os.walk(os.path.join(mod_path, 'files'))])
                    blacklist_txt = os.path.join(mod_path, 'blacklist.txt')
                    styling_txt = os.path.join(mod_path, 'styling.txt') 

                    for box in checkboxes:
                        if box.var.get() == 1 and checkboxes[box] == folder: # step into folders that have ticked checkboxes only
                            print("→ Installing " + folder)
                            # ----------------------------------- files ---------------------------------- #
                            if files_total == 0:    print(f"    files: empty folder, skipping")
                            elif files_total == 1:  print(f"    files: Found {files_total} file")
                            else:                   print(f"    files: Found {files_total} files")
                            shutil.copytree(os.path.join(mod_path, 'files'), mpaths.game_dir, dirs_exist_ok=True)
                            # ------------------------------- blacklist.txt ------------------------------ #
                            if os.stat(blacklist_txt).st_size == 0:   print("    blacklist.txt: empty file, skipping")
                            else:
                                with open(blacklist_txt) as file:

                                    lines = file.readlines()

                                    for index, line in enumerate(lines):
                                        line = line.strip()

                                        if line.startswith('#') or line.isspace():
                                            continue

                                        elif line.startswith('@@'):
                                            for path in helper.processBlackList(index, line, folder, blank_file_extensions, mpaths.pak01_dir):
                                                blacklist_data.append(path)
                                            continue

                                        elif line.startswith('>>'):
                                            for path in helper.processBlacklistDir(index, line, folder, mpaths.pak01_dir):
                                                blacklist_data.append(path)
                                            continue   

                                        else:
                                            if line.endswith(tuple(blank_file_extensions)):
                                                blacklist_data.append(line)
                                            else:
                                                helper.warnings.append(f"[Invalid Extension] '{line}' in 'mods\\{folder}\\blacklist.txt' [line: {index+1}] does not end in one of the valid extensions -> {blank_file_extensions}")
                                
                                print(f"    blacklist.txt: Found {len(blacklist_data)} paths")

                                for index, line in enumerate(blacklist_data):
                                    line = line.strip()
                                    path, extension = os.path.splitext(line)

                                    # blacklist_dictionary["blacklist-key{}".format(index+1)] = path, extension

                                    if not os.path.exists(os.path.join(mpaths.game_dir, os.path.dirname(path))): os.makedirs(os.path.join(mpaths.game_dir, os.path.dirname(path)))

                                    try:
                                        shutil.copy(os.path.join(mpaths.blank_files_dir, 'blank{}').format(extension), os.path.join(mpaths.game_dir, path + extension))
                                    except FileNotFoundError as exception:
                                        helper.warnings.append(f"[Invalid Extension] '{line}' in 'mods\\{os.path.basename(mod_path)}\\blacklist.txt' does not end in one of the valid extensions -> {blank_file_extensions}")    

                                blacklist_data = []
                            # --------------------------------- styling.txt --------------------------------- #
                            if os.stat(styling_txt).st_size == 0:   print("    styling.txt: empty file, skipping")
                            else:
                                with open(styling_txt) as file:

                                    lines = file.readlines()

                                    for line in lines:
                                        line = line.strip()

                                        if line.startswith('#') or line.isspace():
                                            continue

                                        elif line.startswith('@@'):
                                            for path in helper.urlValidator(line):
                                                styling_data.append(path)
                                            continue
                                        else:
                                            styling_data.append(line)

                                print(f"    styling.txt: Found styling.txt")

                                for index, line in enumerate(styling_data):
                                    try:
                                        line = line.split("@@")
                                        path = line[0].strip()
                                        style = line[1].strip()

                                        styling_dictionary["styling-key{}".format(index+1)] = path, style
                                                                                                
                                    except Exception as exception:
                                        helper.warnings.append("[{}]".format(type(exception).__name__) + " Could not validate '{}' in --> 'mods\\{}\\styling.txt' [line: {}]".format(line, folder, index+1))

                                    if not os.path.exists(os.path.join(mpaths.build_dir, os.path.dirname(path))): os.makedirs(os.path.join(mpaths.build_dir, os.path.dirname(path)))

                                    for key, value in list(styling_dictionary.items()):
                                        construct1 = Path(value[0], value[1])
                                        try:
                                            helper.vpkExtractor(construct1.path.vcss_c, mpaths.pak01_dir, mpaths.build_dir)
                                        except KeyError:
                                            helper.warnings.append("Path does not exist in VPK -> '{}', error in 'mods\\{}\\styling.txt'".format(construct1.path.vcss_c, folder))
                                            del styling_dictionary[key]
                                
                except Exception as exception:
                    exceptiondata = traceback.format_exc().splitlines()
                    helper.warnings.append(exceptiondata[-1])
            # ---------------------------------- STEP 2 ---------------------------------- #
            # ------------------- Decompile all files in "build" folder ------------------ #
            # ---------------------------------------------------------------------------- #
            print("→ Decompiling")
            with open(os.path.join(mpaths.logs_dir, 'decompiler.txt'), 'w') as file:
                subprocess.run([mpaths.minify_dir + '/Decompiler.exe', '--input', "build", '--recursive', '--vpk_decompile', '--output', "build"], stdout=file)
            # ---------------------------------- STEP 3 ---------------------------------- #
            # -------- Check what .css files are in "build" folder and write mods -------- #
            # ---------------------------------------------------------------------------- #
            print("→ Patching")
            for key, value in list(styling_dictionary.items()):
                construct2 = Path(value[0], value[1])
                
                with open(os.path.join(mpaths.build_dir, construct2.path.css), 'r+') as file: 
                    if construct2.style not in file.read():
                        file.write("\n" + construct2.style.strip())
            # ---------------------------------- STEP 4 ---------------------------------- #
            # -----------------  Move uncompiled files in build to content --------------- #
            # ---------------------------------------------------------------------------- #
            copytree(mpaths.build_dir, mpaths.content_dir, dirs_exist_ok=True, ignore=ignore_patterns("*.vcss_c"))
            # ---------------------------------- step 5 ---------------------------------- #
            # -------------- Compile content to game with resource compiler -------------- #
            # ---------------------------------------------------------------------------- #
            with open(os.path.join(mpaths.logs_dir, 'resourcecompiler.txt'), 'wb') as file:
                print("→ Compiling")
                sp_compiler = subprocess.run([mpaths.resource_compiler, '-i', mpaths.content_dir + '/*', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if sp_compiler.stdout != b"":
                    file.write(sp_compiler.stdout)
                
                if sp_compiler.stderr != b"":
                    decoded_err = sp_compiler.stderr.decode("utf-8")
                    raise Exception(decoded_err)
            # ---------------------------------- STEP 6 ---------------------------------- #
            # -------- Create VPK from game folder and save into Minify directory -------- #
            # ---------------------------------------------------------------------------- #
            newpak = vpk.new(mpaths.game_dir)
            newpak.save(os.path.join(mpaths.dota_minify, 'pak01_dir.vpk'))

            patching = False
            helper.toggleFrameOn(self.checkboxesFrame, self.buttonsFrame, mpaths.mods_dir, mpaths.mods_folders, checkboxes)
            print("→ Done!")
            print("-------------------------------------------------")
            helper.handleWarnings(mpaths.logs_dir)

        except Exception:
            with open(os.path.join(mpaths.logs_dir, 'crashlog.txt'), 'w') as file:
                file.write(traceback.format_exc())

            patching = False
            helper.toggleFrameOn(self.checkboxesFrame, self.buttonsFrame, mpaths.mods_dir, mpaths.mods_folders, checkboxes)
            print("")
            print("Patching failed.")
            print("Check 'logs\\crashlog.txt' for more info.")
            print("-------------------------------------------------")

if __name__ == '__main__':
    app = App()