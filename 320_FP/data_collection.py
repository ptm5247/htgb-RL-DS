import requests, carball
import sys, json, gzip
from time import time, sleep
from os import environ as env
from os.path import exists
from dotenv import load_dotenv

load_dotenv()

# hush stderr, since carball is loud
if len(sys.argv) == 2 and sys.argv[1].lower() == '-h':
  class Hush:
    def __init__(self, stream):
      self.stream = stream
    def write(self, _): pass
    def flush(self): pass
  sys.stderr = Hush(sys.stderr)

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