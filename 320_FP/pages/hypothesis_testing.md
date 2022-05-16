---
layout: page
title: Hypothesis Testing
description: >
  Step 6 of the pipeline is hypothesis testing. Are your results statistically significant?
hide_description: true
sitemap: false
---

Just because you have found a correlation does not mean that it is statistically significant. For
example, if I flip a coint 10 times and get 6 heads, that is more heads than I might have been
expecting, but it would be unreasonable to conclude that the coin is somehow unfair. This is
because the results are not *statistically significant*. Random samples, like flipping a coin or
random players' replay files contain noise, and as a result we would not expect to measure the
mean or "expected" value every single time. Intead, we would expect to find values within a certain
range (which is likely centered around the mean). The width of this range is determined by factors
like sample size.

In statistics, a *hypothesis test* involves calculating the likelihood of our data being generated
if the *null hypothesis* is true. If the likelihood is below a certain threshold, we can say that
we have *statistically significant* evidence to reject the null hypothesis. The null hypothesis is
the assumption that we are trying to disprove. In the context of a linear regression, it would be
that there is no linear relationship between the variables we are considering. A common threshold
to use in data science is 5%. Using a threshold of 5% means that we only reject the null hypothesis
if the cumulative probability of finding our dataset or any dataset more extreme (farther from the
null hypothesis in either direction) is less than 5%. If you would like to learn more about
hypothesis testing, check out [this paper][00]

Fortunately, the `statsmodels` library which I used to calculate my linear regression models
automatically performs statistical analysis on the results, So all I need to do now is check the
probability values it generated and see if they fall below the 5% threshold. I do so in
[hypothesis_testing.ipynb][01], which is discussed below.

### Imports

```python
# file: "hypothesis_testing.ipynb"
import pickle
import numpy as np
from display_lib import html_table

with open('summaries\\models', 'rb') as f:
  cube_models, diff_models = pickle.load(f)
```

Since this is a new file, the first thing I do is load the `statsmodels` regression results that I
saved to a file in the last step.

### Displaying the Results of the Cubic Models

```python
# file: "hypothesis_testing.ipynb"
k, v = zip(*cube_models.items())
# calculate the indices to sort the models by rsquared
ind = np.flip(np.argsort([m.rsquared for m in v]))

# format the data for the table
cols = ['R Squared', 'P(const = 0)', 'P(x = 0)', 'P(x^2 = 0)', 'P(x^3 = 0)', 'P(F)']
rows = np.array([
  (k, dict(zip(cols, np.round([v.rsquared, *v.pvalues, v.f_pvalue], 4))))
for k, v in cube_models.items()])

html_table(cols, rows[ind])
```
Output:
<table style="margin-left:auto;margin-right:auto;"><tr><td></td><td style="text-align:center"><b>R Squared</b></td><td style="text-align:center"><b>P(const = 0)</b></td><td style="text-align:center"><b>P(x = 0)</b></td><td style="text-align:center"><b>P(x^2 = 0)</b></td><td style="text-align:center"><b>P(x^3 = 0)</b></td><td style="text-align:center"><b>P(F)</b></td></tr><tr><td style="text-align:center"><b>percent_supersonic_speed</b></td><td style="text-align:center">0.5829</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_speed_percentage</b></td><td style="text-align:center">0.4216</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_low_air</b></td><td style="text-align:center">0.3972</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>bpm</b></td><td style="text-align:center">0.3591</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_slow_speed</b></td><td style="text-align:center">0.3145</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0057</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>amount_collected</b></td><td style="text-align:center">0.2628</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0097</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_powerslide_duration</b></td><td style="text-align:center">0.1331</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_distance_to_ball</b></td><td style="text-align:center">0.1288</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0193</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_behind_ball</b></td><td style="text-align:center">0.087</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.084</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_offensive_third</b></td><td style="text-align:center">0.01</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.8356</td><td style="text-align:center">0.8267</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>inflicted</b></td><td style="text-align:center">0.0067</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.3121</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_defensive_third</b></td><td style="text-align:center">0.0017</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0826</td><td style="text-align:center">0.0144</td><td style="text-align:center">0.0</td></tr></table>

I use `numpy.argsort` on the values of R-squared for each model so that I can order the table by
strength of fit. Then, it is just a matter of extracting the probability values from the model
summaries in the format that is expected by `html_table`. As always, check out the
[display_lib page][02] for information about how that function works.

