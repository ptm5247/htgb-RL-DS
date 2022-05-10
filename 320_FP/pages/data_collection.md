---
layout: page
title: Data Collection
description: >
  Step 2 of the pipeline is data collection. Where is the data you will be working with?
hide_description: true
sitemap: false
---

Now that you have a goal in mind, you need to identify a data source. Find a source that includes
all of the specific attributes you would like to study, or ensure you have a plan to compute those
attributes with pre-processing steps.

## Rocket League Replay Files

Rocket League allows players to save a replay of any of their matches, which they can later view
from a variety of angles, including through a free-flying, player-controlled camera or from the
perspective of any player in the match. A player can save a replay by pressing a certain key or
button during the match (which will create a *keyframe*, or a marker in the replay file that the
player can easily skip to when viewing) or by selecting the "Save Replay" option at the end of the
match. When a player does this, the game saves a binary file containing all of the data it needs to
visually recreate the match at a later date, including the map on which the match was played, the
car type, cosmetic items, and camera settings used by each player, and a copy of the network data
(which includes updates to the positions and velocities of the cars and the ball, certain game
events, and more). By parsing these files, I will be able to extract the metrics I will be using
for this project.

## The Ballchasing Replay Repository

[ballchasing.com][DC00] is an online repository where players can upload their replay files to
share with others and view positional statistics extracted from them. By default, the uploaded
replays and their associated statistics are publicly available and able to be downloaded manually
or through the ballchasing API. When a player uploads a replay file, it is processed by the
ballchasing servers and a summary of positional statistics are compiled and made available along
with the replay file itself. It is these auto-generated statistics that were used by Smithies et
al., as discussed in the [motivation][DC01] section. For this project, I will be downloading both
the auto-generated statistics as well as the replay files themselves in order to extract additional
statistics.

In case you are curious, *ballchasing* is what players call it when someone just blindly goes after
the ball with no regard for the positioning of their teammates, the likelihood that they get
beaten to the ball by the opponent, or proper rotations. Nobody likes a ballchasing teammate!
{:.note}

## The carball Python Library by Saltie

[Saltie][CB00] is a team of developers behind multiple Rocket League themed projects, one of which
is [calculated.gg][CB01]. In this project, they have developed an app that Rocket League players
can download and use to analyze their replays and create custom training packs that focus on
recreating shots from their actual matches. [carball][CB02] is a python library upon which this
project is built, and has the ability to parse raw replay files, provide similar (and additional)
statistics to those available from ballchasing.com, and create a json object that summarizes the
events in a match. Creating these analyses would likely fall under the category of the next step in
the pipeline (Pre-Processing), but creating them is time consuming and worth doing while
downloading the replay files since we will have some downtime due to the ballchasing API's rate
limits.

## Downloading the Data from the Ballchasing API

Here we will walk through the contents of `data_collection.py`, which is available to be downloaded
from the project's [main directory][DD00].

### Imports

```python
# file: "data_collection.py"
import requests, carball
import sys, json, gzip
from time import time, sleep
from os import environ as env
from os.path import exists
from dotenv import load_dotenv

load_dotenv()
```

The reason for most of these imports will become clear as they are used, but to clarify a few of
them: `carball` is described above, and will be used for some pre-processing as we download the
data. `dotenv` is a library that allows you to create environment variables using a `.env` file
in the current directory. I have a personal API key that I will be using as authentication for the
ballchasing API, but I obviously don't want to upload it to a public repository! To import the key,
I created a file called `.env` with one line: `BALLCHASING_AUTH=xxx`, where "xxx" is my API key.
The method `load_dotenv` will locate this file and create an environment variable containing the
key. Don't forget to add `.env` to your `.gitignore` file so it stays safe on your computer!

### Hushing `stderr`

```python
# file: "data_collection.py"
# hush stderr, since carball is loud
if len(sys.argv) == 2 and sys.argv[1].lower() == '-h':
  class Hush:
    def __init__(self, stream):
      self.stream = stream
    def write(self, _): pass
    def flush(self): pass
  sys.stderr = Hush(sys.stderr)
```

Analyzing replays with carball can get kind of noisy, since it prints every warning and error it
comes across to `stderr`. I will be printing a progress update each time I am done with a new
replay file, and if I leave the program running for a while, I don't want to have to dig through
tons of carball output to see the progress. Luckily, all of my output comes through `stdout` and
all of the carball output comes through `stderr`, so I created a simple fake stream class that I
can use to discard `stderr` and clear up my terminal. Now, when I run this program with the `-h`
option, I will only get my progress updates.

### Setting up Variables

```python
# file: "data_collection.py"
base_url = 'https://ballchasing.com/api/'
headers = { 'Authorization': env.get('BALLCHASING_AUTH') }
ranks = [
  ('Bronze', 'bronze-2'),
  ('Silver', 'silver-2'),
  ('Gold', 'gold-2'),
  ('Plat', 'platinum-2'),
  ('Diamond', 'diamond-2'),
  ('Champ', 'champion-2'),
  ('GC', 'grand-champion-2'),
  ('SSL', 'supersonic-legend')
]
dates = ['2022-03-10T23:59:59Z'] * 8
```

