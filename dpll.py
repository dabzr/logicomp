from formula import Formula, Not, Or, And, Implies, Atom
from functions import is_cnf
def sat_dpll(f: Formula):
    formula = f
    if not is_cnf(f):
        formula = to_cnf(f)
    s = cnf_to_set(formula)
    first = next(iter(s[-1]))
    s.pop()
    pos, neg = first, negate(first)
    return sat_rec(pos, s) or sat_rec(neg, s) 

def sat_rec(f: Formula, lst: list[set[Formula]]):
    i = 0
    lst = remove_duplicates(lst)
    interp = {}
    while True:
        if isinstance(f, Atom):
            interp[f] = True
        if isinstance(f, Not):
            interp[f.inner] = False 
        if not lst:
            return interp
        if f not in lst[i] and negate(f) not in lst[i]:
            f = next(iter(lst[i]))
            i+=1
            continue
        if f in lst[i]:
            lst.pop(i)
            continue
        if negate(f) in lst[i]:
            lst[i].discard(negate(f))
            if lst[i] == {}:
                return None
            f = next(iter(lst[i]))
            continue

def remove_duplicates(lst):
    stack = []
    for i in lst:
        if i not in stack:
            stack.append(i)
    return stack

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

def cnf_to_set(f: Formula) -> list[set[Formula]]:
    clauses = all_clauses_from_cnf(f)
    return all_literals_from_cnf(clauses)

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
    return remove_duplicates(list((map(lambda x: literals_in_clause(x, set()), clauses))))

formula = And(And(Not(Atom("p")), Atom("q")), Not(Atom("q")))
formula_cnf = to_cnf(formula)
formula_set = cnf_to_set(formula_cnf)
print(f"Formula: {formula}")
print(f"Formula equivalente na CNF: {formula_cnf}")
print(f"CNF como set: {formula_set}")
