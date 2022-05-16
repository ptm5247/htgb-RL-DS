---
layout: page
title: Bias & Missing Data
description: >
  Step 4 of the pipeline is addressing bias and missing data. What is your data hiding from you?
hide_description: true
sitemap: false
---

Just because you have your entire dataset does not mean you have the whole picture of what the data
is aiming to represent. This can be for two main reasons:
- Missing Data: There are holes in your dataset, or incomplete observations. There are multiple
kinds of missing data, and each kind has different implications of your analysis and has different
ways of combatting their adverse effects.
- Bias: There is a flaw in the dataset itself, or the way it was collected. The world is very
complicated, and it is impossible to take into account everything that could possibly have an
effect on your data. If you are collecting data with a specific goal in mind, you need to make a
concerted effort to collect enough data to fairly and accurately represent your target of study. If
it is not possible to do so (which it likely will not be unless you have total control over the
scenario or object(s) you are studying), take note of the bias that may be present in your data and
the implications it may have on your results.

## Missing Data

There are 3 basic types of missing data: Missing Completely at Random (MCAR), Missing at Random
(MAR), and Missing Not at Random (MNAR).

MAR data is the most common type of missing data, and it data which is absent but able to be
imputed (or inferred) from neighboring data which is present in the dataset. For example, if you
are tracking your weight and you forget to record it one day, you can probably make a pretty
accurate guess about what it was based on your weight the days before and after. Ignoring this
kind of data may bias your dataset and it is a good idea to try to impute the missing values.

MNAR data is the most difficult to deal with. Data in this category is missing for a reason, and
that reason is not present elsewhere in the dataset. This may make it impossible to impute, since
the missing values may or may not be related to neighboring values. For example, if you are
collecting data from a person and they are embarrassed or scared to tell you something, you can't
really guess at what the data should be since you don't know exactly why they didn't tell you.
Ignoring this kind of data likely to bias your data, and if possible you should find a way to fill
in the blanks, though the method of doing so will likely depend on the situation.

MCAR data is just that: data which is missing for a reason which has nothing to do with what you
are studying. If you are collecting a random sample in a notebook and somehow end up losing a page,
this is likely MCAR. The data that you lost was essentially another random sample of your data. As
long as the missing data is not a significant portion of your dataset, ignoring it is not unlikely
to have a statistically significant effect on your results. It would just be as if you had
collected less data to begin with.

If you would like to look more into the concept of missing data and the methods of dealing with it,
here are a few starting places:
- The [`pandas` documentation][00] contains a discussion of missing data and how to deal with it
when using the library.
- This [very detailed analysis][01] of handling missing data in regression models using the
National Survey on Drug Use and Health.

For this project, I exlpored missing data in [bias_and_missing.ipynb][03]. We will take a look at
the first part of this notebook now.

### Imports

```python
# file: "bias_and_missing.ipynb"
from pre_processing import aggregate
from display_lib import html_table, ranks
import os
import pandas as pd
```

`aggregate` is the function I defined in the [last section][04] on pre-processing. The remainder of
the imports will be used in the next section of this page, which is about bias.

### Aggregating the Data and Searching for Missing Values

```python
# file: "bias_and_missing.ipynb"
# aggregate the data under the chosen metrics
data = aggregate()

# count the number of explicitly missing values
print(f'Missing Values: {data.isna().sum().sum()}')
```
Output:
```
Error with summaries\Bronze\83e60134-c175-422f-a48d-5659ce2de70a: 'duration'
Error with summaries\GC\439c9822-992c-4d97-bc9b-d5539a02c878: 'match_guid'
Error with summaries\GC\64b54590-ba50-4c20-9157-5521a05a7819: 'match_guid'
Error with summaries\GC\7b4e0791-4115-4dca-a361-eb62c7bc5c39: 'match_guid'
Error with summaries\GC\cd6ec699-9867-428a-93f0-376a5919bf0b: 'match_guid'
Missing Values: 0
```

