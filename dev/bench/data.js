window.BENCHMARK_DATA = {
  "lastUpdate": 1682110459287,
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
          "id": "23cca849e606181524a298a11796df1ebe597052",
          "message": "chore: update dependency flake8-builtins to v2 (#656)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2022-11-30T07:30:44-05:00",
          "tree_id": "bae0f6f3aae1a7b9c7cf2f1c0b3aac97f757f72b",
          "url": "https://github.com/tophat/syrupy/commit/23cca849e606181524a298a11796df1ebe597052"
        },
        "date": 1669811566060,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6754078596653935,
            "unit": "iter/sec",
            "range": "stddev: 0.06391877117699159",
            "extra": "mean: 1.4805868567999994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6345993135561808,
            "unit": "iter/sec",
            "range": "stddev: 0.23174880874067105",
            "extra": "mean: 1.5757974814000022 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6315599143065584,
            "unit": "iter/sec",
            "range": "stddev: 0.0923523543680502",
            "extra": "mean: 1.5833810495999927 sec\nrounds: 5"
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
          "id": "a74e57eed8c6b1ed39cf2e286066cc41b058381e",
          "message": "Merge pull request #669 from tophat/xdist_improvements\n\npytest-xdist compatibility improvements",
          "timestamp": "2022-12-30T12:56:36-05:00",
          "tree_id": "5d18b6a68b2f6deceb24f99ec61a6a2bf85f188a",
          "url": "https://github.com/tophat/syrupy/commit/a74e57eed8c6b1ed39cf2e286066cc41b058381e"
        },
        "date": 1672423107152,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6613239119922573,
            "unit": "iter/sec",
            "range": "stddev: 0.06946618661061309",
            "extra": "mean: 1.512118315800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6270476940824629,
            "unit": "iter/sec",
            "range": "stddev: 0.20891100295390286",
            "extra": "mean: 1.594775021800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6195362479531112,
            "unit": "iter/sec",
            "range": "stddev: 0.07838133500038841",
            "extra": "mean: 1.6141105598000194 sec\nrounds: 5"
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
          "id": "4a9695d341456193b644c92ee068ed6b8950ded9",
          "message": "Merge pull request #670 from tophat/dev_3_11\n\nchore: update local dev to python 3.11",
          "timestamp": "2022-12-30T13:16:12-05:00",
          "tree_id": "40f4f5635d2737b338ade6ac04696ca4c0450046",
          "url": "https://github.com/tophat/syrupy/commit/4a9695d341456193b644c92ee068ed6b8950ded9"
        },
        "date": 1672424285096,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7296203604304284,
            "unit": "iter/sec",
            "range": "stddev: 0.06998880932094288",
            "extra": "mean: 1.3705757873999915 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7493454158687369,
            "unit": "iter/sec",
            "range": "stddev: 0.0681236333409167",
            "extra": "mean: 1.3344980550000058 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6334887477951046,
            "unit": "iter/sec",
            "range": "stddev: 0.26213611433462386",
            "extra": "mean: 1.5785600036000005 sec\nrounds: 5"
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
          "id": "02abef59992487d669aa29f0bef93cbeb114d68a",
          "message": "chore: remove ABC from SnapshotComparator (#671)",
          "timestamp": "2022-12-30T13:26:40-05:00",
          "tree_id": "852ff70dc0c8b6b78d8f007410a8a55eecdffd89",
          "url": "https://github.com/tophat/syrupy/commit/02abef59992487d669aa29f0bef93cbeb114d68a"
        },
        "date": 1672424900354,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8381195242511715,
            "unit": "iter/sec",
            "range": "stddev: 0.04240394140227035",
            "extra": "mean: 1.1931472433999943 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8626650008455868,
            "unit": "iter/sec",
            "range": "stddev: 0.05153168408309042",
            "extra": "mean: 1.159198529000014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7465173870618954,
            "unit": "iter/sec",
            "range": "stddev: 0.1502009356924296",
            "extra": "mean: 1.3395535285999813 sec\nrounds: 5"
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
          "id": "5eee3d845cd3d3c4a47ea981911e5d4f8ebe83e0",
          "message": "Merge pull request #605 from tophat/next\n\nGraduate Syrupy v4 pre-release.",
          "timestamp": "2023-02-02T15:08:58-05:00",
          "tree_id": "7a2283ec8bf2a68aa3a821130aef5d0993da31d3",
          "url": "https://github.com/tophat/syrupy/commit/5eee3d845cd3d3c4a47ea981911e5d4f8ebe83e0"
        },
        "date": 1675368678568,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5308695012724054,
            "unit": "iter/sec",
            "range": "stddev: 0.08240487393124026",
            "extra": "mean: 1.883702110600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5160934616849223,
            "unit": "iter/sec",
            "range": "stddev: 0.07159902297368662",
            "extra": "mean: 1.9376335377999907 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4835373874179867,
            "unit": "iter/sec",
            "range": "stddev: 0.21397077226596534",
            "extra": "mean: 2.068092408199999 sec\nrounds: 5"
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
          "id": "4b9b7d16512ded762f3c94ef8f075bc9adebfc7c",
          "message": "chore: update dependency flake8-bugbear to ^22.12.6 (#686)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-02T18:36:26-05:00",
          "tree_id": "e24b6774cadde0dc1b9017ca1714ef4928de7b59",
          "url": "https://github.com/tophat/syrupy/commit/4b9b7d16512ded762f3c94ef8f075bc9adebfc7c"
        },
        "date": 1675381082893,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8685318578232368,
            "unit": "iter/sec",
            "range": "stddev: 0.03719902244972196",
            "extra": "mean: 1.1513682440000026 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8629443042309985,
            "unit": "iter/sec",
            "range": "stddev: 0.038943126152893054",
            "extra": "mean: 1.1588233390000027 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7818423779036421,
            "unit": "iter/sec",
            "range": "stddev: 0.12486732726109595",
            "extra": "mean: 1.2790301834000162 sec\nrounds: 5"
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
          "id": "6f63c360b2e6a11c17fbb1c4b19bf03fbcb2e689",
          "message": "chore: update dependency twine to ^4.0.2 (#663)",
          "timestamp": "2023-02-02T18:40:21-05:00",
          "tree_id": "f1bb701515c2dbcf67cd78768dc481076bab71b1",
          "url": "https://github.com/tophat/syrupy/commit/6f63c360b2e6a11c17fbb1c4b19bf03fbcb2e689"
        },
        "date": 1675381355676,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5538915285924507,
            "unit": "iter/sec",
            "range": "stddev: 0.08196607951684563",
            "extra": "mean: 1.805407644600018 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5362515253596856,
            "unit": "iter/sec",
            "range": "stddev: 0.08322507773834141",
            "extra": "mean: 1.8647965604000092 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4855304033426754,
            "unit": "iter/sec",
            "range": "stddev: 0.20233347526330112",
            "extra": "mean: 2.059603256800017 sec\nrounds: 5"
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
          "id": "69932cca66e5fe68ffd9c2548d57d221b586e9ea",
          "message": "chore: update dependency debugpy to ^1.6.5 (#662)",
          "timestamp": "2023-02-02T18:40:52-05:00",
          "tree_id": "b68acc66da93a7bace2ea74fd8785b608e4df6de",
          "url": "https://github.com/tophat/syrupy/commit/69932cca66e5fe68ffd9c2548d57d221b586e9ea"
        },
        "date": 1675381449079,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5696770729649375,
            "unit": "iter/sec",
            "range": "stddev: 0.05842421087382475",
            "extra": "mean: 1.7553804557999968 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5611161658219701,
            "unit": "iter/sec",
            "range": "stddev: 0.07026033154176464",
            "extra": "mean: 1.7821621634000082 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5116724442837831,
            "unit": "iter/sec",
            "range": "stddev: 0.1789742797799624",
            "extra": "mean: 1.954375325799998 sec\nrounds: 5"
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
          "id": "b7c9f4ad0c89b0f048924396ae5d35f01e002e25",
          "message": "chore: update dependency black to ^22.12.0 (#674)",
          "timestamp": "2023-02-02T18:41:21-05:00",
          "tree_id": "c557e30b247adcb07fc8aa56ab48836e26d2b46e",
          "url": "https://github.com/tophat/syrupy/commit/b7c9f4ad0c89b0f048924396ae5d35f01e002e25"
        },
        "date": 1675381554755,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8218555291330201,
            "unit": "iter/sec",
            "range": "stddev: 0.04870635481045464",
            "extra": "mean: 1.216758863999985 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8294772444505106,
            "unit": "iter/sec",
            "range": "stddev: 0.045070389067531164",
            "extra": "mean: 1.2055785817999776 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7323042026181422,
            "unit": "iter/sec",
            "range": "stddev: 0.17119781242605997",
            "extra": "mean: 1.3655527258000006 sec\nrounds: 5"
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
          "id": "86692042fd4ed2cfe84bbebe2ea654981b84b037",
          "message": "chore: update actions/setup-python action to v4.5.0 (#692)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-02T20:19:12-05:00",
          "tree_id": "b7f90a68bc722618c4532160ce9960a66ff3d1d3",
          "url": "https://github.com/tophat/syrupy/commit/86692042fd4ed2cfe84bbebe2ea654981b84b037"
        },
        "date": 1675387265323,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6858977287247615,
            "unit": "iter/sec",
            "range": "stddev: 0.05248115035745914",
            "extra": "mean: 1.457943302800004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6779626102104527,
            "unit": "iter/sec",
            "range": "stddev: 0.06071003652517057",
            "extra": "mean: 1.475007596200004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6103556743541225,
            "unit": "iter/sec",
            "range": "stddev: 0.1930274523875393",
            "extra": "mean: 1.6383889623999948 sec\nrounds: 5"
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
          "id": "06c759610287b6f665ef5b4249e7c744953ee1e6",
          "message": "chore: update actions/checkout action to v3.3.0 (#691)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-02T20:19:42-05:00",
          "tree_id": "cc5390d9af42de611ce7883ec5f61ab47a0d1d35",
          "url": "https://github.com/tophat/syrupy/commit/06c759610287b6f665ef5b4249e7c744953ee1e6"
        },
        "date": 1675387277388,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8618203732819798,
            "unit": "iter/sec",
            "range": "stddev: 0.043550510061149295",
            "extra": "mean: 1.1603346021999983 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8515895833669757,
            "unit": "iter/sec",
            "range": "stddev: 0.0416117915615079",
            "extra": "mean: 1.1742745796000065 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7668394543628501,
            "unit": "iter/sec",
            "range": "stddev: 0.140870622544487",
            "extra": "mean: 1.3040539246000038 sec\nrounds: 5"
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
          "id": "6dd1c35431cc9d173100349c774b2ec8052d4e60",
          "message": "chore: update dependency flake8-builtins to ^2.1.0 (#688)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>\nCo-authored-by: Noah <noahnu@gmail.com>",
          "timestamp": "2023-02-02T20:20:24-05:00",
          "tree_id": "eb0f63307bba853be8620132ef482479232c6ffd",
          "url": "https://github.com/tophat/syrupy/commit/6dd1c35431cc9d173100349c774b2ec8052d4e60"
        },
        "date": 1675387446158,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.761263102660694,
            "unit": "iter/sec",
            "range": "stddev: 0.05633219376539964",
            "extra": "mean: 1.3136062899999956 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7472385817639099,
            "unit": "iter/sec",
            "range": "stddev: 0.0597657298701964",
            "extra": "mean: 1.3382606632000034 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6656625004064892,
            "unit": "iter/sec",
            "range": "stddev: 0.19186805010774044",
            "extra": "mean: 1.5022627824000097 sec\nrounds: 5"
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
          "id": "f114adf54615c4bfcece23a3a65a7cb870ec620b",
          "message": "chore: update dependency isort to ^5.11.4 (#689)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-02T21:56:14-05:00",
          "tree_id": "6667afb073d976150526bda5753d9ad42f9fdeaa",
          "url": "https://github.com/tophat/syrupy/commit/f114adf54615c4bfcece23a3a65a7cb870ec620b"
        },
        "date": 1675393078303,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7999329867339503,
            "unit": "iter/sec",
            "range": "stddev: 0.029776992072672835",
            "extra": "mean: 1.250104716999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8383118892227122,
            "unit": "iter/sec",
            "range": "stddev: 0.06067948017435051",
            "extra": "mean: 1.1928734554000016 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6801415414703391,
            "unit": "iter/sec",
            "range": "stddev: 0.19559065490965166",
            "extra": "mean: 1.4702821971999924 sec\nrounds: 5"
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
          "id": "4133faee759d343687c530e35df32a90658e9020",
          "message": "chore: update dependency setuptools-scm to ^7.1.0 (#690)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-03T07:48:17-05:00",
          "tree_id": "55dcffb7a2773df428d17bb5e546e97e643fdc2f",
          "url": "https://github.com/tophat/syrupy/commit/4133faee759d343687c530e35df32a90658e9020"
        },
        "date": 1675428603735,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8493779941754908,
            "unit": "iter/sec",
            "range": "stddev: 0.04885672713161211",
            "extra": "mean: 1.1773321264000032 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8382803990026247,
            "unit": "iter/sec",
            "range": "stddev: 0.043533747225891824",
            "extra": "mean: 1.1929182660000008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7580929583413449,
            "unit": "iter/sec",
            "range": "stddev: 0.1406063995532564",
            "extra": "mean: 1.3190994441999977 sec\nrounds: 5"
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
          "id": "ebfd090461d13d53e6f80c81dab3e570e5d4597b",
          "message": "chore: update dependency coverage to v7 (#693)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-03T15:26:05-05:00",
          "tree_id": "efd8f83a9cba3ab96f5c7776fa8f527a1a5a07f5",
          "url": "https://github.com/tophat/syrupy/commit/ebfd090461d13d53e6f80c81dab3e570e5d4597b"
        },
        "date": 1675456095544,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6055942842944636,
            "unit": "iter/sec",
            "range": "stddev: 0.07813443536135091",
            "extra": "mean: 1.6512705385999993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.576950223363084,
            "unit": "iter/sec",
            "range": "stddev: 0.10942954223542899",
            "extra": "mean: 1.733251777199996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5460622857733486,
            "unit": "iter/sec",
            "range": "stddev: 0.1827628608131666",
            "extra": "mean: 1.8312929240000018 sec\nrounds: 5"
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
          "id": "c0568c28158789eef76d14fc9968218cc49fa08f",
          "message": "chore: update dev dependencies (#698)",
          "timestamp": "2023-02-03T15:47:17-05:00",
          "tree_id": "db052abbb25ba40c98db8506dacbcda2e9f88716",
          "url": "https://github.com/tophat/syrupy/commit/c0568c28158789eef76d14fc9968218cc49fa08f"
        },
        "date": 1675457331373,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8721822446597747,
            "unit": "iter/sec",
            "range": "stddev: 0.039573595913622674",
            "extra": "mean: 1.1465493664000064 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8653525900831389,
            "unit": "iter/sec",
            "range": "stddev: 0.034032946071262477",
            "extra": "mean: 1.155598320799993 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7871895291257989,
            "unit": "iter/sec",
            "range": "stddev: 0.12050103403575309",
            "extra": "mean: 1.27034210060001 sec\nrounds: 5"
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
          "id": "f1934ea4470fe487aa2ccd3c081edfeb2955723d",
          "message": "chore: add deps label to renovate PRs, change range strategy (#705)",
          "timestamp": "2023-02-09T14:09:45-05:00",
          "tree_id": "f4c418bbc87ea7fc2bd6a798f78df38547ce34c2",
          "url": "https://github.com/tophat/syrupy/commit/f1934ea4470fe487aa2ccd3c081edfeb2955723d"
        },
        "date": 1675969887060,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8551507047556702,
            "unit": "iter/sec",
            "range": "stddev: 0.041231405351750613",
            "extra": "mean: 1.1693845241999952 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8483173278585645,
            "unit": "iter/sec",
            "range": "stddev: 0.03640567423487899",
            "extra": "mean: 1.1788041657999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7658983404846162,
            "unit": "iter/sec",
            "range": "stddev: 0.1292373300171719",
            "extra": "mean: 1.3056563085999868 sec\nrounds: 5"
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
          "id": "967cab8a1ea22377983280e47d9b7d36438fe01a",
          "message": "chore: update dependency invoke to v2 (#701)\n\n* chore: update dependency invoke to v2\r\n\r\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>\r\nCo-authored-by: Noah Negin-Ulster <noah.negin-ulster@tophatmonocle.com>",
          "timestamp": "2023-02-09T19:19:52Z",
          "tree_id": "c6013b3b25078044a204d22f86a7b6c5f9d50f2c",
          "url": "https://github.com/tophat/syrupy/commit/967cab8a1ea22377983280e47d9b7d36438fe01a"
        },
        "date": 1675970495706,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8498359286869936,
            "unit": "iter/sec",
            "range": "stddev: 0.0478411700008997",
            "extra": "mean: 1.176697720399997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8436281630994096,
            "unit": "iter/sec",
            "range": "stddev: 0.04094433094491234",
            "extra": "mean: 1.1853563498000057 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7604871007305798,
            "unit": "iter/sec",
            "range": "stddev: 0.1507718255254209",
            "extra": "mean: 1.3149466953999962 sec\nrounds: 5"
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
          "id": "c4fd0d6e76ee814b6235cdd8ecee237f7969994f",
          "message": "chore: update python docker tag to v3.11.2 (#704)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-09T14:20:24-05:00",
          "tree_id": "fad772ebe1c1bd21e54698a3267c862e09aedd16",
          "url": "https://github.com/tophat/syrupy/commit/c4fd0d6e76ee814b6235cdd8ecee237f7969994f"
        },
        "date": 1675970587455,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8462592162063106,
            "unit": "iter/sec",
            "range": "stddev: 0.041383846926841245",
            "extra": "mean: 1.181671030399991 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8377196625272739,
            "unit": "iter/sec",
            "range": "stddev: 0.04402313401257273",
            "extra": "mean: 1.1937167584000008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7545708024870992,
            "unit": "iter/sec",
            "range": "stddev: 0.14731249680226643",
            "extra": "mean: 1.325256684599981 sec\nrounds: 5"
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
          "id": "3166746ad465f850d6a11465f4cc2d8c1f68a168",
          "message": "Revert \"chore: update python docker tag to v3.11.2 (#704)\"\n\nThis reverts commit c4fd0d6e76ee814b6235cdd8ecee237f7969994f.",
          "timestamp": "2023-02-09T14:27:18-05:00",
          "tree_id": "c6013b3b25078044a204d22f86a7b6c5f9d50f2c",
          "url": "https://github.com/tophat/syrupy/commit/3166746ad465f850d6a11465f4cc2d8c1f68a168"
        },
        "date": 1675970980507,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5368180846949078,
            "unit": "iter/sec",
            "range": "stddev: 0.044798011259726066",
            "extra": "mean: 1.8628284487999962 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5442585476666452,
            "unit": "iter/sec",
            "range": "stddev: 0.08050144610613397",
            "extra": "mean: 1.837362048400007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4870095904373355,
            "unit": "iter/sec",
            "range": "stddev: 0.23014109374718014",
            "extra": "mean: 2.0533476539999924 sec\nrounds: 5"
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
          "id": "03cc361858d2ae74297572300259e71f6847a1c8",
          "message": "chore: consistency with dependabot (#708)",
          "timestamp": "2023-02-09T14:30:57-05:00",
          "tree_id": "0f206fb07210f39487ec675d42f857447f5c79bb",
          "url": "https://github.com/tophat/syrupy/commit/03cc361858d2ae74297572300259e71f6847a1c8"
        },
        "date": 1675971191677,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5503772735546203,
            "unit": "iter/sec",
            "range": "stddev: 0.06110293979727681",
            "extra": "mean: 1.8169354878000035 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5436381906570457,
            "unit": "iter/sec",
            "range": "stddev: 0.09537139896031895",
            "extra": "mean: 1.839458701000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4978705125750861,
            "unit": "iter/sec",
            "range": "stddev: 0.22524260393547457",
            "extra": "mean: 2.0085543826000047 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "266da13ff22a600c84b9ce2c6b140bdddcec9f47",
          "message": "chore(deps): bump cryptography from 39.0.0 to 39.0.1 (#702)\n\n* chore(deps): bump cryptography from 39.0.0 to 39.0.1\r\n\r\nBumps [cryptography](https://github.com/pyca/cryptography) from 39.0.0 to 39.0.1.\r\n- [Release notes](https://github.com/pyca/cryptography/releases)\r\n- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)\r\n- [Commits](https://github.com/pyca/cryptography/compare/39.0.0...39.0.1)\r\n\r\n---\r\nupdated-dependencies:\r\n- dependency-name: cryptography\r\n  dependency-type: indirect\r\n...\r\n\r\nSigned-off-by: dependabot[bot] <support@github.com>\r\n\r\n* chore(deps): update lock file\r\n\r\n---------\r\n\r\nSigned-off-by: dependabot[bot] <support@github.com>\r\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>\r\nCo-authored-by: Noah Negin-Ulster <noah.negin-ulster@tophatmonocle.com>",
          "timestamp": "2023-02-09T14:40:46-05:00",
          "tree_id": "9f1121f95b3554588cc8d50ce842c31e783aee78",
          "url": "https://github.com/tophat/syrupy/commit/266da13ff22a600c84b9ce2c6b140bdddcec9f47"
        },
        "date": 1675971756338,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7669822697311539,
            "unit": "iter/sec",
            "range": "stddev: 0.05802613690011905",
            "extra": "mean: 1.3038111042000025 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7660710393397627,
            "unit": "iter/sec",
            "range": "stddev: 0.05951735207537321",
            "extra": "mean: 1.305361968599999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6824267091593954,
            "unit": "iter/sec",
            "range": "stddev: 0.1876703598787301",
            "extra": "mean: 1.4653588239999977 sec\nrounds: 5"
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
          "id": "b831ee21b54f0b0dd287a7a0c6e138d6b553f26b",
          "message": "chore(deps): update dependency mypy to v1 (#706)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-02-09T16:19:51-05:00",
          "tree_id": "b6998866492f13a04fbe5c491262c4baf962beb7",
          "url": "https://github.com/tophat/syrupy/commit/b831ee21b54f0b0dd287a7a0c6e138d6b553f26b"
        },
        "date": 1675977731575,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5422523489597115,
            "unit": "iter/sec",
            "range": "stddev: 0.07107393517809005",
            "extra": "mean: 1.8441598306000118 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5442580110397968,
            "unit": "iter/sec",
            "range": "stddev: 0.07305733591449298",
            "extra": "mean: 1.8373638599999935 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4950789059711019,
            "unit": "iter/sec",
            "range": "stddev: 0.207632681483958",
            "extra": "mean: 2.0198800391999954 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "794719+tolgaeren@users.noreply.github.com",
            "name": "Tolga Eren",
            "username": "tolgaeren"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "efe687e263647b1efa2673847372389ea90961eb",
          "message": "fix(serializer): handling of multi-part file extensions in SingleFileExtension (#710)\n\nCo-authored-by: tolga.eren <tolga.eren@adevinta.com>\r\nCo-authored-by: noahnu <noahnu@gmail.com>",
          "timestamp": "2023-02-20T18:57:14-05:00",
          "tree_id": "5d2337b5c1fd6a3cf8c2219d3861ec5474081aae",
          "url": "https://github.com/tophat/syrupy/commit/efe687e263647b1efa2673847372389ea90961eb"
        },
        "date": 1676937575879,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5673304534145591,
            "unit": "iter/sec",
            "range": "stddev: 0.03897020002283442",
            "extra": "mean: 1.7626411449999864 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5639545547386794,
            "unit": "iter/sec",
            "range": "stddev: 0.07884229350116835",
            "extra": "mean: 1.773192523399996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5052809751869447,
            "unit": "iter/sec",
            "range": "stddev: 0.18403436484223545",
            "extra": "mean: 1.9790968770000064 sec\nrounds: 5"
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
          "id": "5e8f86d17726e16ba684bf25c8dc68aac7871ea4",
          "message": "chore: update dev dependencies (#713)",
          "timestamp": "2023-02-20T19:19:34-05:00",
          "tree_id": "71f5907f640f29846308198b22573f60472645f0",
          "url": "https://github.com/tophat/syrupy/commit/5e8f86d17726e16ba684bf25c8dc68aac7871ea4"
        },
        "date": 1676938892995,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7550932781345063,
            "unit": "iter/sec",
            "range": "stddev: 0.06870802080626849",
            "extra": "mean: 1.3243396928000037 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.74933598258812,
            "unit": "iter/sec",
            "range": "stddev: 0.06161751693193264",
            "extra": "mean: 1.3345148547999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6622649532076629,
            "unit": "iter/sec",
            "range": "stddev: 0.22030250069084037",
            "extra": "mean: 1.5099696807999976 sec\nrounds: 5"
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
          "id": "ef135ba4a1e26f1319de7b58907b93dc36fbef3c",
          "message": "chore(deps): update dependency mypy to v1.1.1 (#721)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-14T14:24:03-04:00",
          "tree_id": "d929fbbbc77fec98dcc6febfda67bc411ba2856e",
          "url": "https://github.com/tophat/syrupy/commit/ef135ba4a1e26f1319de7b58907b93dc36fbef3c"
        },
        "date": 1678818357975,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.842900100562369,
            "unit": "iter/sec",
            "range": "stddev: 0.03755820379334626",
            "extra": "mean: 1.1863802119999947 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8383664096235052,
            "unit": "iter/sec",
            "range": "stddev: 0.047100836443841804",
            "extra": "mean: 1.1927958807999972 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7496321818004764,
            "unit": "iter/sec",
            "range": "stddev: 0.14813446991083945",
            "extra": "mean: 1.3339875532000065 sec\nrounds: 5"
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
          "id": "4cae64a7c82903a62e30fb5c71ca5857314e7012",
          "message": "chore(deps): update cycjimmy/semantic-release-action action to v3.3.0 (#720)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-14T14:24:32-04:00",
          "tree_id": "007855a878e0b244cd354bc9e971f392e0321f38",
          "url": "https://github.com/tophat/syrupy/commit/4cae64a7c82903a62e30fb5c71ca5857314e7012"
        },
        "date": 1678818382873,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7684967311836257,
            "unit": "iter/sec",
            "range": "stddev: 0.061905503248241615",
            "extra": "mean: 1.3012417092000077 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7659080753571008,
            "unit": "iter/sec",
            "range": "stddev: 0.04932307262877105",
            "extra": "mean: 1.3056397134000122 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6845406428630921,
            "unit": "iter/sec",
            "range": "stddev: 0.17650348410446542",
            "extra": "mean: 1.4608336414000178 sec\nrounds: 5"
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
          "id": "e8a1fa7c38bace49d85803f31963cff0225f99c4",
          "message": "chore(deps): update dependency pytest-xdist to v3.2.1 (#722)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-21T07:37:01-04:00",
          "tree_id": "79c1432407006230debbc6ea1c39ca97b5e9fddd",
          "url": "https://github.com/tophat/syrupy/commit/e8a1fa7c38bace49d85803f31963cff0225f99c4"
        },
        "date": 1679398763779,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5554645971785553,
            "unit": "iter/sec",
            "range": "stddev: 0.07304830245344164",
            "extra": "mean: 1.8002947534000042 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5478273157427168,
            "unit": "iter/sec",
            "range": "stddev: 0.07277764200335438",
            "extra": "mean: 1.825392731000005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5018327853682971,
            "unit": "iter/sec",
            "range": "stddev: 0.23685996414956448",
            "extra": "mean: 1.9926956332000032 sec\nrounds: 5"
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
          "id": "836043e98c231061021d85edc721ef004015a455",
          "message": "chore(deps): update actions/checkout action to v3.4.0 (#725)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-22T18:07:39-04:00",
          "tree_id": "01a2f4d513b332b519681d6c7453a0f811c2d48a",
          "url": "https://github.com/tophat/syrupy/commit/836043e98c231061021d85edc721ef004015a455"
        },
        "date": 1679522965362,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8148376583117384,
            "unit": "iter/sec",
            "range": "stddev: 0.04499699718283312",
            "extra": "mean: 1.2272383213999944 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8170383952899005,
            "unit": "iter/sec",
            "range": "stddev: 0.05027004798204536",
            "extra": "mean: 1.2239326887999937 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7267233221156959,
            "unit": "iter/sec",
            "range": "stddev: 0.18068966622972768",
            "extra": "mean: 1.376039504399995 sec\nrounds: 5"
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
          "id": "265fc5f93e5be2aa406dc44e2ea8db8bcf86f9f6",
          "message": "chore(deps): update dependency pytest to v7.2.2 (#718)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-24T11:04:05-04:00",
          "tree_id": "28927520f5d13b60dd39abbf20b81883e70682fb",
          "url": "https://github.com/tophat/syrupy/commit/265fc5f93e5be2aa406dc44e2ea8db8bcf86f9f6"
        },
        "date": 1679670356270,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7776514466067239,
            "unit": "iter/sec",
            "range": "stddev: 0.05249237039436248",
            "extra": "mean: 1.285923152800001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7808564405453985,
            "unit": "iter/sec",
            "range": "stddev: 0.05362673032040278",
            "extra": "mean: 1.2806451328000037 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6894013976735608,
            "unit": "iter/sec",
            "range": "stddev: 0.18972903912063885",
            "extra": "mean: 1.4505337577999966 sec\nrounds: 5"
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
          "id": "ffef974aec669cf6a19e68208c54ea0094834438",
          "message": "chore(deps): update cycjimmy/semantic-release-action action to v3.4.0 (#724)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-24T11:03:42-04:00",
          "tree_id": "a08b676cd6d1fb02a4cdb1116db587795b8cf627",
          "url": "https://github.com/tophat/syrupy/commit/ffef974aec669cf6a19e68208c54ea0094834438"
        },
        "date": 1679670362976,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5693588594455413,
            "unit": "iter/sec",
            "range": "stddev: 0.05495942555334164",
            "extra": "mean: 1.7563615343999914 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5697458452414049,
            "unit": "iter/sec",
            "range": "stddev: 0.055264611751760825",
            "extra": "mean: 1.7551685691999979 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.514851297082002,
            "unit": "iter/sec",
            "range": "stddev: 0.20342481628996337",
            "extra": "mean: 1.9423084017999996 sec\nrounds: 5"
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
          "id": "493e70f2229789dc0c4255389acd0764f917e127",
          "message": "chore(deps): update dependency coverage to v7.2.2 (#716)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-24T12:53:35-04:00",
          "tree_id": "e18332d85c7d59a70c4710f92d83974bbab7f296",
          "url": "https://github.com/tophat/syrupy/commit/493e70f2229789dc0c4255389acd0764f917e127"
        },
        "date": 1679676924950,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7699385074859887,
            "unit": "iter/sec",
            "range": "stddev: 0.06924559222778465",
            "extra": "mean: 1.2988050218000011 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7735120847195411,
            "unit": "iter/sec",
            "range": "stddev: 0.06419010196667062",
            "extra": "mean: 1.2928046241999938 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6790741462888331,
            "unit": "iter/sec",
            "range": "stddev: 0.2120857961070597",
            "extra": "mean: 1.4725932439999951 sec\nrounds: 5"
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
          "id": "68c17bc9a4244fcc9c7ffd72ec253c182738e371",
          "message": "chore(deps): update dependency flake8-comprehensions to v3.11.0 (#726)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-25T08:14:11-04:00",
          "tree_id": "988a02383791b17b22549f55784351fb46399fc3",
          "url": "https://github.com/tophat/syrupy/commit/68c17bc9a4244fcc9c7ffd72ec253c182738e371"
        },
        "date": 1679746557122,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8606676549325574,
            "unit": "iter/sec",
            "range": "stddev: 0.04012733238788097",
            "extra": "mean: 1.1618886735999865 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8514134626169724,
            "unit": "iter/sec",
            "range": "stddev: 0.03388448249085389",
            "extra": "mean: 1.174517486399992 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7608862496002571,
            "unit": "iter/sec",
            "range": "stddev: 0.13842072140831677",
            "extra": "mean: 1.314256895199992 sec\nrounds: 5"
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
          "id": "8e30c2bf111c81485358c82a5aeaec472e437c57",
          "message": "chore(deps): update dependencies (#727)",
          "timestamp": "2023-03-29T13:16:58-04:00",
          "tree_id": "44dd500eb06d2bca277fb186782ed5e1b9c278d9",
          "url": "https://github.com/tophat/syrupy/commit/8e30c2bf111c81485358c82a5aeaec472e437c57"
        },
        "date": 1680110538986,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.597198281646268,
            "unit": "iter/sec",
            "range": "stddev: 0.07358015365881923",
            "extra": "mean: 1.6744857290000028 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5935189995342299,
            "unit": "iter/sec",
            "range": "stddev: 0.06860342461300059",
            "extra": "mean: 1.684866029200009 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5376839525360029,
            "unit": "iter/sec",
            "range": "stddev: 0.2139083982070716",
            "extra": "mean: 1.8598286135999955 sec\nrounds: 5"
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
          "id": "650d5a8427f0cad4063d5649e6c8cd4aa3bb572c",
          "message": "chore(deps): update actions/checkout action to v3.5.0 (#728)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-03-30T08:53:14-04:00",
          "tree_id": "7ed782251b1de091fa05eaf70da960f2bcb23e34",
          "url": "https://github.com/tophat/syrupy/commit/650d5a8427f0cad4063d5649e6c8cd4aa3bb572c"
        },
        "date": 1680180988192,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5774985577897503,
            "unit": "iter/sec",
            "range": "stddev: 0.054079483531598464",
            "extra": "mean: 1.731606056000004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5695561703595191,
            "unit": "iter/sec",
            "range": "stddev: 0.0591028262135273",
            "extra": "mean: 1.7557530794000058 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5182469907391999,
            "unit": "iter/sec",
            "range": "stddev: 0.2167004402622668",
            "extra": "mean: 1.929581874799993 sec\nrounds: 5"
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
          "id": "c51afa9d831282d9151e7ce1e9d8d0844cf51092",
          "message": "chore: remove codecov package (#735)",
          "timestamp": "2023-04-12T13:10:31-04:00",
          "tree_id": "72d6354d96fdeb2c172f83dc853649a98aeb8494",
          "url": "https://github.com/tophat/syrupy/commit/c51afa9d831282d9151e7ce1e9d8d0844cf51092"
        },
        "date": 1681319542078,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7682827293818367,
            "unit": "iter/sec",
            "range": "stddev: 0.056987957075827746",
            "extra": "mean: 1.301604164400004 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7527335943515198,
            "unit": "iter/sec",
            "range": "stddev: 0.057284532748958",
            "extra": "mean: 1.3284912583999926 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7119076455788897,
            "unit": "iter/sec",
            "range": "stddev: 0.07115046844919795",
            "extra": "mean: 1.4046765843999993 sec\nrounds: 5"
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
          "id": "c6bb72e075efdceab9f86c8dc4cabc37f0587cfb",
          "message": "chore(deps): update cycjimmy/semantic-release-action action to v3.4.2 (#729)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-04-14T17:31:13-04:00",
          "tree_id": "6a98cacbd03ac35246ab7c41451db311b3867d8d",
          "url": "https://github.com/tophat/syrupy/commit/c6bb72e075efdceab9f86c8dc4cabc37f0587cfb"
        },
        "date": 1681507982929,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.751196764016454,
            "unit": "iter/sec",
            "range": "stddev: 0.05813822418371182",
            "extra": "mean: 1.3312091424000017 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7355617726750191,
            "unit": "iter/sec",
            "range": "stddev: 0.06097854870573387",
            "extra": "mean: 1.3595051254000026 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7004355984471496,
            "unit": "iter/sec",
            "range": "stddev: 0.0705833285085385",
            "extra": "mean: 1.427683005 sec\nrounds: 5"
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
          "id": "21165d8b97e22a526fdb5d6da5cf718d33dda3c7",
          "message": "chore(deps): update actions/checkout action to v3.5.2 (#737)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-04-21T16:52:16-04:00",
          "tree_id": "d2c4109930c392f05050850e2c4a8310cceb94f0",
          "url": "https://github.com/tophat/syrupy/commit/21165d8b97e22a526fdb5d6da5cf718d33dda3c7"
        },
        "date": 1682110457755,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6587344224033427,
            "unit": "iter/sec",
            "range": "stddev: 0.04989500734346245",
            "extra": "mean: 1.5180624634000082 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6560832619500758,
            "unit": "iter/sec",
            "range": "stddev: 0.08020420911916856",
            "extra": "mean: 1.5241967871999975 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6258137513314044,
            "unit": "iter/sec",
            "range": "stddev: 0.07624078560169513",
            "extra": "mean: 1.597919505400006 sec\nrounds: 5"
          }
        ]
      }
    ]
  }
}