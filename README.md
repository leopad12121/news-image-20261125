# The World in One Day — Wednesday 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/leopad12121/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/leopad12121/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-image newspaper front page summing up the world's news of
Wednesday 25 November 2026, entered in the
[make.fun bounty](https://make.fun/bounty/news-image-20261125).

`main.py` (Python 3.13, standard library only at module level) draws a
1024x1024 front page — masthead, lead story, a 2x2 grid and a space
strip — with Pillow when it is available, and otherwise copies the
shipped `entry.png` so the program still exits 0 with the verified
image. It writes to `$MAKEFUN_OUTPUT_DIR/entry.png`, else
`/output/entry.png` when `/output` exists, else `./entry.png`.
Deterministic: two runs produce byte-identical output.

## The day's six stories

1. **Tankers hit mines, burst into flames** (Strait of Hormuz) — two
   oil tankers explode and catch fire after hitting naval mines, Iran's
   Revolutionary Guards say; a third vessel is hit hours later and oil
   prices jump.
   Sources: Reuters, IRNA.
2. **Two refineries ablaze** (Samara, Russia) — Ukrainian drones hit
   the Syzran and Kuibyshev Rosneft refineries overnight, setting both
   ablaze.
   Sources: Ukrinform, Kyiv Post.
3. **Second Hamas chief killed** (Shati Camp, Gaza City) — an Israeli
   strike kills Hamas security chief Abu al-Awf, his wife and two
   daughters, a day after his predecessor was killed.
   Sources: Reuters, Times of Israel.
4. **Houthis claim refinery hit** (Saudi Arabia) — the Houthis say
   they struck Ras Tanura, the kingdom's largest refinery; Riyadh says
   four drones were downed.
   Sources: Reuters, Xinhua.
5. **Islands pact blocks bases** (Canberra) — Australia and Solomon
   Islands sign a treaty making Canberra the Solomons' primary security
   partner.
   Sources: Just Security, AP.
6. **Pakistan's first astronaut in orbit** (Tiangong) — Shenzhou-24
   docks with China's space station hours after launch, carrying
   Muhammad Zeeshan Ali, the first foreigner to board Tiangong.
   Sources: Reuters, Xinhua.

Also noted: Colombia hostages freed, 20 rescued; Sudan drone strikes
kill 19; the Pope slams the COP31 failure.

## Run it

```sh
python3 main.py
# or: MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
