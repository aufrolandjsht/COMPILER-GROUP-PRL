import requests

def get_pokemon_stats(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception("Pokemon not found")
    data = res.json()
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    return stats

if __name__ == "__main__":
    print(get_pokemon_stats("bulbasaur"))
