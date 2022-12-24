import time

import client
import stats

current_lobby = {
    "us" : [],
    "them": [],
}
while(1):
    new_lobby = client.read_lobby()
    if new_lobby != current_lobby:
        print()
        print("Our chances:", stats.check_synergies(new_lobby["us"]))
        print("Their chances:", stats.check_synergies(new_lobby["them"]))
        print()

    time.sleep(5)