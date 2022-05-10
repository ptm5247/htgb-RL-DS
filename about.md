---
layout: about
---

# About

<!--author-->

# Rocket League

## About the Game

Rocket League, at its simplest, can be described as "rocket powered car soccer." It was released
by Psyonix in July of 2015 as the successor of the less eloquently named "Supersonic Acrobatic
Rocket-Powered Battle-Cars," or SARP BC, which was released in 2008 and followed the same premise.
A standard match of Rocket League involves two teams of three cars fully enclosed in a 3D 
rectangular arena attempting to hit a large ball into the opposing team's net. The cars have the
ability to jump, and can collect periodically regenerating "boost" pads on the ground of the arena,
which they can store and use to gain extra speed. Boosting applies a constant, forward-facing force
on the car, so by jumping and angling the car upwards, the player can use boost to fly. The player
has full control of the car's rotation in all three dimensions, allowing for very precise aerial
movement after enough practice.

The game saw huge success, and saw an even bigger surge of popularity after becoming free-to-play
in September of 2020. According to [ActivePlayer][RL00], the game clocks in almost six million
daily players, and over 90 million monthly players in recent months. The game also has an active
professional scene, with multiple big name Esports Organizations like NRG, Cloud9, and G2
sponsoring pro teams.

The game includes both ranked and unranked (casual) play, with various team sizes. A player's
cometitive rank is determined by an ELO-like system, and there are eight tiers, or groupings, of 
ranks in the current version of the game. Each rank (excluding the highest one) has three
sub-tiers, and each sub-tier is divided into four divisions. At the time I am doing this project
(May 2022), the game is in its sixth competitive season since going free-to-play. The distributions
of players' competitive ranks from Season 5 can be seen below (credit to [Esports Tales][RL01])
Note that in this distribution, only the ranks and their sub-tiers are shown. The three bars for
each rank do not correspond to divisions, but the three competitive playlists: 1v1s, 2v2s, and
3v3s).

![RL02]

## Gameplay

Gameplay is usually separated into two different skill sets: gamesense and mechanics.

*Positional* aspects of gameplay include things like awareness of the game (or *gamesense*).
Where are your teammates and oponents, what are they ready for, and what are they preparing to do?
Where is the ball, who can get to it the fastest, and who has the best angle to make a play? How
much boost is available to everyone on the field? If you are in posession of the ball, what is the
most productive thing you can do with it? If your teammate has the ball, where on the field should
you be in order to be helpful to them? These things are difficult to train and usually come with
experience in the game. Players often neglect focusing on these kinds of skills because training
them effectively usually involves retroactively examining your own gameplay and identifying places
where you could have improved, and the things you are consistently doing right or wrong. For the
casual player, this sort of training may not be as enjoyable as just playing the game.

*Mechanical* aspects of gameplay involve how well you can control your car. How quickly can you
turn around, accelerate, or get into the air? How far in advance are you able to predict the path
of the ball? What are the types of complex plays you are able to reliably execute, and how much
control do you have of the ball during posessions? Over the last 7 years, players have discovered
many very complex mechanics that take insane amounts of time to learn and perfect, and the skill of
the players at the highest rank continues to improve every day.

Players of any rank are often driven to improve at the game by the thought of being able to perform
flashy mechanics and score cool goals. Training mechanics is much easier to do for many players,
especialy since the game has a function where the player can enter into a single-player training
session where the ball is repeatedly set up in a specific manner, allowing the player to practice
a certain type of shot. Additionally, there is an entire community of players dedicated to
something called *freestyling,* in which players in casual 1v1 matches will take turns scoring the
most mechanically difficult shots they can, with little to no defending from the other team. This
sometimes leads to a "mechanics over gamesense" mindset for players trying to improve, while in
reality, both are essential to keeping up with higher level gameplay. Part of this project will be
dedicated to seeing which types of tendencies, mechanical or positional, appear to be more
statistically significant to improvement.

# Sources

## Previous Work

In this paper, Smithies et al. analyzed rocket league replay statistics and identified which
positional aspects of players' 1v1 gameplay had the most predictive power in determining player
rank and match outcome. The article was published in September of 2021 and is openly accessible
[here][PW00]. The citation of the paper is also listed below:

Smithies, T.D., Campbell, M.J., Ramsbottom, N. et al. A Random Forest approach to identify metrics
that best predict match outcome and player ranking in the esport Rocket League. Sci Rep 11, 19285
(2021). https://doi.org/10.1038/s41598-021-98879-9

## Hydejack

This website was built using [Hydejack][HJ00], which is an open source Jekyll theme.
Hydejack is distributed under the [GNU General Public License][HJ01].
Parts of the program are provided under [separate licenses][HJ02].

[RL00]: https://activeplayer.io/rocket-league/
[RL01]: https://www.esportstales.com/rocket-league/seasonal-rank-distribution-and-players-percentage-by-tier
[RL02]: https://images.squarespace-cdn.com/content/v1/59af2189c534a58c97bd63b3/bbd07e16-17df-40d7-a9fe-2cbd50f823ea/Rocket+League+rank+distribution+Season+5.jpg

[PW00]: https://doi.org/10.1038/s41598-021-98879-9

[HJ00]: https://hydejack.com/
[HJ01]: licenses/GPL-3.0.md
[HJ02]: NOTICE.md