from conf_button import *
from threading import Thread
# To set the tasks for startup

# add_startup_callbacks(some_func, arg1, arg2, ...)
add_startup_callbacks(print, "arg3", "arg4")
# add_pause_callbacks(some_func, arg1, arg2, ...)
add_pause_callbacks(print, "arg3", "arg4")


# this needs to run on a thread
def working_thread()
    button_states()


button_th = Thread(target=working_thread)
button_th.start()

# if you need to changes states:
set_active()
set_ready()
set_error()