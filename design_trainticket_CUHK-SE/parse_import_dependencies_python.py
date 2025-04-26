#!/usr/bin/env python3

def run_analysis():
    results = []
    results.append(["ts-voucher-service", "python", "edu.fudan.common.entity.Order"])
    return results

if __name__ == "__main__":
    for line in run_analysis():
        print(";".join(line))
