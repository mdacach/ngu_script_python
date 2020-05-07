branch to get the script working in steam proton + xpra.   

xpra does not have vulkan support. I needed to disable proton's use of vulkan in favor of wined3d.
the game was very laggy. messing around with the config, I found out that disabling d3d11 worked.
Now, it was kind of blurred. adding WINE_FULLSCREEN_INTEGER_SCALING did the trick. 

I am running a xpra server with openbox window manager and steam ngu in display :1 
need to change user_settings.py in steam proton directory. 

Now it seems to be running well. 

Note that kongregates colors and steam colors are slightly differente. I will need to tweak that once again, but for now, the speedrunning script is working.
