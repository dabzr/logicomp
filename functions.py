"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """


from formula import Formula, Atom, Not, Implies, And, Or


def length(formula: Formula) -> int:
    """Determines the length of a formula in propositional logic."""
    if isinstance(formula, Not):
        return length(formula.inner) + 1
    if isinstance(formula, (Implies, And, Or)):
        return length(formula.left) + length(formula.right) + 1
    return 1


def subformulas(formula: Formula) -> set:
    """Returns the set of all subformulas of a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for subformula in subformulas(my_formula):
        print(subformula)

    This piece of code prints p, s, (p v s), (p → (p v s))
    (Note that there is no repetition of p)
    """
    if isinstance(formula, Not):
        return {formula}.union(subformulas(formula.inner))
    if isinstance(formula, (Implies, And, Or)):
        sub1 = subformulas(formula.left)
        sub2 = subformulas(formula.right)
        return {formula}.union(sub1).union(sub2)
    return {formula}

#  we have shown in class that, for all formula A, len(subformulas(A)) <= length(A).


def atoms(formula: Formula) -> set:
    """Returns the set of all atoms occurring in a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for atom in atoms(my_formula):
        print(atom)

    This piece of code above prints: p, s
    (Note that there is no repetition of p)
    """
    atoms_set = set()
    if isinstance(formula, Atom):
        atoms_set.add(formula)
    if isinstance(formula, Not):
        atoms_set.update(atoms(formula.inner))
    if isinstance(formula, (Implies, And, Or)):
        atoms_set.update(atoms(formula.left))
        atoms_set.update(atoms(formula.right))
    return atoms_set


def number_of_atoms(formula: Formula) -> int:
    """Returns the number of atoms occurring in a formula.
    For instance,
    number_of_atoms(Implies(Atom('q'), And(Atom('p'), Atom('q'))))

    must return 3 (Observe that this function counts the repetitions of atoms)
    """
    if isinstance(formula, Not):
        return number_of_atoms(formula.inner)
    if isinstance(formula, (Implies, And, Or)):
        return number_of_atoms(formula.left) + number_of_atoms(formula.right)
    return 1
def number_of_connectives(formula: Formula) -> int:
    """Returns the number of connectives occurring in a formula."""
    if isinstance(formula, Not):
        return number_of_connectives(formula.inner) + 1
    if isinstance(formula, (Implies, And, Or)):
        return number_of_connectives(formula.left) + number_of_connectives(formula.right) + 1
    return 0

def is_literal(formula: Formula) -> bool:
    """Returns True if formula is a literal. It returns False, otherwise"""
    return isinstance(formula, Atom) or (isinstance(formula, Not) and isinstance(formula.inner, Atom))

def substitution(formula: Formula, old_subformula: Formula, new_subformula: Formula) -> Formula:
    """Returns a new formula obtained by replacing all occurrences
    of old_subformula in the input formula by new_subformula."""
    if formula == old_subformula:
        return new_subformula
    if isinstance(formula, Not):
        formula.inner = substitution(formula.inner, old_subformula, new_subformula)
    if isinstance(formula, (Implies, And, Or)):
        formula.left = substitution(formula.left, old_subformula, new_subformula)
        formula.right = substitution(formula.right, old_subformula, new_subformula)
    return formula

def is_clause(formula: Formula) -> bool:
    """Returns True if formula is a clause. It returns False, otherwise"""
    if isinstance(formula, Or):
        return is_clause(formula.left) and is_clause(formula.right)
    return is_literal(formula)


def is_negation_normal_form(formula: Formula):
    """Returns True if formula is in negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_cnf(formula: Formula):
    """Returns True if formula is in conjunctive normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_term(formula: Formula):
    """Returns True if formula is a term. It returns False, otherwise"""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_dnf(formula: Formula):
    """Returns True if formula is in disjunctive normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_decomposable_negation_normal_form(formula: Formula):
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========
