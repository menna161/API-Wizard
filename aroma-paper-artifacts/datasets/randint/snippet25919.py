import random
import decimal


def make_attack(self):
    attack = 0
    if (random.random() > 0.95):
        attack = (self.attack + 25)
        print(f"{self.name}'s attack does {attack} damage!!! That's a critical attack! o.O")
        return attack
    attack = (self.attack + random.randint(1, 5))
    print(f"{self.name}'s attack does {attack} damage")
    return attack
