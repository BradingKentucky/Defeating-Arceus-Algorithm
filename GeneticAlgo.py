"""
Genetic algorithm for the "Defeating Arceus" project (CSC2400).

Problem : pick the team of Pokemon (Black & White pool, neutral stats) that
          defeats Arceus in the FEWEST TURNS.
Chromosome : an ordered team of TEAM_SIZE distinct Pokemon names.
             (order matters: Arceus attacks the first living member, as in MinMaxAlgo.py)
Fitness : mean over several simulated battles (battles are random: damage roll)
          - win  -> 1 + (MAX_TURNS - turns)/MAX_TURNS + small survivor-HP tie-breaker
          - loss -> fraction of Arceus' HP removed (0..1), so partial progress is rewarded
Operators : tournament selection, one-point crossover with duplicate repair,
            per-gene replacement mutation + swap mutation, elitism.

Uses the same files / classes as the rest of the project:
    pokemon/pokemonB&W.csv, pokemon/Arceus.csv, TurnTaker.py

Usage examples
    python GeneticAlgo.py
    python GeneticAlgo.py --pop 100 --gens 60 --runs 10 --seed 1 --out ga_history.csv
"""
import argparse
import copy
import csv
import random
import statistics
import time
from collections import namedtuple

import pandas as pd

import TurnTaker

# ---------------------------------------------------------------- settings
DATA_CSV = "pokemon/pokemonB&W.csv"
BOSS_CSV = "pokemon/Arceus.csv"
BOSS_NAME = "Arceus"

PLAYER_LEVEL = 64      # same level used in MinMaxAlgo.py for every team member
BOSS_LEVEL = 100
MAX_TURNS = 100        # a fight lasting longer than this counts as a loss

Result = namedtuple("Result", "won turns boss_dmg_frac team_hp_frac")
Fitness = namedtuple("Fitness", "value win_rate mean_turns")


# ---------------------------------------------------------------- data
def load_pool():
    """Build one TurnTaker.pokemon per row ONCE (the constructor reads the move
    CSVs, which is slow). Battles then work on cheap copies of these templates."""
    df = pd.read_csv(DATA_CSV)
    df["score"] = 0.0  # TurnTaker.pokemon expects a score field
    pool = {}
    for _, row in df.iterrows():
        if row["name"] in pool:
            continue
        try:
            mon = TurnTaker.pokemon(row, PLAYER_LEVEL)
        except ValueError:          # name not found in the moves dataset
            continue
        if mon.BestAttack is None:  # no damaging move -> can't hurt Arceus
            continue
        pool[mon.name] = mon

    boss_df = pd.read_csv(BOSS_CSV)
    boss_df["score"] = 0.0
    boss = TurnTaker.pokemon(boss_df.loc[boss_df["name"] == BOSS_NAME].iloc[0], BOSS_LEVEL)
    return pool, boss


def _fresh(template):
    """Copy of a template at full HP (templates never fight, so their hp is base hp)."""
    return copy.copy(template)


# ---------------------------------------------------------------- battle
def simulate_battle(team_names, pool, boss_template):
    """Same turn structure as MinMaxAlgo.py: every living member attacks, then
    Arceus attacks the first living member. Stops the moment Arceus faints."""
    team = [_fresh(pool[n]) for n in team_names]
    boss = _fresh(boss_template)
    boss_start = boss.hp
    team_start = sum(m.hp for m in team)

    for turn in range(1, MAX_TURNS + 1):
        for m in team:
            if m.hp > 0:
                m.Attack(boss)
                if boss.hp <= 0:
                    hp_frac = sum(max(x.hp, 0) for x in team) / team_start
                    return Result(True, turn, 1.0, hp_frac)
        target = next((m for m in team if m.hp > 0), None)
        if target is None:
            break
        boss.Attack(target)
        if all(m.hp <= 0 for m in team):
            break
    return Result(False, MAX_TURNS, max(0.0, (boss_start - boss.hp) / boss_start), 0.0)


def evaluate(team_names, pool, boss, trials):
    """Fitness of a team = mean battle value over `trials` random battles."""
    total, wins, win_turns = 0.0, 0, []
    for _ in range(trials):
        r = simulate_battle(team_names, pool, boss)
        if r.won:
            wins += 1
            win_turns.append(r.turns)
            total += 1 + (MAX_TURNS - r.turns) / MAX_TURNS + 0.01 * r.team_hp_frac
        else:
            total += r.boss_dmg_frac
    mean_turns = statistics.mean(win_turns) if win_turns else float("inf")
    return Fitness(total / trials, wins / trials, mean_turns)


# ---------------------------------------------------------------- GA operators
def random_team(names, k):
    return random.sample(names, k)


def tournament(pop, fits, k):
    contenders = random.sample(range(len(pop)), min(k, len(pop)))
    return pop[max(contenders, key=lambda i: fits[i].value)]


