import subprocess

#cmd = 'xpra start-desktop :1 --start="xrandr -s 1400x600" --start=kwin --start=alacritty --speaker=off'
cmd = 'xpra start-desktop :100 --start=kwin_x11 --start=alacritty --speaker=off'
subprocess.run(cmd.split(" "))


#cmd = "xpra control :1 start alacritty"
#subprocess.run(cmd.split(" "))
