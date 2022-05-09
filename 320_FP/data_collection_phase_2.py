from rlutilities.simulation import Game
from rlutilities.linear_algebra import dot, vec3

from carball_pandas_read import *

import pandas as pd
import gzip

Game.set_mode('soccar')
ball = Game().ball

with gzip.open('./data/dataframes/SSL/00dce8e0-98ba-4ac2-b566-74d8032f8a3e', 'rb') as f:
  df = read_numpy_from_memory(f)

balldf = df[['ball', 'game']].dropna(subset=[('ball', 'vel_x')])
balldf[('ball', 'touch')] = 0.

print(balldf['ball'].head())

for i, row in balldf.iterrows():
  ball.step(row.game.delta)
  #for _ in range(int(row.game.delta * 120)):
  #  ball.step(1 / 120)
  #ball.step(row.game.delta % (1 / 120))

  x = vec3(row.ball.pos_x, row.ball.pos_y, row.ball.pos_z)
  v = vec3(row.ball.vel_x, row.ball.vel_y, row.ball.vel_z) * 1
  w = vec3(row.ball.ang_vel_x, row.ball.ang_vel_y, row.ball.ang_vel_z)

  print(i, ball.position, x, v)
  #row.ball.touch = dot(dx, dx) + dot(dv, dv) + dot(dw, dw)

  dx = ball.position - x
  dv = ball.velocity - v
  dw = ball.angular_velocity - w

  ball.position = x
  ball.velocity = v
  ball.angular_velocity = w

for i in balldf[('ball', 'touch')]:
  if i != 0.0:
    print(i, end=' | ')

#for _ in range(100):
#  game.ball.step(1 / 120)
#  #print(dot(x, game.ball.position) + dot(v, game.ball.velocity) + dot(w, game.ball.angular_velocity))
