"""Quatro colegas precisam se reunir em algum dia útil da semana.
João pode na Segunda, Quarta ou Quinta.
Carol não pode na Quarta.
Ana não pode na Sexta.
Pedro não pode Terça nem Quinta.
Existe um dia que eles possam se reunir satisfazendo todas as demandas?"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from formula import Atom, Or, Not, And
from semantics import satisfiability_brute_force
from dpll import sat_dpll
meeting_monday = Atom('reuniao na segunda')
meeting_tuesday = Atom('reuniao na terca')
meeting_wednesday = Atom('reuniao na quarta')
meeting_thursday = Atom('reuniao na quinta')
meeting_friday = Atom('reuniao na sexta')

joao = Or(Or(meeting_monday, meeting_wednesday), meeting_thursday)
carol = Not(meeting_wednesday)
ana = Not(meeting_friday)
pedro = And(Not(meeting_tuesday), Not(meeting_thursday))

all_requirements = And(And(And(joao, carol), ana), pedro)

print(sat_dpll(all_requirements))
print(satisfiability_brute_force(all_requirements))
