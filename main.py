import time

import client
import stats

current_lobby = {
    "us" : [],
    "them": [],
}

loop_check = True

while(loop_check):
    new_lobby = client.read_lobby()
    if new_lobby != current_lobby:
        print()
        print("Our chances:", stats.check_synergies(new_lobby["us"]))
        print("Their chances:", stats.check_synergies(new_lobby["them"]))
        print()

        if len(new_lobby["us"]) == 5 and len(new_lobby["them"]) == 5:
            loop_check = False

    time.sleep(5)