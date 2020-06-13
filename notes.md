branch to get the script working in steam proton + xpra.   

xpra does not have vulkan support. I needed to disable proton's use of vulkan in favor of wined3d.
the game was very laggy. messing around with the config, I found out that disabling d3d11 worked.
Now, it was kind of blurred. adding WINE_FULLSCREEN_INTEGER_SCALING did the trick. 

I am running a xpra server with openbox window manager and steam ngu in display :1 
need to change user_settings.py in steam proton directory. 

Now it seems to be running well. 

Note that kongregates colors and steam colors are slightly differente. I will need to tweak that once again, but for now, the speedrunning script is working.

https://lists.devloop.org.uk/pipermail/shifter-users/2019-July/002365.html  
https://github.com/ValveSoftware/Proton

Needed for the script in Arch-based distros:  
`sudo pacman -S tk scrot` -> tkinter and scrot  

Add this to launch settings in steam:  
`DISPLAY=:100 PROTON_USE_WINED3D=1 PROTON_NO_D3D11=1 WINE_FULLSCREEN_INTEGER_SCALING=1 %command%`  

