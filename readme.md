Developer Requirements:

install Python 3.7.3 from https://www.python.org/downloads/release/python-373/
install pip from https://pip.pypa.io/en/stable/installing/

install packages
pip install flask flask-jsonpify


data model:
Speedrun
    id:string(uuid)
    player_name:string
    duration:integer
    category:string
    game_title:title

Game
    game_title:string
    categories:string[]

Player
    player_name:string
    speedrun_ids:string[] (uuid)
