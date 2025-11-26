from managers.character_class import Character

cards = {
    "Strike": {"energy": 2, "effect": "deal 5 damage", "num": 5},
    "Block": {"energy": 2, "effect": "block 5 damage", "num": 5},
    "Heal": {"energy": 3, "effect": "heal for 5", "num": 5},

}

Trev = Character("trev", "Gambler", 20, cards)
enemy = Character("enemy", "bean farmer", 10, cards)

Trev.roll_dice()
input("Press enter to continue...")
enemy.roll_dice()
input("Press enter to continue...")

##player turn// combat phase

for key in cards:
    print(f'{key}: cost:{cards[key]["energy"]}: effect: {cards[key]["effect"]} ')
choice = input("which card would you like to use?").title()
if choice in cards:
    energy_cost = cards[choice]["energy"]
    Trev.energy -= energy_cost
    print(f" -{energy_cost} energy")
    print(f" total energy: {Trev.energy}")
    effect = cards[choice]["num"]
    if cards[choice]["effect"] == "deal 5 damage":
        enemy.health -= effect
        print(f"{Trev.name} dealt 5 damage to {enemy.name}")
    elif cards[choice]["effect"] == "block 5 damage":
        pass
    elif cards[choice]["effect"] == "heal for 5":
        Trev.health += effect
        print(f"{Trev.name} healed for {effect}")
# enemy_card = cards[]
