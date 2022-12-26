import requests
import stats

def test_graphql():
    """
    Tests GraphQL Call
    """
    found = False
    try:
        stats.graphql("Viktor", "LEESIN")
    except Exception:
        found = True
    
    assert found

    assert stats.graphql("viktor", "leesin") > 0

def test_check_synergies():
    """
    Tests checking synergies
    """
    team = ["viktor", "leesin", "olaf"]
    a = stats.check_synergies(team)

    team2 = ["viktor", "olaf"]
    b = stats.check_synergies(team2)
    
    assert a > 0
    assert b > 0
    
    assert a != b

    team3 = []
    c = stats.check_synergies(team3)
    assert c == 0

