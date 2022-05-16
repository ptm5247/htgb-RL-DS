---
layout: page
title: Exploratory Data Analysis
description: >
  Step 5 of the pipeline is EDA. Time to explore your data!
hide_description: true
sitemap: false
---

Now that you've tidied everything that needs tidying and considered everything that needs
considering, it's finally time to start looking for correlations in your data! As you do so, it is
important to consider the assumptions associated with that specific correlation. If those
conditions are not satisfied, you may need to apply some sort of transformation to your data or
explore a different kind of correlation. For this project, I will be looking for linear
relationships (with or without transformations) and will be performing linear regressions. So, what
are the assumptions that I am making?

## Assumptions of the Linear Regression Model

1. The Existance of a Linear Relationship: This one might seem kind of obvious, but if you are
using linear regression, you should be doing it to model a truly linear relationship! You can draw
a line of best fit over any dataset, and you might get a statistically significant result. However,
that does not necessarily mean there is a truly linear relationship. If there is a linear
relationship, we would expect the residuals from the model to be have a mean of 0. If the mean of
the residuals is not zero in some parts of the graph, we should consider a transformation or a
different model.
2. Independence of Residuals: There should be no correlation between consecutive residuals. As part
of my pre-processing steps, I removed metrics that would contribute significantly to correlations
between residuals. For example, `shots` is directly correlated with `shots_against` for the
opponent. Since I removed all of these kinds of metrics, it is now safe to assume this.
3. Homoscedastity and Normality of Residuals: These conditions basically mean that tje residuals
should be normally distributed with a mean of 0. In my exploration I will be plotting residual
distributions for the purpose of verifying this assumption.

## Searching for Linear Relationships in the Data

I'm finally ready to start plotting, so let's get right into it. Below is an explanation of the
code found in [exploratory_data_analysis.ipynb][00]. The outputs of some of the code cells in this
file are large arrays of plots, and in order to keep this page neat will not be shown in their
entirety. Specific plots will be shown in the discussion following the code cell, and a link will
be provided to a separate page where you will be able to view the full figure.

### Imports

```python
# file: "exploratory_data_analysis.ipynb"
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from display_lib import html_table, violinplot, errorbar, ranks, rank_colors
from statsmodels.api import OLS, add_constant
import pickle

data = pd.read_pickle('summaries\\data_frame')
```

In this file I am introducing a new package, which is `statsmodels.api`. I will be performing a
few linear regressions for this project, and `OLS` and `add_constant` will be of great use for
this. There are many libraries that allow you to do linear regression, like `numpy` or `sklearn`,
but `statsmodels` performs a detailed statistical analysis as it calculates the results, which will
make the next part of the pipeline, hypothesis testing, only a matter of checking some of the
values generated in this stage. I begin this notebook by reading the data table updated in the last
step back into memory.

### Defining a Regression Function

```python
# file: "exploratory_data_analysis.ipynb"
def show_regressions(x):
  # initialize the figure
  gs = plt.GridSpec(19, 2)
  plt.figure(figsize=(15, 75))

  models = {}

  data_ = data.drop(['title', 'duration', 'shots', 'goals', 'saves', 'score'], axis=1)
  for i, (metric, df) in enumerate(data_.iteritems()):
    # separate metrics into distributions by rank
    _, series = zip(*df.groupby('rank'))

    # create error bar plots by rank
    plt.subplot(gs[i, 0])
    errorbar(series)
    plt.title('Mean and Stdev by Rank')
    plt.ylabel(metric)

    # create a linear regression model for the metric
    model = OLS(df, x)
    res = model.fit()
    models[metric] = res

    # calculate the residuals from the linear model
    df_res = df.subtract((x * res.params.array).sum(axis=1))
    # separate into distributions by rank
    _, series = zip(*df_res.groupby('rank'))

    # create a violin and error bar plots for residuals
    plt.subplot(gs[i, 1])
    errorbar(series)
    violinplot(series)
    plt.title('Regression Residuals by Rank')

  # show the figure
  plt.tight_layout()
  plt.show()

  return models
```

First, I want to view a linear regression of all of my selected metrics against player rank. I am
looking for metrics that have strong correlations (positive or negative) with a player's total
skill level. I will be making plots for 19 different metrics, so I use a `GridSpec` to organize
them all in one grid.

