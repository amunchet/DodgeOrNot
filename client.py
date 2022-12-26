"""
Chat GPT Prompts:
    - Using python and the Riot Games API LCU, list the current champions selected in champ select  and determine champion name based on the resultant id
    - Using python and the riot LCU api, list all champion ids

"""
import requests
import base64

def find_current_version(url=""):
    if url == "": # pragma: no cover
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
    a = requests.get(url)
    return a.json()[0]

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

    return output

def read_lobby(lockfile, url=""):
    """
    Reads lobby with Riot Client API
    """
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
    print(headers)

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
        return lobby
    
    if "myTeam" in data:
        for player in data["myTeam"]:
            if str(player["championId"]) != "0":
                print(f"Our Champion: {champs[str(player['championId'])]}")
                lobby["us"].append(champs[str(player["championId"])])

    if "theirTeam" in data:
        for player in data["theirTeam"]:
            if str(player["championId"]) != "0":
                print(f"Their Champion: {champs[str(player['championId'])]}")
                lobby["them"].append(champs[str(player["championId"])])
    
    return lobby
