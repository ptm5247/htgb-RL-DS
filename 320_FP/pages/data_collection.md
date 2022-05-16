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
attributes with pre-processing steps. Data can come from many sources, including the following:
- API's: API data is accessible directly from the internet using commands like HTTP GET, and
responses will usually come in predictable formats like JSON or even entire files.
- Dowloadable Files: Some online data sources allow you to manually download easy-to-use files
containing the data, like CSVs or SQL databases.
- Web Scraping: Sometimes, there is no easy way to download the data. If it located in the HTML of
a website, you can GET the page containing the data and parse it using HTML tools or regular
expressions.

There are countless programs and libraries available to help you with any of these formats, so be
sure to see what's available before writing code to parse/manage data yourself.

For this project, the data I am using is available via an API. Before going through how I got it,
let's make sure we understand what it is and how it was generated.

## Rocket League Replay Files

Rocket League allows players to save a replay of any of their matches, which they can later view
from a variety of angles, including through a free-flying, player-controlled camera or from the
perspective of any player in the match. A player can save a replay by pressing a certain key or
button during the match (which will create a *keyframe*, or a marker in the replay file that the
player can easily skip to when viewing) or by selecting the "Save Replay" option at the end of the
match. When a player does this, the game saves a binary file containing all of the data it needs to
visually recreate the match at a later date. This includes the map on which the match was played,
the car type, cosmetic items, and camera settings used by each player, and a copy of the network
data which was sent during the match (which includes updates to the positions and velocities of the
cars and the ball, certain game events, and more).

## The Ballchasing Replay Repository

[ballchasing.com][00] is an online repository where players can upload their replay files to share
with others and view statistics extracted from them. Currently, over 50 million total replays have
been uploaded to the site by players of all ranks. By default, the uploaded replays and their
associated statistics are publicly available and able to be downloaded manually or through the
ballchasing API. When a player uploads a replay file, it is processed by the ballchasing servers
and a summary of positional statistics are compiled and made available along with the replay file
itself. It is these auto-generated statistics that I will be analyzing for this project.

Anyone can browse public replays and statistics on the ballchasing website. However, if you would
like to upload your own replays or use their API, you will need a [Steam][01] account. Their API is
[well documented][02], and allows you to browse, upload, or download replay files and statistics
programatically. In order to use it, you will also need to [generate an API key][03].

In case you're curious, *ballchasing* is what players call it when someone just blindly goes after
the ball with no regard for the positioning of their teammates, the likelihood that they get
beaten to the ball by the opponent, or proper rotations. Nobody likes a ballchasing teammate!
{:.note}

## Downloading the Data from the Ballchasing API

Now, we will walk through the contents of `data_collection.py`. Check out the project's
[main directory][04] to download any or all of the code referenced in this project.

### Imports

```python
# file: "data_collection.py"
import requests, json
from time import time, sleep
from os import environ as env
from os.path import exists
from dotenv import load_dotenv

load_dotenv()
```

The reason for these imports will become clear or be explained as they are used. `dotenv` is a
library that allows you to create environment variables using local files on your computer. I have
a private API key that I will be using as authentication for the ballchasing API, and I obviously
don't want to upload it to a public repository! To import the key, I created a file called `.env`
with one line: `BALLCHASING_AUTH=xxx`, where "xxx" is my API key. The method `load_dotenv` locates
this file and creates an environment variable containing the key. Don't forget to add `.env` to
your `.gitignore` file so it stays safe on your computer!

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

Here, I set up some variables I will need. All ballchasing API requests require your API key as a
request header, so I create one using my key, which was stored in the environment in the last step.
Next comes a list of the 8 ranks, with both the colloquial name (which will be used as folder
names), and the name in the format that the API is expecting. The '2' is specifying the sub rank
(recall that each rank excluding SSL is divided into three sub ranks). I am only taking replays
from the middle of each rank in an effort to provide some separation between each category,
eliminating some of the overlapping which would make the analysis less effective. I don't want a
Champ 1 on a temporary losing streak contributing data as a Diamond 3. Finally, the `dates` list
will be used to track my progress for each rank as I download replay statistics. The API will let
me make requests in batches of 200, and I will be sorting by date. However, 200 replays will span a
different amount of time in each rank, so I need to keep track of where I left off in each one. I'm
examining replays from Season 5, so I initialized the list with a date at the end of that season.

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
  # make a copy of the earliest replays downloaded
  dates_copy = dates.copy()

  for i, (rank_name, rank) in enumerate(ranks):
    # retrieve a filtered selection of replays
    replays = requests.get(
      url=base_url + 'replays',
      headers=headers,
      params={
        'playlist': 'ranked-duels',
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
      s_path = f'./summaries/{rank_name}/{id}'
      dates[i] = r.get('date')

      # skip replays that have already been downloaded
      if not exists(s_path):
        t = time()
        # retrieve and save the auto-generated statistics
        summary = requests.get(
          url=f'{base_url}replays/{id}',
          headers=headers,
        )
        with open(s_path, 'w+') as f:
          json.dump(summary.json(), f)

        # success message and time taken for this replay
        dt = time() - t
        print('[%.1f] Downloaded summary for %s replay %s from %s'
          % (dt, rank_name, id, dates[i]))
        if dt < 3.6:
          sleep(3.6 - dt)
  
  # break out of the loop if all eligible replays have been downloaded
  if dates == dates_copy:
    break
```

Now comes the loop in which I download all of the data. The comments provide a description of each
step, but there are a couple things worth noting:
- Skipping replays that have already been downloaded: If I had only run this program once and
downloaded everything in one go, this would not be necessary. However, due to API rate limits,
collecting statistics on thousands of replays took about 20 hours. Artificially terminating the
program and restarting at a later time will start again from the end of the Season, so before
using part of my allotted bandwidth, I check to see if I have already seen the replay.
- `time.sleep`: As mentioned above, this API has a rate limit. For requesting replay statistics, it
is 1000 requests per hour. In order to avoid ever hitting the rate limit, I wait until 1/1000th of
an hour has passed before moving onto the next replay.

I terminated this program after a total of about 20,000 replays were downloaded, as I felt like
that was a large enough sample size to perform my analysis. At this point, there is a sub-folder in
the `summaries` folder for each rank containing the statistics for thousands of matches, each
stored in a JSON file. Now, we are ready to move onto the next step: Pre-Processing.

Continue with [Pre-Processing](pre_processing.md){:.heading.flip-title}
{:.read-more}

[00]: https://ballchasing.com/
[01]: https://store.steampowered.com/
[02]: https://ballchasing.com/doc/api
[03]: https://ballchasing.com/upload

[04]: /320_FP/