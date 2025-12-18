from .gameModule import *
import json

def main(config_path: str = "config.json") -> None:
    c: Config = json.load(open(config_path))
    game: Game = Game(c)

    # print(f"Initialized new game instance from {str} configuration file:\n\n{game}")

    game.play()
