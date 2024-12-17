"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """

from typing import List
from formula import Formula, Not, Or, And, Implies, Atom
from functions import atoms, is_literal
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
        if partial_truth_value(formula.left, interp) is not None or partial_truth_value(formula.right, interp) is True:
            return not partial_truth_value(formula.left, interp) or partial_truth_value(formula.right, interp)
    return None

def create_truth_table(formula: Formula):
    interp = get_partial_interpretation(formula)
    atoms_list = [i for i in atoms(formula) if i not in interp]
    def create_row(combination):
        row = dict(zip(atoms_list, combination)) | interp
        row[formula] = truth_value(formula, row)
        return row
    yield from map(create_row, product([False, True], repeat=len(atoms_list)))

def get_partial_interpretation(formula: Formula):
    interp = {}
    if isinstance(formula, Atom):
        interp[formula] = True
    if isinstance(formula, Not) and is_literal(formula):
        interp = get_partial_interpretation(formula.inner)
        interp[formula.inner] = not interp[formula.inner]
    if isinstance(formula, And):
        interp = get_partial_interpretation(formula.left) | get_partial_interpretation(formula.right)
    return interp

def is_logical_consequence(premises: List[Formula], conclusion: Formula):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    return is_valid(conclusion) if not premises else is_valid(Implies(reduce(lambda acc, pre: And(acc, pre), premises), conclusion))

def is_logical_equivalence(formula1, formula2): 
    """Checks whether formula1 and formula2 are logically equivalent."""
    return is_valid(And(Implies(formula1, formula2), Implies(formula2, formula1)))    

def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    return all(i[formula] is True for i in create_truth_table(formula))

def satisfiability_brute_force(formula):
    """it will return true if is satisfiable and false if it isnt"""
    return not all(i[formula] is False for i in create_truth_table(formula))

def duplo_satisfativel(f):
    first = sat_interpretation(f)
    if not first:
        return False
    lst = []
    for key, value in first.items():
        atom = key if value else Not(key)
        lst.append(atom)
    and_all = reduce(lambda acc, x: And(acc, x), lst)
    return sat_interpretation(And(f, Not(and_all))) is not False


def sat_interpretation(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    for i in create_truth_table(formula):
        if i[formula]:
            return i
    return False


teste = Implies(Atom('p'), Atom('q'))
print(f"{teste} é satisfatível? {sat_interpretation(teste)}")
print(f"{teste} é duplamente satisfatível? {duplo_satisfativel(teste)}")
teste2 = Not(teste)
print(f"{teste2} é satisfatível? {sat_interpretation(teste2)}")
print(f"{teste2} é duplamente satisfatível? {duplo_satisfativel(teste2)}")
