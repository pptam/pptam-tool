| Relative path from /api/v1               | **Test 1 (1 user)** |         |         | **Test 6 (10 users)** |         |         | **Test 7 (15 users)** |         |         |
|------------------------------------------|----------------------|---------|---------|------------------------|---------|---------|------------------------|---------|---------|
|                                          | E[T] (ms)            | T_max (ms) | N(F)  | E[T] (ms)              | T_max (ms) | N(F)  | E[T] (ms)              | T_max (ms) | N(F)  |
| /users/login                             | 2823.64              | 5495.79     | 0     | 2680.06                | 3885.74     | 0     | 3797.03                | 9703.70     | 0     |
| /contactservice/contacts/account/user    | 16.89                | 31.92      | 0     | 8.85                   | 47.85      | 0     | 8.96                   | 14.58      | 0     |
| /travelservice/trips/left                | 966.55               | 60068.17   | 1     | 2613.38                | 16605.83   | 0     | 7272.07                | 60012.93   | 2     |
| /contactservice/contacts                 | 4486.83              | 4486.83    | 0     | 12.41                  | 19.11      | 0     | 12.88                  | 22.61      | 0     |
| /assuranceservice/assurances/types       | 39.62                | 4141.64    | 0     | 8.26                   | 71.46      | 0     | 8.56                   | 36.22      | 0     |
| /foodservice/foods/departure/shanghai/suzhou/D1345 | 207.13 | 13989.11 | 0     | 37.93                  | 395.83     | 0     | 40.66                  | 127.44     | 0     |
| /preserveservice/preserve               | 839.53               | 17147.60   | 0     | 21758.64               | 47667.52   | 0     | 58774.59               | 60031.60   | 266   |
| /orderservice/order/refresh              | 121.34               | 717.76     | 0     | 786.90                 | 5799.69    | 0     | 2188.82                | 13301.61   | 0     |
| /inside_pay_service/inside_payment       | 159.63               | 12814.37   | 0     | 803.99                 | 7304.95    | 0     | 1913.49                | 6103.88    | 0     |
| /executeservice/execute/collected/order  | 105.72               | 11613.38   | 0     | 552.56                 | 3402.89    | 0     | 921.92                 | 6902.55    | 0     |
| /executeservice/execute/execute/order    | 46.40                | 466.54     | 0     | 542.50                 | 12108.89   | 0     | 1542.63                | 7106.19    | 0     |