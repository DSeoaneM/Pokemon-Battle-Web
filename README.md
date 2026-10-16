# POKÉMON BATTLE WEB


## Short description:

Simulation of Pokémon battles with Python and Flask

## Used technologies:

- Python 3.14.7
- Flask 3.1.3

## Functionalities

- Login in the Pokémon Battle Page
- Show the list of selectable Pokémon
- Filter Pokémon by name, types, stats values and/or move type
- Access to detailed information about each Pokémon
- Choose a starter Pokémon to battle

## Web page access

To enjoy all functionalities of POKÉMON BATTLE WEB, a valid trainer name is required.

## Project structure:
```
Pokemon-Battle-Web/
├─ requirements: file with project requirements to rebuild it. List of project libraries and modules with their versions.
├─ README: fthis file containing all project information and updates.
├─ .gitignore: file with rules to determine which file are not uploaded to the repository.
├─ venv/: folder containing the libraries and modules required for the project correct working. Not included in this repository; use the requirements file to recreate it.
├─ data/: folder contianing Pokémon data used in this project in JSON format.
└─ app/ 
    ├─ main.py: file with the Python code to run the project.
    ├─ templates: project html templates.
    └─ static/:
        ├─ css: project CSS style sheets.
        ├─ img: folder with images used in this project.
        ├─ js: project JavaScript functionality files.
        └─ video: introductory video.
```

## Web routes and views

- /: landing page showing a video with available Pokémon used in this webpage.
- /login: register form to access Pokémon list, details and battle screens.
- /pokemons/: list of Pokémon available in this webpage. Filters by name, types, stats and move types are available. Form to choose the Pokémon to start a battle.
- /details: specific features of each Pokémon, including Pokédex number, name, front and back sprites for normal and shiny forms, height, weight, stats and list of moves.
- /battle: work in progress. Schema of Pokémon battle.