#The Damage Dealt formula is given by https://bulbapedia.bulbagarden.net/wiki/Damage
import random

from pylablib.devices.IMAQdx.nivision_defs import CThresholdData

#TODO: make class pokemon better. make it where, just put pokemon name, and rest is automated for you

#power is excluded
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

    def Attack(self,defender_defense,defender_type):
        #Prelude to damage calucation
        threshold=self.speed/2
        randomnumber= random.randint(0,255)/256
        if randomnumber < threshold:
            crit = 2
        else:
            crit =1
        #todo: make way to get all the against_n's into a list that can be searched through to determine if the attacker has an against_n against the defender for bonus
        typebuff1=1
        typebuff2=2
        #todo make random have floor function before it is divided

        #attack is conducted
        damage=(((((2*self.level)/5)+2)*(self.attack/defender_defense))/50)*crit*(random.randint(85,100)/100)*typebuff1*typebuff2
        return damage