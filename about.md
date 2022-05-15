---
layout: about
---

# About

<!--author-->

# Rocket League

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

# Sources

## The Ballchasing Replay Repository

[ballchasing.com][BC00] allows players on PC platforms like Steam or Epic Games to upload their
replay files and compile statistics on both individual and groups of replays. Currently, over 50
million total replays have been uploaded to the site by players of all ranks. Public replays and
their associated statistics can be searched through and downloaded manually or via the website's
API (see the [documentation][BC01]). In order to download data from their API, you must first sign
in using a [Steam][BC02] account, then [generate an API key][BC03]. The API is well-documented, so
check it out if you are interested in using it in ways not mentioned in this project.

## Hydejack

This website was built using [Hydejack][HJ00], which is an open source Jekyll theme.
Hydejack is distributed under the [GNU General Public License][HJ01].
Parts of the program are provided under [separate licenses][HJ02].

[RL00]: https://activeplayer.io/rocket-league/
[RL01]: https://www.esportstales.com/rocket-league/seasonal-rank-distribution-and-players-percentage-by-tier
[RL02]: https://images.squarespace-cdn.com/content/v1/59af2189c534a58c97bd63b3/bbd07e16-17df-40d7-a9fe-2cbd50f823ea/Rocket+League+rank+distribution+Season+5.jpg

[BC00]: https://ballchasing.com/
[BC01]: https://ballchasing.com/doc/api
[BC02]: https://store.steampowered.com/
[BC03]: https://ballchasing.com/upload

[HJ00]: https://hydejack.com/
[HJ01]: licenses/GPL-3.0.md
[HJ02]: NOTICE.md