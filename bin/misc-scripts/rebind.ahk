#NoEnv 
#SingleInstance Force
SendMode Input 
SetWorkingDir %A_ScriptDir% 

NumpadClear::suspend

#If WinActive("ahk_exe dota2.exe")
toggle:= 0
~Enter::
 toggle := !toggle
return
#If WinActive("ahk_exe dota2.exe") AND toggle=0
Space::LAlt
