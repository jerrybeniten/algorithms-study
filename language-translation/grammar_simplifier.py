
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Grammar Simplifier
==================

Removes (in order):
  1) ε-productions (empty productions)
  2) Unit productions
  3) Useless symbols (non-generating and unreachable)

It also shows each step performed.

-----------------------------
INPUT GRAMMAR FORMAT (plain text)
-----------------------------
- One rule per line:  Nonterminal -> production1 | production2 | ...
- Symbols in a production are SPACE-SEPARATED tokens.
- Use uppercase identifiers for nonterminals (e.g., S, A, Expr). Terminals can be lowercase or quoted.
- Use 'ε' to denote the empty string (epsilon). You can also use 'epsilon' or 'eps' or an empty RHS token.
- Lines starting with '#' are comments. Blank lines are ignored.

Example:
--------
S  -> A B | ε
A  -> a A | ε
B  -> b B | C
C  -> c

Run:
----
$ python3 grammar_simplifier.py --file mygrammar.txt --show-steps
$ python3 grammar_simplifier.py --demo

You can also paste grammar in stdin (end with Ctrl-D on Linux/Mac, Ctrl-Z then Enter on Windows):
$ python3 grammar_simplifier.py --stdin

Notes:
------
- Internally, ε is represented as an empty tuple () in productions.
- To preserve an ε-derivation of the original start symbol S during ε-elimination, a fresh start S' is used:
    S0 -> S   and S0 -> ε if S was nullable. S0 becomes the new start.
