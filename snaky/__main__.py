import snaky
import json

def main(config_path: str = "config.json") -> None:
    config: snaky.Config = json.load(open(config_path))

    snaky.app.run(config)
    snaky.pygame.quit()

if __name__ == "__main__":
    main()
