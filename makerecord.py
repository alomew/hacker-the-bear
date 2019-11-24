import json
from datetime import datetime, timedelta

daydelta = timedelta(days=1)
dates = [datetime.now().replace(hour = 0, minute = 0, second=0, microsecond=0) - i * daydelta for i in range(5)]

data1 = [[ dates[0].replace(hour=9),
          dates[0].replace(hour=9, minute=2, second=3),
          dates[0].replace(hour=9, minute = 4),
          dates[0].replace(hour=11, minute=37),
           dates[0].replace(hour=12, minute=8),
           dates[0].replace(hour=12, minute=9),
           dates[0].replace(hour=17, minute=37, second=55),
        ],
         [ dates[1].replace(hour=9, minute=30),
           dates[1].replace(hour=9, minute=40),
           dates[1].replace(hour=9, minute=41),
           dates[1].replace(hour=22, minute=59)],
         [dates[2].replace(hour=9),
          dates[2].replace(hour=9, minute=1),
          dates[2].replace(hour=9, minute=1, second=30),
          dates[2].replace(hour=13, minute=44),
          dates[2].replace(hour=13, minute=44, second=30),
          dates[2].replace(hour=23, minute=44),
          dates[2].replace(hour=23, minute=44, second=59)],
         [],
         [],
         "Russell Person"]