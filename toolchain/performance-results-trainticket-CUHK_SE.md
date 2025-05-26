| Relative path from /api/v1               | **Test 1 (1 user)** |         |         | **Test 6 (10 users)** |         |         | **Test 8 (20 users)** |         |         |
|------------------------------------------|----------------------|---------|---------|------------------------|---------|---------|------------------------|---------|---------|
|                                          | E[T] (ms)            | T_max (ms) | N(F)  | E[T] (ms)              | T_max (ms) | N(F)  | E[T] (ms)              | T_max (ms) | N(F)  |
| /users/login                             | 126.69               | 161.58     | 0     | 163.94                 | 208.87     | 0     | 223.96                 | 344.74     | 0     |
| /contactservice/contacts/account/user    | 17.55                | 36.00      | 0     | 10.83                  | 29.35      | 0     | 13.35                  | 61.30      | 0     |
| /travelservice/trips/left                | 183.28               | 431.60     | 0     | 2478.16                | 22907.77   | 1     | 15318.02               | 53053.67   | 10    |
| /contactservice/contacts                 | 148.94               | 148.94     | 0     | 27.25                  | 51.27      | 0     | 21.41                  | 67.09      | 0     |
| /assuranceservice/assurances/types       | 22.67                | 2420.70    | 0     | 9.25                   | 32.02      | 0     | 11.20                  | 45.38      | 0     |
| /foodservice/foods/departure/shanghai/suzhou/D1345 | 68.75 | 151.63 | 0     | 34.07                  | 105.68     | 0     | 2604.84                | 28128.80   | 0     |
| /preserveservice/preserve               | 332.27               | 539.17     | 0     | 5063.50                | 23707.25   | 1     | 34769.36               | 57195.09   | 4     |
| /orderservice/order/refresh              | 17.16                | 82.63      | 0     | 95.50                  | 6238.24    | 0     | 686.70                 | 12232.73   | 0     |
| /inside_pay_service/inside_payment       | 66.23                | 153.49     | 0     | 232.70                 | 4567.65    | 0     | 1799.67                | 24958.50   | 0     |
| /executeservice/execute/collected/order  | 31.45                | 73.50      | 0     | 140.45                 | 8634.27    | 0     | 538.35                 | 11579.05   | 0     |
| /executeservice/execute/execute/order    | 31.69                | 181.46     | 0     | 102.84                 | 2122.53    | 0     | 342.22                 | 14535.79   | 0     |
