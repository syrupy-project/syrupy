window.BENCHMARK_DATA = {
  "lastUpdate": 1669766474615,
  "repoUrl": "https://github.com/tophat/syrupy",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4f66267b1c44c3f16ee05f7b4d89fcb3214a75ba",
          "message": "chore: add benchmark github action (#613)",
          "timestamp": "2022-08-11T16:59:35-04:00",
          "tree_id": "091864111b50406923240de5c6b402c1aa7c64a5",
          "url": "https://github.com/tophat/syrupy/commit/4f66267b1c44c3f16ee05f7b4d89fcb3214a75ba"
        },
        "date": 1660251723698,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7838002556681452,
            "unit": "iter/sec",
            "range": "stddev: 0.05409515953131718",
            "extra": "mean: 1.2758352562000084 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7485245241769561,
            "unit": "iter/sec",
            "range": "stddev: 0.16001935776226286",
            "extra": "mean: 1.3359615720000022 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7322481784381983,
            "unit": "iter/sec",
            "range": "stddev: 0.07215602247276584",
            "extra": "mean: 1.3656572039999957 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "09698c2c85c8a2cc8fd527a8f87a65f2a25133ef",
          "message": "chore: fix release action order (#614)",
          "timestamp": "2022-08-11T17:03:53-04:00",
          "tree_id": "62b4354b8c4f65704a89cb91f7896bd720e5f1ff",
          "url": "https://github.com/tophat/syrupy/commit/09698c2c85c8a2cc8fd527a8f87a65f2a25133ef"
        },
        "date": 1660252015645,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5288857147518898,
            "unit": "iter/sec",
            "range": "stddev: 0.11078921781854142",
            "extra": "mean: 1.890767649999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.502105660474314,
            "unit": "iter/sec",
            "range": "stddev: 0.2246051588620599",
            "extra": "mean: 1.9916126798000051 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5013767645514013,
            "unit": "iter/sec",
            "range": "stddev: 0.11303430331780326",
            "extra": "mean: 1.9945080640000015 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f341355200ca5d5a04249eca2e6b28d14a5e4d5a",
          "message": "docs: add note about benchmarks (#615)",
          "timestamp": "2022-08-11T17:06:05-04:00",
          "tree_id": "9b0e6596e4744adb5eeab87d16663582fbd00b79",
          "url": "https://github.com/tophat/syrupy/commit/f341355200ca5d5a04249eca2e6b28d14a5e4d5a"
        },
        "date": 1660252250892,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6714027163621854,
            "unit": "iter/sec",
            "range": "stddev: 0.07992748316164767",
            "extra": "mean: 1.489419055999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6280396548564035,
            "unit": "iter/sec",
            "range": "stddev: 0.24841403467148906",
            "extra": "mean: 1.5922561453999946 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6288116664997968,
            "unit": "iter/sec",
            "range": "stddev: 0.10171100440099168",
            "extra": "mean: 1.590301283000008 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a73fac2bec0c1ac0bb985911b45b5900ab3e18c6",
          "message": "chore: only run workflow once for next (#616)",
          "timestamp": "2022-08-11T17:24:58-04:00",
          "tree_id": "a9abfb877162ab2e93d983acf3a3f6c4ab945b29",
          "url": "https://github.com/tophat/syrupy/commit/a73fac2bec0c1ac0bb985911b45b5900ab3e18c6"
        },
        "date": 1660253323490,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6743524675517246,
            "unit": "iter/sec",
            "range": "stddev: 0.078243655327627",
            "extra": "mean: 1.4829040422000048 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6422536691526739,
            "unit": "iter/sec",
            "range": "stddev: 0.2328981030183329",
            "extra": "mean: 1.5570171849999723 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.635550832760935,
            "unit": "iter/sec",
            "range": "stddev: 0.09141909305056715",
            "extra": "mean: 1.5734382655999979 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "f49678136d89efd1e8b929487e0a360720f4fc6b",
          "message": "chore: remove commit sha action",
          "timestamp": "2022-08-11T17:28:34-04:00",
          "tree_id": "6daf3e9d314d64b37c9d32a45ea91c32613a5622",
          "url": "https://github.com/tophat/syrupy/commit/f49678136d89efd1e8b929487e0a360720f4fc6b"
        },
        "date": 1660253499495,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5694844708740344,
            "unit": "iter/sec",
            "range": "stddev: 0.07397852816921413",
            "extra": "mean: 1.7559741330000065 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5469822733087769,
            "unit": "iter/sec",
            "range": "stddev: 0.29029145004471374",
            "extra": "mean: 1.8282128120000152 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5524267837756454,
            "unit": "iter/sec",
            "range": "stddev: 0.10959872907861361",
            "extra": "mean: 1.8101946345999864 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "huon@exoflare.io",
            "name": "Huon Wilson",
            "username": "huonw"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f2b2e774b6055fde887a36d2a995ebb284ebc76e",
          "message": "fix: avoid reporting crash for snapshot dir outside pytest dir (#621)",
          "timestamp": "2022-09-20T09:11:47-04:00",
          "tree_id": "bc2bcdc0bab4e65554ccec7686b65c1e263edb10",
          "url": "https://github.com/tophat/syrupy/commit/f2b2e774b6055fde887a36d2a995ebb284ebc76e"
        },
        "date": 1663679719408,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.4820492496535262,
            "unit": "iter/sec",
            "range": "stddev: 0.11977233617181143",
            "extra": "mean: 2.0744768314000113 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.45807324605881017,
            "unit": "iter/sec",
            "range": "stddev: 0.24841780381063927",
            "extra": "mean: 2.183056986200006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.424082402577015,
            "unit": "iter/sec",
            "range": "stddev: 0.33641448922170325",
            "extra": "mean: 2.3580322926000123 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "e078c8a44d5cc60d2b28ed2c0322d60aa09ee723",
          "message": "refactor: support dry-release mode",
          "timestamp": "2022-09-23T08:56:30-04:00",
          "tree_id": "0496d435bc0774ed5cca7bf534fc2247737dfae2",
          "url": "https://github.com/tophat/syrupy/commit/e078c8a44d5cc60d2b28ed2c0322d60aa09ee723"
        },
        "date": 1663937956674,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6653167122673878,
            "unit": "iter/sec",
            "range": "stddev: 0.09970989125664284",
            "extra": "mean: 1.5030435604000048 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6269378562934125,
            "unit": "iter/sec",
            "range": "stddev: 0.2580210492542531",
            "extra": "mean: 1.595054421999987 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5816504834642097,
            "unit": "iter/sec",
            "range": "stddev: 0.24107036647694174",
            "extra": "mean: 1.7192455407999887 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "07a1490ae683c97f384b9f68669c4be34f96f2ff",
          "message": "refactor: update poetry version in pyproject.toml",
          "timestamp": "2022-09-23T09:29:01-04:00",
          "tree_id": "f8b833a44d048c206738e45fb50050c1a67ffb6d",
          "url": "https://github.com/tophat/syrupy/commit/07a1490ae683c97f384b9f68669c4be34f96f2ff"
        },
        "date": 1663939934105,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.533536829971345,
            "unit": "iter/sec",
            "range": "stddev: 0.07121052751687179",
            "extra": "mean: 1.8742848549999962 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5073418177705352,
            "unit": "iter/sec",
            "range": "stddev: 0.355825872291898",
            "extra": "mean: 1.9710577069999942 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4466190630324451,
            "unit": "iter/sec",
            "range": "stddev: 0.34604416735238924",
            "extra": "mean: 2.239044597000003 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "43d78ecc0a2175487db1c9bf5857d6ee34344046",
          "message": "fix: update classifiers (no material change)",
          "timestamp": "2022-09-23T09:32:19-04:00",
          "tree_id": "db0b6b26616e6629cb8f4795f41eee854218728c",
          "url": "https://github.com/tophat/syrupy/commit/43d78ecc0a2175487db1c9bf5857d6ee34344046"
        },
        "date": 1663940129216,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.591218644327224,
            "unit": "iter/sec",
            "range": "stddev: 0.09951887267854263",
            "extra": "mean: 1.691421624799989 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5656792967488631,
            "unit": "iter/sec",
            "range": "stddev: 0.2522504063790964",
            "extra": "mean: 1.767786103800006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5220711586121666,
            "unit": "iter/sec",
            "range": "stddev: 0.24857965130791945",
            "extra": "mean: 1.9154476999999814 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "54351068868bc88a106ed4c6dac8df6e360aabd9",
          "message": "chore: update github actions (#628)\n\n* chore: update github actions\r\n\r\n* chore: update benchmarks lib",
          "timestamp": "2022-11-03T13:24:55-04:00",
          "tree_id": "1177c638e801a332ebfa73fc4d96aa91fe28d3ce",
          "url": "https://github.com/tophat/syrupy/commit/54351068868bc88a106ed4c6dac8df6e360aabd9"
        },
        "date": 1667496483216,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5755224890240087,
            "unit": "iter/sec",
            "range": "stddev: 0.0899354309245626",
            "extra": "mean: 1.7375515623999944 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5476440364886462,
            "unit": "iter/sec",
            "range": "stddev: 0.24409972504385055",
            "extra": "mean: 1.826003632600009 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.509048242407251,
            "unit": "iter/sec",
            "range": "stddev: 0.24224036865828522",
            "extra": "mean: 1.964450353999996 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "6a766e78d72fd3e74cc7725fead46b7f839b468a",
          "message": "fix: use more expressive glob when building whl (#627)",
          "timestamp": "2022-11-03T13:26:32-04:00",
          "tree_id": "11b351478c20391f68f021ab2aa6bb0c979b72c5",
          "url": "https://github.com/tophat/syrupy/commit/6a766e78d72fd3e74cc7725fead46b7f839b468a"
        },
        "date": 1667496658757,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6708924501291043,
            "unit": "iter/sec",
            "range": "stddev: 0.09433337308793241",
            "extra": "mean: 1.4905518758000085 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6334903287117528,
            "unit": "iter/sec",
            "range": "stddev: 0.23211612472399185",
            "extra": "mean: 1.5785560642000178 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5879955294633928,
            "unit": "iter/sec",
            "range": "stddev: 0.22142337773556642",
            "extra": "mean: 1.700693202400032 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "1eb8e1a59df5a723965612781e41ee70dd3ee8b2",
          "message": "chore: support manual release",
          "timestamp": "2022-11-03T13:35:45-04:00",
          "tree_id": "65472f3ed5d0b007d5f528500b75997f091f97e3",
          "url": "https://github.com/tophat/syrupy/commit/1eb8e1a59df5a723965612781e41ee70dd3ee8b2"
        },
        "date": 1667497101389,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6669596012817182,
            "unit": "iter/sec",
            "range": "stddev: 0.0865580016749817",
            "extra": "mean: 1.4993411866000088 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6298953509274227,
            "unit": "iter/sec",
            "range": "stddev: 0.2400443857885053",
            "extra": "mean: 1.5875652972000125 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5813951035695989,
            "unit": "iter/sec",
            "range": "stddev: 0.24457666896872546",
            "extra": "mean: 1.720000725600005 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f444787e13bab0ddeb291655b051c2bda5dd0f4b",
          "message": "chore: remove broken and outdated flake8-i18n (#630)",
          "timestamp": "2022-11-03T16:09:24-04:00",
          "tree_id": "8d3a26c4e14ca78ac4d13946a74fe6b8dbce3962",
          "url": "https://github.com/tophat/syrupy/commit/f444787e13bab0ddeb291655b051c2bda5dd0f4b"
        },
        "date": 1667506354113,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7711612546899341,
            "unit": "iter/sec",
            "range": "stddev: 0.06665926014198113",
            "extra": "mean: 1.2967456468000023 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7337313469199126,
            "unit": "iter/sec",
            "range": "stddev: 0.17533425630210533",
            "extra": "mean: 1.3628966571999968 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6702402936318492,
            "unit": "iter/sec",
            "range": "stddev: 0.16742175000112403",
            "extra": "mean: 1.4920022109999878 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "48190261f31ee801d60daab046e37d6a910b3efc",
          "message": "fix: update poetry build backend (#631)",
          "timestamp": "2022-11-03T17:13:24-04:00",
          "tree_id": "661393675ade57362a2974e8b0054bc9f8ffa014",
          "url": "https://github.com/tophat/syrupy/commit/48190261f31ee801d60daab046e37d6a910b3efc"
        },
        "date": 1667510115139,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7731687150709737,
            "unit": "iter/sec",
            "range": "stddev: 0.06315633775745262",
            "extra": "mean: 1.293378767799993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7412417590036489,
            "unit": "iter/sec",
            "range": "stddev: 0.1658742045504701",
            "extra": "mean: 1.3490875114000118 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6790983820866824,
            "unit": "iter/sec",
            "range": "stddev: 0.15597016006618394",
            "extra": "mean: 1.4725406898000188 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "57612883+mhwaage@users.noreply.github.com",
            "name": "Magnus Heskestad Waage",
            "username": "mhwaage"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "7f0fe2255e56cafbad86f6e505019b8e507afd00",
          "message": "fix: only instantiate colored objects if color is not disabled (#634)",
          "timestamp": "2022-11-08T13:13:56-05:00",
          "tree_id": "119410f81f3e2dc3d1819003e0d25d49a35c792e",
          "url": "https://github.com/tophat/syrupy/commit/7f0fe2255e56cafbad86f6e505019b8e507afd00"
        },
        "date": 1667931375280,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5633271033576926,
            "unit": "iter/sec",
            "range": "stddev: 0.06506650388290493",
            "extra": "mean: 1.7751675607999915 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5359620889728962,
            "unit": "iter/sec",
            "range": "stddev: 0.26055523471472447",
            "extra": "mean: 1.8658036091999974 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5007340426575037,
            "unit": "iter/sec",
            "range": "stddev: 0.24671916369182198",
            "extra": "mean: 1.9970681335999927 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "darrenburns@users.noreply.github.com",
            "name": "darrenburns",
            "username": "darrenburns"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "aded3ee51646f0fe83b2c55479c63c816fd17fb8",
          "message": "docs: update names of image snapshot extension classes (#635)",
          "timestamp": "2022-11-08T14:02:46-05:00",
          "tree_id": "96577981001e85b88bac82703fd7951e634d2a2e",
          "url": "https://github.com/tophat/syrupy/commit/aded3ee51646f0fe83b2c55479c63c816fd17fb8"
        },
        "date": 1667934307315,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5142446202575975,
            "unit": "iter/sec",
            "range": "stddev: 0.06374579386963966",
            "extra": "mean: 1.944599827799999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.48855129949798093,
            "unit": "iter/sec",
            "range": "stddev: 0.22598445680515478",
            "extra": "mean: 2.046867956400007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4615636634825626,
            "unit": "iter/sec",
            "range": "stddev: 0.2136260609033771",
            "extra": "mean: 2.166548364000016 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "2ce5140d51ba53d2d7573ce92d3cbe4ce4a4d688",
          "message": "docs: rename master branch to main",
          "timestamp": "2022-11-08T18:10:02-05:00",
          "tree_id": "c93da5c435b027f2578a37aa021598b4b7c54766",
          "url": "https://github.com/tophat/syrupy/commit/2ce5140d51ba53d2d7573ce92d3cbe4ce4a4d688"
        },
        "date": 1667949144797,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6580954369002266,
            "unit": "iter/sec",
            "range": "stddev: 0.09250263264844616",
            "extra": "mean: 1.5195364440000048 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6170292596782908,
            "unit": "iter/sec",
            "range": "stddev: 0.2544525859428212",
            "extra": "mean: 1.6206686868000133 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5791811006304881,
            "unit": "iter/sec",
            "range": "stddev: 0.24345627459184319",
            "extra": "mean: 1.7265756753999995 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "committer": {
            "email": "noah.negin-ulster@tophatmonocle.com",
            "name": "Noah Negin-Ulster",
            "username": "noahnu"
          },
          "distinct": true,
          "id": "7338a37ab35a48a346fc85e891daef57f48c4be9",
          "message": "chore: enable renovate",
          "timestamp": "2022-11-08T18:13:24-05:00",
          "tree_id": "e15524c5eac09963fc370a6cba3b8b1f7b071c43",
          "url": "https://github.com/tophat/syrupy/commit/7338a37ab35a48a346fc85e891daef57f48c4be9"
        },
        "date": 1667949321201,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7709457808187364,
            "unit": "iter/sec",
            "range": "stddev: 0.048477423261161674",
            "extra": "mean: 1.2971080779999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7324448561011113,
            "unit": "iter/sec",
            "range": "stddev: 0.1797315355688859",
            "extra": "mean: 1.3652904947999986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6751254128832423,
            "unit": "iter/sec",
            "range": "stddev: 0.17226093415862248",
            "extra": "mean: 1.481206277999999 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d6906dea46fa1ba57803d29c755896ceeace59d8",
          "message": "chore: update cycjimmy/semantic-release-action action to v3.1.2 (#638)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-24T15:46:24-05:00",
          "tree_id": "fd5b7d9ab0c5be4cea6de2bdfcd056e58fc87d17",
          "url": "https://github.com/tophat/syrupy/commit/d6906dea46fa1ba57803d29c755896ceeace59d8"
        },
        "date": 1669322898315,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6503630428091709,
            "unit": "iter/sec",
            "range": "stddev: 0.09295590401749011",
            "extra": "mean: 1.5376027451999903 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6082224473774979,
            "unit": "iter/sec",
            "range": "stddev: 0.2743384634436813",
            "extra": "mean: 1.644135306599992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6195327058812389,
            "unit": "iter/sec",
            "range": "stddev: 0.112121109388099",
            "extra": "mean: 1.614119788200003 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f220a181051a1d2e5ddd12cd6f16690f97256a77",
          "message": "chore: update dependency debugpy to ^1.6.3 (#642)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-28T10:02:12-05:00",
          "tree_id": "1da405fd0a5d1a762a02cac6180df3cb722261e4",
          "url": "https://github.com/tophat/syrupy/commit/f220a181051a1d2e5ddd12cd6f16690f97256a77"
        },
        "date": 1669647854792,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7696472072182828,
            "unit": "iter/sec",
            "range": "stddev: 0.06094270656537945",
            "extra": "mean: 1.2992966006000017 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7399826011590898,
            "unit": "iter/sec",
            "range": "stddev: 0.15850395032926587",
            "extra": "mean: 1.351383125000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7202355966001934,
            "unit": "iter/sec",
            "range": "stddev: 0.0752223025226581",
            "extra": "mean: 1.3884345687999997 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "73c47a41b0021de51ca9f0c1fcc85f322cdcae91",
          "message": "chore: update dependency flake8-comprehensions to ^3.10.1 (#646)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-28T20:19:51-05:00",
          "tree_id": "84366fcd1f226120cbd8cf817e77edb2387bd65f",
          "url": "https://github.com/tophat/syrupy/commit/73c47a41b0021de51ca9f0c1fcc85f322cdcae91"
        },
        "date": 1669684922261,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5884288233733176,
            "unit": "iter/sec",
            "range": "stddev: 0.07778860154127402",
            "extra": "mean: 1.6994408843999964 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5557759027308996,
            "unit": "iter/sec",
            "range": "stddev: 0.24616220137977843",
            "extra": "mean: 1.799286358200004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5503724294388713,
            "unit": "iter/sec",
            "range": "stddev: 0.1005678664957945",
            "extra": "mean: 1.816951479599993 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "noahnu@gmail.com",
            "name": "Noah",
            "username": "noahnu"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "14ab21a3930b78ad43c5eb96bcc0ecb3df516283",
          "message": "chore: change semantic commit type to chore (#648)",
          "timestamp": "2022-11-29T09:22:34-05:00",
          "tree_id": "4c492f2570afef43628edd4f16e927a2dc13b034",
          "url": "https://github.com/tophat/syrupy/commit/14ab21a3930b78ad43c5eb96bcc0ecb3df516283"
        },
        "date": 1669732487325,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.4868036230165678,
            "unit": "iter/sec",
            "range": "stddev: 0.06723656379899748",
            "extra": "mean: 2.0542164288000095 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.4710462758160044,
            "unit": "iter/sec",
            "range": "stddev: 0.2479902322595474",
            "extra": "mean: 2.1229336720000105 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.46062740035125915,
            "unit": "iter/sec",
            "range": "stddev: 0.11862908886411708",
            "extra": "mean: 2.1709520520000183 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ee2a6b53eaac1f5fce865c62758c33ffcbd7e9a2",
          "message": "chore: update dependency invoke to ^1.7.3 (#647)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-29T09:22:50-05:00",
          "tree_id": "a33c503f8a992acc668e137b577b512377bd2a5c",
          "url": "https://github.com/tophat/syrupy/commit/ee2a6b53eaac1f5fce865c62758c33ffcbd7e9a2"
        },
        "date": 1669732512253,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6506949129573444,
            "unit": "iter/sec",
            "range": "stddev: 0.08481020633455286",
            "extra": "mean: 1.5368185305999986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6235858737357954,
            "unit": "iter/sec",
            "range": "stddev: 0.2340310885297924",
            "extra": "mean: 1.6036283728 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6185872508742525,
            "unit": "iter/sec",
            "range": "stddev: 0.09927867349421177",
            "extra": "mean: 1.616586825199994 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "925c15d65053c4e79af96074b7dc55687eb7b96b",
          "message": "chore: update dependency flake8-bugbear to ^21.11.29 (#644)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-29T14:05:20-05:00",
          "tree_id": "03789039b6fe1d8661918b307d05e329f5a4202c",
          "url": "https://github.com/tophat/syrupy/commit/925c15d65053c4e79af96074b7dc55687eb7b96b"
        },
        "date": 1669748832888,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7702034297559945,
            "unit": "iter/sec",
            "range": "stddev: 0.054548089324431344",
            "extra": "mean: 1.2983582795999837 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7408028396637026,
            "unit": "iter/sec",
            "range": "stddev: 0.15676040311451792",
            "extra": "mean: 1.3498868341999923 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7258959499354564,
            "unit": "iter/sec",
            "range": "stddev: 0.06435925345651014",
            "extra": "mean: 1.3776079065999967 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f13541ec0ab7fee6d87f85ad2601dc404317098c",
          "message": "chore: update dependency py-githooks to ^1.1.1 (#649)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-29T14:43:45-05:00",
          "tree_id": "4495262984a8099637bceaf824f512f0b63990ee",
          "url": "https://github.com/tophat/syrupy/commit/f13541ec0ab7fee6d87f85ad2601dc404317098c"
        },
        "date": 1669751144395,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6585464727312003,
            "unit": "iter/sec",
            "range": "stddev: 0.07689429794015488",
            "extra": "mean: 1.5184957195999913 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.627870648306165,
            "unit": "iter/sec",
            "range": "stddev: 0.23556675029902518",
            "extra": "mean: 1.5926847396000199 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6220105460178718,
            "unit": "iter/sec",
            "range": "stddev: 0.0917194414407591",
            "extra": "mean: 1.6076897834000192 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "79723014e02ca4c5a322dd699a266057b31f2e85",
          "message": "chore: update cycjimmy/semantic-release-action action to v3.2.0 (#651)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-29T15:08:58-05:00",
          "tree_id": "71eb63b19a24eed9d0f6908a2b5517208b86bf1e",
          "url": "https://github.com/tophat/syrupy/commit/79723014e02ca4c5a322dd699a266057b31f2e85"
        },
        "date": 1669752699253,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.43521254623876354,
            "unit": "iter/sec",
            "range": "stddev: 0.10842962987757437",
            "extra": "mean: 2.2977278771999976 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.40402013424416267,
            "unit": "iter/sec",
            "range": "stddev: 0.3174959933417652",
            "extra": "mean: 2.4751241714 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4028334270393001,
            "unit": "iter/sec",
            "range": "stddev: 0.10816609132184796",
            "extra": "mean: 2.482415641000023 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3b70c7fa4408613b8e057b6d5bf8db87b2175172",
          "message": "chore: update dependency coverage to ^6.5.0 (#641)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-29T15:09:49-05:00",
          "tree_id": "27d787e437cfc337a163a840e9191b6ccf392d71",
          "url": "https://github.com/tophat/syrupy/commit/3b70c7fa4408613b8e057b6d5bf8db87b2175172"
        },
        "date": 1669752725967,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7745483720945433,
            "unit": "iter/sec",
            "range": "stddev: 0.05541635470530563",
            "extra": "mean: 1.2910749490000057 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7429968188800754,
            "unit": "iter/sec",
            "range": "stddev: 0.1578092005613063",
            "extra": "mean: 1.3459007825999947 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7219449918639627,
            "unit": "iter/sec",
            "range": "stddev: 0.06493203243842256",
            "extra": "mean: 1.385147083600009 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "29139614+renovate[bot]@users.noreply.github.com",
            "name": "renovate[bot]",
            "username": "renovate[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "523720b07ddb3db09919c52c4cc16d71cc5a12fa",
          "message": "chore: update dependency black to ^22.10.0 (#639)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-29T18:59:11-05:00",
          "tree_id": "9577d89b95d7445d953e5335403b63b35f8c3d30",
          "url": "https://github.com/tophat/syrupy/commit/523720b07ddb3db09919c52c4cc16d71cc5a12fa"
        },
        "date": 1669766473085,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.659247435638915,
            "unit": "iter/sec",
            "range": "stddev: 0.08223877892508105",
            "extra": "mean: 1.5168811374000142 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.622193522464764,
            "unit": "iter/sec",
            "range": "stddev: 0.2471156928861965",
            "extra": "mean: 1.6072169894000012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6219535882163693,
            "unit": "iter/sec",
            "range": "stddev: 0.10593092000477092",
            "extra": "mean: 1.6078370137999969 sec\nrounds: 5"
          }
        ]
      }
    ]
  }
}