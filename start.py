import subprocess 

cmd = "xpra start-desktop :1 --start=openbox" 
subprocess.run(cmd.split(" "))


cmd = "xpra control :1 start alacritty" 
subprocess.run(cmd.split(" ")) 

