import os
import psutil
import helper
import mpaths
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def setFolder(main_window):
    dialog_root = tk.Tk()
    dialog_root.withdraw()
    folder = filedialog.askdirectory()
    with open(mpaths.path_file, 'w') as file: file.write(folder)
    messagebox.showinfo("","Path saved, go start Minify again.")
    main_window.destroy()

# this class is called with getattr method and calls all functions here alphabetically
# use naming convention (a_, b_, c_ ...etc) to run this class top to bottom if order mattters

class MyClass:
    def __init__(self, checkboxes, main_window):
        self.checkboxes = checkboxes
        self.toggle_flag = False
        self.main_window = main_window

    def a_isSteamFound(self):
        if mpaths.steam_dir == "":
            mpaths.toggle_flag = True
            print("Error: 'Steam is not installed on this system.")

    def b_isDotaInstallFound(self):
        dota2path = os.path.join(mpaths.steam_dir, "steamapps\\common\\dota 2 beta\\game\\bin\\win64\\dota2.exe")

        if not os.path.exists(dota2path):
            self.toggle_flag = True
            
            message_root = tk.Tk()
            message_root.withdraw()
            messagebox.showinfo("",f"Dota2 not found in '{dota2path}' ---- Select where your 'SteamLibrary' folder is. For example 'D:\SteamLibrary'")
            message_root.destroy()
            setFolder(self.main_window)
            
    def c_isMinifyFolderPresent(self):
        if not os.path.exists(mpaths.dota_minify):
            os.makedirs(mpaths.dota_minify)

    def d_isDotaRunning(self):
        if "dota2.exe" in (p.name() for p in psutil.process_iter()):
            self.toggle_flag = True
            print("Error: Please close Dota 2 and restart Minify.")

    def e_isDecompilerFound(self):
        if not os.path.exists(os.path.join(mpaths.minify_dir, 'Decompiler.exe')):
            self.toggle_flag = True
            print("Error: 'Decompiler.exe' not found, click Help for instructions.")
    
    def f_isDllFound(self):
        if not os.path.exists(os.path.join(mpaths.minify_dir, 'libSkiaSharp.dll')):
            self.toggle_flag = True
            print("Error: 'libSkiaSharp.dll' not found, click Help for instructions.")

    def g_isCompillerFound(self):
        if not os.path.exists(mpaths.resource_compiler):
            helper.workshop_installed == False
            print("Styling mods have been disabled.")
            print("Install Steam Workshop Tools to use them. Click Help for instructions.")
        else:
            helper.workshop_installed = True

    def h_verifyMods(self):
        for folder in mpaths.mods_folders:
            mod_path = os.path.join(mpaths.mods_dir, folder)

            if not os.path.exists(os.path.join(mod_path, 'files')):
                self.toggle_flag = True
                print("Missing 'files' folder in 'mods/{}'".format(folder))
            if not os.path.exists(os.path.join(mod_path, 'blacklist.txt')):
                self.toggle_flag = True
                print("Missing 'blacklist.txt' folder in 'mods/{}'".format(folder))
            if not os.path.exists(os.path.join(mod_path, 'styling.txt')):
                self.toggle_flag = True
                print("Missing 'styling.txt' folder in 'mods/{}'".format(folder))