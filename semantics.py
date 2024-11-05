"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import Formula, Not, Or, And, Implies, Atom
from functions import atoms


def truth_value(formula: Formula, interpretation: dict):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        return interpretation[formula]
    if isinstance(formula, Not):
        return not truth_value(formula.inner, interpretation)
    if isinstance(formula, Or):
        return truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    if isinstance(formula, And):
        return truth_value(formula.left, interpretation) and truth_value(formula.right, interpretation)
    if isinstance(formula, Implies):
        return not truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)

def partial_truth_value(formula: Formula, partial_interpretation: dict):
    if isinstance(formula, Atom):
        return partial_interpretation.get(formula)
    if isinstance(formula, Not):
        if partial_truth_value(formula.inner, partial_interpretation) is not None:
            return not partial_truth_value(formula.inner, partial_interpretation)
    if isinstance(formula, Or):
        pl = partial_truth_value(formula.left, partial_interpretation)
        pr = partial_truth_value(formula.right, partial_interpretation)
        return pl or pr
    if isinstance(formula, And):
        pl = partial_truth_value(formula.left, partial_interpretation)
        pr = partial_truth_value(formula.right, partial_interpretation)
        return pl and pr
    if isinstance(formula, Implies):
        pl = partial_truth_value(formula.left, partial_interpretation)
        pr = partial_truth_value(formula.right, partial_interpretation)
        return not pl or pr
    return None

def create_truth_table(formula: Formula):
    atoms_list = sorted(list(atoms(formula)), key=str)
    truth_table = []
    num_atoms = len(atoms_list)
    size = 2 ** num_atoms
    for i in range(size):
        logic_dict = {}
        for j, atom in enumerate(atoms_list):
            logic_dict[atom] = (i >> (num_atoms - j - 1)) & 1 == 1
        logic_dict[formula] = truth_value(formula, logic_dict)
        truth_table.append(logic_dict)
    return truth_table

def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2): 
    """Checks whether formula1 and formula2 are logically equivalent."""
    return is_valid(And(Implies(formula1, formula2), Implies(formula2, formula1)))

    

def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    for i in create_truth_table(formula):
        if not i[formula]:
            return False
    return True
    # ======== YOUR CODE HERE ========


def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


