import re
import random

todos = [
    "### todo managers severely bloated need to update, all managers bloated, mostly overworld, ui and game manager (HIGH Priority)"
    "## todo fix bugginess in check collision (High Priority)",
    '### todo fix house tops rendering incorrectly in map( High Priority)(in fact refactor how maps work'
    '# todo fix lucky rabbit\'s foot (it gives reroll for rest of combat) '
    "# todo fix flaky combat flickery system, stop from rerolling if end turn or attack phase"
    '#todo make more maps and add x, y detection to switch between maps (dict?)'
    "### todo update hitboxes and collision in overworld (including using y positions for draw order) !!!(HIGH PRIORITY)!!!",
    "## todo make E (done-ish) and W walk animations + NW, NE, SW, SE",
    "## todo card animations and fixing combat window",
    "## todo fix resize function (maybe resize maps and window in general) !!!(High Priority)!!!",
    "# todo add puzzles?",
    "# todo more cards",
    "# todo emotion mechanic (Med Priority)",
    "# todo let player go elsewhere other than town (spooky forest next?) !!!(High Priority)!!!",
    "# todo branching dialogue (dialogue manager?)",
    "# todo crafting system",
    "# todo inventory manager",
    "# todo inventory menu",
    "# todo dice manager + make more dice !!(Highish Priority)!!",
    "# todo level system",
    "# todo separate managers properly",
    "# todo write characters and story overview",
    "# todo make map (in game)",
    "# todo break down todos into chunks instead of long list, maybe make a random todo picker",
    "# todo get better at animation and pixel art !!!(high priority)!!!"
]

def categorize(todo):
    if "HIGH PRIORITY" in todo.upper():
        return "High Priority"
    elif "HIGHISH" in todo.upper():
        return "Highish Priority"
    elif "MED" in todo.upper():
        return "Medium Priority"
    else:
        return "Low Priority"

# Sort todos by category
sorted_todos = {}
for t in todos:
    category = categorize(t)
    sorted_todos.setdefault(category, []).append(t)

# Print nicely
for category in ["High Priority", "Highish Priority", "Medium Priority", "Low Priority"]:
    print(f"\n=== {category} ===")
    for item in sorted_todos.get(category, []):
        print("-", item)

def random_picker():
    return random.choice(sorted_todos.get(category, []))

print(f""" 
RANDOM TASK OF THE DAY:
{random_picker()}""")



