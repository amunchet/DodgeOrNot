"""
Chat GPT prompt: 
    - Write a python program that calls a graphql endpoint found in the variable graphql_url.  It queries v2CounteriwthCounterStatsPage with the variables $friendlyNameClean (which is a string) and $enemyNameClean (which is a string).  It receives back ["data"]["v2ChampionWithChampion"]["winRate"]
"""
import logging
import requests
from typing import List
from itertools import combinations

graphql_url = "https://www.mobachampion.com/graphql"

logger = logging.getLogger("dodgeOrNot_logger")

def graphql(friendly_name_clean, enemy_name_clean):
    """ """

    # Define the GraphQL request payload
    payload = {
        "query": 'query v2CounterWithCounterStatsPage($friendlyNameClean: String!,\n                  $enemyNameClean: String!,\n                  $language: String!,\n                  $tier: String = "all") {\n                  v2ChampionWithChampion(\n                    query: {friendlyNameClean: $friendlyNameClean,\n                      enemyNameClean: $enemyNameClean,\n                      language: $language,\n                      tier: $tier}\n                  ) {\n                    friendlyNameClean\n                    friendlyName\n                    friendlyTierLetter\n                    friendlyTags\n                    friendlyDamageDealt{\n                      physical\n                      magical\n                      true\n                    }\n                    friendlyPlayStyle{\n                      difficulty\n                      attack\n                      magic\n                      utility\n                      defense\n                    }\n                    enemyNameClean\n                    enemyName\n                    enemyTierLetter\n                    enemyTags\n                    enemyDamageDealt{\n                      physical\n                      magical\n                      true\n                    }\n                    enemyPlayStyle{\n                      difficulty\n                      attack\n                      magic\n                      utility\n                      defense\n                    }\n                    guide{\n                      playingAs\n                      playingAgainst\n                    }\n                    tier\n                    possibleTiers\n                    summaries{\n                      method\n                      matchup\n                      stats\n                      whoIsBetter\n                      furtherInsights\n                    }\n                    numAnalyzed\n                    winRate\n                    pickRate\n                    kda\n                    strongAgainst{\n                      nameClean\n                      name\n                      winRate\n                    }\n                    weakAgainst{\n                      nameClean\n                      name\n                      winRate\n                    }\n                    topSynergies{\n                      nameClean\n                      name\n                      winRate\n                      numAnalyzed\n                    }\n                    championStatComparison{\n                      f\n                      e\n                      name\n                      direc\n                    }\n                    build{\n                      winRate\n                      summonerSpells{\n                        nameClean\n                        name\n                      }\n                      skillOrder{\n                        first\n                        second\n                        third\n                        order\n                      }\n                      primaryRuneSet{\n                        id\n                        name\n                        runes{\n                          id\n                          name\n                          active\n                          row\n                        }\n                      }\n                      secondaryRuneSet{\n                        id\n                        name\n                        runes{\n                          id\n                          name\n                          active\n                          row\n                        }\n                      }\n                      coreItems{\n                        id\n                        name\n                      }\n                      perks{\n                        offense{\n                          id\n                          name\n                        }\n                        flex{\n                          id\n                          name\n                        }\n                        defense{\n                          id\n                          name\n                        }\n                      }\n                      starterItems{\n                        id\n                        name\n                      }\n                      earlyItems{\n                        id\n                        name\n                      }\n                      optionalItems{\n                        id\n                        name\n                        description\n                      }\n                    }\n                    abilityDetails{\n                      q{\n                        name\n                        description\n                        cooldown\n                        cost\n                      }\n                      w{\n                        name\n                        description\n                        cooldown\n                        cost\n                      }\n                      e{\n                        name\n                        description\n                        cooldown\n                        cost\n                      }\n                      r{\n                        name\n                        description\n                        cooldown\n                        cost\n                      }\n                      p{\n                        name\n                        description\n                        cooldown\n                        cost\n                      }\n                    }\n                  }\n                }\n            ',
        "variables": {
            "friendlyNameClean": f"{friendly_name_clean}",
            "enemyNameClean": f"{enemy_name_clean}",
            "tier": "all",
            "position": "all",
            "language": "en",
        },
    }

    # Send the GraphQL request
    response = requests.post(graphql_url, json=payload)
    try: 
        answer = response.json()["data"]["v2ChampionWithChampion"]["winRate"]
        logger.debug(f"Winrate for {friendly_name_clean} and {enemy_name_clean}: {answer}")
        return answer
    except Exception:
        logger.error(f"Error in response: {response.text}, with {friendly_name_clean} and {enemy_name_clean}")
        raise Exception(f"Error in response: {response.text}, with {friendly_name_clean} and {enemy_name_clean}")


def check_synergies(team: List[str]):
    """
    Check the team Champs for synergy
        - This will be done for both our team and the enemy team
    """
    def cleanup(name:str):
        return name.lower().replace(" ", "")
    

    result = 0
    idx = 0
    for (champ_a, champ_b) in combinations(team, 2):
        output = (graphql(cleanup(champ_a), cleanup(champ_b)))
        logger.debug("For", champ_a, "and", champ_b, "the odds of winning together is:", output)
        
        result += output
        idx += 1
    
    if idx == 0:
        idx = 1

    return round(result/idx, 1)