Before performing the regressions, I drop 6 columns from the data. `title` is dropped since it is
not actually a metric. I normalized the columns using `duration`, so the values in this column will
all be the same. I drop the other 4 because I do not believe they will provide meaningful insight.
`shots`, `goals`, `saves` and `score` are metrics that actually appear on the scoreboard in game,
and are obvious objectives when playing. As a result, these metrics are obviously correlated with
good performance (especially since `goals` determines the outcome of the entire match). What I am
more interested in finding through this analysis is which of the other metrics (which players might
not be thinking of as often since they are not tracked and displayed in game) are most conducive to
good performance. In other words, which of these other things, when done well, allow players to
take more shots, make more saves, and score more goals?

The `score` metric is a general performance metric shown in game, not a record of the number of
goals each team has scored. 100 points are awarded for a goal, 50 for a save (plus an extra 25 if
the ball was particularly close to going in), 50 for an assist, 20 for a clear (getting the ball
away from the area around the net while on defense), 10 for a shot (getting the ball in the
vicinity of the opponent's net, even if it doesn't go in), and 2 for a meaningful hit on the ball.
{:.note}

Next, I iterate though each metric, and separate the data by rank each time. I make two plots for
each metric. The first is an error bar plot showing the progression of the mean aand standard
deviation of the metric across ranks. I then calculate a linear regression on the metric, and use
the second plot to evaluate it. The second plot shows the regression residuals for each rank in a
violin plot (with another error bar plot overlayed). Since the assumptions of the linear model I
need to verify are centered around the shape of residual distributions, this plot will make it easy
to evaluate whether or not the relationship I am modeling is likely to be linear. To create these
plots I am using two methods I wrote in [display_lib.py][00]. To see the source code with a quick
explanation, check out the [diaplay_lib page][01].

Finally, I return a dictionary containing each of the regression models that were calculated, since
I will need them for hypothesis testing.

### Making the First Plots

```python
# file: "exploratory_data_analysis.ipynb"
r = data.index.get_level_values('rank')
r = r.map(dict((r, i) for i, r in enumerate(ranks)))
x = add_constant(r)

models = show_regressions(x)
```
Output is hidden to conserve space... [View it here.][02]
{:.faded}

There's a lot to unpack here. First of all, there are a few plots that look pretty bad. For
example:

![eda_ex_01](/assets/img/eda/eda_ex_01.png)

These are the plots created by the `count_powerslide` metric, which counts how many times a player
uses powerslide during a match. Powerslide causes the car's wheels to lose grip, allowing the
player to drift. This can be helpful when turning around quickly. It also allows players to
maintain more of their momentum when landing sideways from a jump. As shown by the plot on the
left, there doesn't seem to be much change in usage at the lower ranks, but it starts to increase
dramatically after Gold and then levels off again at the higher ranks. This is clearly not a linear
relationship, and this is reflected in the plot on the right. According to the assumptions of the
linear regression model, we would expect the regression residual distributions to be approximately
normally distributed and have means very close to zero. This is clearly not the case, as the means
are all over the place and the distributions are heavily skewed, some even appearing to be bimodal.

However, there are also some prmomising results. Take a look at the plots for
`avg_distance_to_ball`:

![eda_ex_02](/assets/img/eda/eda_ex_02.png)

The vertical axis units for this metric are Unreal Units, which are the units of measurement used
by the game engine Rocket League is built on. For reference, the playing field is approximately
rectangular, and measures 8,192 by 10,240 Unreal Units.
{:.note}

This measures exactly what is sounds like: the average distance between the player and the ball
during the match. These plots look much better than the last ones. First of all, the progression of
the means in the left plot actually looks relatively linear. More importantly, the residual
distributions in the right plot look great! They are all centered very close to zero, and they all
appear to be approximately normal. This is evidence supporting a linear relationship and the use
of a linear regression model, which is exactly what I am looking for. In this plot we can also see
that the Bronze distribution is much wider than the others, which is something I said I was
expecting during the last step. The sample size of Bronze data is unfortunately much smaller than
it is for other ranks, so we would naturally expect wider and less strictly normal distributions.
In this case though, while it is wider than the rest, it still looks approximately normal.

These are two extremes of the spectrum of plots I got, so let's take a look at one that lies
somewhere in the middle:

![eda_ex_03](/assets/img/eda/eda_ex_03.png)

