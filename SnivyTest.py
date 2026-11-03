import pandas as pd
from rustworkx.rustworkx import hits
from scipy.constants import hp

import TurnTaker
# Test to make sure everything is right and well
pokemon=pd.read_csv("pokemon/pokemonB&W.csv")

# Snivy is my favorite pokemon. This sees if he is in the dataset
print(pokemon.loc[pokemon["name"] == "Snivy"].T)

#Attack test.

#IMPORTANT: when writing code, .iloc is very imporant. make it that when making a pokemon
Snivy= TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Snivy"].iloc[0], 1)
print(Snivy)
#stunkfish looks silly. So we are gonna kill it
Stunfisk = TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Stunfisk"].iloc[0],1)

#attack based off TurnTaker
print(Stunfisk.hp)

#todo: add https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/moves.csv so can do moves propely
#https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/pokemon_moves.csv to get moves for each pokemon
# Multidata set interactions. Class needs to interact with pokemon.csv to get pokemon id which interacts with pokemon_moves.csv to get move id selection which then interacts with moves.csv to get the power of the move
#snivy's id: 495
#snivy's moves' ids: alot
# Plan: make way for it to parse through move id's, since they show up many times, and just get the power from it. accuracy is maybe
# priotty rn is power
while Stunfisk.hp > 0:
    hit= Snivy.Attack(defender_defense=Stunfisk.defense, defender_type=Stunfisk.type1)
    Stunfisk.hp = Stunfisk.hp-hit
    print(f"{hit} damage dealt to the defenseless {Stunfisk.name}. Health remaining: {Stunfisk.hp}")

print("He is dead now")