Here, I set up some variables I will need. The ballchasing API requests all require your API key as
a request header, so I create one using my key, which I imported from the environment. Next comes a
list of the 8 ranks, with both the colloquial name (which will be used as folder names), and the
name in the format that the API is expecting. The '2' is specifying the sub rank (recall that each
rank excluding SSL is divided into three sub ranks). I am only taking replays from the middle of
each rank in an effort to provide some separation between each category, eliminating some of the
overlapping which would make the analysis less effective. I don't want a Champ 1 on a temporary
losing streak contributing data as a Diamond 3. Finally, the dates list will be used so I can cycle
through each rank repeatedly, slowly searching for older and older replays. I will be using replays
from Season 5, so the date there is a date at the end of Season 5.

### Pinging the API

```python
# file: "data_collection.py"
# verify connection
ping = requests.get(
  url=base_url,
  headers=headers
)
assert ping.status_code == 200, ping.json().get('error')
```

This is just a quick ping to the API to make sure my token is valid and the API is up and running.

### The Main Loop

```python
# file: "data_collection.py"
while True:
  # make a copy of the earliest dates of replays downloaded
  dates_copy = dates.copy()

  for i, (rank_name, rank) in enumerate(ranks):
    # retrieve a filtered selection of replays
    replays = requests.get(
      url=base_url + 'replays',
      headers=headers,
      params={
        'playlist': 'ranked-doubles',
        'season': 'f5',
        'min-rank': rank,
        'max-rank': rank,
        'count': 200,
        'sort-by': 'replay-date', # newest to oldest by default
        'replay-date-before': dates[i]
      }
    )

    for r in replays.json().get('list'):
      # locate the files where this replay's data will be stored
      id = r.get('id')
      s_path, r_path, d_path, a_path = [
        f'./data/{dir}/{rank_name}/{id}'
      for dir in ('summaries', 'replays', 'dataframes', 'analyses')]
      dates[i] = r.get('date')

      # skip replays that have already been downloaded
      if not exists(d_path):
        t = time()
        try:
          # retrieve and save the auto-generated statistics
          summary = requests.get(
            url=f'{base_url}replays/{id}',
            headers=headers,
          )
          with open(s_path, 'w+') as f:
            json.dump(summary.json(), f)

          # retrieve and save the actual replay file
          while True:
            replay = requests.get(
              url=f'{base_url}replays/{id}/file',
              headers=headers,
            )
            if replay.status_code == 429:
              print('Rate Limit Reached! zzzzz...')
              sleep(36)
            else: break
          with open(r_path, 'wb') as f:
            f.write(replay.content)

          # create and save the carball analysis and data table
          analysis = carball.analyze_replay_file(r_path)
          # use gzip here to reduce file size
          with gzip.open(d_path, 'wb') as f:
            analysis.write_pandas_out_to_file(f)
          with open(a_path, 'w+') as f:
            json.dump(analysis.get_json_data(), f)

          # success message and time taken for this replay
          print('[%.1f] Successfully downloaded %s replay %s from %s'
            % (time() - t, rank_name, id, dates[i]))
        
        # if carball failed to parse or analyze a replay, skip it
        except:
          print('[%.1f] Error with %s replay %s'
            % (time() - t, rank_name, id))
  
  # break out of the loop if all eligible replays have been downloaded
  if dates == dates_copy:
    break
```

Now comes the loop in which I download all of the data. The comments provide a description of each
step, but there are a couple things worth noting:
- The use of the `dates` list: As ranks get lower, there are less replays available on the website.
People who have barely played the game or are not super dedicated to improving are less likely to
go out of their way to upload their replays to an online repository. Before running the program I
do not know how many total replays will be available for each rank, so instead of setting a target
number I just attempt to download 200 at a time, starting from the end of the Season and moving
in time. However, 200 replays will get me much further back in time in Bronze 2 than in SSL. So, I
use `dates` to keep track of where I left off in each rank after each set of 200. If I end up
exhausting the supply of replays for a certain rank (which ended up happening for Bronze 2, Silver
2, and Gold 2), the value in `dates` corresponding to that rank will ensure that subsequent API
calls return an empty list instead of any duplicate replays. The final if statement in the program
will therefore terminate the program `if` the replay supply for every rank is exhausted (this did
not happen).
- Skipping replays that have already been downloaded: If I had only run this program once and
downloaded everything in one go, this would not be necessary. However, due to the rate limit of the
API and the expensive analyses, collecting almost 7000 replays took dozens of hours. Artificially
terminating the program and restarting at a later time will start again from the end of the Season,
so before downloading any replays and wasting part of my allotted bandwidth, I check to see if the
replay has already been downloaded and analyzed.
- The rate limit check: Why did I only check to see if I hit the rate limit (status code = 429)
once? Downloading the actual replay file itself requires the most bandwidth, and therefore has the
smallest rate limit, at 200 files per hour. Therefore, I am guaranteed to hit this rate limit
first, so I only need to check when I am making that specific request. Theoretically, if I had
enough replays already saved on my computer I could hit the limit for the first request in the
outer `while` loop too, but I was not downloading anywhere near enough data for this to occur.

[DC00]: https://ballchasing.com/
[DC01]: ../motivation/#previous-work

[CB00]: https://github.com/SaltieRL
[CB01]: https://www.calculated.gg/
[CB02]: /about/#the-carball-python-library-by-saltie

[DD00]: /320_FP/