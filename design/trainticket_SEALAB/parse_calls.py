import parse_calls_java
import parse_calls_javascript
import parse_calls_go
import parse_calls_python
import csv

if __name__ == "__main__":
    results = parse_calls_java.main()
    results += parse_calls_javascript.main()
    results += parse_calls_go.main()
    results += parse_calls_python.main()

    with open("service_calls.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(["from", "to"])  
        for row in results:
            writer.writerow(row)