There seems to be issues with 5 files being reported by the `iter_stats` function in
[`pre_processing.py`][03]. For the first file, it was unable to find a match duration in the
summary. After manually checking that file, I discovered that the match did not in fact occur. If a
player loses connection with the server while a competitive match is in the process of starting,
the match will be cancelled. However, when this happens it is still possible to save a replay. Why
would someone do this? The answer is probably *they didn't*. There is a popular mod for the game
called [bakkesmod][05], which among many other things offers players the option to automatically
save and upload a replay for every single match that they play. This is the source for many of the
ballchasing replays, as it would be quite tedious to manually save and upload each one. However, it
can sometimes result in a replay being uploaded for a match that never took place, which is likely
what happened here. Therefore this is not missing data, just a match that didn't happen. The other
4 errors report an inability to even find a match GUID at all. I checked these 4 files and all of
them contain error responses from the API claiming that the match could not be found. Since I only
got match ID's to request from the API itself, I'm not sure how this happened, but this classifies
as MCAR. Whatever the error was that caused me to request 4 unfindable matches almost certainly had
nothing to do with the positional tendencies of the players during the match itself, so it is safe
to simply ignore these errors. Finally, there are no `NaN` values in my data table. This means that
for all of the metrics I am analyzing, a value was returned for every single match. One less thing
to worry about!

## Bias

There are 2 specific steps that I took to eliminate potential sources of bias. The first was
discussed during [pre-processing][04], which was using match GUID's to detect when multiple players
uploaded the same replay and only count one of them. The second will be to remove data from any
matches shorter than 150 seconds, or half the length of a standard match. There are a couple
reasons behind this. If there were severe issues with the server or one of the players' internet,
one or more players would likely lose connection towards the beginning of the match and terminate
the game early. The shortest match I had data for was only 4 seconds, so this is likely what
happened for matches that short. A more common cause for short matches is a player forfeitting. If
a player forfeits at the end of the match, it is likely because they have been genuinely trying up
until that point but have decided that they are far enough behind for it to be impossible to come
back. This is not uncommon, especially in 1v1s but these are totally legitimate matches and data
from them shouldbe included. If a player forfeits in the beginning of a match, it is an indicator
that there may be other factors at play. If they are experiencing connection issues that make the
game unplayable, if the opponent is being unnecessarily toxic or not taking the match seriously, or
if there is a significant skill gap between players, one player may decide to forfeit early. These
kinds of matches are uncommon and generally unrepresentative of normal gameplay, so in order to
minimize the adverse effects they may have on the dataset, they were removed. This was also done in
[bias_and_missing.ipynb][03]; let's take a look at that now.

### Detecting Bias

```python
# file: "bias_and_missing.ipynb"
# find the number of downloaded summaries for each rank
tot = dict((r.split('\\')[-1], len(f)) for r, _, f in os.walk('summaries'))
dup, dur, rem = {}, {}, {}

for rank, df in data['duration'][::2].groupby('rank'):
  # determine the number of duplicated matches
  dup[rank] = tot[rank] - len(df)
  # determine the number of matches less than half the length of a full match
  dur[rank] = (df < 150).sum()
  rem[rank] = len(df) - dur[rank]

# drop matches which were less than half the length of a full match
data['duration'].where(data['duration'] > 150, pd.NA, inplace=True)
data.dropna(inplace=True)

# display a table with the calculated values
html_table(ranks, [
  ('Total Matches', tot),
  ('Duplicates', dup),
  ('Short Matches', dur),
  ('Remaining Matches', rem)
])
```
Output:
<table style="margin-left:auto;margin-right:auto;"><tr><td></td><td style="text-align:center"><b>Bronze</b></td><td style="text-align:center"><b>Silver</b></td><td style="text-align:center"><b>Gold</b></td><td style="text-align:center"><b>Plat</b></td><td style="text-align:center"><b>Diamond</b></td><td style="text-align:center"><b>Champ</b></td><td style="text-align:center"><b>GC</b></td><td style="text-align:center"><b>SSL</b></td></tr><tr><td style="text-align:center"><b>Total Matches</b></td><td style="text-align:center">180</td><td style="text-align:center">933</td><td style="text-align:center">2877</td><td style="text-align:center">3184</td><td style="text-align:center">3185</td><td style="text-align:center">3185</td><td style="text-align:center">3185</td><td style="text-align:center">3183</td></tr><tr><td style="text-align:center"><b>Duplicates</b></td><td style="text-align:center">7</td><td style="text-align:center">0</td><td style="text-align:center">0</td><td style="text-align:center">9</td><td style="text-align:center">35</td><td style="text-align:center">82</td><td style="text-align:center">130</td><td style="text-align:center">174</td></tr><tr><td style="text-align:center"><b>Short Matches</b></td><td style="text-align:center">106</td><td style="text-align:center">215</td><td style="text-align:center">470</td><td style="text-align:center">361</td><td style="text-align:center">268</td><td style="text-align:center">204</td><td style="text-align:center">145</td><td style="text-align:center">154</td></tr><tr><td style="text-align:center"><b>Remaining Matches</b></td><td style="text-align:center">67</td><td style="text-align:center">718</td><td style="text-align:center">2407</td><td style="text-align:center">2814</td><td style="text-align:center">2882</td><td style="text-align:center">2899</td><td style="text-align:center">2910</td><td style="text-align:center">2855</td></tr></table>

