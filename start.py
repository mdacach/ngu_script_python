import subprocess 

cmd = "xpra start-desktop :1 --start=kwin" 
subprocess.run(cmd.split(" "))


cmd = "xpra control :1 start alacritty" 
subprocess.run(cmd.split(" ")) 

