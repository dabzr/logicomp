from formula import Formula, Not, Or, And, Implies, Atom
from functions import is_cnf

def sat_dpll(f: Formula):
    f = to_cnf(f) if not is_cnf(f) else f
    clauses = get_clauses_list(f)
    return dpll(clauses, set())

def dpll(clauses: list[set[Formula]], assignment: set[Formula]) -> bool:
    clauses = pure_literal_elimination(unit_propagate(clauses))

    if not clauses:
        return True 
    if any(clause == set() for clause in clauses):
        return False

    literal = choose_literal(clauses)
    return dpll(
        [clause - {literal} for clause in clauses if literal not in clause],
        assignment | {literal}
    ) or dpll(
        [clause - {negate(literal)} for clause in clauses if negate(literal) not in clause],
        assignment | {negate(literal)}
    )

def unit_propagate(clauses: list[set[Formula]]) -> list[set[Formula]]:
    while True:
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        if not unit_clauses:
            break
        unit_literal = next(iter(unit_clauses[0]))
        clauses = [clause - {negate(unit_literal)} for clause in clauses if unit_literal not in clause]
    return clauses

def pure_literal_elimination(clauses: list[set[Formula]]) -> list[set[Formula]]:
    all_literals = {literal for clause in clauses for literal in clause}
    pure_literals = {literal for literal in all_literals if negate(literal) not in all_literals}
    for pure_literal in pure_literals:
        clauses = [clause for clause in clauses if pure_literal not in clause]
    return clauses

def choose_literal(clauses: list[set[Formula]]) -> Formula:
    literal_counts = {}
    for clause in clauses:
        for literal in clause:
            literal_counts[literal] = literal_counts.get(literal, 0) + 1
    return max(literal_counts, key=lambda x: literal_counts[x])

def negate(f: Formula) -> Formula:
    if isinstance(f, Not):
        return f.inner
    return Not(f)

def to_cnf(f: Formula) -> Formula:
    return distribute(double_neg_remove(de_morgan(replace_implies(f))))

def replace_implies(f: Formula) -> Formula:
    if isinstance(f, Implies):
        return Or(Not(replace_implies(f.left)), replace_implies(f.right))
    if isinstance(f, Not):
        return Not(replace_implies(f.inner))
    if isinstance(f, Or):
        return Or(replace_implies(f.left), replace_implies(f.right))
    if isinstance(f, And):
        return And(replace_implies(f.left), replace_implies(f.right))
    return f

def de_morgan(f: Formula) -> Formula:
    if isinstance(f, Not):
        if isinstance(f.inner, And):
            return Or(Not(de_morgan(f.inner.left)), Not(de_morgan(f.inner.right)))
        if isinstance(f.inner, Or):
            return And(Not(de_morgan(f.inner.left)), Not(de_morgan(f.inner.right)))
        return Not(de_morgan(f.inner))
    if isinstance(f, And):
        return And(de_morgan(f.left), de_morgan(f.right))
    if isinstance(f, Or):
        return Or(de_morgan(f.left), de_morgan(f.right))
    if isinstance(f, Implies):
        return Implies(de_morgan(f.left), de_morgan(f.right))
    return f

def double_neg_remove(f: Formula) -> Formula:
    if isinstance(f, Not):
        if isinstance(f.inner, Not):
            return double_neg_remove(f.inner.inner)
        return Not(double_neg_remove(f.inner))
    if isinstance(f, Or):
        return Or(double_neg_remove(f.left), double_neg_remove(f.right))
    if isinstance(f, And):
        return And(double_neg_remove(f.left), double_neg_remove(f.right))
    if isinstance(f, Implies):
        return Implies(double_neg_remove(f.left), double_neg_remove(f.right))
    return f

def distribute(f: Formula) -> Formula:
    if isinstance(f, Or):
        if isinstance(f.left, And):
            return And(Or(distribute(f.left.left), distribute(f.right)), Or(distribute(f.left.right), distribute(f.right)))
        return Or(distribute(f.left), distribute(f.right))
    if isinstance(f, Not):
        return Not(distribute(f.inner))
    if isinstance(f, And):
        return And(distribute(f.left), distribute(f.right))
    if isinstance(f, Implies):
        return Implies(distribute(f.left), distribute(f.right))
    return f

def get_clauses_list(f: Formula) -> list[set[Formula]]:
    return all_literals_from_cnf(all_clauses_from_cnf(f))

def all_clauses_from_cnf(f: Formula) -> set[Formula]:
    def acc_clauses(f: Formula, s: set[Formula]):
        if isinstance(f, And):
            return acc_clauses(f.left, s) | acc_clauses(f.right, s)
        s.add(f)
        return s
    return acc_clauses(f, set())

def all_literals_from_cnf(clauses: set[Formula]) -> list[set[Formula]]:
    def literals_in_clause(f: Formula, s: set[Formula]):
        if isinstance(f, Or):
            return literals_in_clause(f.left, s) | literals_in_clause(f.right, s)
        s.add(f)
        return s
    return list(map(lambda x: literals_in_clause(x, set()), clauses))

