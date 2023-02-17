<!-- PROJECT LOGO -->
<h1 align="center">
  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="bin/images/logo.png" alt="Markdownify" width="150"></a>
  <br>
  Dota 2 Minify
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg">
</p>

<h4 align="center" style="font-weight: bold;">Automation and Modding Tool for Dota 2</h4>

<br>

<p align="center" style="font-size: 16px">
  <span>✔️500+ Spells Simplified •</span>
  <span>✔️7,000+ mods •</span>
  <span>✔️Boost FPS •</span>
  <span>✔️Creator Toolkit •</span>
  <span>✔️Active Development</span>
</p>

<p align="center">
    <img src="bin/images/screenshot-1.png">
    <img src="bin/images/screenshot-2.png">
    <img src="bin/images/screenshot-3.png">
    <!-- <img src="bin/images/gui.png"> -->
</p>

<!-- [![Benchmark](https://i.imgur.com/Lglso6f.pngg)](https://www.youtube.com/watch?v=0TuS7qbgsQQ") -->

|                               Benchmark (click to play)                               |         App (click to zoom)          |
| :-----------------------------------------------------------------------------------: | :----------------------------------: |
| [![](https://i.imgur.com/Lglso6f.pngg)](https://www.youtube.com/watch?v=0TuS7qbgsQQ") | ![](https://i.imgur.com/brFM4HX.jpg) |

<hr>

## :rocket: Installation

[Dota 2 Workshop Tools](https://developer.valvesoftware.com/wiki/Dota_2_Workshop_Tools) must be installed to use mods that edit the Interface like "Minify HUD". You can skip step 1 if you don't want those.

1. Right-click on Dota 2 in Steam and select **Properties** > **DLC** then install **"Dota 2 Workshop Tools DLC"**

2. [Click here and download latest Minify(Full)](https://github.com/robbyz512/dota2-minify/releases)

3. Extract zip file and run Minify.exe

4. Patch gameinfo using [Dota2Patcher by Wolf49406](https://github.com/Wolf49406/Dota2Patcher/releases)

5. Go play dota2!

<hr>

Optional: If you want to manually get Decompiler.exe and libSkiaSharp.dll

1. Open https://github.com/SteamDatabase/ValveResourceFormat/releases

2. Download "Decompiler-windows-x64.zip" (version: 0.2.0.864)

3. Extract both files into Minify folder.

Optional: To compile project from source [Click Here for instructions](https://github.com/robbyz512/dota2-minify/wiki/Minify#compiling-minify)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ABOUT THE PROJECT -->

## :books: Developing Your Own Mods

### Loading custom mods is disabled in stable branch and is under development.

[The wiki](https://github.com/robbyz512/dota2-minify/wiki) will teach you the basics of working with steam files and more.

Once you get comfortable with the tools you can use Minify to patch them quickly.

## :open_file_folder: Minify File Structure

| Name                                                                                  | Description                                                                                   |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [`Files`](https://github.com/robbyz512/dota2-minify/wiki/Minify#files)                | Compiled files you want to pack (Models, Meshes, Textures...etc)                              |
| [`blacklist.txt`](https://github.com/robbyz512/dota2-minify/wiki/Minify#blacklisttxt) | _Paths_ to files to replace with blanks so they wont appear in game (Particles, Sounds...etc) |
| [`styling.txt`](https://github.com/robbyz512/dota2-minify/wiki/Minify#stylingtxt)     | Custom CSS you want to apply to the Panorama (Interfaces, Layouts, HUD's...etc)               |
| `notes.txt`                                                                           | Optionally include this file to have a details button beside your mod for users to read.      |

[Click here to do the Beginner Mod Tutorial](https://github.com/robbyz512/dota2-minify/wiki/Minify#create-your-first-mod-tutorial)

<hr>

<div align="center">

## :video_game: Community

<a href="https://discord.gg/2YDnqpbcKM"><img style="margin-right: 10px" src="https://img.shields.io/badge/Discord-%237289DA.svg?style=for-the-badge&logo=discord&logoColor=white"></a>
<a href="https://github.com/robbyz512/dota2-minify/wiki"><img src="https://img.shields.io/badge/Github_Wiki-%23000000.svg?style=for-the-badge"></a>

<br>

</div>

<hr>

## :wrench: Features under development

-   ⚙️Smaller Spells & Items Mod. (Current one mods nearly every item and spell)
-   ⚙️Swapping terrain tileset with other textures
-   ⚙️Remove all cosmetic items
-   ⚙️Remove taunts/tipping/hero voice lines/anything else annoying.
-   ⚙️Upload your own main menu background
-   ⚙️Swap hero/item sounds with your own audio files.
-   ⚙️Tree mod and Dark Terrain for immortal gardens map.

## 🔨 Next version of Minify under development

-   ⚙️Built with [Svelte](https://github.com/sveltejs/svelte) and [Pywebview](https://github.com/r0x0r/pywebview)
-   ⚙️Much more mod specific customization
-   ⚙️Mod plugins, mod development more intuitive
-   Join Discord if you would like to help develop!

![alt text](https://i.imgur.com/chp63hH.png)
![alt text](https://i.imgur.com/Dn4hD69.png)

<p align="right">(<a href="#top">back to top</a>)</p>
