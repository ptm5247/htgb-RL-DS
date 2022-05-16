# This file contains helper methods for displaying nicely formatted outputs in Jupyter Notebooks.

import numpy as np
from IPython.display import display, Markdown
from matplotlib import pyplot as plt

# the order and color associated with each rank
ranks = ['Bronze', 'Silver', 'Gold', 'Plat', 'Diamond', 'Champ', 'GC', 'SSL']
rank_colors = np.array([
  [147, 80, 5],
  [92, 91, 89],
  [197, 150, 29],
  [44, 173, 231],
  [4, 57, 155],
  [136, 86, 211],
  [193, 43, 29],
  [224, 135, 193]
]) / 255

def html_table(cols, rows):
  '''Generates html for a table containing the passed information,
  and displays it using Jupyter Notebooks Markdown.

  ## Parameters:
  cols
    A sequence of strings containing the labels of the table's columns.
  rows
    A sequence of 2-tuples, each containing the row label and a dictionary of values
    for that row. The dictionary's keys should match the column labels.
  '''
  html = f'''<table style="margin-left:auto;margin-right:auto;">{
    f"""<tr><td></td>{
      ''.join([f'<td style="text-align:center"><b>{col}</b></td>' for col in cols])
  }</tr>"""
  }{
    ''.join([
      ''.join([f'<tr><td style="text-align:center"><b>{name}</b></td>', *[
        f'<td style="text-align:center">{row[col]}</td>'
      for col in cols], '</tr>'])
    for name, row in rows])
  }</table>'''

  # display the html table in the Jupyter Notebook
  display(Markdown(html))

def violinplot(dataset):
  '''Creates a violinplot similar to `plt.violinplot`, but with some added bonuses:
  - The datasets for each x value do not have to be the same length
  - The violins will be colored according to the associated rank color

  ## Parameters:
  dataset
    The same parameter that would be passed to `plt.violinplot`. It is assumed that the plot should
    be against rank, and there will be no length check.
  '''
  for i, s in enumerate(dataset):
    # plot one violin to the current axes and iterate through its container (dict)
    for coll in plt.violinplot(s, positions=[i]).values():
      # the first value is a list whose first element represents the violin body
      if type(coll) == list:
        coll = coll[0]
        # retain the original alpha value of the violin body (.3)
        coll.set_fc([*rank_colors[i], coll.get_fc()[0, -1]])
      # the rest of the values represent the solid lines
      else:
        # for consistency, retain the alpha value here too (1)
        coll.set_ec([*rank_colors[i], coll.get_ec()[0, -1]])
  
  # put the ranks on the x axis
  plt.xticks(range(len(ranks)), ranks)

def errorbar(dataset):
  '''Creates an errorbar plot showing the means and standard deviations of the columns of
  `dataset`.
  
  ## Parameters:
  dataset
    The distributions for each rank. It is assumed that there is one for each rank, in order.
  '''
  plt.errorbar(
    range(len(ranks)),                # x values, to be replaced by ranks
    [d.mean() for d in dataset],      # y values, the means of each distribution
    yerr=[d.std() for d in dataset],  # errors, the stdev of each distribution
    capsize=5, capthick=2
  )

  # put the ranks on the x axis
  plt.xticks(range(len(ranks)), ranks)