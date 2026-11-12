import pandas as pd
from kagglesdk.competitions.types.team import Team
import random

from six import moves

import TurnTaker

pokemon=pd.read_csv("pokemon/pokemonB&W.csv")
#adds another collumn that algorthim will use to determine which pokemon is better than others.
# at first its zero, but will get filled
# as soon as boss is defeated, algo should end

pokemon["score"] = 0.0 #Score it determined by taking pokemon health at end of a battle and dividing it by the product of boss health and turns

boss=pd.read_csv("pokemon/Arceus.csv")
#lets try just between the main four starters:
Snivy = TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Snivy"].iloc[0], 1)
Tepig = TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Tepig"].iloc[0], 1)
Oshawott  = TurnTaker.pokemon(pokemon.loc[pokemon["name"] == "Oshawott"].iloc[0], 1)
#put them in a team
Team1= [Snivy,Tepig,Oshawott]

#add the bosss to fight and (probably) die too
Arceus=TurnTaker.pokemon(boss.loc[boss["name"] == "Arceus"].iloc[0], 100)

#let battle commence
move=0
while Team1[0].hp >0 or Team1[1].hp >0 or Team1[2].hp >0:
    for member in Team1:
        if member.hp <=0:
            continue
        hit= member.Attack(Arceus)
        print(f" {member.name} attacks with {member.BestAttack}! Dealing {hit}dmg to {Arceus.name}! {Arceus.hp}hp remaining")
    for member in Team1:
        if member.hp <= 0:
            continue
        hit= Arceus.Attack(member)
        print(f" {Arceus.name} attacks with {Arceus.BestAttack}! Dealing {hit}dmg to {member.name}! {member.hp}hp remaining!")
        break

    move= move+1
#battle ends, stats are assigned
for member in Team1:
    member.AdjustScore(Arceus,turn=move)
    #assigns score to the pandas df
    pokemon.loc[pokemon["name"] == member.name, "score"] = member.score

#since last team failed, remove all members and start anew
Team1.clear()

#assign new, better (should be-) team
# does this by looking in dataset, and getting best 3 highest scores.
best_of_best = pokemon.sort_values(by="score", ascending=False)
mate1 = TurnTaker.pokemon(best_of_best.iloc[0], 64)
mate2 = TurnTaker.pokemon(best_of_best.iloc[1], 64)
mate3 =TurnTaker.pokemon(best_of_best.iloc[2], 64)
Team1 = [mate1,mate2,mate3]
for fella in Team1:
    print(fella.name)