def crossover(p1, p2):
    """One-point crossover; duplicates are repaired from the parents' genes."""
    n = len(p1)
    if n < 2:
        return list(p1)
    cut = random.randint(1, n - 1)
    child = list(p1[:cut])
    for g in p2:
        if len(child) < n and g not in child:
            child.append(g)
    for g in p1:
        if len(child) < n and g not in child:
            child.append(g)
    return child


def mutate(team, names, rate):
    team = list(team)
    for i in range(len(team)):
        if random.random() < rate:
            choices = [x for x in names if x not in team]
            if choices:
                team[i] = random.choice(choices)
    if len(team) > 1 and random.random() < rate:   # order mutation
        i, j = random.sample(range(len(team)), 2)
        team[i], team[j] = team[j], team[i]
    return team


# ---------------------------------------------------------------- main GA loop
def run_ga(pool, boss, team_size=3, pop_size=50, generations=40, trials=10,
           mutation_rate=0.15, crossover_rate=0.9, tournament_k=3, elite=2,
           patience=15):
    names = list(pool.keys())
    pop = [random_team(names, team_size) for _ in range(pop_size)]
    history, evals = [], 0
    best_team, best_fit, stale = None, None, 0
    start = time.perf_counter()

    for gen in range(generations):
        fits = [evaluate(t, pool, boss, trials) for t in pop]
        evals += len(pop) * trials
        order = sorted(range(len(pop)), key=lambda i: fits[i].value, reverse=True)
        gen_best = fits[order[0]]

        if best_fit is None or gen_best.value > best_fit.value + 1e-9:
            best_team, best_fit, stale = list(pop[order[0]]), gen_best, 0
        else:
            stale += 1

        history.append({
            "generation": gen,
            "best_fitness": gen_best.value,
            "mean_fitness": statistics.mean(f.value for f in fits),
            "best_win_rate": gen_best.win_rate,
            "best_mean_turns": gen_best.mean_turns,
            "best_team": " | ".join(pop[order[0]]),
            "battles_so_far": evals,
        })
        if stale >= patience:
            break

        # next generation: elites + offspring
        nxt = [list(pop[i]) for i in order[:elite]]
        while len(nxt) < pop_size:
            a, b = tournament(pop, fits, tournament_k), tournament(pop, fits, tournament_k)
            child = crossover(a, b) if random.random() < crossover_rate else list(a)
            nxt.append(mutate(child, names, mutation_rate))
        pop = nxt

    return {"team": best_team, "fitness": best_fit, "history": history,
            "generations_run": len(history), "battles": evals,
            "seconds": time.perf_counter() - start}


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="Genetic algorithm: best team vs Arceus")
    ap.add_argument("--team-size", type=int, default=3)
    ap.add_argument("--pop", type=int, default=50)
    ap.add_argument("--gens", type=int, default=40)
    ap.add_argument("--trials", type=int, default=10, help="battles per fitness evaluation")
    ap.add_argument("--mutation", type=float, default=0.15)
    ap.add_argument("--patience", type=int, default=15, help="stop after this many generations without improvement")
    ap.add_argument("--runs", type=int, default=1, help="independent GA runs (use >1 for experiments)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", default=None, help="CSV file for per-generation history of every run")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print("Loading Pokemon (one-time cost)...")
    pool, boss = load_pool()
    print(f"{len(pool)} usable Pokemon in pool; boss = {boss.name} (hp {boss.hp})")

    rows, summaries = [], []
    for run in range(args.runs):
        res = run_ga(pool, boss, args.team_size, args.pop, args.gens, args.trials,
                     args.mutation, patience=args.patience)
        # re-score the winner with many battles for a trustworthy final number
        final = evaluate(res["team"], pool, boss, 500)
        summaries.append((res, final))
        for h in res["history"]:
            rows.append({"run": run, **h})
        print(f"run {run}: team={res['team']}  win_rate={final.win_rate:.2%}  "
              f"mean_turns={final.mean_turns:.2f}  gens={res['generations_run']}  "
              f"battles={res['battles']}  time={res['seconds']:.2f}s")

    if args.runs > 1:
        wr = [f.win_rate for _, f in summaries]
        tn = [f.mean_turns for _, f in summaries if f.win_rate > 0]
        print("\n=== across runs ===")
        print(f"win rate  mean {statistics.mean(wr):.2%}  stdev {statistics.pstdev(wr):.2%}")
        if tn:
            print(f"turns     mean {statistics.mean(tn):.2f}  stdev {statistics.pstdev(tn):.2f}")
        print(f"time      mean {statistics.mean(r['seconds'] for r, _ in summaries):.2f}s")

    if args.out:
        with open(args.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"history written to {args.out}")


if __name__ == "__main__":
    main()
