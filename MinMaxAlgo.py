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
TARGET_RATE = 0.90

win = False
Teams = {}
best_team_names = None
best_rate = -1.0

while not win:
    battleWin = 0
    Team1HP, Team2HP, Team3HP = [member.hp for member in Team1]

    for _ in range(TRIALS):
        # Reset HP for each trial.
        Team1[0].hp = Team1HP
        Team1[1].hp = Team2HP
        Team1[2].hp = Team3HP
        Arceus.hp = 120
        print("Starting:", [(m.name, m.hp) for m in Team1])
        move = 0

        while Arceus.hp > 0 and any(member.hp > 0 for member in Team1):
            move += 1

            # Every living Pokémon attacks first.
            for member in Team1:
                if member.hp > 0:
                    member.Attack(Arceus)
                    if Arceus.hp <= 0:
                        break

            # Arceus attacks the first living Pokémon.
            if Arceus.hp > 0:
                target = next(
                    (member for member in Team1 if member.hp > 0),
                    None,
                )
                if target is not None:
                    Arceus.Attack(target)

        if Arceus.hp <= 0:
            print(
                f"Trial belh: Arceus HP={Arceus.hp}, "
                f"team HP={[member.hp for member in Team1]}, "
                f"wins so far={battleWin}"
            )
            battleWin += 1

    rate = battleWin / TRIALS
    members = tuple(member.name for member in Team1)
    team_key = frozenset(members)
    Teams[members] = rate

    print(f"Battles counted as wins: {battleWin} out of {TRIALS}")
    print(f"Team {members} win rate: {rate:.1%}")

    if rate > best_rate:
        best_rate = rate
        best_team_names = members

    # Use the team's win rate as a heuristic score for its members.
    for member in Team1:
        member.score = rate
        pokemon.loc[pokemon["name"] == member.name, "score"] = rate

    # Stop before choosing another team if this one met the target.
    if rate >= TARGET_RATE:
        win = True
        best_team_names = members
        best_rate = rate
        print("Target win rate reached.")
        break

    best_of_best = (
        pokemon.sort_values(by="score", ascending=False)
        .reset_index(drop=True)
    )
    tested_teams = {frozenset(team) for team in Teams}

    chosen_rows = None

    # Find the highest-ranked untested trio.
    for i in range(len(best_of_best)):
        for j in range(i + 1, len(best_of_best)):
            for k in range(j + 1, len(best_of_best)):
                rows = [
                    best_of_best.iloc[i],
                    best_of_best.iloc[j],
                    best_of_best.iloc[k],
                ]
                team_names = tuple(row["name"] for row in rows)

                if frozenset(team_names) not in tested_teams:
                    chosen_rows = rows
                    break
            if chosen_rows is not None:
                break
        if chosen_rows is not None:
            break

    if chosen_rows is None:
        print("No untested team combinations remain.")
        break

    Team1 = [TurnTaker.pokemon(row, 64) for row in chosen_rows]

print(f"\nBest team found: {best_team_names}")
print(f"Win rate: {best_rate:.1%}")
