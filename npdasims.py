# -*- coding: utf-8 -*-
"""npdasims.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14hneEfAkXD1KKFpqI0j4cfWBz3Ia5mRX
"""

import pandas as pd
from datascience import *
import numpy as np
import random
from sys import exit
from scipy import stats
from operator import itemgetter
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
print('x' in np.arange(5))

raw = Table.from_df(pd.read_html('https://forensicstournament.net/NPDA/24/entries')[1])
entries = make_array()
for i in range(raw.num_rows):
  entries = np.append(entries, raw.column('School').item(i) + ' - ' + raw.column('Student(s)').item(i))
elos = make_array(1450,1450,1584.88,1534.7,1504.33,1534.25, 1520.11,1563.73,1487.74,1430.95,1539.64,1569.7,2012.57,1731.09,1701.48,1695.86,1550.13,1521.33,1563.67,1501.82,1480.74,1448.5,1429.33,1575.34,1484.74,1551.29,1509.88,1559.32,1511.13,1523.39,1471.91,1465.04,1538.3,1836.74,1762.14,1580.79,1566.63)
teams = Table().with_columns('School', np.append(raw.column('School'), 'Bye'), 'Team', np.append(raw.column('Student(s)'), 'Bye'), 'Elo', np.append(elos, 0))

def prelims():
  # Round 1
  round1 = teams
  for j in range(2):
    round1 = round1.sample(round1.num_rows, with_replacement=False)
    wins = make_array()
    for i in range(0, round1.num_rows, 2):
      if 1 / (math.pow(10.0, (-(round1.column('Elo').item(i) - round1.column('Elo').item(i+1)) / 400.0)) + 1) > random.random():
        wins = np.append(np.append(wins, 1), 0)
      else:
        wins = np.append(np.append(wins, 0), 1)
    round1 = round1.with_column('Round ' + str(j + 1), wins)
  total_wins = np.add(list(round1.column('Round 1')),list(round1.column('Round 2')))
  # Rounds 3-8
  round3 = round1.with_column('Wins', np.array(total_wins)).select('School', 'Team', 'Elo', 'Wins', 'Round 1', 'Round 2')
  for j in range(2,8):
    round3 = round3.sample(round3.num_rows, with_replacement = False).sort('Wins', descending = True)
    wins = make_array()
    for i in range(0, round1.num_rows, 2):
        if 1 / (math.pow(10.0, (-(round3.column('Elo').item(i) - round3.column('Elo').item(i+1)) / 400.0)) + 1) > random.random():
          wins = np.append(np.append(wins, 1), 0)
        else:
          wins = np.append(np.append(wins, 0), 1)
    round3 = round3.with_column('Round ' + str(j + 1), wins)
    total_wins = np.add(list(round3.column('Wins')), wins)
    round3 = round3.with_column('Wins', total_wins)
  prelim_tbl = round3.sample(round3.num_rows, with_replacement=False).sort('Wins', descending = True)
  return prelim_tbl

