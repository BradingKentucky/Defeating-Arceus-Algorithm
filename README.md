# Defeating-Arceus-Algorithm
A collection of three algorithms to find the best Pokémon team to defeat Arceus, aka the god of the Pokémon universe.

## Overiew
Computational Problem: there are alot of pokemon, and to shorten compute time we only work with black and white. The inputs for the algorthims are as follows:
- Pokemon (Including Attack, health, defense, type, weakeness, and speed)
- The attack of each pokemon is simplifed to one attack move. This attack move is ran through a damage calcuator which takes into thought randomness and the defender's health, weakenesses, and type
When the above inputs are put in, the algorthim run throughs TurnTaker's battle method. Which outputs the following:
- Defender's total health minus damage. Automatcily chaning the defender's health.
After every battle, the pokemon get's a score based off how well they did.

An opmtial soltuion would be a team of three pokemon who can consitently beat Arceus with the fewest turns possible.

## Team responsiblies
- Combs: Making TurnTaker class and thrid algorthim

## Algorithms used
1: Greedy Monte Carlo
2: Genetic
3: Brute Force

## Dataset
We'll get our data from the Kaggle dataset "ultimate-pokmon-dataset-2025"
Battles are based off the battle formula from https://bulbapedia.bulbagarden.net/wiki/Damage
Dataset for moves that pokemon can do is attained from: https://github.com/veekun/pokedex