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
#copy below format. just change the pokemon name
Serperior= TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Serperior"].iloc[0], 50)
print(Serperior)
#Archeops looks cool. It's also a dinosaur, lets see if we can make it go exixnct again
Stunfisk = TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Stunfisk"].iloc[0],1)

#attack based off TurnTaker
#print(Stunfisk.hp)

#todo: add https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/moves.csv so can do moves propely
#https://github.com/veekun/pokedex/blob/master/pokedex/data/csv/pokemon_moves.csv to get moves for each pokemon

#demonstration of an battle
# Serperior atomoized the Stunfisk before buffs were applied, now its more evenish

while Serperior.hp >0 :
    hit= Serperior.Attack(Stunfisk)
    Stunfisk.hp = Stunfisk.hp-hit
    print(f"{hit} damage dealt with {Serperior.GetBestAttackMoveName()} to the defenseless {Stunfisk.name}. Health remaining: {Stunfisk.hp}")
    if  Stunfisk.hp < 0:
        break
    hit2= Stunfisk.Attack(Serperior)
    Serperior.hp = Serperior.hp - hit
    print(f"{hit2} damage dealt with {Stunfisk.GetBestAttackMoveName()} to the cooler {Serperior.name}. Health remaining: {Serperior.hp}")


print("He is dead now")

#ok lets make this more fair.
