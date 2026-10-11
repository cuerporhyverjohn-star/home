import time
import threading

try:
    import RPi.GPIO as GPIO
    LIB_AVAILABLE = True
except (ImportError, RuntimeError):
    LIB_AVAILABLE = False
    print("[pir] RPi.GPIO not available — simulation mode active")

import random

PIR_PINS = {
    "zone_1": 17,
    "zone_2": 27,
    "zone_3": 22,
}

SIMULATION_MODE = not LIB_AVAILABLE
_lock = threading.Lock()
_setup_done = False


def setup_pir_sensors():
    global _setup_done, SIMULATION_MODE
    if not LIB_AVAILABLE:
        return False
    try:
        GPIO.setmode(GPIO.BCM)
        for name, pin in PIR_PINS.items():
            GPIO.setup(pin, GPIO.IN)
        _setup_done = True
        print("[pir] HC-SR501 sensors ready on pins: " + str(PIR_PINS))
        return True
    except Exception as e:
        print("[pir] Setup error: " + str(e) + " — falling back to simulation")
        SIMULATION_MODE = True
        return False


def read_pir_states():
    """Returns dict of {zone_name: bool} for motion detected per zone."""
    if SIMULATION_MODE or not _setup_done:
        return {name: random.random() < 0.3 for name in PIR_PINS}
    try:
        with _lock:
            return {name: bool(GPIO.input(pin)) for name, pin in PIR_PINS.items()}
    except Exception as e:
        print("[pir] Read error: " + str(e))
        return {name: False for name in PIR_PINS}


def get_pir_activity_score():
    """Returns 0.0-1.0 score based on how many zones currently show motion."""
    states = read_pir_states()
    if not states:
        return 0.0
    active_count = sum(1 for v in states.values() if v)
    return round(active_count / len(states), 3)


def cleanup_pir():
    if LIB_AVAILABLE and _setup_done:
        try:
            GPIO.cleanup()
        except Exception:
            pass