This shows the data for `percent_supersonic_speed`, which is the percentage of the match a player
spends at *supersonic speed*. The maximum speed attainable by the cars is 2,300 Unreal Units per
second. *Supersonic speed* refers to any speed above 2,200 Unreal Units per second. When a player
is moving at supersonic speed, a trail will appear behind their wheels, and running into an
opponent at this speed will demolish (or *demo*) them. *Demoing* a player will blow up their car
and remove them from the game for 3 seconds, after which they will respawn at the back of their
side of the field. Looking at the residual distributions for this plot, there are two things to
note. First, the shapes look good. The distributions appear to be normally distributed (with the
possible exception of the lowest ranks, but this is permissible due to their smaller sample size).
Second, the distributions are not centered around zero. However, unlike with `count_powerslide`,
they follow a much smoother path. Specifically, the progression of means appears to behave like the
graph of x cubed. As a matter of fact, this cubic-like progression of means is pretty common among
the plots generated in this step, and for that reason I am going to apply a cubic transformation of
the data. I am going to add two new terms to the regression, which are rank squared and rank cubed.
Essentially, this means that I will be finding a "cubic of best fit" for the data. I am hoping that
the added flexibility of the cubic model will counteract the cubic-like variations in the
residuals.

### Modeling the Transformed Data

```python
# file: "exploratory_data_analysis.ipynb"
x = np.array([(r - 3.5)**i for i in range(4)]).T

cube_models = show_regressions(x)
```
Output is hidden to conserve space... [View it here.][03]
{:.faded}

In many cases, this seemed to have the desired effect! Models that were already performing well,
like `avg_distance_to_ball` still look good, and models with cubic-like variations in regression
means are looking much better. Let's revisit `percent_supersonic_speed` to see a specific example:

![eda_ex_04](/assets/img/eda/eda_ex_04.png)

Much better! The approximately normal shapes we saw before have been preserved, and now they are
centered around zero too. This aligns much better with the assumptions of the linear regression
model, and is exactly the kind of relationship I was looking for. Out of my initial 19 metrics, I
now have good models for over half of them. Since what I am trying to do is find the simple, strong
correlations, instead of looking for more complex models for the remaining metrics, I am going to
drop them. These metrics either have more complex behavior, or are not appreciably different among
certain ranks, and therefore do not align with the goals of this analysis.

### Dropping the Weak Cubic Models

```python
# file: "exploratory_data_analysis.ipynb"
for metric in [
  'avg_amount', 'amount_stolen', 'amount_used_while_supersonic', 'percent_zero_boost',
  'percent_full_boost', 'count_powerslide', 'percent_high_air'
]:
  cube_models.pop(metric)
```

These are the metrics whose residual distributions showed the least support for the assumptions of
the linear model, either because they did not appear approximately normal or because they were not
consistantly centered around zero.

## Another Point of View

The models I just made examined trends across ranks, which considered combined data from each
player in each match in each rank. Now I want to take a different approach. Many people have
many different playstyles, and one of the strengths a player can have is the ability to adapt to
their opponent's playstyle, playing to their weaknesses and being aware of their strengths? But
what are the aspects of your opponent's playstyle that you should be focusing on? To answer that,
I will now change what I am considering to be a sinlge observation. Before, both players in each
match were counted separately. Now, I will consider the difference in metrics between players for
each match, making each match a single observation. By doing this I hope to identify which metrics
gives players an edge over their opponent, regardless of rank.

### Calculating the Metric Differences

```python
# file: "exploratory_data_analysis.ipynb"
diff = data.drop(['title', 'duration'], axis=1).diff()[1::2]
```

First, I drop the title and duration, since they are not useful anymore (and because having strings
in the table will mess up the next step). Then I use `DataFrame.diff`, which calculates the
difference between every row in the data and the row above it. Because of the way I set up my
table, rows for the two players in one game are always right next to eachother. Now, when I take
every other row of the table using `[1::2]`, I will get 1 row per game, each containing the
difference between the metrics for each player.

### Creating the Goal Difference Plots

