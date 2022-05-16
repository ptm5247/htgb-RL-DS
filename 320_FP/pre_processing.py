import os
import pandas as pd
import json as json_lib

from display_lib import ranks

def iter_stats():
  '''A generator function which yields a `pd.Series` for each player in each summary in the
  subfolders of `summaries`.
  
  ## Yields:
  ((rank, guid, color), series)
    where rank is the rank of the match,
    guid is the unique id of the match,
    color is the team color of the yielded `Series`, and
    series is a `Series` containing all of the ballchasing statistics.
  '''
  for folder, _, files in [f for f in os.walk('summaries')][1:]:
    rank = folder.split('\\')[-1]

    for file in files:
      try:
        # read the match summary and find the guid
        with open(f'{folder}\\{file}') as f:
          json = json_lib.load(f)
        guid = json['match_guid']
        metadata = (json['title'], json['duration'])
  
        # for each team, yield a series containing all the stats
        for color in ['blue', 'orange']:
          series = pd.concat((
            pd.Series(metadata, index=('title', 'duration')), *[
              pd.Series(v, dtype=float)
            for v in json[color]['players'][0]['stats'].values()]
          ))
  
          # yield with tuple as key (for pd.MultiIndex)
          yield (rank, guid, color), series
      
      # skip the file if there is an error
      except Exception as e:
        print(f'Error with {folder}\\{file}: {e}')

def prepare_metrics(data: pd.DataFrame):
  # calculate new metrics to replace some of the existing ones
  data.loc['amount_collected'] = data.loc['count_collected_big'] * 100 + data.loc['count_collected_small'] * 12
  data.loc['amount_stolen'] = data.loc['count_stolen_big'] * 100 + data.loc['count_stolen_small'] * 12

  # drop irrelevant or redundant metrics
  data.drop(labels=[
    'shots_against',                      # reciprocal of shots
    'goals_against',                      # reciprocal of goals
    'assists',                            # no assists in 1v1
    'mvp',                                # no mvp in 1v1
    'shooting_percentage',                # -> shots and goals
    'bcpm',                               # boost metrics will be normalized by duration
    'amount_collected_big',               # -> amount_collected
    'amount_collected_small',             # -> amount_collected
    'amount_stolen_big',                  # -> amount_stolen
    'amount_stolen_small',                # -> amount_stolen
    'count_collected_big',                # -> amount_collected
    'count_stolen_big',                   # -> amount_stolen
    'count_collected_small',              # -> amount_collected
    'count_stolen_small',                 # -> amount_stolen
    'amount_overfill',                    # represented in wasted metrics
    'amount_overfill_stolen',             # represented in wasted_stolen metrics
    'time_zero_boost',                    # percentage equivalent exists
    'time_full_boost',                    # percentage equivalent exists
    'time_boost_0_25',                    # not useful
    'time_boost_25_50',                   # not useful
    'time_boost_50_75',                   # not useful
    'time_boost_75_100',                  # not useful
    'percent_boost_0_25',                 # not useful
    'percent_boost_25_50',                # not useful
    'percent_boost_50_75',                # not useful
    'percent_boost_75_100',               # not useful
    'avg_speed',                          # percentage equivalent exists
    'total_distance',                     # -> avg_speed_percentage and duration
    'time_supersonic_speed',              # percentage equivalent exists
    'time_boost_speed',                   # percentage equivalent exists
    'time_slow_speed',                    # percentage equivalent exists
    'time_ground',                        # percentage equivalent exists
    'time_low_air',                       # percentage equivalent exists
    'time_high_air',                      # percentage equivalent exists
    'time_powerslide',                    # -> count_powerslide and avg_powerslide_duration
    'percent_boost_speed',                # -> percent_slow_speed and percent_supersonic_speed
    'percent_ground',                     # -> percent_low_air and percent_high_air,
    'time_defensive_third',               # percentage equivalent exists
    'time_neutral_third',                 # percentage equivalent exists
    'time_offensive_third',               # percentage equivalent exists
    'time_defensive_half',                # percentage equivalent exists
    'time_offensive_half',                # percentage equivalent exists
    'time_behind_ball',                   # percentage equivalent exists
    'time_infront_ball',                  # percentage equivalent exists
    'time_most_back',                     # percentage equivalent exists
    'time_most_forward',                  # percentage equivalent exists
    'goals_against_while_last_defender',  # always last defender in 1v1
    'time_closest_to_ball',               # percentage equivalent exists
    'time_farthest_from_ball',            # percentage equivalent exists
    'percent_defensive_half',             # -> thirds
    'percent_offensive_half',             # -> thirds
    'percent_neutral_third',              # -> percent_offensive_third and percent_defensive_third
    'percent_infront_ball',               # -> percent_behind_ball
    'percent_most_back',                  # always most back in 1v1
    'percent_most_forward',               # always most forward in 1v1
    'percent_closest_to_ball',            # always closest to ball in 1v1
    'percent_farthest_from_ball',         # always farthest from ball in 1v1
    'avg_distance_to_ball_possession',    # -> avg_distance_to_ball
    'avg_distance_to_ball_no_possession', # -> avg_distance_to_ball
    'taken',                              # reciprocal of inflicted
  ], inplace=True)

def normalize(data):
  # identify count-like metrics
  clm = [
    # core
    'shots', 'goals', 'saves', 'score',
    # boost
    'amount_collected', 'amount_stolen', 'amount_used_while_supersonic',
    # movement
    'count_powerslide',
    # demo
    'inflicted',
  ]
  # normalize by 5-minute duration
  data[clm] = data[clm].multiply(300 / data['duration'], axis=0)

def aggregate():
  # where to store the pickled data
  pickle_path = 'summaries\\data_frame'

  if os.path.exists(pickle_path):
    # if the data has already been aggregated, just read it from the file
    data = pd.read_pickle(pickle_path)
  else:
    # extract all the desired data into one table
    data = pd.concat(dict(iter_stats()), names=('rank', 'guid', 'team'), axis=1)
    # remove the undesired metrics
    prepare_metrics(data)
    # order by rank
    data = data.T.reindex(ranks, level='rank')
    # convert applicable columns to dtype float
    for col in data.columns:
      if col != 'title':
        data[col] = data[col].astype(float)
    # normalize the count-like metrics
    normalize(data)
    data.to_pickle(pickle_path)
  
  return data