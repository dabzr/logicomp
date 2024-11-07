"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """

from typing import List
from formula import Formula, Not, Or, And, Implies, Atom
from functions import atoms
from functools import reduce
from itertools import product

def truth_value(formula: Formula, interpretation: dict) -> bool:
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Not):
        return not truth_value(formula.inner, interpretation)
    if isinstance(formula, Or):
        return truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    if isinstance(formula, And):
        return truth_value(formula.left, interpretation) and truth_value(formula.right, interpretation)
    if isinstance(formula, Implies):
        return not truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    return interpretation[formula] # Caso seja Atom

def partial_truth_value(formula: Formula, interp: dict):
    if isinstance(formula, Atom):
        return interp.get(formula)
    if isinstance(formula, Not):
        if partial_truth_value(formula.inner, interp) is not None:
            return not partial_truth_value(formula.inner, interp)
    if isinstance(formula, Or):
        return partial_truth_value(formula.left, interp) or partial_truth_value(formula.right, interp)
    if isinstance(formula, And):
        return partial_truth_value(formula.left, interp) and partial_truth_value(formula.right, interp)
    if isinstance(formula, Implies):
        return not partial_truth_value(formula.left, interp) or partial_truth_value(formula.right, interp)
    return None

def create_truth_table(formula: Formula):
    atoms_list = list(atoms(formula))
    truth_combinations = product([False, True], repeat=len(atoms_list))
    truth_table = []
    for combination in truth_combinations:
        row = dict(zip(atoms_list, combination)) 
        row[formula] = truth_value(formula, row)
        truth_table.append(row)
    return truth_table

def is_logical_consequence(premises: List[Formula], conclusion: Formula):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    return is_valid(conclusion) if not premises else is_valid(Implies(reduce(lambda acc, pre: And(acc, pre), premises), conclusion))

def is_logical_equivalence(formula1, formula2): 
    """Checks whether formula1 and formula2 are logically equivalent."""
    return is_valid(And(Implies(formula1, formula2), Implies(formula2, formula1)))    

def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    return all([i[formula] is True for i in create_truth_table(formula)])

def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    return not all([i[formula] is False for i in create_truth_table(formula)])
