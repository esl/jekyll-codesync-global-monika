# Conference migration inventory

Generated 2026-07-06 by `migration-data/build_inventory.py` from the probe data
in `migration-data/*.json` (live codesync.global listing, CMS page probes, external
link health, ESL brand-repo archives, Code Sync YouTube playlists, and the
erlang-factory.com census). See MIGRATION.md for the migration contract.

Statuses used in Action: `extract` = pull out of the Sonata CMS into a brand
repo; `none - hub links out` = already archived/alive elsewhere, the hub just
links to it; `reconstruct-from-wayback` = original site dead, rebuild from
Wayback Machine captures; `OPEN` = needs a decision or missing information.

## Code BEAM America

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Code BEAM America 2025 | 6-7 Mar 2025 | codebeamamerica.com root page (live - still serves the 2025 edition; no CBA_2025 in repo archives/ yet) | [Code BEAM America 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZvlH5oMb_hvvTi5ppljk9On), 26 videos | snapshot into esl/code-beam-america archives/CBA_2025 before a future edition replaces the root (a second 2-video 2025 playlist also exists) |
| Code BEAM America 2024 | 7-8 Mar 2024 | esl/code-beam-america archives/CBA_2024 (codebeamamerica.com/archives/CBA_2024 responds 200) | [Code BEAM America 2024](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtPB-dh2s63eaUXPEFNOaxl), 38 videos | none - hub links out |
| Code BEAM America 2022 | 3-4 Nov 2022 | esl/code-beam-america archives/CBA_2022 (alive) | [Code BEAM America 2022](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZueYk1VvTJUpwniZ7sWn_hm), 31 videos | none - hub links out |
| Code BEAM America 2021 (SF) | 3-5 Nov 2021 | CMS: /conferences/code-beam-sf-2021/ (63 speakers, cms-native schedule) | [Code BEAM America 2021](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZszGANDDqI25eXjIXs4iqig), 34 videos | extract to esl/code-beam-america archives/ |
| Code BEAM V America 2021 | 10-12 Mar 2021 | CMS: /conferences/code-beam-v-america-2021/ (57 speakers, cms-native schedule) | [Code BEAM V America 2021](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtsGA-ZEVHfVE4Ch2wMMyKg), 30 videos | extract to esl/code-beam-america archives/ |
| Code BEAM SF 2020 | 5-6 Mar 2020 | CMS: /conferences/code-beam-sf/ (61 speakers, cms-native schedule) | [Code BEAM SF 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zv85s835EGDeCIBYMipJKgL), 16 videos | extract to esl/code-beam-america archives/ |
| Code BEAM SF 2019 | 28 Feb - 1 Mar 2019 | CMS: /conferences/code-beam-sf-2019/ (60 speakers, cms-native schedule) | [Code BEAM SF 2019](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zui_Qx0kycNL-21atr0-iiw), 39 videos | extract to esl/code-beam-america archives/ |
| Code BEAM SF 2018 | 15-17 Mar 2018 | CMS: /conferences/code-beam-sf-2018/ (54 speakers); secondary copy live on erlang-factory.com | [Code BEAM SF 2018](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtZD26dICR-ui1UIlhdVm-v), 50 videos | extract to esl/code-beam-america archives/ |