'''

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, List, Iterable, Optional
import argparse
import re
import sys
import itertools

EPS = "ε"

Symbol = str
Production = Tuple[Symbol, ...]  # empty tuple means epsilon
Productions = Set[Production]
Rules = Dict[Symbol, Productions]

# ---------------------- Utilities ----------------------

def _is_nonterminal(sym: str) -> bool:
    # Heuristic: Nonterminals are identifiers that start with uppercase letter or are wrapped like <Expr>
    return bool(re.match(r"^([A-Z][A-Za-z0-9_]*)|(<[^<>]+>)$", sym))

def _fresh_start(base: str, existing: Set[str]) -> str:
    i = 0
    while True:
        candidate = f"{base}{i}"
        if candidate not in existing:
            return candidate
        i += 1

def _prod_to_str(p: Production) -> str:
    return EPS if len(p) == 0 else " ".join(p)

def _sorted_symbols(syms: Iterable[str]) -> List[str]:
    return sorted(syms, key=lambda x: (x.replace('<','').replace('>',''), x))

def _sorted_prods(prods: Iterable[Production]) -> List[Production]:
    return sorted(prods, key=lambda t: (len(t), " ".join(t)))

# ---------------------- Data Model ----------------------

@dataclass
class Grammar:
    start: Symbol
    rules: Rules = field(default_factory=dict)

    @property
    def nonterminals(self) -> Set[Symbol]:
        return set(self.rules.keys())

    @property
    def terminals(self) -> Set[Symbol]:
        nts = self.nonterminals
        ts: Set[Symbol] = set()
        for rhs_set in self.rules.values():
            for rhs in rhs_set:
                for s in rhs:
                    if s not in nts:
                        ts.add(s)
        return ts

    def copy(self) -> 'Grammar':
        return Grammar(self.start, {A: set(map(tuple, prods)) for A, prods in self.rules.items()})

    # ---------- Parsing / Printing ----------
    @staticmethod
    def parse(text: str, epsilon_tokens: Optional[Set[str]] = None) -> 'Grammar':
        '''
        Parse grammar from text. Returns Grammar.
        The start symbol is the LHS of the first non-comment rule encountered.
        '''
        if epsilon_tokens is None:
            epsilon_tokens = {EPS, "epsilon", "eps", "ɛ"}

        rules: Rules = {}
        start: Optional[Symbol] = None

        lines = [ln.strip() for ln in text.splitlines()]
        for ln in lines:
            if not ln or ln.startswith('#'):
                continue
            # Allow both '->' and ':' or '::=' as arrow
            m = re.split(r"\s*(?:->|::=|:)\s*", ln, maxsplit=1)
            if len(m) != 2:
                raise ValueError(f"Cannot parse rule line: '{ln}'. Expected 'A -> ...'")
            lhs, rhs = m[0].strip(), m[1].strip()
            if not lhs:
                raise ValueError(f"Missing LHS in rule: '{ln}'")
            if start is None:
                start = lhs
            if lhs not in rules:
                rules[lhs] = set()

            # Split alternatives by | but allow | inside quotes
            alts = _split_alternatives(rhs)

            for alt in alts:
                alt = alt.strip()
                if alt == "" or alt in epsilon_tokens:
                    prod: Production = tuple()  # epsilon
                else:
                    # Tokenize: space-separated tokens, but respect single/double quotes as terminals with spaces
                    tokens = _tokenize(alt)
                    prod = tuple(tokens)
                rules[lhs].add(prod)

        if start is None:
            raise ValueError("No rules found.")
        return Grammar(start, rules)

    def to_text(self) -> str:
        lines: List[str] = []
        nts = _sorted_symbols(self.nonterminals)
        for A in nts:
            rhs = self.rules.get(A, set())
            rhs_str = " | ".join(_prod_to_str(p) for p in _sorted_prods(rhs))
            line = f"{A} -> {rhs_str if rhs_str else '/* no productions */'}"
            if A == self.start:
                line = f"{line}    # (start)"
            lines.append(line)
        return "\n".join(lines)

    # ---------- Simplification Pipeline ----------

    def simplify(self, show_steps: bool = True) -> 'SimplifyResult':
        G = self.copy()
        steps = StepLog()

        # 1) Remove ε-productions (epsilon)
        steps.note("Initial grammar", G.to_text())
        G, eps_info = eliminate_epsilon(G, steps)
        steps.note("After ε-elimination", G.to_text())

        # 2) Remove unit productions
        G = eliminate_unit(G, steps)
        steps.note("After unit-production elimination", G.to_text())

        # 3) Remove useless symbols (non-generating + unreachable)
        G = remove_useless(G, steps)
        steps.note("After removing useless symbols", G.to_text())

        return SimplifyResult(original=self, simplified=G, steps=steps)

# ---------------------- Tokenization helpers ----------------------

def _split_alternatives(rhs: str) -> List[str]:
    out = []
    cur = []
    in_single = False
    in_double = False
    for ch in rhs:
        if ch == "'" and not in_double:
            in_single = not in_single
            cur.append(ch)
        elif ch == '"' and not in_single:
            in_double = not in_double
            cur.append(ch)
        elif ch == '|' and not in_single and not in_double:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out

def _tokenize(alt: str) -> List[str]:
    # Split by whitespace unless within quotes
    tokens: List[str] = []
    buf = []
    in_single = False
    in_double = False
    i = 0
    while i < len(alt):
        ch = alt[i]
        if ch == "'" and not in_double:
            in_single = not in_single
            buf.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            buf.append(ch)
            i += 1
            continue
        if ch.isspace() and not in_single and not in_double:
            if buf:
                tokens.append(_unquote("".join(buf)))
                buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if buf:
        tokens.append(_unquote("".join(buf)))
    return tokens

def _unquote(tok: str) -> str:
    if (tok.startswith("'") and tok.endswith("'")) or (tok.startswith('"') and tok.endswith('"')):
        return tok[1:-1]
    return tok

# ---------------------- Steps Logging ----------------------

from dataclasses import dataclass

@dataclass
class Step:
    title: str
    body: str

class StepLog:
    def __init__(self) -> None:
        self.steps: List[Step] = []

    def note(self, title: str, body: str) -> None:
        self.steps.append(Step(title, body))

    def extend(self, title_prefix: str, lines: Iterable[str]) -> None:
        collected = "\n".join(lines)
        if collected.strip():
            self.note(title_prefix, collected)

    def __str__(self) -> str:
        out = []
        for i, s in enumerate(self.steps, 1):
            out.append(f"Step {i}: {s.title}\n" + "-" * (7 + len(s.title)))
            out.append(s.body.rstrip() + "\n")
        return "\n".join(out)

@dataclass
class SimplifyResult:
    original: Grammar
    simplified: Grammar
    steps: StepLog

# ---------------------- Algorithm Implementations ----------------------

def eliminate_epsilon(G: Grammar, steps: StepLog) -> Tuple[Grammar, Set[Symbol]]:
    '''
    Remove ε-productions. Preserve possible ε-derivation by introducing a fresh start S0.
    Returns the transformed grammar and the set of nullable nonterminals.
    '''
    steps.note("ε-elimination: computing nullable nonterminals", "")
    nullable: Set[Symbol] = set()
    changed = True
    while changed:
        changed = False
        for A, prods in G.rules.items():
            if A in nullable:
                continue
            for p in prods:
                if len(p) == 0 or all(sym in nullable for sym in p):
                    nullable.add(A)
                    changed = True
                    break
    steps.note("Nullable nonterminals", ", ".join(_sorted_symbols(nullable)) or "(none)")

    # Fresh start to preserve epsilon if needed
    orig_start = G.start
    new_start = _fresh_start(orig_start + "_S", G.nonterminals | {orig_start})
    new_rules: Rules = {A: set(map(tuple, rhs)) for A, rhs in G.rules.items()}
    new_rules[new_start] = { (orig_start,) }
    if orig_start in nullable:
        new_rules[new_start].add(tuple())

    # Generate new productions by removing nullable occurrences
    added_lines = []
    for A, prods in list(new_rules.items()):
        updated: Productions = set()
        for p in prods:
            if len(p) == 0:
                # drop epsilon except possibly for new start (handled already)
                if A == new_start:
                    updated.add(p)
                continue
            # positions of nullable symbols
            idxs = [i for i, s in enumerate(p) if s in nullable]
            if not idxs:
                updated.add(p)
                continue
            for mask in itertools.product([0,1], repeat=len(idxs)):
                # mask bit 1 means "remove this occurrence"
                out = list(p)
                for bit, pos in sorted(list(zip(mask, idxs)), key=lambda x: -x[1]):
                    if bit == 1:
                        del out[pos]
                if len(out) == 0:
                    # keep ε only if A == new_start
                    if A == new_start:
                        updated.add(tuple())
                else:
                    updated.add(tuple(out))
        # Remove explicit ε from non-start
        if A != new_start:
            updated = {q for q in updated if len(q) > 0}
        if updated != prods:
            added = updated - prods
            if added:
                added_lines.append(f"{A}: {', '.join(_prod_to_str(p) for p in _sorted_prods(added))}")
        new_rules[A] = updated

    # Remove any remaining explicit ε productions in non-start (safety)
    for A, prods in list(new_rules.items()):
        if A != new_start and tuple() in prods:
            prods.discard(tuple())
            new_rules[A] = prods

    steps.extend("ε-elimination: new productions added", added_lines)
    result = Grammar(new_start, new_rules)
    return result, nullable

def eliminate_unit(G: Grammar, steps: StepLog) -> Grammar:
    '''
    Remove unit productions A -> B where A,B are nonterminals.
    Add A -> γ for each non-unit production B -> γ reachable via unit chain.
    '''
    nts = G.nonterminals
    rules = {A: set(map(tuple, rhs)) for A, rhs in G.rules.items()}

    # Compute unit-closure: unit_pairs[A] = set of B such that A =>* B via unit productions
    unit_pairs: Dict[Symbol, Set[Symbol]] = {A: {A} for A in nts}
    changed = True
    while changed:
        changed = False
        for A in nts:
            for p in list(rules.get(A, set())):
                if len(p) == 1 and p[0] in nts:
                    B = p[0]
                    if B not in unit_pairs[A]:
                        unit_pairs[A].add(B)
                        changed = True
                        # also inherit B's unit targets transitively
                        unit_pairs[A] |= unit_pairs.get(B, {B})

    # Collect non-unit productions for each B and add to A
    added_lines = []
    for A in nts:
        to_add: Set[Production] = set()
        for B in unit_pairs[A]:
            for p in rules.get(B, set()):
                if not (len(p) == 1 and p[0] in nts):  # non-unit
                    to_add.add(p)
        # remove unit productions
        rules[A] = {p for p in rules.get(A, set()) if not (len(p) == 1 and p[0] in nts)}
        before = len(rules[A])
        rules[A] |= to_add
        after = len(rules[A])
        if after > before:
            added_lines.append(f"{A}: added {after-before} production(s) via unit-closure")

    steps.extend("Unit-production elimination: additions", added_lines)
    return Grammar(G.start, rules)

def remove_useless(G: Grammar, steps: StepLog) -> Grammar:
    '''
    Remove non-generating and unreachable symbols.
    '''
    nts = G.nonterminals
    rules = {A: set(map(tuple, rhs)) for A, rhs in G.rules.items()}

    # 1) Generating symbols (can derive terminals)
    generating: Set[Symbol] = set()
    changed = True
    while changed:
        changed = False
        for A in nts:
            if A in generating:
                continue
            for p in rules.get(A, set()):
                if all((s not in nts) or (s in generating) for s in p):
                    generating.add(A)
                    changed = True
                    break
    steps.note("Generating nonterminals", ", ".join(_sorted_symbols(generating)) or "(none)")

    # Remove non-generating
    for A in list(rules.keys()):
        if A not in generating and A != G.start:
            del rules[A]
    nts2 = set(rules.keys())
    for A in list(rules.keys()):
        new_rhs = {p for p in rules[A] if all((sym not in nts2) or (sym in rules) for sym in p)}
        rules[A] = new_rhs

    # 2) Reachable symbols from start
    reachable_nts: Set[Symbol] = set([G.start])
    reachable_ts: Set[Symbol] = set()
    changed = True
    while changed:
        changed = False
        for A in list(reachable_nts):
            for p in rules.get(A, set()):
                for s in p:
                    if s in rules and s not in reachable_nts:
                        reachable_nts.add(s)
                        changed = True
                    elif s not in rules:
                        reachable_ts.add(s)

    steps.note("Reachable nonterminals", ", ".join(_sorted_symbols(reachable_nts)) or "(none)")
    steps.note("Reachable terminals", ", ".join(sorted(reachable_ts)) or "(none)")

    # Remove unreachable
    for A in list(rules.keys()):
        if A not in reachable_nts:
            del rules[A]
    for A in list(rules.keys()):
        rules[A] = {p for p in rules[A] if all((sym not in rules) or (sym in reachable_nts) for sym in p)}

    return Grammar(G.start, rules)

# ---------------------- CLI ----------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Simplify a context-free grammar and show the steps.")
    src = parser.add_mutually_exclusive_group(required=False)
    src.add_argument("--file", type=str, help="Path to grammar text file.")
    src.add_argument("--stdin", action="store_true", help="Read grammar from STDIN (end with EOF).")
    src.add_argument("--demo", action="store_true", help="Run a built-in demo grammar.")
    parser.add_argument("--no-steps", action="store_true", help="Do not print step-by-step log.")
    parser.add_argument("--print-simplified", action="store_true", help="Print only the simplified grammar at the end.")
    args = parser.parse_args(argv)

    if args.demo:
        text = (
            "# Demo grammar\n"
            "S  -> A B | ε\n"
            "A  -> a A | ε\n"
            "B  -> b B | C\n"
            "C  -> c | ε\n"
        )
    elif args.stdin:
        text = sys.stdin.read()
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        print("No input given. Use --file, --stdin, or --demo.", file=sys.stderr)
        return 2

    try:
        G = Grammar.parse(text)
    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    result = G.simplify(show_steps=(not args.no_steps))

    if not args.no_steps:
        print("=== Step-by-step log ===")
        print(result.steps)

    print("=== Simplified grammar ===")
    print(result.simplified.to_text())

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
