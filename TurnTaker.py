#The Damage Dealt formula is given by https://bulbapedia.bulbagarden.net/wiki/Damage
import random, pandas as pd
from math import floor, nan


#done: make class pokemon better. make it where, just put pokemon name, and rest is automated for you

#power is incldued in attack class
class pokemon():
    def __init__(self, pokemon,level):
        self.name = pokemon["name"]
        self.hp = int(pokemon["hp"])
        self.defense = int(pokemon["defense"])
        self.level = level
        self.attack = int(pokemon["attack"])
        self.speed = int(pokemon["speed"])
        self.type1 =pokemon["type1"]
        self.type2 = pokemon["type2"]
        self.BestAttack = self.BestAttackMove()
        self.against={"bug": pokemon["against_bug"],"dark":pokemon["against_dark"],"dragon":pokemon["against_dragon"],"electric":pokemon["against_electric"],"fairy":pokemon["against_fairy"],"fight":pokemon["against_fight"],"flying":pokemon["against_flying"],"ghost":pokemon["against_ghost"],"grass":pokemon["against_grass"],"ground":pokemon["against_ground"],"ice":pokemon["against_ice"],"normal":pokemon["against_normal"],"poison":pokemon["against_poison"],"psychic":pokemon["against_psychic"],"rock":pokemon["against_rock"],"steel":pokemon["against_steel"],"water":pokemon["against_water"]}
        #fancy setters and getters:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def type1(self):
        return self._type1

    @type1.setter
    def type1(self, value):
        self._type1 = value

    @property
    def type2(self):
        return self._type2

    @type2.setter
    def type2(self, value):
        self._type2 = value

    @property
    def against(self):
        return self._against

    @against.setter
    def against(self, value):
        self._against = value


    def Attack(self,defender):
        #assign defender variables
        defender_defense = defender.defense
        defender_type1 = defender.type1
        defender_type2 = defender.type2
        typebuff1=1
        typebuff2=1
        #Prelude to damage calucation
        threshold=self.speed/2
        randomnumber= random.randint(0,255)/256
        if randomnumber < threshold:
            crit = 2
        else:
            crit =1
        #done: make way to get all the against_n's into a list that can be searched through to determine if the attacker has an against_n against the defender for bonus

        for buff in self.against:
            if buff == defender_type1:
                typebuff1=self._against[buff]
                break
        if defender_type2 != nan:
            for buff in self.against:
                if buff == defender_type2:
                    typebuff2 = self._against[buff]
                    break



        #Move finder
        #gets most powerful move pokemon can do. doesn't consider if move has limits per battle.
        #Could add defense too. but rn, focus on attack

        # Multidata set interactions.
        # pokemon.csv to get pokemon id ->
        # interacts with pokemon_moves.csv ->
        # move id selection ->
        # moves.csv to get the power of the move
        #attack is conducted
        damage=(((((2*self.level)/5)+2)*(self.attack/defender_defense))/50)*crit*(random.randint(85,100)/100)*typebuff1*typebuff2*self.BestAttack["power"]
        defender.hp = defender.hp-floor(damage)
        return floor(damage)

        #instead of searching everytime, use this to get the best attack just once
    def BestAttackMove(self):
        pokemoncsv = pd.read_csv("pokemon/moves/pokemon.csv")
        moves = pd.read_csv("pokemon/moves/moves.csv")
        pokemonmoves = pd.read_csv("pokemon/moves/pokemon_moves.csv")

        #testing to see why worng
        name = str(self.name).strip().lower()
        matches = pokemoncsv.loc[
            pokemoncsv["identifier"].str.strip().str.lower() == name, "id"
        ]

        if matches.empty:
            raise ValueError(f"No Pokémon matched {self.name!r}")
        pokemon_id = pokemoncsv.loc[
            pokemoncsv["identifier"].str.strip().str.lower() == name,
            "id"
        ].iloc[0]

        moveset = pokemonmoves.loc[
            pokemonmoves["pokemon_id"] == pokemon_id, "move_id"
        ].drop_duplicates()

        possible_moves = (
            moves.loc[moves["id"].isin(moveset)]
            .dropna(subset=["power"])
            .sort_values("power", ascending=False)
        )

        if possible_moves.empty:
            return None

        best = possible_moves.iloc[0]
        return {"move": best["identifier"], "power": int(best["power"])}

    def GetBestAttackMoveName(self):
        return self.BestAttackMove()["move"]