## Code BEAM Europe / STO

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Code BEAM Europe 2025 (Berlin) | 5-6 Nov 2025 | esl/code-beam-europe archives/berlin_2025 | [Code BEAM Europe 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zsb00vrNRGm1db6CK53Yq5V), 43 videos | hub entry still has past:false - flip it (also: Gleam Talks CBE 2025 playlist exists) |
| Code BEAM Europe 2024 (Berlin) | 14-15 Oct 2024 | esl/code-beam-europe archives/berlin_2024 | [Code BEAM Europe 2024](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zui6Gkr8Nniwyo4TnE17bF0), 51 videos | add hub entry (missing from _conferences) |
| Code BEAM Europe 2023 (Berlin) | 19-20 Oct 2023 | esl/code-beam-europe archives/berlin_2023 (alive) | [Code BEAM Europe 2023](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZvcztbHJ4LMeXOlHYamUMSR), 48 videos | add hub entry |
| Code BEAM Europe 2022 (Stockholm) | 19-20 May 2022 | CMS: /conferences/code-beam-sto-2022/ (43 speakers, cms-native schedule) | [Code BEAM Europe 2022](https://www.youtube.com/playlist?list=PLvL2NEhYV4Ztt98wXV5oV3YE9O7HiZhh9), 32 videos | extract to esl/code-beam-stockholm archive/ - VERIFY playlist mapping (titled Europe, event branded STO) |
| Code BEAM STO 2021 (virtual) | 19-21 May 2021 | CMS: /conferences/code-beam-sto-2021/ (63 speakers) | [Code BEAM V Europe 2021](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtkHrA2Uqq8AgDBCjnltUHd), 26 videos | extract to esl/code-beam-stockholm archive/ - VERIFY playlist mapping |
| Code BEAM STO 2020 (virtual) | 10-11 Sep 2020 | CMS: /conferences/code-beam-sto/ (55 speakers) | [Code BEAM V 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtZ3c4NEvwvvvpOlEY2NrYQ), 51 videos | extract to esl/code-beam-stockholm archive/ - VERIFY playlist mapping (V 2020 may be a distinct virtual event) |
| Code BEAM STO 2019 | 16-17 May 2019 | CMS: /conferences/code-beam-sto-2019/ (67 speakers) | [Code BEAM STO 2019](https://www.youtube.com/playlist?list=PLvL2NEhYV4Ztq2fM3aGvXlj_jOfiopM2B), 49 videos | extract to esl/code-beam-stockholm archive/ |
| Code BEAM STO 2018 | 31 May - 1 Jun 2018 (verify) | erlang-factory.com (live static page); MISSING from codesync.global listing | [Code BEAM STO 2018](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsuMetmDORnzhpkYrYsuK28), 54 videos | add edition to hub listing + archive to esl/code-beam-stockholm; verify exact dates from page |

## Code BEAM Lite

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Code BEAM Lite Stockholm 2026 | 2026 (upcoming/recent - verify) | esl/code-beam-stockholm (current site) | [Code BEAM Lite Stockholm 2026](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsO47bB1V65xElZOYyLW-VJ), 3 videos | verify status; hub upcoming/past entry |
| Code BEAM Lite Stockholm 2025 | Jun 2025 (verify) | esl/code-beam-stockholm archive/june_2025 | [Code BEAM Lite Stockholm 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZuG35A0D7CShTCGcGjKHpDD), 12 videos | add hub entry |
| Code BEAM Lite London 2025 | Jan 2025 | esl/code-beam-london archive/january_2025 | none | add hub entry; no playlist found |
| Code BEAM Lite NYC 2024 | Nov 2024 | esl/code-beam-nyc archive/nov_2024 | none | add hub entry; no playlist found |
| Code BEAM Lite Stockholm 2024 | May 2024 (verify) | esl/code-beam-stockholm archive/may_2024 | [Code BEAM Lite Stockholm 2024](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZvqAwZu5lg2A4U9OTDxCT26), 7 videos | add hub entry |
| Code BEAM Lite Stockholm 2023 | 12 May 2023 | esl/code-beam-stockholm archive/may_2023 (codebeamstockholm.com alive) | [Code BEAM Lite Stockholm 2023](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZuwsPpgYaNmwbWsu0Nsfi_H), 11 videos | none - hub links out |
| Code BEAM Lite Virtual 2020 | 3-4 Apr 2020 | CMS: /conferences/code-beam-lite-virtual/ (9 speakers) | none | extract to new esl/code-beam-lite archives/ |
| Code BEAM Lite Amsterdam 2019 | 28 Nov 2019 | CMS: /conferences/code-beam-lite-amsterdam/ (20 speakers) | [Code BEAM Lite Amsterdam 19](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtHPqiRFH4nAJwbrfz04V_Q), 12 videos | extract |
| Code BEAM Lite India 2019 | 14 Nov 2019 | CMS: /conferences/code-beam-lite-india/ (5 speakers, NO schedule section) | none | extract; page was never fully built - mark partial |
| Code BEAM Lite Berlin 2019 | 11 Oct 2019 | CMS: /conferences/code-beam-lite-berlin-2019/ (16 speakers) | none | extract |
| Code BEAM Lite Budapest 2019 | 20 Sep 2019 | CMS: /conferences/code-beam-lite-budapest/ (19 speakers) | none | extract |
| Code BEAM Lite Italy 2019 | 22 Mar 2019 | CMS: /conferences/code-beam-lite-italy/ (16 speakers) | none | extract |
| Code BEAM Lite Munich 2018 | 7 Dec 2018 | CMS: /conferences/cbl-munich-2018/ (14 speakers) | [Code BEAM Lite Munich 2018](https://www.youtube.com/playlist?list=PLvL2NEhYV4Ztyk61upvBMvVPbfTyfFgCE), 9 videos | extract |
| Code BEAM Lite Amsterdam 2018 | 30 Nov 2018 | CMS: /conferences/cbl-amsterdam-2018/ (18 speakers) | none | extract; hub entry exists but has broken brand ref + missing init date |
| Code BEAM Lite Berlin 2018 | 12 Oct 2018 | CMS: /conferences/code-beam-lite-berlin-2018/ (14 speakers) | [Code BEAM Lite Berlin 2018](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zs6eFJ9yx-jR7UShGGfPnY4), 10 videos | extract |

## Partner-run Code BEAM editions

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Code BEAM Mexico 2023 | 3-4 Mar 2023 | codebeammexico.com root page (live, partner-run); esl/code-beam-mexico repo holds only 2015-2020 legacy content | [Code BEAM Lite Mexico 2023](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsImAG9iMk0rXl5LOtvvCa8), 9 videos | hub links out; consider snapshotting since root page will not last forever |
| Code BEAM Lite A Coruna 2022 | 10-11 Jun 2022 | codebeamcorunha.es (live, partner-run; content is JS-rendered) | [Code BEAM Lite A Coruña 2022](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtiUgLe26sb7gMUMnaDOjoo), 11 videos | hub links out; later partner editions exist (Code BEAM Corunha 2024 CfP on Sessionize) - decide if they belong on the listing |
| Code BEAM Brasil 2020 (virtual) | 6-7 Nov 2020 | site possibly codebeambr.com (Cloudflare-blocked to curl - verify in a browser); reported by InfoQ | none | OPEN: confirm site and speaker/schedule data; no playlist on the Code Sync channel - talks may be on a Brazilian community channel |

## Code Mesh

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Code Mesh V 2020 | 5-6 Nov 2020 | CMS: /conferences/code-mesh-ldn/ (50 speakers) | [Code Mesh V 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zu0Jrp0l90aU83_AfuFcN_q), 32 videos | extract to new esl/code-mesh archives/ |
| Code Mesh LDN 2019 | 6-8 Nov 2019 | CMS: /conferences/code-mesh-ldn-2019/ (51 speakers) | [Code Mesh LDN 2019](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsX7qLphosGW_WoYT4u-udv), 34 videos | extract |
| Code Mesh LDN 2018 | 8-9 Nov 2018 | CMS: /conferences/code-mesh-2018/ (45 speakers) | [Code Mesh LDN 2018](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtWFBNOrApXaIoCTtj-yk7Y), 36 videos | extract |
| Code Mesh 2017 | 8-9 Nov 2017 | codemesh.io/codemesh2017 (alive) | none | none - hub links out; consider mirroring later |
| Code Mesh 2016 | 3-4 Nov 2016 | codemesh.io/codemesh2016 (alive) | none | none - hub links out; consider mirroring later |

## Code Elixir LDN / Elixir LDN

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Code Elixir LDN 2019 | 18 Jul 2019 | CMS: /conferences/code-elixir-ldn-2019/ (15 speakers) | [Code Elixir LDN 2019](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZvvzEOmlqLUyrZdsW27w7zH), 13 videos | extract to new esl/code-elixir-ldn archives/ |
| Code Elixir LDN 2018 | 16 Aug 2018 | NOT on live listing; hub entry exists; check Wayback for codesync.global/conferences/code-elixir-ldn-2018 | [Code Elixir LDN 2018](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zu4zxnZXtCSOCvsUHtxTYIl), 16 videos | reconstruct from Wayback + playlist (16 videos) |
| Elixir LDN 2017 | 17 Aug 2017 | LOST - elixir.london DNS dead; Wayback captures exist (verify post-event snapshots); no playlist | none | reconstruct-from-wayback (partial); hub entry exists |
| Elixir.LDN 2016 | 22 Sep 2016 | LOST - elixir.london/2016 DNS dead; Wayback capture 2016-09-21 is PRE-event; no playlist | none | reconstruct-from-wayback (partial); check for post-event captures |

## ElixirConf EU

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| ElixirConf EU 2026 (Malaga) | 23-24 Apr 2026 | www.elixirconf.eu (current site; not yet in archives/) | [ElixirConf EU 2026](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsIgecSexrk26--PBWiEyUy), 14 videos | add hub entry; archive to elixirconf-eu-jekyll archives/ when the site rolls over |
| ElixirConf EU 2025 (Krakow) | 2025 (verify) | esl/elixirconf-eu-jekyll archives/krakow_2025 | [ElixirConf EU 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zu421KzHuLICUqieJXI2o_Z), 43 videos | add hub entry (missing from listing); 2026 playlist also already exists |
| ElixirConf EU 2024 (Lisbon) | 18-19 Apr 2024 | elixirconf.eu/archives/lisbon_2024 (alive, in repo) | [ElixirConf EU 2024](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtQulvJh7sZFDWkaDvB3QT2), 45 videos | none - hub links out |
| ElixirConf EU 2023 (Lisbon) | 20-21 Apr 2023 | elixirconf.eu/archives/lisbon_2023 (alive, in repo) | [ElixirConf EU 2023](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtBoR52raL_l7XQIb1YH-H7), 40 videos | none |
| ElixirConf EU 2022 (London) | 9-10 Jun 2022 | elixirconf.eu/archives/london_2022 (alive, in repo) | [ElixirConf EU 2022](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZuuF39_A_DAh6IwIuh8K6gd), 25 videos | none |
| ElixirConf EU 2021 (Warsaw) | 9-10 Sep 2021 | elixirconf.eu/archives/warsaw_2021 (alive, in repo) | [ElixirConf EU 2021](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtdiDIxP_rPMQ5VmVhs4CKJ), 24 videos | none |
| ElixirConf EU Virtual X 2020 | 7-8 Oct 2020 | elixirconf.eu/archives/virtual_x_2020 (alive, in repo) | [ElixirConf EU Virtual October 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZuqgpAyZVzeCoz6GQrQx9Xc), 24 videos | none |
| ElixirConf EU Virtual VI 2020 | 18-19 Jun 2020 | elixirconf.eu/archives/virtual_2020 (alive, in repo) | [ElixirConf EU Virtual June 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZuKXQqD64oZFss2fGERjKyK), 15 videos | none |
| ElixirConf EU 2019 (Prague) | 8-9 Apr 2019 | archive.elixirconf.eu/elixirconfeu2019 (alive; SEPARATE old host - longevity risk) | [ElixirConf EU 2019](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtoiQC735NjHyPJUS_nmrxy), 33 videos | consider mirroring 2015-2019 into elixirconf-eu-jekyll archives/ |
| ElixirConf EU 2018 (Warsaw) | 16-17 Apr 2018 | archive.elixirconf.eu/elixirconfeu2018 (alive; old host) | none | as above |
| ElixirConf EU 2017 (Barcelona) | 5 Apr 2017 | archive.elixirconf.eu/elixirconf2017 (alive; old host) | none | as above |
| ElixirConf EU 2016 (Berlin) | 11-12 May 2016 | archive.elixirconf.eu/elixirconf2016 (alive; old host) | none | as above |
| ElixirConf EU 2015 (Krakow) | 23-24 Apr 2015 | archive.elixirconf.eu/elixirconf2015 (alive; old host) | none | as above |

## ElixirConf US

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| ElixirConf US 2025 | 28-29 Aug 2025 | esl/elixirconf-us archives/elixirconf_2025 | none | hub entry has past:false (stale) and references missing brand file elixirconf-us.md - fix both |

## Lambda Days

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| Lambda Days 2025 | 2025 (verify) | lambdadays.org (alive); MISSING from codesync.global listing | [Lambda Days 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtDZCilo_GAk0piEyUDhtMG), 49 videos | add hub entry |
| Lambda Days 2024 | 27-28 May 2024 | lambdadays.org/lambdadays2024 (alive) | [Lambda Days 2024](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtX2TurK0BIlKD_cHct0rSs), 45 videos | none - hub links out |
| Lambda Days 2023 | 5-6 Jun 2023 | lambdadays.org/lambdadays2023 | [Lambda Days 2023](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsFoD9SCSIib8QJCsHI4wgc), 43 videos | none |
| Lambda Days 2022 | 28-29 Jul 2022 | lambdadays.org/lambdadays2022 | [Lambda Days 2022](https://www.youtube.com/playlist?list=PLvL2NEhYV4Ztg01ZtwkIVTDhSHDTB7RTu), 42 videos | none |
| Lambda Days 2021 | 17-18 Feb 2021 | lambdadays.org/lambdadays2021 | [Lambda Days 2021](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zvmd7P5p2hz8D0-QkIKuwOt), 36 videos | none |
| Lambda Days 2020 | 13-14 Feb 2020 | lambdadays.org/lambdadays2020 | [Lambda Days 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsV9Bw0wp1P46SOdtk4pFW6), 51 videos | none |
| Lambda Days 2019 | 14-15 Feb 2019 | lambdadays.org/lambdadays2019 | [Lambda Days 2019](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZvCRCVlXTfB6-d09K3r0Sxa), 40 videos | none |
| Lambda Days 2018 | 22-23 Feb 2018 | lambdadays.org/lambdadays2018 | none | none |
| Lambda Days 2017 | 9-10 Feb 2017 | lambdadays.org/lambdadays2017 | none | none |
| Lambda Days 2016 | 25-26 Feb 2016 | lambdadays.org/lambdadays2016 | none | none |
| Lambda Days 2015 | 26-27 Feb 2015 | lambdadays.org/lambdadays2015 | none | none |
| Lambda Days 2014 | 27-28 Feb 2014 | lambdadays.org/lambdadays2014 | none | none |

## MQ Summit (incl. RabbitMQ Summit)

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| MQ Summit 2025 (Berlin) | 6 Nov 2025 | esl/mq-summit-page archives/berlin_2025 (mqsummit.com) | [MQ Summit 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZufbYkb1FM9e6onSpjQ8Zdv), 12 videos | hub entry has past:false - flip it |
| RabbitMQ Summit 2024 | 15 Oct 2024 (Berlin) | rabbitmqsummit.com/2024 (alive - canonical reference) | [RabbitMQ Summit 2024](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtLJy7PwHNt_CbDcBqVkk8P), 12 videos | done - hub entry added, date verified on site 2026-07-07 |
| RabbitMQ Summit 2023 | 20 Oct 2023 (Berlin) | rabbitmqsummit.com/2023 (alive - canonical reference); mq-summit-page archives/berlin_2023 may duplicate it | [RabbitMQ Summit 2023](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsALsESTtvpUSSnB-ut0SRJ), 12 videos | done - hub entry added, date verified on site 2026-07-07 |
| RabbitMQ Summit 2022 | 16 Sep 2022 (London) | rabbitmqsummit.com/2022 (alive - canonical reference) | [RabbitMQ Summit 2022](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zvf7In1ZoxcL5BgqvvJYscQ), 17 videos | done - hub entry added, date verified on site 2026-07-07 |
| RabbitMQ Summit 2021 | 13-14 Jul 2021 (online) | rabbitmqsummit.com/2021 (alive - canonical reference) | [RabbitMQ Summit 2021](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zs2ZakMrMBO_tr-CgEbOLRL), 21 videos | done - hub entry added; date CORRECTED (was 5 Jul, site says 13-14 Jul online), verified 2026-07-07 |
| RabbitMQ Summit 2019 | 4 Nov 2019 (London) | rabbitmqsummit.com/2019 (alive - canonical reference) | none | done - hub entry added, date verified on site 2026-07-07; no playlist found |
| RabbitMQ Summit 2018 | 12 Nov 2018 (London) | rabbitmqsummit.com/2018 (alive - canonical reference) | none | done - hub entry added, date verified on site 2026-07-07; no playlist found (no 2020 edition exists on the site) |

## Upcoming (for the hub banner)

| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |
|---|---|---|---|---|
| ElixirConf Brasil 2026 | Nov 2026 (Curitiba & online) | elixirconf.com.br (partner-run, first edition); NOTE esl/elixirconf-brasil repo is a stale EU fork (CNAME still www.elixirconf.eu) | none | add to hub upcoming/banner; move to ElixirConf section once past |
| Code BEAM Europe 2026 (Haarlem) | 21-22 Oct 2026 | codebeameurope.com (live) | none | add to hub upcoming/banner |
| Code BEAM Lite London 2026 | 2026 (verify) | codebeamlondon.com (live) | none | verify date; add to hub upcoming/banner |

## Older Conferences (pre-Sonata, erlang-factory.com era)

Per the migration decision these all go into a single "Older Conferences"
section at the end of /conferences/, not under the modern brands. Live editions
(2014-2018) are static single-page sites and can be scraped directly; 2009-2013
editions return 403 on the live server and must come from the Wayback Machine
(speaker and programme pages are all in the CDX index). Dates below come from
the census; `null` year means the archived page does not state one.

### Erlang Factory

| Edition | Year | City | URL | Live? | Speakers/Schedule | Source |
|---|---|---|---|---|---|---|
| Erlang & Elixir Factory SF Bay Area 2017 | 2017 | San Francisco | http://www.erlang-factory.com/sfbay2017 | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang Factory SF Bay Area 2016 | 2016 | San Francisco | http://www.erlang-factory.com/sfbay2016/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang Factory SF Bay Area 2015 | 2015 | San Francisco | http://www.erlang-factory.com/sfbay2015/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Chicago Erlang 2014 | 2014 | Chicago | http://www.erlang-factory.com/chicago2014/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang Factory SF Bay Area 2014 | 2014 | San Francisco | http://www.erlang-factory.com/sfbay2014/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| (unnamed) | 2013 | San Francisco | http://www.erlang-factory.com/conference/SFBay2013 | 403 | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2013 | Krakow | http://www.erlang-factory.com/conference/Krakow2013 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2013 | Budapest | http://www.erlang-factory.com/conference/Budapest2013 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2013 | Dublin | http://www.erlang-factory.com/conference/Dublin2013 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2013 | New York City | http://www.erlang-factory.com/conference/NYC2013 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2012 | San Francisco | http://www.erlang-factory.com/conference/SFBay2012 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2012 | Munich | http://www.erlang-factory.com/conference/Munich2012 | wayback-only | yes/yes | Wayback CDX index (distinct from ErlangFactoryLiteMunich: different archived speaker rosters); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2012 | Zurich | http://www.erlang-factory.com/conference/Zurich2012 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2011 | Krakow | http://www.erlang-factory.com/conference/Krakow2011 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2011 | Brisbane | http://www.erlang-factory.com/conference/Brisbane2011 | 403 | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang Factory London 2011 | 2011 | London | http://www.erlang-factory.com/conference/London2011 | 403 | yes/yes | wayback homepage 2011-06 link text; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang Factory SF Bay Area 2011 | 2011 | San Francisco | http://www.erlang-factory.com/conference/SFBay2011 | wayback-only | yes/yes | wayback homepage 2011-06 nav title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2010 | San Francisco | http://www.erlang-factory.com/conference/SFBay2010 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2010 | London | http://www.erlang-factory.com/conference/London2010 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Testing Tutorial Workshop 2010 | 2010 | null | http://www.erlang-factory.com/conference/TestingTutorialWorkshop2010 | wayback-only | yes/yes | url (self-describing slug); alias /conference/testingtutorialworkshop also archived; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| (unnamed) | 2009 | London | http://www.erlang-factory.com/conference/London2009 | wayback-only | yes/yes | Wayback CDX index; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| SF Bay Area Erlang Factory 2009 | 2009 | San Francisco | http://www.erlang-factory.com/conference/SFBayAreaErlangFactory2009 | wayback-only | yes/yes | url (self-describing slug); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| SIGPLAN Erlang Workshop 2009 | 2009 | Edinburgh | http://www.erlang-factory.com/conference/2009ErlangWorkshop | wayback-only | yes/yes | wayback page <title>; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |

### Erlang User Conference

| Edition | Year | City | URL | Live? | Speakers/Schedule | Source |
|---|---|---|---|---|---|---|
| Erlang User Conference 2017 | 2017 | null | http://www.erlang-factory.com/euc2017/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang User Conference 2016 | 2016 | null | http://www.erlang-factory.com/euc2016/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang User Conference 2015 | 2015 | null | http://www.erlang-factory.com/euc2015/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang User Conference 2014 | 2014 | null | http://www.erlang-factory.com/euc2014/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Erlang User Conference 2013 | 2013 | null | http://www.erlang-factory.com/conference/ErlangUserConference2013 | 403 | yes/yes | url (self-describing slug); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang User Conference 2012 | 2012 | null | http://www.erlang-factory.com/conference/ErlangUserConference2012 | wayback-only | yes/yes | wayback ErlangFactoryLites page link title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang User Conference 2011 | 2011 | null | http://www.erlang-factory.com/conference/ErlangUserConference2011 | wayback-only | yes/yes | url (self-describing slug); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang User Conference 2010 | 2010 | Stockholm | http://www.erlang-factory.com/conference/ErlangUserConference2010 | wayback-only | yes/yes | wayback homepage 2011-06 nav title 'Erlang User Conference 2010, Stockholm'; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang User Conference 2009 | 2009 | null | http://www.erlang-factory.com/conference/ErlangUserConference2009 | wayback-only | yes/yes | url (self-describing slug); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |

### Factory Lite

| Edition | Year | City | URL | Live? | Speakers/Schedule | Source |
|---|---|---|---|---|---|---|
| Buenos Aires Erlang & Elixir Factory Lite 2017 | 2017 | Buenos Aires | http://www.erlang-factory.com/eflba2017/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| India Erlang & Elixir Factory Lite 2017 | 2017 | null | http://www.erlang-factory.com/india2017/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Rome Erlang Factory Lite 2017 | 2017 | Rome | http://www.erlang-factory.com/rome2017/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Berlin Erlang Factory Lite 2016 | 2016 | Berlin | http://www.erlang-factory.com/berlin2016/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Brussels Erlang Factory Lite 2016 | 2016 | Brussels | http://www.erlang-factory.com/brussels2016/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Mexico City Erlang Factory Lite 2016 | 2016 | Mexico City | http://www.erlang-factory.com/mexico2016/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Berlin Erlang Factory Lite 2015 | 2015 | Berlin | http://www.erlang-factory.com/berlin2015/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Dublin Erlang Factory Lite 2015 | 2015 | Dublin | http://www.erlang-factory.com/dublin2015/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Mexico City Erlang Factory Lite 2015 | 2015 | Mexico City | http://www.erlang-factory.com/mexico2015/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Berlin Erlang Factory Lite 2014 | 2014 | Berlin | http://www.erlang-factory.com/berlin2014/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Vancouver Erlang Factory Lite | 2014 | Vancouver | http://www.erlang-factory.com/vancouver2014/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Zurich Erlang Factory Lite 2014 | 2014 | Zurich | http://www.erlang-factory.com/zurich2014/home | 200 | yes/yes | live /mainpage/past_conferences listing (anchor text) + live status sweep; speakers/programme are sections of the single-page site with per-speaker subpages (verified on sfbay2016 home; sfbay2017 is a single root page with speaker assets) |
| Berlin Erlang Factory Lite 2013 | 2013 | Berlin | http://www.erlang-factory.com/conference/Berlin2013 | wayback-only | yes/yes | wayback homepage 2013-12 nav title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Chicago Erlang Factory Lite 2013 | 2013 | Chicago | http://www.erlang-factory.com/conference/Chicago2013 | wayback-only | yes/yes | wayback homepage 2013-12 nav title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Tel Aviv Erlang Factory Lite 2013 | 2013 | Tel Aviv | http://www.erlang-factory.com/conference/TelAviv2013 | wayback-only | yes/yes | wayback homepage 2013-12 nav link (also present in Wayback CDX index with 15 archived URLs incl. /speakers and /programme); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Toronto Erlang Factory Lite 2013 | 2013 | Toronto | http://www.erlang-factory.com/conference/Toronto2013 | wayback-only | yes/yes | wayback homepage 2013-12 nav title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| London Erlang Factory Lite 2012 | 2012 | London | http://www.erlang-factory.com/conference/London2012 | wayback-only | yes/yes | wayback ErlangFactoryLites page link title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Moscow Erlang Factory Lite 2012 | 2012 | Moscow | http://www.erlang-factory.com/conference/Moscow2012 | wayback-only | yes/yes | wayback ErlangFactoryLites page link title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| St Andrews Erlang Factory Lite 2012 | 2012 | St Andrews | http://www.erlang-factory.com/conference/StAndrews | wayback-only | yes/yes | wayback ErlangFactoryLites page link title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Vancouver Erlang Factory Lite 2012 | 2012 | Vancouver | http://www.erlang-factory.com/conference/Vancouver2012 | wayback-only | yes/yes | wayback ErlangFactoryLites page link title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Edinburgh Factory Lite | 2011 | Edinburgh | http://www.erlang-factory.com/conference/Edinburgh | wayback-only | yes/yes | wayback page <title>; 'August 2011' in page body; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang Factory Lite 2010, Los Angeles | 2010 | Los Angeles | http://www.erlang-factory.com/conference/ErlangFactoryLiteLA | wayback-only | yes/yes | wayback page <title>; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang Factory Lite Krakow 2010 | 2010 | Krakow | http://www.erlang-factory.com/conference/krakow2010 | wayback-only | yes/yes | wayback homepage 2011-06 nav title; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Amsterdam Factory Lite | null | Amsterdam | http://www.erlang-factory.com/conference/Amsterdam | wayback-only | yes/yes | wayback page <title>; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Brussels Erlang Factory Lite | null | Brussels | http://www.erlang-factory.com/conference/Brussels | wayback-only | yes/yes | wayback page <title>; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Erlang Factory Lite Munich | null | Munich | http://www.erlang-factory.com/conference/ErlangFactoryLiteMunich | wayback-only | yes/yes | wayback homepage 2011-06 nav title (no year given; distinct from Munich2012: different archived speaker rosters; likely the 2011 Munich Lite); live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |
| Paris Erlang Factory Lite | null | Paris | http://www.erlang-factory.com/conference/Paris | 403 | yes/yes | wayback page <title>; live app removed: spot-checked slugs 301 to trailing slash then 403 Forbidden (unchecked slugs marked null); speakers/schedule flags from archived /speakers, /programme, /talks, /tracks URLs in CDX (null = no archived evidence, not proof of absence) |

## Appendix: thematic YouTube playlists (not edition-specific)

Kept for the future videos section; may contain talks from lost editions.

- [Lighting talks](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZvRAK83wiV68ndvHlRpmg3F) (9 videos)
- [Top 10 Talks Code Sync Conferences 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zv_ZN7Sehnt43g3KiVRWGLq) (10 videos)
- [Top 10 Talks for the last 90 Days May 2025](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsMINlgaDIjq5LxaouDnpKJ) (10 videos)
- [Women in Elixir - International Women's Day](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsiAuIqUUX_xYeHAljCm4kk) (18 videos)
- [Lambda Ladies: International Women's Day](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zu3neotbUCQLskLVssS3pBs) (23 videos)
- [Women in BEAM: International Women's Day](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZuPf5_-W4DyLCr8J7YbcrLy) (124 videos)
- [Amazing Women on the BEAM](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZtwAWW6NIOH3xGcnODLO_wR) (16 videos)
- [Inspiring Keynotes](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zse7FcIjLZ25Oi_Ro5RvD0l) (25 videos)
- [#BestOfTheBEAM Advent 2020](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsMQ4iKds53f80rUYlOJZpL) (14 videos)
- [Fintech + Erlang and Elixir](https://www.youtube.com/playlist?list=PLvL2NEhYV4Zv16igatbLXvRrUwVWvayiW) (10 videos)
- [Joe Armstrong's Erlang talks](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsIjT55t-kxylCU0BRlQjpl) (20 videos)
- [Pony lang talks 🐎](https://www.youtube.com/playlist?list=PLvL2NEhYV4ZsE4DNpp544kLze6YrelAcn) (1 videos)

## Hub repo data fixes needed (found during inventory)

- Broken `conference_brand` references (point at nonexistent brand files):
  `cbl-amsterdam-2018.md` -> cbl.md, `sample-conference-3.md` -> code-beam-v.md,
  `elixirconf-us-2025.md` -> elixirconf-us.md. This is why brand sections render empty.
- Delete the three `sample-conference*.md` placeholder files.
- `cbl-amsterdam-2018.md` has no `conference_init_date` (breaks date sorting).
- Stale `past: false` on conferences that have happened (as of 2026-07):
  code-beam-europe-2025, elixirconf-us-2025, mq-summit-2025.
- Missing brand files needed: older-conferences (new section), elixirconf-us,
  elixirconf-eu, lambda-days; rename/align cbl vs code-beam-lite.
- Most editions in this inventory have no hub entry yet (~19 real entries vs
  ~115 editions); creating them is the bulk of the hub-side listing work.

## Open questions

1. DECIDED: MQ Summit + RabbitMQ Summit are one brand section on the listing.
   The RabbitMQ era ran on another platform - rabbitmqsummit.com is the canonical
   reference (per-year pages 2018-2024 all alive); current era is mq-summit-page.
2. DECIDED: create esl/code-mesh and esl/code-elixir-ldn on the ESL GitHub for
   those brands' archives.
3. DECIDED: Code BEAM Lite orphan-city editions go into ONE shared new repo,
   esl/code-beam-lite (archives/<city_year>/); Stockholm/NYC/London keep their
   own existing repos.
4. DECIDED: partner-run editions are listed and added as they happen (upcoming ->
   hub banner, then into their brand section once past). Remaining work: add
   Code BEAM Corunha 2024 (and verify any other partner editions we have not
   spotted), and confirm Code BEAM Brasil 2020's site behind codebeambr.com.
5. DECIDED: mirror the five archive.elixirconf.eu editions (2015-2019) into
   elixirconf-eu-jekyll archives/ while the legacy host is still up.
6. EUC 2016 tile on the live site links to erlang-factory.com/sfbay2016 (wrong
   event) - do not carry the link over; the census has the right EUC pages.
7. RESOLVED: ElixirConf Brasil 2026 (first edition, Nov 2026, Curitiba & online)
   lives at elixirconf.com.br, partner-run. The esl/elixirconf-brasil repo is a
   stale EU fork (CNAME still points at www.elixirconf.eu) - clean up or retire it.
