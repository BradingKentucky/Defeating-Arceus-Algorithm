import pandas as pd
from gallery_dl.util import true
from kagglesdk.competitions.types.team import Team
import random

from six import moves

import TurnTaker

pokemon=pd.read_csv("pokemon/pokemonB&W.csv")
#removed legeadnry pokemone. Vicinti's whole gimmick is he always wins
pokemon = pokemon[pokemon["is_legendary"] == 0].copy()

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
mate1 = TurnTaker.pokemon(best_of_best.iloc[0], 10)
mate2 = TurnTaker.pokemon(best_of_best.iloc[1], 10)
mate3 =TurnTaker.pokemon(best_of_best.iloc[2], 10)
Team1 = [mate1,mate2,mate3]
for fella in Team1:
    print(fella.name)

#now we run the whole thing till we get best team. Once every pokemon is fought with, algo gets best scores and prints winning team
TRIALS = 100
TARGET_RATE = 1.0

win = 0
Teams = {}
best_team_names = None
best_rate = -1.0
best_three = []
while win != 3:
    battleWin = 0
    team_hp = Team1[0].hp

    for _ in range(TRIALS):
        # Reset HP for each trial.
        Team1[0].hp = team_hp
        Arceus.hp = 120
        print("Starting:", [(member.name, member.hp) for member in Team1])

        while Arceus.hp > 0 and Team1[0].hp > 0:
            Team1[0].Attack(Arceus)

            # Arceus attacks if it's still alive.
            if Arceus.hp > 0 and Team1[0].hp > 0:
                Arceus.Attack(Team1[0])

        if Arceus.hp <= 0:
            print(
                f"Trial battle: Arceus HP={Arceus.hp}, "
                f"team HP={[member.hp for member in Team1]}, "
                f"wins so far={battleWin}"
            )
            battleWin += 1

    rate = battleWin / TRIALS
    members = (Team1[0].name,)
    Teams[members] = rate

    print(f"Battles counted as wins: {battleWin} out of {TRIALS}")
    print(f"Pokémon {members[0]} win rate: {rate:.1%}")

    if rate > best_rate:
        best_rate = rate
        best_team_names = members

    # Use the win rate as the Pokémon's heuristic score.
    Team1[0].score = rate
    pokemon.loc[pokemon["name"] == Team1[0].name, "score"] = rate

    if rate >= TARGET_RATE:
        win = win+1
        best_team_names = members
        best_rate = rate
        best_three.append(Team1[0].name)
        print("Target win rate reached.")

    best_of_best = (
        pokemon.sort_values(by="score", ascending=False)
        .reset_index(drop=True)
    )
    tested_teams = {frozenset(team) for team in Teams}

    chosen_row = None

    # Find the highest-ranked untested Pokémon.
    for i in range(len(best_of_best)):
        row = best_of_best.iloc[i]
        pokemon_name = row["name"]

        if frozenset([pokemon_name]) not in tested_teams:
            chosen_row = row
            break

    if chosen_row is None:
        print("No untested Pokémon remain.")
        break

    Team1 = [TurnTaker.pokemon(chosen_row, 64)]

print(f"\nBest Pokémon Team found: {best_three}")
print(f"Win rate: {best_rate:.1%}")