def elims():
  elim_tbl = prelims().where('Wins', are.above(4))
  # Octos
  octos_wins = make_array()
  elos = elim_tbl.column('Elo')
  for i in range(16 - elim_tbl.num_rows):
    octos_wins = np.append(octos_wins, 1)
  for i in range(len(octos_wins), 8):
    if 1 / (math.pow(10.0, (-(elim_tbl.column('Elo').item(i) - elim_tbl.column('Elo').item(15 - i)) / 400.0)) + 1) > random.random():
      octos_wins = np.append(octos_wins, 1)
    else:
      octos_wins = np.append(octos_wins, 0)
  for i in range(elim_tbl.num_rows - 8):
    octos_wins = np.append(octos_wins, 1 - octos_wins.item(7 - i))
  elim_tbl = elim_tbl.with_column('Octos', octos_wins).sort('Octos', descending=True)
  # Quarters
  quarters_wins = make_array()
  for i in range(4):
    if 1 / (math.pow(10.0, (-(elim_tbl.column('Elo').item(i) - elim_tbl.column('Elo').item(7 - i)) / 400.0)) + 1) > random.random():
      quarters_wins = np.append(quarters_wins, 1)
    else:
      quarters_wins = np.append(quarters_wins, 0)
  for i in range(4):
    quarters_wins = np.append(quarters_wins, 1 - quarters_wins.item(3 - i))
  for i in range(8, elim_tbl.num_rows):
    quarters_wins = np.append(quarters_wins, 0)
  elim_tbl = elim_tbl.with_column('Quarters', quarters_wins).sort('Quarters', descending = True)
  # Semis
  semis_wins = make_array()
  for i in range(2):
    if 1 / (math.pow(10.0, (-(elim_tbl.column('Elo').item(i) - elim_tbl.column('Elo').item(3 - i)) / 400.0)) + 1) > random.random():
      semis_wins = np.append(semis_wins, 1)
    else:
      semis_wins = np.append(semis_wins, 0)
  for i in range(2):
    semis_wins = np.append(semis_wins, 1 - semis_wins.item(1 - i))
  for i in range(4, elim_tbl.num_rows):
    semis_wins = np.append(semis_wins, 0)
  elim_tbl = elim_tbl.with_column('Semis', semis_wins).sort('Semis', descending = True)
  # Finals
  finals_wins = make_array()
  if 1 / (math.pow(10.0, (-(elim_tbl.column('Elo').item(0) - elim_tbl.column('Elo').item(1)) / 400.0)) + 1) > random.random():
    finals_wins = np.append(np.append(finals_wins, 1), 0)
  else:
    finals_wins = np.append(np.append(finals_wins, 0), 1)
  for i in range(2, elim_tbl.num_rows):
    finals_wins = np.append(finals_wins, 0)
  elim_tbl = elim_tbl.with_column('Finals', finals_wins).sort('Finals', descending = True)
  return elim_tbl

def elims_sim(n):
  team_tbl = teams.sort('Team')
  champ = []
  finals = []
  semis = []
  quarters = []
  for i in range(n):
    one_elim = list(elims().column('Team'))
    champ.append(one_elim[0])
    finals.append(one_elim[:2])
    semis = semis + one_elim[:4]
    quarters = quarters + (one_elim[:8])
  all_quarters = make_array()
  all_semis = make_array()
  all_finals = make_array()
  all_champ = make_array()
  for i in range(team_tbl.num_rows):
    win_octos = np.sum(team_tbl.column('Team').item(i) == np.array(quarters))
    win_quarters = np.sum(team_tbl.column('Team').item(i) == np.array(semis))
    win_semis = np.sum(team_tbl.column('Team').item(i) == np.array(finals))
    win_finals = np.sum(team_tbl.column('Team').item(i) == np.array(champ))
    all_quarters = np.append(all_quarters, win_octos)
    all_semis = np.append(all_semis, win_quarters)
    all_finals = np.append(all_finals, win_semis)
    all_champ = np.append(all_champ, win_finals)
  return team_tbl.with_columns('Quarters', all_quarters / n, 'Semis', all_semis / n, 'Finals', all_finals / n, 'Champ', all_champ / n)

elims_sim(10000).show()

def prelim_sim(n):
  all_wins = make_array()
  team_tbl = teams.sort('Team')
  for i in range(n):
    one_prelim = prelims().sort('Team')
    all_wins = np.append(all_wins, one_prelim.column('Wins'))
  for i in range(9):
    times_with_record = make_array()
    for j in range(teams.num_rows):
      condensed = make_array()
      for x in range(len(all_wins)):
        if (x - j)%teams.num_rows == 0:
          condensed = np.append(condensed, all_wins.item(x))
      times_with_record = np.append(times_with_record, np.sum(condensed == i))
    team_tbl = team_tbl.with_column(str(i) + "-" + str(8 - i), times_with_record / n)
  return team_tbl
prelim_sim(10000).show()

