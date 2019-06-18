Developer Requirements:

install Python 3.7.3 from https://www.python.org/downloads/release/python-373/
install pip from https://pip.pypa.io/en/stable/installing/

install packages
pip install flask flask-jsonpify

seed data in the form of a csv can be used to init the databases, place in root and define file name in speedrunner_consts.py

recommended to use Poster extension on Chrome for testing POST requests

start the server by running the following command on the terminal:
python .\speedrunner_server.py

data model:
Speedrun
    id:string(uuid)
    player_name:string
    duration:string (time)
    category:string
    game_title:title

Game
    game_title:string
    categories:string[]

Player
    player_name:string
    speedrun_ids:string[] (uuid)
