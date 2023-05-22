import random
import decimal


def __init__(self, name, diet, period, weight, armor, hybrid, nature=None, attack=None, defense=None, life=None):
    "\n        :param name: scientific name of dinosaur\n        :param diet: whether dinosaur is 'herbivore' or 'carnivore'\n        :param period: geologic period of dinosaur existence\n        :param weight: weight of dinosaur (in lbs to nearest 100)\n        :param armor: boolean whether dinosaur sports armor or not\n        :param hybrid: boolean whether dinosaur is hybrid or not\n        :param nature: random value used for calculating attack and defense\n        :param attack: attack points for dinodaur\n        :param defense: defense points of dinosaur\n        :param life: life points of dinosaur\n        "
    self.name = name
    self.diet = diet
    self.period = period
    self.weight = int(round(weight, (- 2)))
    self.armor = armor
    self.hybrid = hybrid
    self.nature = nature
    self.attack = attack
    self.defense = defense
    self.life = life
    if (self.nature is None):
        if (self.diet == 'herbivore'):
            self.nature = random.randint(1, 8)
        else:
            self.nature = random.randint(5, 12)
    if (self.attack is None):
        self.initialize_attack()
    if (self.defense is None):
        self.initialize_defense()
    if (self.life is None):
        self.initialize_life()
