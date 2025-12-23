import app
import json

def main(config_path: str = "config.json") -> None:
    config: app.Config = json.load(open(config_path))

    app.run(config)

if __name__ == "__main__":
    main()
