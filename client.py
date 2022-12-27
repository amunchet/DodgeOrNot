"""
Chat GPT Prompts:
    - Using python and the Riot Games API LCU, list the current champions selected in champ select  and determine champion name based on the resultant id
    - Using python and the riot LCU api, list all champion ids

"""
import logging
import requests
import base64

logger = logging.getLogger("dodgeOrNot_logger")

def find_current_version(url=""):
    if url == "": # pragma: no cover
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
    a = requests.get(url)
    version = a.json()[0]
    logger.debug(f"[Client] Current version:{version}")
    return version

def list_champ_ids(url=""):
    """
    Lists all champ ids
    """
    if url == "": # pragma: no cover
        url = f"http://ddragon.leagueoflegends.com/cdn/{find_current_version()}/data/en_US/champion.json"
    
    request = requests.get(
        url,
    )
    data = request.json()
    output = {}
    for x in data["data"].keys():
        output[data["data"][x]["key"]] = x.lower()

    output_len = len(output)
    logger.debug(f"[Client][Champion Ids] Have : {output_len} number of champions")
    return output

def read_lobby(lockfile, url=""):
    """
    Reads lobby with Riot Client API
    """
    logger.debug(f"[Read Lobby] Lockfile: {lockfile}")
    champs = list_champ_ids()

    with open(lockfile) as f:
        items = f.read()
    
    items = items.split(":")

    port = items[2]
    password = 'riot:' + items[3]

    password = base64.b64encode( password.encode("utf-8"))

    headers = {
        "Host" : f"127.0.0.1:{port}",
        "Authorization" : f"Basic {password.decode('utf-8')}",
        "User-Agent" : "insomnia/7.1.1",
        "Accept" : "*/*"
    }
    logger.debug(f"[Read Lobby] Headers: {headers}")

    if url == "": # pragma: no cover
        url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"

    request = requests.get(
        url,
        headers=headers,
        verify=False
    )
    
    lobby = {
        "us" : [],
        "them" : []
    }
    try:
        data = request.json()
    except Exception:
        logger.debug(f"[Read Lobby] Had an error in reading json: {request.text}")
        return lobby
    
    if "myTeam" in data:
        for player in data["myTeam"]:
            if str(player["championId"]) != "0":
                logger.debug(f"Our Champion: {champs[str(player['championId'])]}")
                lobby["us"].append(champs[str(player["championId"])])

    if "theirTeam" in data:
        for player in data["theirTeam"]:
            if str(player["championId"]) != "0":
                logger.debug(f"Their Champion: {champs[str(player['championId'])]}")
                lobby["them"].append(champs[str(player["championId"])])
    
    return lobby
