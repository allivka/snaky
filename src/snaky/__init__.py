from .gameModule import *
import json

def main(config_path: str = "config.json") -> None:
    c: Config = json.load(open(config_path))
    game: Game = Game(c)

    game.play()
