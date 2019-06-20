# Speedrunner API

Speedrunner API is a server that stores and retrieves speedrun data, including players, durations, games, and categories.

A Trello board has been established for task tracking and feature scoping, available at:
[Speedrunner-api Trello](https://trello.com/invite/b/da5zQP2d/00359915a05a4a06023ff6c22356cf82/speedrunner-api)


## Installation

This api was built using Python 3.7.3, available at:
[Python 3.7.3](https://www.python.org/downloads/release/python-373/)

Pip as a package manager is required to install Flask dependencies, pip available at: [Pip](https://pip.pypa.io/en/stable/installing/)

```bash
pip install flask flask-jsonify
```

## Usage

Seed data in the form of a csv can be used to init the databases, place in "/data/" and define file path in speedrunner_consts.py.

It is recommended to use the Chrome extension [Poster](https://chrome.google.com/webstore/detail/chrome-poster/cdjfedloinmbppobahmonnjigpmlajcd?hl=en)
 extension on Chrome for testing POST requests.

Start the server by running the following command on the terminal:

```bash
python .\speedrunner_server.py
```

## Testing

## Data Model
The data is stored in a single Sqlite3 database, with the following table/column format:

Games

    id:int

    game:string

Category

    id:int

    category:string

GamesCategories

    id:int

    game_id:int

    category_id:int

Player

    id:int

    player:string

Speedrun

    id:int

    player_id:int

    game_id:int

    category_id:int

    duration:string

## License
[MIT](https://choosealicense.com/licenses/mit/)