Looking at the table, there are a lot of zeros! I rounded all of the values to 4 decimal places, so
a probability of 0 in this table represents any probability less than 1/200th of a percent (which
is definitely statistically significant!). The right-most column shows the probability associated
with the F-statistic. The F-statistic is calculated by `statsmodels` and is basically a measure of
how likely I am to see data similar to mine if there is no correlation in these metrics. The
associated probabilities are all zero, meaning there defninitely is a correlation in every case.
One of the benefits with using large sample sizes (nearly 20,000 for this project) is that it makes
it easier to detect slight correlations. In small sample sizes, small correlations can be covered
up by noise, but if they are still there in large sample sizes it is much more likely to be
significant. The `P(const = 0)` (probability associated with the y-intercept of my models) and the
`P(x = 0)` (probability associated with the coefficient of the first power of x in the models)
columns also contain all zeros, which is good. The nonzero values in the other columns give some
insight about the effectiveness of the cubic transformation on those metrics. For example, the
values for `percent_offensive_third` are 82-83% for the higher dimensional coefficients, meaning
there is not statistically significant evidence to say that the cubic model was any more effective
than the linear model. Other values above 0.05 for different metrics suggest similar things.

### Displaying the Results of the Difference Models

```python
# file: "hypothesis_testing.ipynb"
k, v = zip(*diff_models.items())
# calculate the indices to sort the model by rsquared
ind = np.flip(np.argsort([m.rsquared for m in v]))

# format the data for the table
cols = ['R Squared', 'P(const = 0)', 'P(x = 0)', 'P(F)']
rows = np.array([
  (k, dict(zip(cols, np.round([v.rsquared, *v.pvalues, v.f_pvalue], 4))))
for k, v in diff_models.items()])

html_table(cols, rows[ind])
```
Output:
<table style="margin-left:auto;margin-right:auto;"><tr><td></td><td style="text-align:center"><b>R Squared</b></td><td style="text-align:center"><b>P(const = 0)</b></td><td style="text-align:center"><b>P(x = 0)</b></td><td style="text-align:center"><b>P(F)</b></td></tr><tr><td style="text-align:center"><b>percent_behind_ball</b></td><td style="text-align:center">0.5537</td><td style="text-align:center">0.0176</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_distance_to_ball</b></td><td style="text-align:center">0.0663</td><td style="text-align:center">0.0728</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_amount</b></td><td style="text-align:center">0.058</td><td style="text-align:center">0.0727</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>amount_collected</b></td><td style="text-align:center">0.0471</td><td style="text-align:center">0.0539</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_high_air</b></td><td style="text-align:center">0.0408</td><td style="text-align:center">0.0716</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_speed_percentage</b></td><td style="text-align:center">0.0205</td><td style="text-align:center">0.0287</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>bpm</b></td><td style="text-align:center">0.0182</td><td style="text-align:center">0.0284</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_slow_speed</b></td><td style="text-align:center">0.0151</td><td style="text-align:center">0.0259</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>count_powerslide</b></td><td style="text-align:center">0.0107</td><td style="text-align:center">0.0328</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>inflicted</b></td><td style="text-align:center">0.0077</td><td style="text-align:center">0.0204</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>amount_used_while_supersonic</b></td><td style="text-align:center">0.0048</td><td style="text-align:center">0.025</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>avg_powerslide_duration</b></td><td style="text-align:center">0.0035</td><td style="text-align:center">0.0186</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_supersonic_speed</b></td><td style="text-align:center">0.0018</td><td style="text-align:center">0.0205</td><td style="text-align:center">0.0</td><td style="text-align:center">0.0</td></tr><tr><td style="text-align:center"><b>percent_low_air</b></td><td style="text-align:center">0.0004</td><td style="text-align:center">0.0216</td><td style="text-align:center">0.0075</td><td style="text-align:center">0.0075</td></tr></table>

Extracting these values is done in the same way as it was for the cubic models, only this time
there are no higher order x coefficients.

This table is a little more interesting. The probabilities associated with the F-statistics are
still all below the 5% threshold, so we have statistically significant evidence to support the
existance of a linear relationship (also supportedd by the `P(x = 0)` column). However, there
are 4 values in the `P(const = 0)` column which are above the 5% threshold. This means that for
`avg_distance_to_ball`, `avg_amount` (of boost), `amount_collected` (also boost), and
`percent_high_air` (percentage of the match spent near the ceiling), there is not statistically
significant evidence to reject the null hypothesis that the y-intercept of the model should be
zero. What does that mean? It means that if you perform similar to you opponent for thse metrics,
the model should predict that you have a goal difference close to zero. This suggests that
opponents evenly matched for these metrics are likely to be evenly matched overall, and the winner
of the match would be more dependent on other metrics.

Now that I have verified a subset of my results to be statistically significant, it is time to
answer the project's central questions.

Continue with [Results](results.md){:.heading.flip-title}
{:.read-more}

[00]: https://www.westga.edu/academics/research/vrc/assets/docs/tests_of_significance_notes.pdf

[01]: /320_FP/

[02]: /320_FP/pages/display_lib/