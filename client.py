import requests
import base64

def read_lobby():
    """
    Reads lobby with Riot Client API
    """
    lockfile = "D:\\Riot Games\\League of Legends\\lockfile"

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

    url = "lol-champ-select/v1/session"

    request = requests.get(
        f"https://127.0.0.1:{port}/{url}",
        headers=headers,
        verify=False
    )
    data = request.json()
    print(data)
    if "myTeam" in data:
        for player in data["myTeam"]:
            print(f"Champion: {player['championId']}")

    if "theirTeam" in data:
        for player in data["theirTeam"]:
            print(f"Champion: {player['championId']}")
