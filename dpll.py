from formula import Formula, Not, Or, And, Implies, Atom
from functions import is_cnf

def sat_dpll(f: Formula):
    f = to_cnf(f) if not is_cnf(f) else f
    s = get_clauses_list(f)
    first = next(iter(s[-1]))
    return sat_rec(first, s, set()) or sat_rec(negate(first), s, set()) 

def sat_rec(literal: Formula, clauses: list[set[Formula]], visited_literals: set):
    if negate(literal) in visited_literals:
        return False
    if not clauses:
        return True
    visited_literals.add(literal)
    if literal in clauses[-1]:
        return sat_rec(literal, clauses[:-1], visited_literals)
    if negate(literal) in clauses[-1]:
        if clauses[-1] == {negate(literal)}:
            return False
        clauses[-1].remove(negate(literal))
    return sat_rec(next(iter(clauses[-1])), clauses, visited_literals)

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
            s.add(f.left)
            return acc_clauses(f.right, s)
        s.add(f)
        return s
    return acc_clauses(f, set())

def all_literals_from_cnf(clauses: set[Formula]) -> list[set[Formula]]:
    def literals_in_clause(f: Formula, s: set[Formula]):
        if isinstance(f, Or):
            s.add(f.left)
            return literals_in_clause(f.right, s)
        s.add(f)
        return s
    return list((map(lambda x: literals_in_clause(x, set()), clauses)))