First, I find the number of replay summaries I started with by counting the actual files. In order
to calculate how many were removed due to GUID duplicates, I count how many games are in the
dataset at this point and subtract that from the total number of files. It should be noted that the
1 Bronze and 3 GC replays whose files caused errors are included in this count. I then count how
many of the matches are under 150 seconds before removing them. In order to remove them, I use
`DataFrame.where` to replace all values of `duration` less than 150 with `NaN`. Then, I can use
`DataFrame.dropna` to get rid of all rows with `NaN` in them, since I already verified that `NaN`
was not present in the table before. Finally, I display all of these counts, separated by rank, in
an HTML table using a method in [`display_lib.py`][03]. To see how this method works, check out the
[display_lib][06] page.

### Updating the Data File

```python
# file: "bias_and_missing.ipynb"
# save the updated data table
data.to_pickle('summaries\\data_frame')
```

Since I made changes to the data in this file, I use `pickle` to save them back to the file.

## Other Potential Sources of Bias

There are a few things about this dataset which are completely out of my control, but are still
worth noting so that I and anyone I share my results with are aware of the potential limitations of
my analysis:

Rocket League replay files are generated client-side. That means if a player is experiencing
connection issues and does not receive all of the packets containing information about other
players, that is reflected in the replay file. I do not believe this would have a signigicant
effect on this analysis, as minor packet loss would have a minimal effect on the types of
statistics compiled by ballchasing.com, and major packet loss would likely cause a player to
disconnect or forfeit.

Only players playing on PC are able to upload replays. Other platforms (Xbox, PlayStation, and
the Nintendo Switch) still allow players to save replays, but do not make the files accessible to
the user. Bakkesmod, the mod which many players use to automatically upload replays, is also not
available on those platforms. However, the game is cross-platform, and I do not have any reason to
believe that people who play on certain platforms would be predisposed to different playstyles.

This is only a sample of replays from players who have gone out of their way to upload their
replays to a third-party online repository. A large portion of players, especially those who are
not particularly dedicated to improving at the game, would likely not do this, and probably do not
even know that they are able to. However, there are still replays from players of all ranks, albeit
significantly less for Bronze and Silver. Additionally, nearly every replay contains data from the
opponent as well as the uploader, so people who do not know about this repository or are not
compelled to use it are still sampled from.

The Bronze rank only has 67 remaining replays. I downloaded every single available replay from
Bronze 2 Season 5 1v1s. However, after all of my preprocessing steps only 67 remained, compared to
nearly 3000 from most other categories. Additionally, Bronze makes up the lowest ranked 1.5% of the
playerbase, which is mostly players who are brand new to the game. These factors will make data
from Bronze much more susceptible to noise than other ranks. This is something to keep in mind when
analyzing the shapes of distributions in future steps.

This analysis only considers 1v1 matches. Team plays are a huge part of Rocket League, and they are
completely unrepresented here. As long as the results are only considered in the light of 1v1 play,
this does not necessarily add bias, but it is still something to keep in mind.

Now that I've addressed bias and missing data, it is time to move on to exploratory data analysis.

Continue with [Exploratory Data Analysis](exploratory_data_analysis.md){:.heading.flip-title}
{:.read-more}

[00]: https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
[01]: https://www.samhsa.gov/data/report/methods-handling-missing-item-values-regression-models-using-national-survey-drug-use-and

[03]: /320_FP/

[04]: /320_FP/pages/pre_processing/

[05]: https://bakkesplugins.com/

[06]: /320_FP/pages/display_lib/