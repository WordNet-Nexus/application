import csv
import sys
import os

MAX_AVG_RESPONSE_TIME = 500
MAX_FAILURE_RATE = 1.0
MIN_SUCCESS_RATE = 99.0

def evaluate_quality_gates(test_name, csv_file):
    if not os.path.exists(csv_file):
        print(f"❌ Results for {test_name} not found: {csv_file}")
        sys.exit(1)

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        stats = list(reader)

    total_requests = sum(int(row['Request Count']) for row in stats)
    total_failures = sum(int(row['Failure Count']) for row in stats)
    avg_response_time = sum(float(row['Average Response Time']) for row in stats) / len(stats)

    failure_rate = (total_failures / total_requests) * 100
    success_rate = 100 - failure_rate

    print(f"\n=== Results for {test_name} ===")
    print(f"Total Requests: {total_requests}")
    print(f"Failures: {total_failures}")
    print(f"Average Response Time: {avg_response_time:.2f} ms")
    print(f"Failure Rate: {failure_rate:.2f}%")
    print(f"Success Rate: {success_rate:.2f}%")

    if avg_response_time > MAX_AVG_RESPONSE_TIME:
        print(f"❌ {test_name}: Average Response Time exceeds {MAX_AVG_RESPONSE_TIME} ms")
        sys.exit(1)
    if failure_rate > MAX_FAILURE_RATE:
        print(f"❌ {test_name}: Failure Rate exceeds {MAX_FAILURE_RATE}%")
        sys.exit(1)
    if success_rate < MIN_SUCCESS_RATE:
        print(f"❌ {test_name}: Success Rate is below {MIN_SUCCESS_RATE}%")
        sys.exit(1)

    print(f"✅ {test_name}: Quality gates passed!")

tests = {
    "AllPaths": "Locust/load_tests/AllPaths/results_stats.csv",
    "ShortestPath": "Locust/load_tests/Shortest/results_stats.csv",
    "IsolatedNodes": "Locust/load_tests/Isolated/results_stats.csv",
    "MaxDistance": "Locust/load_tests/Max/results_stats.csv",
    "NodeConnections": "Locust/load_tests/NodeCon/results_stats.csv",
    "StronglyConnected": "Locust/load_tests/Strongly/results_stats.csv",
    "TopConnections": "Locust/load_tests/Top/results_stats.csv"
}

for test_name, csv_file in tests.items():
    evaluate_quality_gates(test_name, csv_file)
