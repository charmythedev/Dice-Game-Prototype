# 🎲 Dice Game Prototype

A **small, experimental turn-based dice game prototype** exploring the intersection of **Yahtzee-style dice combinations** and **card-based combat mechanics**.

This project represents my **first intentional foray into game design**, built as a learning exercise and conceptual precursor to a larger idea.

---

## Core Gameplay Loop

1. The player rolls **five dice**
2. Dice are evaluated to form **Yahtzee-style combinations**
3. Combinations:
   - Generate **energy** used to play cards
   - Provide **synergies** that strengthen or modify card effects
4. Cards are played to resolve combat decisions
5. The loop repeats until **combat ends**
6. The game concludes with a simple **credit scene**

The focus is on **system interaction**, not content volume.

---

## Project Status

**Early Prototype / Learning Project / Showcase Only**

This project is:
- Intentionally **small**
- **Unfinished**
- **Buggy in places**
- Not balanced or polished

Those limitations are known and accepted — the purpose was to explore mechanics, not ship a product.

This repository is public **for portfolio and demonstration purposes only**.  
It is **read-only** and **not accepting external contributions**.

**All rights reserved.**

---

## Design Goals

- Experiment with dice-driven randomness and player agency
- Combine probabilistic systems with deterministic card effects
- Practice structuring game logic and state cleanly
- Learn through iteration rather than over-engineering

This project prioritizes **learning velocity and experimentation** over completeness.

---

## Technical Overview

- Turn-based game flow
- Dice evaluation system inspired by Yahtzee scoring
- Card effects influenced by active dice synergies
- Energy-based action economy
- Manager-based architecture for separating game systems

---

## Project Structure
Dice-Game-Prototype/
├── managers/ # Game state, dice logic, cards, and flow control
├── prototypetest.py # Prototype entry / testing script
├── .gitignore
└── README.md


---

## Tech Stack

- **Language:** Python
- **Paradigm:** Object-oriented design
- **Focus:** Game systems, state management, rapid iteration

---

## ⚠️ Known Limitations

- Minimal UI
- No save system or progression
- Limited content and balancing
- Bugs and rough edges remain

These are deliberate tradeoffs for a prototype built to **learn, test, and discard ideas quickly**.

---

## What This Project Demonstrates

- Translating abstract mechanics into playable systems
- Designing a coherent game loop from simple components
- Managing randomness, synergy, and player choice
- Comfort prototyping without over-polishing

---

## License / Usage

**All Rights Reserved**

This repository is shared for **evaluation and portfolio review only**.  
Reuse, modification, or redistribution is not permitted.

