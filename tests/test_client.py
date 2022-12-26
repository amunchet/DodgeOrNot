"""
Tests for Client using a separate thread and flask server
    - Functions called on the separate thread won't be counted for coverage
"""
import pytest
import threading
import multiprocessing
import os
import json
import base64

import requests
from flask import Flask, request



import client

app = Flask(__name__)


@app.route("/versions.json")
def version(): # pragma: no cover
    return json.dumps(["1.0.0"])


@app.route("/champion.json")
def champ_ids(): # pragma: no cover
    return json.dumps(
        {
            "type": "champion",
            "format": "standAloneComplex",
            "version": "12.23.1",
            "data": {
                "Aatrox": {
                    "version": "12.23.1",
                    "id": "Aatrox",
                    "key": "266",
                    "name": "Aatrox",
                    "title": "the Darkin Blade",
                    "blurb": "Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find...",
                    "info": {"attack": 8, "defense": 4, "magic": 3, "difficulty": 4},
                    "image": {
                        "full": "Aatrox.png",
                        "sprite": "champion0.png",
                        "group": "champion",
                        "x": 0,
                        "y": 0,
                        "w": 48,
                        "h": 48,
                    },
                    "tags": ["Fighter", "Tank"],
                    "partype": "Blood Well",
                    "stats": {
                        "hp": 650,
                        "hpperlevel": 114,
                        "mp": 0,
                        "mpperlevel": 0,
                        "movespeed": 345,
                        "armor": 38,
                        "armorperlevel": 4.45,
                        "spellblock": 32,
                        "spellblockperlevel": 2.05,
                        "attackrange": 175,
                        "hpregen": 3,
                        "hpregenperlevel": 1,
                        "mpregen": 0,
                        "mpregenperlevel": 0,
                        "crit": 0,
                        "critperlevel": 0,
                        "attackdamage": 60,
                        "attackdamageperlevel": 5,
                        "attackspeedperlevel": 2.5,
                        "attackspeed": 0.651,
                    },
                }
            },
        }
    )


@app.route("/lol-champ-select/v1/session")
def lcu(): # pragma: no cover
    auth = request.headers.get("Authorization")
    password = auth.split("Basic ")[1]
    decoded = base64.b64decode(password).decode("utf-8")
    if decoded == "riot:password":
        return json.dumps({
            "myTeam" : [
                {
                    "championId" : 266
                }
            ],
            "theirTeam" : [
                {
                    "championId" : 266
                }
            ]
        })


@app.route("/lol-champ-select/v1/session-notworking")
def not_working_lcu(): # pragma: no cover
    return ""

@app.route("/shutdown")
def shutdown(): # pragma: no cover
    def shutdown_server(): 
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        func()

    shutdown_server()
    return "Server shutting down..."


def run_server(): # pragma: no cover
    app.run()


@pytest.fixture(scope="session", autouse=True)
def setup():

    # Create lockfile
    with open("lockfile-temp", "w") as f:
        f.write("12:23:5000:password")

    proc = multiprocessing.Process(target=run_server, args=())
    proc.start()
    yield

    # Deletes lockfile
    if os.path.exists("lockfile-temp"):
        os.remove("lockfile-temp")

    # Shut down the server when the thread rejoins the main thread
    requests.get("http://localhost:5000/shutdown")
    proc.terminate()


def test_version(setup):
    """
    Tests Listing the Version
    """
    assert client.find_current_version("http://localhost:5000/versions.json") == "1.0.0"


def test_champ_ids(setup):
    """
    Tests Listing Champ Ids
    """
    a = client.list_champ_ids("http://localhost:5000/champion.json")
    assert a == {"266" : "aatrox"}

def test_read_lobby(setup):
    """
    Test reading the lockfile + LCU
    """
    a = client.read_lobby(
        "lockfile-temp",
        "http://localhost:5000/lol-champ-select/v1/session-notworking"
    )
    assert a == {
        "us" : [],
        "them" : []
    }
    
    a = client.read_lobby(
        "lockfile-temp",
        "http://localhost:5000/lol-champ-select/v1/session"
    )
    assert a == {
        "us" : ["aatrox"],
        "them" : ["aatrox"]
    }