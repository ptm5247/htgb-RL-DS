---
layout: page
title: Results
description: >
  Step 7 of the pipeline is interpreting your results. What did you learn?
hide_description: true
sitemap: false
---

As it turns out, there are statistically significant correlations involving all of the examined
metrics. However, it would not be useful for me to say
*focus on all of these metrics during your gameplay*, as the goal of this project is to determine
which metrics are the most important to consider. This is where the strengths of the correlations
come in. Some of the correlations were much stronger than others, implying that focusing on
improving these skills would have the most benefit.

## Results Based on Metric vs. Rank

With the cubic models, I found many R squared values that were reasonable high. I will pick 2
out of the metrics most strongly correlated with player rank and discuss their implications.
Since there is a large gap between the R squared values of 0.26 for `amount_collected` and 0.13 for
`avg_powerslide_duration`, I will consider metrics which lie above that line.

### Supersonic Speed

`percent_supersonic_speed` had the highest correlation strength by a good margin. Let's look back
at the original graph and see what this implies:

![res_01](/assets/img/results/res_01.png)

So, higher ranked players defnitely spend significantly more time at supersonic speed. The
similarly-shaped graphs for `bpm` (boost per minute) and `amount_collected` give some insight to
how they do this, but what are they doing specifically? Staying at supersonic speed is all about
maintaining momentum, as there is only so much boost you are able to collect while still staying
properly positioned during a play. Two things that kill momentum are hitting the brakes and making
sharp turns. So, when you need to turn around, make a wider turn if possible, so you can keep your
momentum up while conserving boost. If you find yourself hitting the brakes a lot, look over some
of your replays and pay close attention to the scenarios where you ended up needing to brake. Was
there a different path you could have taken, or a different angle from which you could have
approached the play that would have allowed you to maintain more of your momentum?

Many of the other high-correlation metrics are related to speed and boost. In addition to `bpm` and
`amount_collected`, `avg_speed_percentage` (percentage of max speed) and `percent_slow_speed` are
also directly linked to your ability to maintain momentum. If there is one thing that all of these
correlations show it is that momentum is a key part of 1v1s. This makes sense, because if the ball
is overturned to your opponent and you are unable to immediately block them, the only way to
prevent conceding a goal is by getting back to your net quickly, since you have no teammates. Your
ability to do so will depend on your ability to keep up your momentum.

### Low Aerials

The only metric above the R squared = 0.25 line that is not directly related to boost and momentum
is `percent_low_air`. This measures time spent in the air, but not too close to the ceiling. Let's
look at the graph one more time:

![res_02](/assets/img/results/res_02.png)

So, it seems that spending more time in the air is a trait of higher level play. Why could this be?
In 1v1s you only have 1 opponent, and if the ball gets popped up in the air, whichever player can
get to it first will have the advantage. Being more comfortable getting up into the air with speed
and precision will allow you to challenge more often, and take more control of the ball. At higher
ranks when you have posession of the ball, being able to take it into the air will give you a large
advantage, since it will make things much more difficult for your opponent. This correlation
suggests that aerial control and the ability to challenge in the air is a key aspect of 1v1 play,
and would be a good thing to focus on in training.

## Results Based on Goal Difference vs. Metric

There was one correlation here that blew every other metric out of the water, and that was
`percent_behind_ball`. Here is the graph for that again:

![res_03](/assets/img/results/res_03.png)

Considering the spread of the other graphs, this is a remarkable correlation. It makes sense why it
exists too, since you need to be behind the ball in order to defend your net. Players in 1v1s
usually do not intend to be in front of the ball, and when it happens by accident it is usually
because they overcommit, or went for a play they should not have and were beaten to the ball by the
opponent. Overcommitting in 1v1s is deadly, because if the opponent has decent control of the ball
it will likely end in you getting scored on. So, if you are analyzing some of your past games, look
for all the times you overcommit and see why it happened. Did you fail to realize that your
opponent was closer to the ball? Did you approach the play from an angle that allowed the ball to
easily come out in your opponent's favor? Figure out what kinds of mistakes you make the most that
lead to overcommits and allow that to inform your decision-making during future matches.

## Conclusion

Congratulations! You have made it through the Rocket League Data Science pipeline. Now you are
prepared to effectively analyze your own data and communicate your results. More importantly, you
now have data-driven insight on how to improve your Rocket League performance!