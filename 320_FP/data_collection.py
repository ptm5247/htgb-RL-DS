import requests, json
from time import time, sleep
from os import environ as env
from os.path import exists
from dotenv import load_dotenv

load_dotenv()

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

# verify connection
ping = requests.get(
  url=base_url,
  headers=headers
)
assert ping.status_code == 200, ping.json().get('error')

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