"""
CFG Derivation Tool
-------------------

This tool allows you to derive a given target string using a Context-Free Grammar (CFG).
It supports finding *all possible leftmost derivations* (up to a configurable limit).

# Features
- Reads grammar rules from a file.
- Supports epsilon (ε) productions.
- Finds all leftmost derivations of a target string.
- Shows derivations step by step.
- Configurable max steps and max derivations.

# Grammar File Format
Each rule must be written as:
    NonTerminal -> production1 | production2 | ...

- Symbols are space-separated.
- Use `ε` for the empty string (epsilon).
- First nonterminal encountered is treated as the start symbol.

Example `grammar.txt`:
    S -> A B | X
    A -> a A | a
    B -> b
    X -> a b

# Example Usage
Run with:
    python3 grammar_deriver.py --file grammar.txt --string "a b"

Find multiple derivations:
    python3 grammar_deriver.py --file grammar.txt --string "a b" --max-derivations 5

Limit maximum steps:
    python3 grammar_deriver.py --file grammar.txt --string "a b c" --max-steps 30

# Sample Output
    Deriving: a b
    Start symbol: S

    === Derivation 1 ===
    Step 1: S
    Step 2: A B
    Step 3: a B
    Step 4: a b
    ✅ Derived successfully

    === Derivation 2 ===
    Step 1: S
    Step 2: X
    Step 3: a b
    ✅ Derived successfully
"""

import argparse
from collections import deque

EPSILON = "ε"

def parse_grammar(text):
    rules = {}
    start = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        lhs, rhs = line.split("->")
        lhs = lhs.strip()
        if start is None:
            start = lhs
        alts = rhs.split("|")
        for alt in alts:
            symbols = alt.strip().split()
            if symbols == [EPSILON] or symbols == []:
                symbols = []
            rules.setdefault(lhs, []).append(symbols)
    return rules, start

def is_terminal(sym, rules):
    return sym not in rules

def all_leftmost_derivations(rules, start, target, max_steps=50, max_derivations=10):
    """Return all leftmost derivations of target from start."""
    target = target.split()
    start_sentential = [start]

    derivations = []
    queue = deque()
    queue.append((start_sentential, [start_sentential]))

    while queue and len(derivations) < max_derivations:
        sentential, history = queue.popleft()

        # Too long, skip
        if len(history) > max_steps:
            continue

        # Success
        if sentential == target:
            derivations.append(history)
            continue

        # Expand first nonterminal (leftmost)
        for i, sym in enumerate(sentential):
            if not is_terminal(sym, rules):
                for prod in rules[sym]:
                    new_sent = sentential[:i] + prod + sentential[i+1:]
                    queue.append((new_sent, history + [new_sent]))
                break  # only expand leftmost
    return derivations

def main():
    parser = argparse.ArgumentParser(description="CFG Derivation Tool (All Derivations)")
    parser.add_argument("--file", required=True, help="Grammar file")
    parser.add_argument("--string", required=True, help="Target string (space-separated)")
    parser.add_argument("--max-steps", type=int, default=50, help="Max steps per derivation")
    parser.add_argument("--max-derivations", type=int, default=10, help="Max number of derivations to show")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    rules, start = parse_grammar(text)
    print(f"Deriving: {args.string}")
    print(f"Start symbol: {start}\n")

    results = all_leftmost_derivations(
        rules, start, args.string, max_steps=args.max_steps, max_derivations=args.max_derivations
    )

    if results:
        for d_idx, deriv in enumerate(results, 1):
            print(f"=== Derivation {d_idx} ===")
            for i, step in enumerate(deriv, 1):
                print(f"Step {i}: {' '.join(step) if step else EPSILON}")
            print("✅ Derived successfully\n")
    else:
        print("❌ No derivations found for this string.")

if __name__ == "__main__":
    main()
