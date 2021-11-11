#!/usr/bin/env python3

import argparse
import logging
import numpy as np
from scipy.stats import poisson

mu = 61.2
tests = [1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

for i in range(13):    

    if i==0:
        print(poisson.cdf(tests[i], mu))
    else:
        print(poisson.cdf(tests[i], mu)-poisson.cdf(tests[i-1], mu))
