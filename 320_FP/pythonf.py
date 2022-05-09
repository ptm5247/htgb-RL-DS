import os
import carball
import json
import sys

walk = [s for s in os.walk('data/dataframes')]

class Hush:
  def __init__(self, stream):
    self.stream = stream
  def write(self, _): pass
  def flush(self): pass
sys.stderr = Hush(sys.stderr)

total = sum(len(l[2]) for l in walk[1:])
curr = 0

for i in range(8):
  fold = walk[0][1][i]
  
  for file in walk[i + 1][2]:
    a_path = f'./data/analyses/{fold}/{file}'
    r_path = f'./data/replays/{fold}/{file}'

    if not os.path.exists(a_path):
      analysis = carball.analyze_replay_file(r_path)
      with open(a_path, 'w+') as f:
        json.dump(analysis.get_json_data(), f)
    curr += 1
    print(f'Re-analyzed {curr} of {total}')