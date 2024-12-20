"""You can test your functions in this module as in the following code: """

from formula import *
from functions import *


formula1 = Atom('p')  # p
formula2 = Atom('q')  # q
formula3 = And(formula1, formula2)  # (p /\ q)
formula4 = And(Atom('p'), Atom('s'))  # (p /\ s)
formula5 = Not(And(Atom('p'), Atom('s')))  # (¬(p /\ s))
formula6 = Or(Not(And(Atom('p'), Atom('s'))), Atom('q'))  # ((¬(p /\ s)) v q)
formula7 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Atom('r')))  # ((¬(p /\ s)) -> (q /\ r))
formula8 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s')))))
# ((¬(p /\ s)) -> (q /\ (¬(p /\ s))))

formula9 = Not(Not(Atom('q')))


print(formula1 == formula3)
print(formula1 == formula2)
print(formula3 == And(Atom('p'), Atom('q')))

print('formula1:', formula1)
print('formula2:', formula2)
print('formula3:', formula3)
print('formula4:', formula4)
print('formula5:', formula5)
print('formula6:', formula6)
print('formula7:', formula7)
print('formula8:', formula8)
print('formula9:', formula9)

print('length of formula1:', length(formula1))
print('length of formula3:', length(formula3))

print('length of formula7:', length(formula7))

print('subformulas of formula7:')
print(subformulas(formula7))

for subformula in subformulas(formula7):
    print(subformula)
# end for


print('length of formula8:', length(formula8))
print('subformulas of formula8:')

for subformula in subformulas(formula8):
    print(subformula)
# end for

#  we have shown in class that for all formula A, len(subformulas(A)) <= length(A):
# for example, for formula8:
print('number of subformulas of formula8:', len(subformulas(formula8)))
print('len(subformulas(formula8)) <= length(formula8):', len(subformulas(formula8)) <= length(formula8))

print(f'Atoms of formula8: {atoms(formula8)}')

print(f'Number of atoms of formula8 is: {number_of_atoms(formula8)}')

print(f'Number of connectives of formula8 is: {number_of_connectives(formula8)}')
print(f'formula8 is literal: {is_literal(formula8)}')
print(f'formula1 is literal: {is_literal(formula1)}')
print(f'formula9 is literal: {is_literal(formula9)}')
print(f'formula5 is literal: {is_literal(formula5)}')

old_subformula = Not(And(Atom('p'), Atom('s')))
new_subformula = And(Atom('p'), Atom('q'))
print(f'formula8: {formula8}')
print(f'old_subformula: {old_subformula}')
print(f'new_subformula: {new_subformula}')
formula8_clone = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s')))))
substitution(formula8_clone, old_subformula, new_subformula)
print(f'new formula8: {formula8_clone}')
clause = is_clause(Or(Atom('p'), Or(Atom('q'), Not(Atom('s')))))
print(f'is_clause(p ∨ q ∨ ¬s): {clause}')
clause = is_clause(Or(Atom('p'), And(Atom('q'), Atom('s'))))
print(f'is_clause(p ∨ q ∧ s): {clause}')
clause = is_clause(Not(Atom('p')))
print(f'is_clause(¬p): {clause}')
print(f"is formula8 is negation normal form? {is_negation_normal_form(formula8)}")
nnf = is_negation_normal_form(Or(Atom('p'), Or(Atom('q'), Not(Atom('s')))))
print(f"is_negation_normal_form(p ∨ q ∨ ¬s): {nnf} ")
cnf = And(Not(Atom('p')), And(Or(Atom('p'), Not(Atom('q'))), Or(Atom('s'), Atom('p'))))
print(f"is_cnf({cnf}): {is_cnf(cnf)}")
cnf = Or(Not(Atom('p')), And(Or(Atom('p'), Not(Atom('q'))), And(Atom('s'), Atom('p'))))
print(f"is_cnf({cnf}): {is_cnf(cnf)}")
dnnf = Or(And(Or(Atom('a'), Not(Atom('b'))), Or(Atom('c'), Atom('d'))), And(Or(Atom('a'), Atom('b')), Or(Not(Atom('c')), Not(Atom('d')))))
print(f"is_dnnf({dnnf}): {is_decomposable_negation_normal_form(dnnf)}")
height_test = Or(Implies(Atom('p'), Or(Atom('q'), Atom('r'))), Not(Atom('s')))
print(f"height({height_test}): {height(height_test)}")

from semantics import *

val = {
        Atom('p'): True,
        Atom('q'): False,
        Atom('s'): True
      } 

print(f"formula6 ({formula6}) tem v = {val} e portanto tem valor verdade {truth_value(formula6, val)}")

print(create_truth_table(formula8))
formula10 = Implies(Atom('p'), Atom('q'))
formula11 = Or(Not(Atom('p')), Atom('q'))
print(f"{formula10} é equivalente a {formula11}? {is_logical_equivalence(formula10, formula11)}")
print(f"{formula9} é equivalente a {formula2}? {is_logical_equivalence(formula9, formula2)}")
print(f"{formula3} é equivalente a {formula4}? {is_logical_equivalence(formula3, formula4)}")
print(f"{formula8} é equivalente a {formula7}? {is_logical_equivalence(formula8, formula7)}")
formula12 = Or(Implies(Atom('p'), Atom('q')), And(Atom('q'), Not(Atom('q'))))
print(f"{formula10} é equivalente a {formula12}? {is_logical_equivalence(formula10, formula12)}")
tautologia = Implies(Atom('p'), Atom('p'))
print(f"{tautologia} é uma tautologia? {is_valid(tautologia)}")
print(f"{formula10} é uma tautologia? {is_valid(formula10)}")
print(f"{tautologia} é satisfazivel? {satisfiability_brute_force(tautologia)}")
print(f"{formula10} é satisfazivel? {satisfiability_brute_force(formula10)}")
formula13 = And(Atom('p'), Not(Atom('p')))
print(f"{formula13} é satisfazivel? {satisfiability_brute_force(formula13)}")

premissas = [Implies(Atom('c'), Atom('v')), Implies(And(And(Not(Atom('s')), Atom('p')), Not(Atom('c'))), Atom('v')), Implies(And(Not(Atom('c')), Atom('s')), Not(Atom('v'))),Implies(And(And(Not(Atom('s')), Not(Atom('p'))), Not(Atom('c'))), Not(Atom('v')))]
conclusao = Implies(And(Atom('v'), Not(Atom('c'))), Atom('p')) 
print(f"{premissas} |- {conclusao}?")
print(is_logical_consequence(premissas, conclusao))

print(get_partial_interpretation(And(Atom("p"), And(Not(Atom('q')), And(Not(Not(Atom('r'))), Atom('s'))))))