```python
# file: "exploratory_data_analysis.ipynb"
# initialize the figure
gs = plt.GridSpec(19, 2)
plt.figure(figsize=(15, 75))

diff_models = {}
y = diff['goals']
_, ygb = zip(*y.groupby('rank'))

diff_ = diff.drop(['shots', 'goals', 'saves', 'score'], axis=1)
for i, (metric, df) in enumerate(diff_.iteritems()):
  # separate metrics into distributions by rank
  _, series = zip(*df.groupby('rank'))

  # create a regression model for all ranks
  x = add_constant(df)
  model = OLS(y, x)
  res = model.fit()
  diff_models[metric] = res

  # create a scatterplot of goal difference vs metric
  plt.subplot(gs[i, 0])
  for xs, ys, cs in zip(series, ygb, rank_colors):
    # only plot 1 in 10 points since there are so many
    plt.scatter(xs[::10], ys[::10], c=[cs])
  plt.title(f'Goal Difference vs {metric} Difference')
  plt.xlabel(metric)
  plt.ylabel('Goal Difference')

  # plot the regression line over the scatterplot
  xf = np.linspace(df.min(), df.max(), 2)
  yf = (add_constant(xf) * res.params.array).sum(axis=1)
  plt.plot(xf, yf, color='black')

  # calculate regression residuals by rank
  df_res = y.subtract((x * res.params.array).sum(axis=1))
  _, series = zip(*df_res.groupby('rank'))

  # create a violin and error bar plots for residuals
  plt.subplot(gs[i, 1])
  errorbar(series)
  violinplot(series)
  plt.title('Regression Residuals by Rank')

# show the figure
plt.tight_layout()
plt.show()
```
Output is hidden to conserve space... [View it here.][04]
{:.faded}

The code here is very similar to the `show_regressions` function, but it is being used to generate
different types of plots.

The plot on the left is a scatter plot of goal difference versus metric difference. The points are
color coded by rank. A linear regression line is calculated and overlayed. If there is a strong
correlation in on or more of these graphs, it would suggest that outperforming your opponent in
that specific metric is correlated with you scoring more goals than them. The plot on the right
shows the regression residuals, separated by rank, in the same way that it did previously.

Looking at the output, I noticed something unexpected. The residual distributions look almost the
same for every metric! Let's take a look at one:

![eda_ex_05](/assets/img/eda/eda_ex_05.png)

This is `percent_supersonic_speed`, which we looked at last time too. The shape of this plot is
almost the same as every other plot (though the slopes of each regression line are different). This
is good though, since the residual distributions do support the assumptions of the linear model.
They are all centered close to zero and are all approximately "normally distributed". I put that in
quotes since there is a dip near the mean of most of these distributions, which would otherwise be
approximately normally distributed. The reason behind this dip actually comes from the fact that I
am using goal differences. A rocket league match cannot end in a tie, so a goal difference of zero
is actually impossible. If you look at the scatter plot you will see this, as there is a gap in the
plot around the horizontal axis. If you look close enough, this is present in every single plot. As
a result, regression lines with a low slope will have large dips near the means of their regression
distributions. Compare this plot to the plot of `percent_offensive_third`, which measures the
percentage of the match a player spends in the opponent's third of the field:

![eda_ex_06](/assets/img/eda/eda_ex_06.png)

This regression line has a much steeper slope, so the gap in the scatter plot around the horizontal
axis has much less of a visible effect on the regression distributions.

There is one notable outlier in this set of plots. `percent_behind_ball` measures the percentage of
the match that the player spends between the ball and their own net, and the correlation on this
plot appears *much* stronger than on any of the other plots:

![eda_ex_07](/assets/img/eda/eda_ex_07.png)

The regression distributions are very narrow, and there is no dip around the mean since the
regression line has a high slope. I suspect that in the next step, hypothesis testing, I will
confirm that this is in fact a much more accurate model than any of the others.

### Dropping the Weak Difference Models

Unlike last time, there are no trends that suggest to me that I should apply some kind of
transformation to the data. However, some plots still look weaker than others, so I will remove a
few that provide the least support for the linear model, following the same reasoning that I did
for the previous models.

```python
# file: "exploratory_data_analysis.ipynb"
for metric in [
  'amount_stolen', 'percent_zero_boost', 'percent_full_boost',
  'percent_defensive_third', 'percent_offensive_third'
]:
  diff_models.pop(metric)

with open('summaries\\models', 'wb') as f:
  pickle.dump((cube_models, diff_models), f)
```

I have found a set of models that satisfy the conditions I was searching for, so I am ready to move
on to the next step: hypothesis testing. Before doing so, I pickle the models so I will be able to
load them into the next file.

Continue with [Hypothesis Testing](hypothesis_testing.md){:.heading.flip-title}
{:.read-more}

[00]: /320_FP/
[01]: /320_FP/pages/display_lib/
[02]: /320_FP/extras/EDA_01/
[03]: /320_FP/extras/EDA_02/
[04]: /320_FP/extras/EDA_03/