| Relative path from /api/v1               | **Test 1 (1 user)** |         |         | **Test 6 (10 users)** |         |         | **Test 8 (20 users)** |         |         |
|------------------------------------------|----------------------|---------|---------|------------------------|---------|---------|------------------------|---------|---------|
|                                          | E[T] (ms)            | T_max (ms) | N(F)  | E[T] (ms)              | T_max (ms) | N(F)  | E[T] (ms)              | T_max (ms) | N(F)  |
| /users/login                             | 316.72               | 350.60     | 0     | 6033.11                | 8473.41     | 0     | 7049.21                | 13649.01   | 0     |
| /contactservice/contacts/account/user    | 21.96                | 1891.33    | 0     | 20.96                  | 916.78      | 0     | 11.54                  | 223.36     | 0     |
| /travelservice/trips/left                | 136.34               | 1247.44    | 0     | 3598.59                | 13292.13    | 0     | 13458.61               | 31598.91   | 0     |
| /contactservice/contacts                 | 44.02                | 44.02      | 0     | 18.89                  | 23.29       | 0     | 20.21                  | 30.72      | 0     |
| /assuranceservice/assurances/types       | 12.39                | 27.16      | 0     | 11.06                  | 799.71      | 0     | 8.95                   | 117.49     | 0     |
| /foodservice/foods/departure/shanghai/suzhou/D1345 | 73.27 | 1548.45 | 0     | 45.69                  | 888.92      | 0     | 3889.19                | 12591.34   | 0     |
| /preserveservice/preserve               | 379.29               | 2429.46    | 0     | 14030.07               | 20552.11    | 0     | 31597.57               | 59167.20   | 0     |
| /orderservice/order/refresh              | 19.38                | 394.38     | 0     | 347.66                 | 3980.23     | 0     | 455.91                 | 3805.27    | 0     |
| /inside_pay_service/inside_payment       | 76.48                | 381.80     | 0     | 914.30                 | 4702.90     | 0     | 1106.10                | 4704.31    | 0     |
| /executeservice/execute/collected/order  | 35.46                | 401.80     | 0     | 803.62                 | 4316.40     | 0     | 1081.46                | 4495.23    | 0     |
| /executeservice/execute/execute/order    | 33.84                | 302.43     | 0     | 843.22                 | 4402.40     | 0     | 984.53                 | 4597.28    | 0     |