# Pikasearch ---- A pokemon search engine!

import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_data(pokemon_name):
    url = f"{base_url}/pokemon/{pokemon_name}"

    response = requests.get(url)

    if response.status_code == 200:
        information = response.json()
        print("Retrieved data for Pokémon:", pokemon_name.capitalize() + "!")
        return information
    else:
        print("Pokémon not found. Please check the name and try again.")


def main():
    pokemon_name = input("Enter the name of the Pokémon: ").strip().lower()
    pokemon_info = get_pokemon_data(pokemon_name)

    if pokemon_info:
        print("\n--- Pokémon Information ---")

        print(f"{pokemon_info['name'].capitalize()} is the name of that Pokémon! (ID: {pokemon_info['id']})")

        print(f"{pokemon_info['height']} is " + pokemon_name.capitalize() + "'s height!")

        print(f"{pokemon_info['weight']} is " + pokemon_name.capitalize() + "'s weight!")

if __name__ == "__main__":
    while True:
        main()