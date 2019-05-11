from opentrons.drivers.rpi_drivers import gpio
from threading import RLock
from time import sleep, time

STATES = {
    "PLUGIN": 0,
    "STARTUP": 1,
    "READY": 2,
    "ACTIVE": 3,
    "PAUSED": 4,
    "ERROR": 5,
}

INIT_TIME = 200  # ms
HOLD_TIME = 2000  # ms

button_state_lock = RLock()
current_state = STATES["PLUGIN"]


def __set_state(value):
    global current_state
    button_state_lock.acquire()
    current_state = value
    button_state_lock.release()


def __get_state():
    global current_state
    button_state_lock.acquire()
    value = current_state
    button_state_lock.release()
    return value


startup_callbacks = []
pause_callbacks = []


def add_pause_callbacks(func, *args):
    pause_callbacks.append([func, args])


def add_startup_callbacks(func, *args):
    startup_callbacks.append([func, args])


def set_active():
    if __get_state() < STATES["READY"]:
        raise(IOError, "The system is not ready")
    __set_state(STATES["ACTIVE"])
    gpio.set_button_light(green=True)


def set_ready():
    if __get_state() < STATES["READY"]:
        raise(IOError, "The system is not ready")
    __set_state(STATES["READY"])
    gpio.set_button_light(blue=True)


def set_error():
    if __get_state() < STATES["READY"]:
        raise(IOError, "The system is not ready")
    __set_state(STATES["ERROR"])
    gpio.set_button_light(red=True)


def __run_startup():
    __set_state(STATES["STARTUP"])
    # We are going to use magenta instead of orange.
    # For orange we need to use PWM signals.
    gpio.set_button_light(red=True, blue=True)
    for fun, arg in startup_callbacks:
        fun(*arg)
    startup_callbacks.clear()
    __set_state(STATES["READY"])
    gpio.set_button_light(blue=True)


def __run_pause():
    __set_state(STATES["PAUSED"])
    for fun, arg in pause_callbacks:
        fun(arg)
    gpio.set_button_light(green=True, red=True)


def __get_pressed_time():
    current_millis = int(round(time() * 1000))
    elapsed_time = current_millis + 1
    while gpio.read_button()
        elapsed_time = int(round(time() * 1000))
    return elapsed_time - current_millis


def button_states():
    gpio.initialize()
    gpio.set_button_light()  # this make lights off
    while True:
        pressed_time = __get_pressed_time()
        if __get_state() == STATES["PLUGIN"] and pressed_time > INIT_TIME:
            __run_startup()
        elif __get_state() == STATES["ACTIVE"] and pressed_time > HOLD_TIME:  # and time is less than 2 secs:
            set_error()
        elif __get_state() == STATES["ACTIVE"] and pressed_time < HOLD_TIME:  # and time is less than 2 secs:
            __run_pause()
        elif __get_state() == STATES["PAUSED"] and pressed_time < HOLD_TIME: # and time is less than 2 secs:
            set_active()
        elif __get_state() == STATES["PAUSED"] and pressed_time > HOLD_TIME:  # and time is more than 2 secs:
            set_ready()
