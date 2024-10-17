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


def is_negation_normal_form(formula: Formula) -> bool:
    """Returns True if formula is in negation normal form.
    Returns False, otherwise."""
    if isinstance(formula, Implies):
        return False
    if isinstance(formula, Not):
        return isinstance(formula.inner, Atom)
    if isinstance(formula, (And, Or)):
        return is_negation_normal_form(formula.left) and is_negation_normal_form(formula.right)
    return True


def is_cnf(formula: Formula) -> bool:
    """Returns True if formula is in conjunctive normal form.
    Returns False, otherwise."""
    if isinstance(formula, And):
        condL = is_clause(formula.left) or is_cnf(formula.left)
        condR = is_clause(formula.right) or is_cnf(formula.right)
        return condL and condR
    return False



def is_term(formula: Formula) -> bool:
    """Returns True if formula is a term. It returns False, otherwise"""
    if isinstance(formula, And):
        return is_clause(formula.left) and is_clause(formula.right)
    return is_literal(formula)



def is_dnf(formula: Formula) -> bool:
    """Returns True if formula is in disjunctive normal form.
    Returns False, otherwise."""
    if isinstance(formula, And):
        condL = is_term(formula.left) or is_dnf(formula.left)
        condR = is_term(formula.right) or is_dnf(formula.right)
        return condL and condR
    return False


def is_decomposable_negation_normal_form(formula: Formula) -> bool:
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""
    if is_negation_normal_form(formula):
        if isinstance(formula, And):
            if not (atoms(formula.left) & atoms(formula.right)):
                return True
            return is_decomposable_negation_normal_form(formula.left) and is_decomposable_negation_normal_form(formula.right)
        if isinstance(formula, Or):
            return is_decomposable_negation_normal_form(formula.left) and is_decomposable_negation_normal_form(formula.right)
    return False

def height(formula: Formula):
    """Defina uma função recursiva formula_height(formula) que retorna a altura de
formula, onde a altura é o maior numero de conectivos entre o conectivo mais externo
e as fórmulas atômicas. Por exemplo, para a fórmula (p → (q ∧ r)) ∨ ¬s, a altura é 3"""
    pass
