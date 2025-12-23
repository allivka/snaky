# Snaky

Simple snake game written in python for practice

## Dependencies

Uses poetry as dependency management system and needs a pygame library

## installing Running

1. Firstly install poetry dependency management tool.
Pipx example: ```pipx install poetry ```

2. You also need python. Its version 3.13 was used during development(also i know that ny version below 3.10 is incompatible).
Pacman example: ```sudo pacman -Sy python```

3. To install required dependencies simply run: ```poetry install```

4. Then run with: ```PYGAME_HIDE_SUPPORT_PROMPT='hide' poetry run python snaky```

5. Instead of points 3 and 4 you can simply execute run.sh script: ```chmod +x ./run.sh && ./run.sh```


## Configuration

Most common options for configuration are located in config.json file and can be easily edited.
Options that are most likely to be edited are located at the top of json file and separated from other with plenty of blak lines.
Nothing restricts from you changing anything though.
