# Defeating-Arceus-Algorithm
A collection of three algorithms to find the best Pokémon team to defeat Arceus, aka the god of the Pokémon universe.

## Overiew
Computational Problem: there are alot of pokemon, and to shorten compute time we only work with black and white. The **inputs** for the algorthims are as follows:
- Pokemon (Including Attack, health, defense, type, weakeness, and speed)
- The attack of each pokemon is simplifed to one attack move. This attack move is ran through a damage calcuator which takes into thought randomness and the defender's health, weakenesses, and type

When the above inputs are put in, the algorthim run throughs TurnTaker's battle method. Which **output**s the following:
- Defender's total health minus damage. Automatcily chaning the defender's health.
- After every battle, the pokemon get's a score based off how well they did.

An opmtial soltuion would be a team of three pokemon who can consitently beat Arceus with the fewest turns possible. The score is what tracks this.

## Team responsiblies
- Combs: Making TurnTaker class and thrid algorthim. Readme.md, some dataset cleanup, and slides

## Algorithms used
1: Greedy Monte Carlo
- This algorthom goes through indvidual battles against Aresus. Each battle contains 1 pokemon, and each pokemon does n battles. The amount of wins in n is diveded by n. If the result of that is 1, then the pokemon is added to the team. Once 3 pokemon are selected, the algorthim ends. The reasoning behind this is, if 3 pokemon have a 100% win rate against god, then the team will win in the fewest amont of turns regardless of pokemon due to the collective strength of 3 100% pokemons.

2: Genetic
- template

3: Brute Force
- template

## Running yourself
simply download the python files, and follow run instructions in runalgos.md

## Results
Algorthims are evalauted based off the team's collective scores (all pokemone's indisvual scores are added together and divided by team number). Results can be found in results.txt. 

## Generarive AI
ChatGPT was used in bug testing and advice on progamming logic and why MinMan wasn't a good choice, Along with what algorthim it actually was, in the Monte Carlo Greedy Algorithim.

## Dataset
We'll get our data from the Kaggle dataset "ultimate-pokmon-dataset-2025"
Battles are based off the battle formula from https://bulbapedia.bulbagarden.net/wiki/Damage
Dataset for moves that pokemon can do is attained from: https://github.com/veekun/pokedex
