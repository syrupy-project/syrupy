window.BENCHMARK_DATA = {
  "lastUpdate": 1694138291447,
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
          "id": "028cb8f0c100f6be118d5aacf80974e7503980e2",
          "message": "chore(deps): update dependency pytest to v7.3.1 (#739)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-04-21T17:13:50-04:00",
          "tree_id": "93ec22c65021617c7bd8dab6757e97a0cfc5d2f6",
          "url": "https://github.com/tophat/syrupy/commit/028cb8f0c100f6be118d5aacf80974e7503980e2"
        },
        "date": 1682111757440,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6397303546176843,
            "unit": "iter/sec",
            "range": "stddev: 0.060632584140582875",
            "extra": "mean: 1.563158591399997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6363763943681665,
            "unit": "iter/sec",
            "range": "stddev: 0.08780662122151904",
            "extra": "mean: 1.571397067600003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6007326832085811,
            "unit": "iter/sec",
            "range": "stddev: 0.0643389195667781",
            "extra": "mean: 1.6646339177999891 sec\nrounds: 5"
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
          "id": "3152c56fc6fe98618b8f2c08b2f1238e6930c92b",
          "message": "chore(deps): update dependency semver to v3 (#730)\n\n* chore(deps): update dependency semver to v3",
          "timestamp": "2023-04-25T10:47:16-04:00",
          "tree_id": "eee07d79c2aaa27a66ed59eeaee1ac90b495dd3c",
          "url": "https://github.com/tophat/syrupy/commit/3152c56fc6fe98618b8f2c08b2f1238e6930c92b"
        },
        "date": 1682434141203,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8522096917912929,
            "unit": "iter/sec",
            "range": "stddev: 0.039520606559475834",
            "extra": "mean: 1.1734201214000053 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.836317189989203,
            "unit": "iter/sec",
            "range": "stddev: 0.03811244420134587",
            "extra": "mean: 1.195718576599998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.8017164146830378,
            "unit": "iter/sec",
            "range": "stddev: 0.04161063706966816",
            "extra": "mean: 1.247323843799998 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "john.kurkowski@gmail.com",
            "name": "John Kurkowski",
            "username": "john-kurkowski"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "dfd5910cd5ac9a93011d639303cdc060ef4c779a",
          "message": "fix: defer snapshot default extension import (#734)\n\n* test: add coverage for bug #719\r\n\r\n* fix: defer snapshot default extension import\r\n\r\nFixes unable to use pytest's `pythonpath` option with this project's\r\n`--snapshot-default-extension` option. Does cause extension import\r\nerrors to raise later than CLI argument parsing, and therefore emit on\r\nstdout, instead of stderr.\r\n\r\n---------\r\n\r\nCo-authored-by: Noah Negin-Ulster <noah.negin-ulster@tophatmonocle.com>",
          "timestamp": "2023-04-25T10:48:13-04:00",
          "tree_id": "6745d628f63be1c359328c56053001004a93877c",
          "url": "https://github.com/tophat/syrupy/commit/dfd5910cd5ac9a93011d639303cdc060ef4c779a"
        },
        "date": 1682434205532,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7533301643184105,
            "unit": "iter/sec",
            "range": "stddev: 0.055459398894752904",
            "extra": "mean: 1.3274392124000087 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7436940174427946,
            "unit": "iter/sec",
            "range": "stddev: 0.05918633061292454",
            "extra": "mean: 1.3446390269999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7081867525088105,
            "unit": "iter/sec",
            "range": "stddev: 0.06277208716074116",
            "extra": "mean: 1.412056913600003 sec\nrounds: 5"
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
          "id": "689a202407c26a3f8eb3c7b5a2870aca1c41f7a2",
          "message": "chore(deps): update python docker tag to v3.11.3 (#732)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-04-25T12:16:14-04:00",
          "tree_id": "2033ae0c9c65047dc36bf61dc72f7f7dc8e48e57",
          "url": "https://github.com/tophat/syrupy/commit/689a202407c26a3f8eb3c7b5a2870aca1c41f7a2"
        },
        "date": 1682439495514,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6597309197298232,
            "unit": "iter/sec",
            "range": "stddev: 0.05179156637201726",
            "extra": "mean: 1.5157694904000039 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6527667800990558,
            "unit": "iter/sec",
            "range": "stddev: 0.07538294823174536",
            "extra": "mean: 1.5319407030000094 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6233935651994303,
            "unit": "iter/sec",
            "range": "stddev: 0.06200867975406181",
            "extra": "mean: 1.6041230706000136 sec\nrounds: 5"
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
          "id": "9aec6da2c258d5455e16e56b109641e211b38552",
          "message": "chore(deps): update actions/setup-python action to v4.6.0 (#742)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-04-27T09:37:09-04:00",
          "tree_id": "21ee4608bb469cf9dada5df7c838dec6231eaee7",
          "url": "https://github.com/tophat/syrupy/commit/9aec6da2c258d5455e16e56b109641e211b38552"
        },
        "date": 1682602726931,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8385224501358716,
            "unit": "iter/sec",
            "range": "stddev: 0.03860903588598527",
            "extra": "mean: 1.1925739136000033 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8309375213686999,
            "unit": "iter/sec",
            "range": "stddev: 0.04817602947811153",
            "extra": "mean: 1.2034599164000013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7828324846144313,
            "unit": "iter/sec",
            "range": "stddev: 0.04632876610676649",
            "extra": "mean: 1.2774124983999997 sec\nrounds: 5"
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
          "id": "a53165af1b13bf2b88c03aa059eb81d0f06f7449",
          "message": "chore(deps): update dependency coverage to v7.2.4 (#743)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-05-23T07:42:04-04:00",
          "tree_id": "fdea455d02ff9d2175ed57af791f00b67435c9e3",
          "url": "https://github.com/tophat/syrupy/commit/a53165af1b13bf2b88c03aa059eb81d0f06f7449"
        },
        "date": 1684842253792,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5258797387405306,
            "unit": "iter/sec",
            "range": "stddev: 0.06610797973045834",
            "extra": "mean: 1.9015754484000014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5427211009280758,
            "unit": "iter/sec",
            "range": "stddev: 0.06729436728544913",
            "extra": "mean: 1.842567016999999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4972253231867308,
            "unit": "iter/sec",
            "range": "stddev: 0.11726084120164261",
            "extra": "mean: 2.0111606416000143 sec\nrounds: 5"
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
          "id": "2bdcf99daf96daf87ecd6aa239df1a6758b5fb65",
          "message": "chore(deps): update dependency pytest-xdist to v3.3.0 (#748)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-05-23T11:51:17Z",
          "tree_id": "97c905a3f0de1325cabafb9db166065499e399d4",
          "url": "https://github.com/tophat/syrupy/commit/2bdcf99daf96daf87ecd6aa239df1a6758b5fb65"
        },
        "date": 1684842793655,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5783701497393112,
            "unit": "iter/sec",
            "range": "stddev: 0.05413493018372918",
            "extra": "mean: 1.7289965612000031 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5699574812060991,
            "unit": "iter/sec",
            "range": "stddev: 0.07380568441673757",
            "extra": "mean: 1.754516842000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5485538617276983,
            "unit": "iter/sec",
            "range": "stddev: 0.061675160078167326",
            "extra": "mean: 1.8229750436000018 sec\nrounds: 5"
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
          "id": "5ed0946315b0e682066519289a0430623c1f2cf2",
          "message": "chore(deps): update dependency mypy to v1.3.0 (#746)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-05-23T08:52:45-04:00",
          "tree_id": "ec129ea3568351cfbc164996d2f49e82cb86b8d3",
          "url": "https://github.com/tophat/syrupy/commit/5ed0946315b0e682066519289a0430623c1f2cf2"
        },
        "date": 1684846500194,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5540484531452948,
            "unit": "iter/sec",
            "range": "stddev: 0.04309927963693787",
            "extra": "mean: 1.8048962944000095 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5427499169106295,
            "unit": "iter/sec",
            "range": "stddev: 0.06298290101852409",
            "extra": "mean: 1.84246919040001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5189618929582639,
            "unit": "iter/sec",
            "range": "stddev: 0.0729546413174831",
            "extra": "mean: 1.9269237559999852 sec\nrounds: 5"
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
          "id": "33693162292af47d7662cb2ea9b930f54973d6da",
          "message": "chore(deps): update dependency invoke to v2.1.2 (#744)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-05-23T11:03:29-04:00",
          "tree_id": "ad8a3f3bdbda4bd69cb477be0206427a2314f16a",
          "url": "https://github.com/tophat/syrupy/commit/33693162292af47d7662cb2ea9b930f54973d6da"
        },
        "date": 1684854306681,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7667869587938749,
            "unit": "iter/sec",
            "range": "stddev: 0.05832391347220397",
            "extra": "mean: 1.3041432023999988 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7583512004035935,
            "unit": "iter/sec",
            "range": "stddev: 0.05726536422983304",
            "extra": "mean: 1.3186502500000017 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7268869089176014,
            "unit": "iter/sec",
            "range": "stddev: 0.05702362545533737",
            "extra": "mean: 1.3757298249999963 sec\nrounds: 5"
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
          "id": "8fa8b0fedd61906926e83f215d470d084841806a",
          "message": "chore(deps): update actions/setup-python action to v4.6.1 (#751)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-06-01T15:45:31-04:00",
          "tree_id": "b06898288079e138c218fbf2da01d854222fbe89",
          "url": "https://github.com/tophat/syrupy/commit/8fa8b0fedd61906926e83f215d470d084841806a"
        },
        "date": 1685648830836,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7686512547870646,
            "unit": "iter/sec",
            "range": "stddev: 0.06216583398955228",
            "extra": "mean: 1.3009801178000089 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7522257796650924,
            "unit": "iter/sec",
            "range": "stddev: 0.06280548088390653",
            "extra": "mean: 1.3293881000000056 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7174729154164473,
            "unit": "iter/sec",
            "range": "stddev: 0.06897873500168626",
            "extra": "mean: 1.3937808362000168 sec\nrounds: 5"
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
          "id": "96326365891cb5e505ad55bb3e91da76b0b04b2c",
          "message": "chore(deps): update dependency coverage to v7.2.6 (#750)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-06-01T15:45:47-04:00",
          "tree_id": "f97f6cd9b61188f3c2666395146f189d28d09eb1",
          "url": "https://github.com/tophat/syrupy/commit/96326365891cb5e505ad55bb3e91da76b0b04b2c"
        },
        "date": 1685648843651,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8260381642071998,
            "unit": "iter/sec",
            "range": "stddev: 0.05012858083587587",
            "extra": "mean: 1.2105978190000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8046676575682188,
            "unit": "iter/sec",
            "range": "stddev: 0.052777841600473926",
            "extra": "mean: 1.242749090999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7845231326198769,
            "unit": "iter/sec",
            "range": "stddev: 0.04395790466029056",
            "extra": "mean: 1.2746596734000035 sec\nrounds: 5"
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
          "id": "235d82aeb43798161b6cde1383b0c19f2ca21c36",
          "message": "chore(deps): update dev dependencies (#753)",
          "timestamp": "2023-06-01T16:01:55-04:00",
          "tree_id": "01c74de10544e08d06f144b5c3addda0d39120ff",
          "url": "https://github.com/tophat/syrupy/commit/235d82aeb43798161b6cde1383b0c19f2ca21c36"
        },
        "date": 1685649825262,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6523778474364298,
            "unit": "iter/sec",
            "range": "stddev: 0.057335804272165676",
            "extra": "mean: 1.532854010799997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6521472068214408,
            "unit": "iter/sec",
            "range": "stddev: 0.08168525504841187",
            "extra": "mean: 1.5333961251999995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6124003781665417,
            "unit": "iter/sec",
            "range": "stddev: 0.15376727282642308",
            "extra": "mean: 1.6329186520000007 sec\nrounds: 5"
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
          "id": "f7e291fd1f061df192577efb79eda1658518addc",
          "message": "chore(deps): update dependency pytest to v7.3.2 (#757)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-06-18T22:39:20-04:00",
          "tree_id": "97c5b3555ec485b3523d5548c5d32921879f02ea",
          "url": "https://github.com/tophat/syrupy/commit/f7e291fd1f061df192577efb79eda1658518addc"
        },
        "date": 1687142468342,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7506192504855648,
            "unit": "iter/sec",
            "range": "stddev: 0.057535986861826",
            "extra": "mean: 1.3322333518000165 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7503641932005783,
            "unit": "iter/sec",
            "range": "stddev: 0.07097002241480323",
            "extra": "mean: 1.3326861930000065 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7282719804118541,
            "unit": "iter/sec",
            "range": "stddev: 0.06952320322273126",
            "extra": "mean: 1.3731133792000036 sec\nrounds: 5"
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
          "id": "4466cb433bef391b8b5c656454414293c493a9ea",
          "message": "chore(deps): update actions/checkout action to v3.5.3 (#756)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-06-18T22:39:44-04:00",
          "tree_id": "51edb9fd34b6604551c2c21ad0f00117bf74888c",
          "url": "https://github.com/tophat/syrupy/commit/4466cb433bef391b8b5c656454414293c493a9ea"
        },
        "date": 1687142487826,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8513969458346177,
            "unit": "iter/sec",
            "range": "stddev: 0.043118684244449756",
            "extra": "mean: 1.1745402715999973 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.846072821872911,
            "unit": "iter/sec",
            "range": "stddev: 0.04890457963929366",
            "extra": "mean: 1.1819313588 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.8189291827513658,
            "unit": "iter/sec",
            "range": "stddev: 0.04974762918427435",
            "extra": "mean: 1.2211068076000031 sec\nrounds: 5"
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
          "id": "783fc5cf71901c8bb54769358787dabfa2b51e4a",
          "message": "fix: support colored >=1.5.0 dependency, close #758 (#760)\n\n* chore(deps): update dev dependencies\r\n\r\n* fix: support colored >=1.5.0 dependency, close #758",
          "timestamp": "2023-06-18T23:17:54-04:00",
          "tree_id": "0cdaa54cc9c22ddd7b3718a31616b862e80cac51",
          "url": "https://github.com/tophat/syrupy/commit/783fc5cf71901c8bb54769358787dabfa2b51e4a"
        },
        "date": 1687144797354,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6308297334975749,
            "unit": "iter/sec",
            "range": "stddev: 0.051713625654997736",
            "extra": "mean: 1.5852138015999913 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6342425353394988,
            "unit": "iter/sec",
            "range": "stddev: 0.0828116786033814",
            "extra": "mean: 1.5766839091999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6101786430715832,
            "unit": "iter/sec",
            "range": "stddev: 0.0866700410881286",
            "extra": "mean: 1.6388643086000059 sec\nrounds: 5"
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
          "id": "0badfdbb06157a7e2365edd551aaa1914681f3de",
          "message": "fix: incorrect marking of TestClass.test_method as unused, close #717 (#761)",
          "timestamp": "2023-06-18T23:49:53-04:00",
          "tree_id": "09033cb0bd22614bad3317d01fad762753166aa4",
          "url": "https://github.com/tophat/syrupy/commit/0badfdbb06157a7e2365edd551aaa1914681f3de"
        },
        "date": 1687146694864,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7690179402031176,
            "unit": "iter/sec",
            "range": "stddev: 0.047594445252501956",
            "extra": "mean: 1.300359780600013 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7519094470472352,
            "unit": "iter/sec",
            "range": "stddev: 0.04333483494433192",
            "extra": "mean: 1.329947381199986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.723793214832062,
            "unit": "iter/sec",
            "range": "stddev: 0.06166199357258839",
            "extra": "mean: 1.3816100780000056 sec\nrounds: 5"
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
          "id": "b601e6dd23ac6080cc2dcea9e893d64407868890",
          "message": "chore: create SECURITY.md (#762)",
          "timestamp": "2023-06-19T00:04:21-04:00",
          "tree_id": "f6199a5486b2c1a04fa64b941c9b854aff1ae60b",
          "url": "https://github.com/tophat/syrupy/commit/b601e6dd23ac6080cc2dcea9e893d64407868890"
        },
        "date": 1687147563039,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8558306909254053,
            "unit": "iter/sec",
            "range": "stddev: 0.03984199305567669",
            "extra": "mean: 1.1684554090000034 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8560614075831229,
            "unit": "iter/sec",
            "range": "stddev: 0.04424474646227217",
            "extra": "mean: 1.1681404991999955 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.8233998467764522,
            "unit": "iter/sec",
            "range": "stddev: 0.04857960469255008",
            "extra": "mean: 1.2144767866000024 sec\nrounds: 5"
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
          "id": "7e695066081170530d3401d80b920a8c218cd598",
          "message": "chore: update SECURITY.md (#763)",
          "timestamp": "2023-06-19T00:09:18-04:00",
          "tree_id": "afbad533a0464c49c8477cdb40ac2487d1b5ce64",
          "url": "https://github.com/tophat/syrupy/commit/7e695066081170530d3401d80b920a8c218cd598"
        },
        "date": 1687147860120,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.8449974015729933,
            "unit": "iter/sec",
            "range": "stddev: 0.04489653701202901",
            "extra": "mean: 1.1834355918000028 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.8513706386952679,
            "unit": "iter/sec",
            "range": "stddev: 0.045135026916107386",
            "extra": "mean: 1.1745765646000053 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.8143717404747662,
            "unit": "iter/sec",
            "range": "stddev: 0.05526852948826999",
            "extra": "mean: 1.2279404482000018 sec\nrounds: 5"
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
          "id": "440e9f41566653202861d2e10c3a4d55d72dda5a",
          "message": "chore(deps): update python docker tag to v3.11.4 (#755)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-06-19T00:17:09-04:00",
          "tree_id": "eda34986db0ab961d50c2de07602fd85b4ee519e",
          "url": "https://github.com/tophat/syrupy/commit/440e9f41566653202861d2e10c3a4d55d72dda5a"
        },
        "date": 1687148351338,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5357543873511299,
            "unit": "iter/sec",
            "range": "stddev: 0.06175799340133328",
            "extra": "mean: 1.8665269451999962 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5383008811805334,
            "unit": "iter/sec",
            "range": "stddev: 0.07060743483840222",
            "extra": "mean: 1.8576971261999915 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5151145337117479,
            "unit": "iter/sec",
            "range": "stddev: 0.08154938418322916",
            "extra": "mean: 1.9413158327999895 sec\nrounds: 5"
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
          "id": "b322e69a93b26d7bc8434ef5cd06913e20c6ae14",
          "message": "chore(deps): update dependency pytest to v7.4.0 (#767)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-06-30T09:58:46-04:00",
          "tree_id": "e00f753687aa1d72cfb6d0103aa34bb592bec184",
          "url": "https://github.com/tophat/syrupy/commit/b322e69a93b26d7bc8434ef5cd06913e20c6ae14"
        },
        "date": 1688133649205,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5590722693398721,
            "unit": "iter/sec",
            "range": "stddev: 0.058876453530685956",
            "extra": "mean: 1.7886775196000257 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5501040160768219,
            "unit": "iter/sec",
            "range": "stddev: 0.06289912776508881",
            "extra": "mean: 1.8178380283999787 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5359676606932513,
            "unit": "iter/sec",
            "range": "stddev: 0.12038921913453221",
            "extra": "mean: 1.8657842129999835 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "iamogbz+github@gmail.com",
            "name": "Emmanuel Ogbizi",
            "username": "iamogbz"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "8f581d577068f19a9e0fff65f4476f4601c137df",
          "message": "fix: hide empty snapshot report (#768)\n\n* fix: hide empty snapshot report\r\n\r\n* test: does not print empty snapshot report",
          "timestamp": "2023-07-04T13:36:00-04:00",
          "tree_id": "b13059b35174b7117e224b5b0c7dbe71ce14c1af",
          "url": "https://github.com/tophat/syrupy/commit/8f581d577068f19a9e0fff65f4476f4601c137df"
        },
        "date": 1688492263149,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7214816129612851,
            "unit": "iter/sec",
            "range": "stddev: 0.06489018132786964",
            "extra": "mean: 1.3860367084000245 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7320864379628735,
            "unit": "iter/sec",
            "range": "stddev: 0.0858032333813154",
            "extra": "mean: 1.3659589198000048 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.694756948242633,
            "unit": "iter/sec",
            "range": "stddev: 0.11733256694474728",
            "extra": "mean: 1.4393522835999988 sec\nrounds: 5"
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
          "id": "596b29b7eae26292fb671b3f339d255fd5ac8761",
          "message": "fix: improve reporting around xfailed snapshots, close #736 (#769)",
          "timestamp": "2023-07-11T17:09:24-04:00",
          "tree_id": "0f1ee8f05193c253d60c2b211d9a5c704143443e",
          "url": "https://github.com/tophat/syrupy/commit/596b29b7eae26292fb671b3f339d255fd5ac8761"
        },
        "date": 1689109857143,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7635310089567773,
            "unit": "iter/sec",
            "range": "stddev: 0.05228497653813556",
            "extra": "mean: 1.3097045022000002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.764524198070224,
            "unit": "iter/sec",
            "range": "stddev: 0.05621594636200745",
            "extra": "mean: 1.3080030724000011 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7243729092135005,
            "unit": "iter/sec",
            "range": "stddev: 0.05963585108102107",
            "extra": "mean: 1.3805044159999937 sec\nrounds: 5"
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
          "id": "319ac7ebdf1000c0717cc578100521d2ab223c09",
          "message": "chore(deps): update dependency flake8-comprehensions to v3.14.0 (#773)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-07-17T14:36:06-04:00",
          "tree_id": "8606f348cfff51b8ac2e2b8a60323b579d741d8d",
          "url": "https://github.com/tophat/syrupy/commit/319ac7ebdf1000c0717cc578100521d2ab223c09"
        },
        "date": 1689619090600,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5623892551866011,
            "unit": "iter/sec",
            "range": "stddev: 0.10755670860936692",
            "extra": "mean: 1.7781278550000024 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5505784512761549,
            "unit": "iter/sec",
            "range": "stddev: 0.08041569534240654",
            "extra": "mean: 1.8162715915999912 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.575505035062185,
            "unit": "iter/sec",
            "range": "stddev: 0.0845423510553044",
            "extra": "mean: 1.7376042590000054 sec\nrounds: 5"
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
          "id": "90e146fb5cec0f3e0214e1bb7aa9d24a3fd828d8",
          "message": "chore(deps): update dependency flake8-bugbear to v23.7.10 (#772)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-07-17T14:36:30-04:00",
          "tree_id": "95b719481e74b024c4f8875f1af3153c9ef1731a",
          "url": "https://github.com/tophat/syrupy/commit/90e146fb5cec0f3e0214e1bb7aa9d24a3fd828d8"
        },
        "date": 1689619094098,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6285813455951532,
            "unit": "iter/sec",
            "range": "stddev: 0.04484809020412062",
            "extra": "mean: 1.5908839913999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6663993899537946,
            "unit": "iter/sec",
            "range": "stddev: 0.07557434722968452",
            "extra": "mean: 1.5006016138000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6510062956636669,
            "unit": "iter/sec",
            "range": "stddev: 0.0791367492540713",
            "extra": "mean: 1.536083455200003 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "iamogbz+github@gmail.com",
            "name": "Emmanuel Ogbizi",
            "username": "iamogbz"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "24260b17607a11f7afa691c0ecd4da3e09de9bf0",
          "message": "fix: large snapshot diff recursion error (#776)\n\n* style: add pylint dev dependency\n\n* wip: replace ndiff call with sequence matcher\n\n* wip: get sequence match to function the same\n\n* refactor: sequence diff usage\n\n* wip: sequence diff refactor\n\n* refactor: fix test style errors\n\n* wip: yeah this does not work either\n\n* wip: revert and add test to validate fix\n\n* fix: set max diff line count to avoid ndiff limitation\n\n* chore: update lockfile\n\n* test: add test_diff_large_lines\n\n* test: update diff large to always be above max line count",
          "timestamp": "2023-07-20T07:58:09-04:00",
          "tree_id": "039f036490a88350d5956d035c1ba0a44bc02848",
          "url": "https://github.com/tophat/syrupy/commit/24260b17607a11f7afa691c0ecd4da3e09de9bf0"
        },
        "date": 1689854412632,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5432712389786792,
            "unit": "iter/sec",
            "range": "stddev: 0.052241832464524116",
            "extra": "mean: 1.840701160399999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5694314332620367,
            "unit": "iter/sec",
            "range": "stddev: 0.07676355961630807",
            "extra": "mean: 1.7561376867999967 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5543317257461231,
            "unit": "iter/sec",
            "range": "stddev: 0.06717288141995083",
            "extra": "mean: 1.8039739628000064 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "iamogbz+github@gmail.com",
            "name": "Emmanuel Ogbizi",
            "username": "iamogbz"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "64b42653d1c3af5b56347ccd9afd24e87b29aa18",
          "message": "fix: diffing excessively large snapshot lines (#778)\n\n* test: fix invalid testcase\r\n\r\n* fix: diffing excessively large snapshot lines\r\n\r\n* test: snapshot diff for better test representation\r\n\r\n* refactor: include first character change in generated diff",
          "timestamp": "2023-07-20T17:35:51-04:00",
          "tree_id": "1bd550ec2d2c50e6649491820c04982fda7e83b9",
          "url": "https://github.com/tophat/syrupy/commit/64b42653d1c3af5b56347ccd9afd24e87b29aa18"
        },
        "date": 1689889047540,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7905710629626236,
            "unit": "iter/sec",
            "range": "stddev: 0.04736608058330872",
            "extra": "mean: 1.2649084274000018 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.778955120805439,
            "unit": "iter/sec",
            "range": "stddev: 0.05148325749372007",
            "extra": "mean: 1.283771007200005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.747311906368486,
            "unit": "iter/sec",
            "range": "stddev: 0.08089193912759848",
            "extra": "mean: 1.3381293560000074 sec\nrounds: 5"
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
          "id": "7f1c70e3786fd66ffa36817c89128cc4cf136449",
          "message": "chore(deps): update actions/setup-python action to v4.7.0 (#777)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-07-20T18:11:35-04:00",
          "tree_id": "56410cd72be12804bbf80a49294cb356eb9c0ed2",
          "url": "https://github.com/tophat/syrupy/commit/7f1c70e3786fd66ffa36817c89128cc4cf136449"
        },
        "date": 1689891210015,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6072501820065094,
            "unit": "iter/sec",
            "range": "stddev: 0.06721544497119933",
            "extra": "mean: 1.6467677238000078 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6041723974910761,
            "unit": "iter/sec",
            "range": "stddev: 0.07487844365751095",
            "extra": "mean: 1.6551567138000052 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5852242962485704,
            "unit": "iter/sec",
            "range": "stddev: 0.1017264216212603",
            "extra": "mean: 1.7087465548000011 sec\nrounds: 5"
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
          "id": "d0f8da00098fa016e8dfb12fe8e218c89f3de8c2",
          "message": "chore(deps): update snok/install-poetry action to v1.3.4 (#783)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-08-13T20:01:04-04:00",
          "tree_id": "e7dc9ea4280b094b402301e4ae0f222e0904d6a8",
          "url": "https://github.com/tophat/syrupy/commit/d0f8da00098fa016e8dfb12fe8e218c89f3de8c2"
        },
        "date": 1691971398450,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5317635896782987,
            "unit": "iter/sec",
            "range": "stddev: 0.09869442038707753",
            "extra": "mean: 1.880534920799994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5111507090660045,
            "unit": "iter/sec",
            "range": "stddev: 0.08417710316501338",
            "extra": "mean: 1.9563701707999996 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5123492876294338,
            "unit": "iter/sec",
            "range": "stddev: 0.12308306183314652",
            "extra": "mean: 1.9517934817999958 sec\nrounds: 5"
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
          "id": "2ed84ea8e2b9dfa01cd4788f9787809ffc6b2648",
          "message": "chore(deps): update dev dependencies (#782)",
          "timestamp": "2023-08-15T09:48:28-04:00",
          "tree_id": "c0e794b2c4b9fb4d85b003a907eaf03f175dfc91",
          "url": "https://github.com/tophat/syrupy/commit/2ed84ea8e2b9dfa01cd4788f9787809ffc6b2648"
        },
        "date": 1692107428161,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5925003953879575,
            "unit": "iter/sec",
            "range": "stddev: 0.04865581418905636",
            "extra": "mean: 1.6877625867999968 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5671099850788985,
            "unit": "iter/sec",
            "range": "stddev: 0.07653507111647051",
            "extra": "mean: 1.7633263851999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5589981040757587,
            "unit": "iter/sec",
            "range": "stddev: 0.0893878289160392",
            "extra": "mean: 1.7889148329999955 sec\nrounds: 5"
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
          "id": "f4bc8453466af2cfa75cdda1d50d67bc8c4396c3",
          "message": "chore(deps): update dependency debugpy to v1.6.7 (#785)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-08-15T10:07:21-04:00",
          "tree_id": "c0cec5e52c9d28550cb8b9c1d9029c580ff32e3a",
          "url": "https://github.com/tophat/syrupy/commit/f4bc8453466af2cfa75cdda1d50d67bc8c4396c3"
        },
        "date": 1692108545060,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.778894787434532,
            "unit": "iter/sec",
            "range": "stddev: 0.04719469622330271",
            "extra": "mean: 1.283870448400006 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7666487335670356,
            "unit": "iter/sec",
            "range": "stddev: 0.05904571566187082",
            "extra": "mean: 1.304378336800005 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7442668868284715,
            "unit": "iter/sec",
            "range": "stddev: 0.08586868313405226",
            "extra": "mean: 1.3436040454000022 sec\nrounds: 5"
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
          "id": "d210cf192962afc3196c9d6cc81e7c799a6caf26",
          "message": "feat(amber): expose serialize_custom_iterable method of AmberDataSerializer (#788)",
          "timestamp": "2023-08-16T10:44:44-04:00",
          "tree_id": "c93e9d288974928d4bad75807cd7eaee0b7ba7e7",
          "url": "https://github.com/tophat/syrupy/commit/d210cf192962afc3196c9d6cc81e7c799a6caf26"
        },
        "date": 1692197202755,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.606437619287083,
            "unit": "iter/sec",
            "range": "stddev: 0.0583193106330012",
            "extra": "mean: 1.6489742196000008 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5892191093132315,
            "unit": "iter/sec",
            "range": "stddev: 0.07925610463789491",
            "extra": "mean: 1.6971615214000053 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5749693009860934,
            "unit": "iter/sec",
            "range": "stddev: 0.10701844650561114",
            "extra": "mean: 1.7392232912000054 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "55894364+atharva-2001@users.noreply.github.com",
            "name": "Atharva Arya",
            "username": "atharva-2001"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "118ef9260cb67369050c3bf7672e9aed0046f7f4",
          "message": "fix: preserve Falsy values in assertion diff function (#789)",
          "timestamp": "2023-08-17T19:37:35-04:00",
          "tree_id": "f915d8b1e3b9eb014a6eb8cc7a45de53f57e0271",
          "url": "https://github.com/tophat/syrupy/commit/118ef9260cb67369050c3bf7672e9aed0046f7f4"
        },
        "date": 1692315548366,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7964906731811064,
            "unit": "iter/sec",
            "range": "stddev: 0.04283177411686395",
            "extra": "mean: 1.2555074826000123 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7832702985046549,
            "unit": "iter/sec",
            "range": "stddev: 0.04957882334687827",
            "extra": "mean: 1.2766984805999981 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7578275475007488,
            "unit": "iter/sec",
            "range": "stddev: 0.06214663973032043",
            "extra": "mean: 1.3195614270000022 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "iamogbz+github@gmail.com",
            "name": "Emmanuel Ogbizi",
            "username": "iamogbz"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3ac2ce84c5dfe180606ef32d1dd067af952d376e",
          "message": "feat(serializer): add snapshot regex value matcher and bypass custom repr helper (#791)",
          "timestamp": "2023-08-21T07:51:00-04:00",
          "tree_id": "aa0881e1da921aa6efd215ef6ea9eab0e9addc18",
          "url": "https://github.com/tophat/syrupy/commit/3ac2ce84c5dfe180606ef32d1dd067af952d376e"
        },
        "date": 1692618806205,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5087558950508346,
            "unit": "iter/sec",
            "range": "stddev: 0.07724910671552575",
            "extra": "mean: 1.9655791898000132 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.49337831730534415,
            "unit": "iter/sec",
            "range": "stddev: 0.09880546059703803",
            "extra": "mean: 2.026842211999997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.48249111388009897,
            "unit": "iter/sec",
            "range": "stddev: 0.1232547096454394",
            "extra": "mean: 2.072577030399992 sec\nrounds: 5"
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
          "id": "c8524a60f3abeac738dca65fe8f4990e0f0a69f3",
          "message": "chore: update poetry, specify renovate constraint (#793)",
          "timestamp": "2023-08-21T16:03:10-04:00",
          "tree_id": "c036913c8dc07fdff17876f00d1f103d9f0b0578",
          "url": "https://github.com/tophat/syrupy/commit/c8524a60f3abeac738dca65fe8f4990e0f0a69f3"
        },
        "date": 1692648294159,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5050261577394404,
            "unit": "iter/sec",
            "range": "stddev: 0.07816862040087877",
            "extra": "mean: 1.9800954558000001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.4876147152078139,
            "unit": "iter/sec",
            "range": "stddev: 0.08273823592051148",
            "extra": "mean: 2.050799470999999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4694540132781303,
            "unit": "iter/sec",
            "range": "stddev: 0.12028302994148095",
            "extra": "mean: 2.130134095599999 sec\nrounds: 5"
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
          "id": "e2e314fca6f90d9601c3b7d30370d2ca21e09cfe",
          "message": "fix: support python 3.12 (#794)",
          "timestamp": "2023-08-21T16:18:29-04:00",
          "tree_id": "0d5d0a9a78b241dccdf08db7981deb1d1c763db9",
          "url": "https://github.com/tophat/syrupy/commit/e2e314fca6f90d9601c3b7d30370d2ca21e09cfe"
        },
        "date": 1692649207027,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5198448400308384,
            "unit": "iter/sec",
            "range": "stddev: 0.05812831911626532",
            "extra": "mean: 1.923650910799995 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5139725385120247,
            "unit": "iter/sec",
            "range": "stddev: 0.08167385620895319",
            "extra": "mean: 1.9456292410000118 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.4866094944331513,
            "unit": "iter/sec",
            "range": "stddev: 0.1352842241094931",
            "extra": "mean: 2.0550359404000007 sec\nrounds: 5"
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
          "id": "96bffccd229bb1b13e6721baffd80d298000e34b",
          "message": "fix: remove colored dependency (#796)",
          "timestamp": "2023-08-28T16:01:00-04:00",
          "tree_id": "cae1ede5a3b93c0747d0d212c26133695d926e9c",
          "url": "https://github.com/tophat/syrupy/commit/96bffccd229bb1b13e6721baffd80d298000e34b"
        },
        "date": 1693252945439,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7042399733248048,
            "unit": "iter/sec",
            "range": "stddev: 0.05421983222036774",
            "extra": "mean: 1.419970518399964 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6934455573077598,
            "unit": "iter/sec",
            "range": "stddev: 0.07518279239868159",
            "extra": "mean: 1.4420742759999938 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.680851774650648,
            "unit": "iter/sec",
            "range": "stddev: 0.0843281485862728",
            "extra": "mean: 1.468748466599959 sec\nrounds: 5"
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
          "id": "d3f891ea4e561cd1b182e9b2c5d0414821187cd7",
          "message": "feat: add include option to snapshots, similar to exclude (#797)",
          "timestamp": "2023-08-28T18:28:53-04:00",
          "tree_id": "35f01f5e6529c92eead5cd4ddb60b83d669dde05",
          "url": "https://github.com/tophat/syrupy/commit/d3f891ea4e561cd1b182e9b2c5d0414821187cd7"
        },
        "date": 1693261808738,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6766605709559296,
            "unit": "iter/sec",
            "range": "stddev: 0.0722410880423933",
            "extra": "mean: 1.4778458253999986 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6808699176335272,
            "unit": "iter/sec",
            "range": "stddev: 0.05893323903627665",
            "extra": "mean: 1.4687093292000042 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6634708691190315,
            "unit": "iter/sec",
            "range": "stddev: 0.11622671472213789",
            "extra": "mean: 1.5072251798000083 sec\nrounds: 5"
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
          "id": "e1ae7efba16e64fbade4c4336eeadc0222036855",
          "message": "chore(deps): update python docker tag to v3.11.5 (#795)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-08-29T08:12:02-04:00",
          "tree_id": "5b50f0f80346d2fb2d0b2bbd4f3d025db0d2e5ff",
          "url": "https://github.com/tophat/syrupy/commit/e1ae7efba16e64fbade4c4336eeadc0222036855"
        },
        "date": 1693311210288,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7608237284821884,
            "unit": "iter/sec",
            "range": "stddev: 0.06710584926949657",
            "extra": "mean: 1.314364895 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7722149802408419,
            "unit": "iter/sec",
            "range": "stddev: 0.059910919205681944",
            "extra": "mean: 1.2949761732000014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.7445000611518201,
            "unit": "iter/sec",
            "range": "stddev: 0.08523626586547005",
            "extra": "mean: 1.3431832342000007 sec\nrounds: 5"
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
          "id": "ceca97d88b000dda7fe8412ef3baab8d0235b684",
          "message": "chore(deps): update dependency debugpy to v1.6.7 (#792)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-08-29T08:12:21-04:00",
          "tree_id": "23ac4812b2a944226bb14e6d743867a3830e37c6",
          "url": "https://github.com/tophat/syrupy/commit/ceca97d88b000dda7fe8412ef3baab8d0235b684"
        },
        "date": 1693311227374,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.7176880734118378,
            "unit": "iter/sec",
            "range": "stddev: 0.05358647530566296",
            "extra": "mean: 1.3933629902000064 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.7087853277095996,
            "unit": "iter/sec",
            "range": "stddev: 0.06340538927366603",
            "extra": "mean: 1.4108644196 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.691573504979619,
            "unit": "iter/sec",
            "range": "stddev: 0.08570991764227988",
            "extra": "mean: 1.445977893600002 sec\nrounds: 5"
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
          "id": "1676fa554d74edeb1f448edbe661e053bf8ad350",
          "message": "feat(filter): add paths_include filter (#798)\n\nNOTE: The paths_include filter provides a convenience filter for supporting includes on nested objects.",
          "timestamp": "2023-08-29T11:20:05-04:00",
          "tree_id": "5d5dc74834bbab0e347aa9a0d47eb212d47d6812",
          "url": "https://github.com/tophat/syrupy/commit/1676fa554d74edeb1f448edbe661e053bf8ad350"
        },
        "date": 1693322498494,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6362335338821535,
            "unit": "iter/sec",
            "range": "stddev: 0.04916402864201718",
            "extra": "mean: 1.5717499106000048 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.6389395329401083,
            "unit": "iter/sec",
            "range": "stddev: 0.0828392419930386",
            "extra": "mean: 1.5650933280000003 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.6262105105519887,
            "unit": "iter/sec",
            "range": "stddev: 0.11530595686111426",
            "extra": "mean: 1.5969070833999979 sec\nrounds: 5"
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
          "id": "11b0722b91c5f0ed9434fa293dc1169088cc00b9",
          "message": "chore(deps): update dependency debugpy to v1.6.7 (#799)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-08-29T11:37:04-04:00",
          "tree_id": "b6ef2962369df336bc147faf68512604d3456482",
          "url": "https://github.com/tophat/syrupy/commit/11b0722b91c5f0ed9434fa293dc1169088cc00b9"
        },
        "date": 1693323525627,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.6130725736094014,
            "unit": "iter/sec",
            "range": "stddev: 0.07885853960124596",
            "extra": "mean: 1.631128259600007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5929057040043364,
            "unit": "iter/sec",
            "range": "stddev: 0.06561337831384517",
            "extra": "mean: 1.6866088371999979 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5988415334123963,
            "unit": "iter/sec",
            "range": "stddev: 0.09720766799540806",
            "extra": "mean: 1.6698908545999984 sec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "mjelonek92@gmail.com",
            "name": "Michał Jelonek",
            "username": "michaljelonek"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c87755984341ee4772f4f00b9309de6daec30ec0",
          "message": "feat: support setting defaults (#802)",
          "timestamp": "2023-09-01T17:53:54-04:00",
          "tree_id": "7875ea3bf75a756300b36730ecca64c4535f7dd9",
          "url": "https://github.com/tophat/syrupy/commit/c87755984341ee4772f4f00b9309de6daec30ec0"
        },
        "date": 1693605342066,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5321480065992378,
            "unit": "iter/sec",
            "range": "stddev: 0.03082435282365477",
            "extra": "mean: 1.8791764464000011 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5191784167069702,
            "unit": "iter/sec",
            "range": "stddev: 0.06790009853063964",
            "extra": "mean: 1.9261201309999962 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5058054166715812,
            "unit": "iter/sec",
            "range": "stddev: 0.11614888580473141",
            "extra": "mean: 1.9770448616000067 sec\nrounds: 5"
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
          "id": "3b7462439b40a0aef9c8388665e806cd5db9fa50",
          "message": "chore(deps): update actions/checkout action to v3.6.0 (#801)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-09-05T18:53:30-04:00",
          "tree_id": "6b77caea7908a4895c00e8912750c0fea6cb9cc1",
          "url": "https://github.com/tophat/syrupy/commit/3b7462439b40a0aef9c8388665e806cd5db9fa50"
        },
        "date": 1693954513620,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5583550818640047,
            "unit": "iter/sec",
            "range": "stddev: 0.11605874851043468",
            "extra": "mean: 1.7909750129999964 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.558849442609524,
            "unit": "iter/sec",
            "range": "stddev: 0.10275990665203748",
            "extra": "mean: 1.7893907083999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.556939810828826,
            "unit": "iter/sec",
            "range": "stddev: 0.09708342229298775",
            "extra": "mean: 1.7955261602000063 sec\nrounds: 5"
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
          "id": "b28482019ab0ae022ddded7d5d5df3466f420616",
          "message": "chore(deps): update cycjimmy/semantic-release-action action to v4 (#804)\n\nCo-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com>",
          "timestamp": "2023-09-07T21:56:27-04:00",
          "tree_id": "28ad7d58b2df5ced3a389a8d491e1185f2c2c287",
          "url": "https://github.com/tophat/syrupy/commit/b28482019ab0ae022ddded7d5d5df3466f420616"
        },
        "date": 1694138290099,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_1000x.py::test_1000x_reads",
            "value": 0.5270188600379563,
            "unit": "iter/sec",
            "range": "stddev: 0.07716474760194987",
            "extra": "mean: 1.8974653011999976 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_1000x.py::test_1000x_writes",
            "value": 0.5333475069508831,
            "unit": "iter/sec",
            "range": "stddev: 0.04479258439470401",
            "extra": "mean: 1.874950172200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_standard.py::test_standard",
            "value": 0.5185013777617061,
            "unit": "iter/sec",
            "range": "stddev: 0.0770425303392652",
            "extra": "mean: 1.9286351837999973 sec\nrounds: 5"
          }
        ]
      }
    ]
  }
}