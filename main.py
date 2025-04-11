from game_logic import start_game_loop
from powerpoint_control import wait_for_slideshow_ready

def main():
    wait_for_slideshow_ready()
    start_game_loop()

if __name__ == "__main__":
    main()
