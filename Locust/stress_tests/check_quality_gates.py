import csv
import sys
import os

MAX_AVG_RESPONSE_TIME = 5000
MAX_FAILURE_RATE = 50.0
MIN_SUCCESS_RATE = 50.0

def evaluate_quality_gates(test_name, csv_file, error_log):
    if not os.path.exists(csv_file):
        error_log.append(f"❌ Results for {test_name} not found: {csv_file}")
        return

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
        error_log.append(f"❌ {test_name}: Average Response Time exceeds {MAX_AVG_RESPONSE_TIME} ms")
    if failure_rate > MAX_FAILURE_RATE:
        error_log.append(f"❌ {test_name}: Failure Rate exceeds {MAX_FAILURE_RATE}%")
    if success_rate < MIN_SUCCESS_RATE:
        error_log.append(f"❌ {test_name}: Success Rate is below {MIN_SUCCESS_RATE}%")
    if (
        avg_response_time <= MAX_AVG_RESPONSE_TIME
        and failure_rate <= MAX_FAILURE_RATE
        and success_rate >= MIN_SUCCESS_RATE
    ):
        print(f"✅ {test_name}: Quality gates passed!")

tests = {
    "AllPaths": "Locust/stress_tests/AllPaths/results_stats.csv",
    "ShortestPath": "Locust/stress_tests/Shortest/results_stats.csv",
    "IsolatedNodes": "Locust/stress_tests/Isolated/results_stats.csv",
    "MaxDistance": "Locust/stress_tests/Max/results_stats.csv",
    "NodeConnections": "Locust/stress_tests/NodeCon/results_stats.csv",
    "StronglyConnected": "Locust/stress_tests/Strongly/results_stats.csv",
    "TopConnections": "Locust/stress_tests/Top/results_stats.csv"
}

error_log = []
for test_name, csv_file in tests.items():
    evaluate_quality_gates(test_name, csv_file, error_log)

if error_log:
    print("\n=== Errors Summary ===")
    for error in error_log:
        print(error)
else:
    print("\n✅ All tests passed successfully!")
