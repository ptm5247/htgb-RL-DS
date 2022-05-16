---
layout: page
title: About display_lib.py
description: >
  A description of the contents of the `display_lib` file.
hide_description: true
sitemap: false
---

`display_lib.py` is a file containing a few common variables and helper functions designed to
create neat-looking output in Jupyter Notebooks. Below is an explanation of its contents.

### Imports

```python
# file: "display_lib.py"
import numpy as np
from IPython.display import display, Markdown
from matplotlib import pyplot as plt
```

`IPython.display` is one of the packages which Jupyter Notebooks uses extensively. By calling
`display(Markdown(''))`, any code that can be used in Jupyter Notebook Markdown cells can be passed
in place of the empty string and it will be displayed as if it were a Markdown cell. This allows
for full use or Markdown or HTML style with code-generated values.

### Common Variables

```python
# file: "display_lib.py"
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
```

`ranks` is a list containing the colloquial names of the 8 ranks, and is ordered from lowest to
highest. `rank_colors` is a `numpy.ndarray` containing RGB values of the colors commonly associated
with each rank, in the same order as `ranks`. This is used to color-code graphs. The RBG values are
represented as `float`s between 0 and 1, since that is the format expected by `matplotlib` methods.

### The `html_table` Function

```python
# file: "display_lib.py"
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
```

The docstring for this method is fairly self-explanatory. This function makes extensive use of
python's format strings (`f'{}'`) and list comprehension in order to iterate though the parameters
and generate an HTML string for a table. Then, it uses the `IPython.dislpay` package to display the
table nicely in Jupyter Notebooks.

### The `violinplot` Function

```python
# file: "display_lib.py"
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
```

See the docstring for a description of the function and its parameters. `pyplot.violinplot`
requires that the vectors forming the distributions are the same length. This function gets around
that restriction by plotting them one at a time. Normally, this would have the side effect of each
violin being a different and random color. However, this method was designed to plot one violin for
each of the ranks, whose colors are also defined in this file. So, after plotting each of the
violins, it uses the return value to set the color to that of the associated rank. For simplicity,
it is required that the distributions passed in are in order of ascending rank. This is the reason
why the `ranks` variable is provided in this file.

### The `errorbar` Function

```python
# file: "display_lib.py"
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
```

This function will create an error bar plot using `pyplot.errorbar`. It is written to take the same
input as `violinplot`, so that no additional processing needs to be done in the calling scope. The
central line to this plot will be the means of the distributions, and the error bars will have a
length equal to the standard deviation. This plot will retain the default blue color of `matplotlib`.