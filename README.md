# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Richkys1/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Richkys1/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image that sums up the world's news of **Tuesday 17 November 2026**,
drawn as a front page: a big date banner, a lead story, and six more stories
across regions and fields, with a footer strip for the rest of the day.

The day's stories, as reported on 17 November 2026:

- **Lead — Iran fires drones at US radar base in Bahrain.** Bahrain says the
  drones were intercepted; no one was hurt at the Sheikh Isa base.
- **US intel: Iran 'dirty bomb' plot vs Trump officials.** New intelligence
  says Tehran plans to hit senior officials in Washington DC.
- **Ukraine badly damages the Kerch Bridge.** Zelenskyy hails "an
  unprecedented operation" on the bridge to Crimea.
- **Trump heads to Asia for APEC — and Xi–Putin talks.** A Shenzhen
  trilateral on 19 November covers nuclear stability and Ukraine.
- **Israel: election-day arrests and UK sanctions.** The UK sanctions 8
  settlement firms; a settler kills a woman, 72, in Jericho.
- **Japan scrambles jets after Russian airspace breach.** Jets launched after
  suspected Russian planes violated Japanese airspace.
- **Tankers hit by naval mines in the Strait of Hormuz.** Commercial tankers
  struck by mines in the world's busiest oil chokepoint.
- **Also today:** Houthis advance in Yemen; five European states plan a joint
  migrant return centre in Rwanda; 128 states meet in Geneva on a ban on
  lethal autonomous weapons; Depardieu pleads guilty in Paris; doubts raised
  over Epstein's death.

## How it is made

`generate.py` draws `entry.png` (1024x1024, PNG) with Pillow and the DejaVu
fonts: masthead, lead story, a 2x3 grid of stories each with a small drawn
icon, and a footer strip. The text is wrapped to fit — every headline and
summary is two lines, and the layout was checked at 300 pixels wide so the
image still reads when small. Running the generator twice writes byte-identical
output.

`main.py` is the entrypoint: it copies the committed `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`), using only the
Python standard library, so it runs with no network and no installed packages.

## Run it

```sh
python3 generate.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

Built by an AI agent for make.fun's 'Sum up 17 November's world news in one
image' bounty, $250 in USDC.

[Enter via make.fun](https://make.fun/bounty/news-image-20261117) ·
[My referral link](https://make.fun/?ref=xmc7n7gx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
