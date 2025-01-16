
# Performance Testing with Locust

<div align="justify">

## 1. What is Locust?

[Locust](https://locust.io/) is an open-source load testing tool that enables the simulation of real-world user interactions with web applications. It is designed to measure system performance under both load and stress scenarios, allowing developers and engineers to identify bottlenecks, optimize performance, and ensure scalability. Locust provides an intuitive interface for writing test scripts in Python and generates insightful metrics such as request rates, response times, and error rates.

---

## 2. Tests Performed

We conducted **load tests** and **stress tests** to evaluate the performance of our application. Below are the details of each test:

### Load Testing
Load testing simulates normal user behavior to verify that the application can handle expected traffic levels. Each test was conducted with:
- **50 users** 
- A spawn rate of **10 users/second**
- Test duration: **1 minute**

### Stress Testing
Stress testing pushes the application beyond its normal operational capacity to determine its breaking point and behavior under extreme conditions. Each test was conducted with:
- **100 users**
- A spawn rate of **50 users/second**
- Test duration: **1 minute**

### Endpoints Tested
The following API endpoints were tested in both load and stress scenarios:
- **AllPaths**: Returns all paths between two nodes.
- **ShortestPath**: Calculates the shortest path between two nodes.
- **IsolatedNodes**: Identifies isolated nodes in the graph.
- **MaxDistance**: Finds the longest path between two nodes.
- **NodeConnections**: Selects nodes with a specific number of connections.
- **StronglyConnected**: Detects clusters of strongly connected nodes.
- **TopConnections**: Identifies nodes with the highest number of connections.

---

## 3. Test Results

### Load Testing Results

| Endpoint             | Total Requests | Failures | Avg. Response Time (ms) | Failure Rate | Success Rate | Quality Gates Passed |
|----------------------|----------------|----------|--------------------------|--------------|--------------|-----------------------|
| **AllPaths**         | 1970           | 0        | 609.99                   | 0.00%        | 100.00%      | ✅ Yes                |
| **ShortestPath**     | 1956           | 84       | 42.05                    | 4.29%        | 95.71%       | ✅ Yes                |
| **IsolatedNodes**    | 1910           | 0        | 52.60                    | 0.00%        | 100.00%      | ✅ Yes                |
| **MaxDistance**      | 1134           | 0        | 1783.78                  | 0.00%        | 100.00%      | ✅ Yes                |
| **NodeConnections**  | 746            | 0        | 4162.75                  | 0.00%        | 100.00%      | ✅ Yes                |
| **StronglyConnected**| 880            | 216      | 3926.70                  | 24.55%       | 75.45%       | ✅ Yes                |
| **TopConnections**   | 1900           | 0        | 50.65                    | 0.00%        | 100.00%      | ✅ Yes                |

---

### Stress Testing Results

| Endpoint             | Total Requests | Failures | Avg. Response Time (ms) | Failure Rate | Success Rate | Quality Gates Passed |
|----------------------|----------------|----------|--------------------------|--------------|--------------|-----------------------|
| **AllPaths**         | 4594           | 0        | 2405.26                  | 0.00%        | 100.00%      | ✅ Yes                |
| **ShortestPath**     | 2778           | 480      | 2900.23                  | 17.28%       | 82.72%       | ✅ Yes                |
| **IsolatedNodes**    | 6982           | 2226     | 1331.93                  | 31.88%       | 68.12%       | ✅ Yes                |
| **MaxDistance**      | 3920           | 0        | 2146.90                  | 0.00%        | 100.00%      | ✅ Yes                |
| **NodeConnections**  | 802            | 0        | 12523.99                 | 0.00%        | 100.00%      | ❌ No (Response Time) |
| **StronglyConnected**| 618            | 118      | 17033.55                 | 19.09%       | 80.91%       | ❌ No (Response Time) |
| **TopConnections**   | 11338          | 16       | 765.52                   | 0.14%        | 99.86%       | ✅ Yes                |

---

### Insights
1. **Load Testing**: All endpoints passed quality gates, showing the system can handle expected traffic smoothly.
2. **Stress Testing**: Most endpoints performed well, but **NodeConnections** and **StronglyConnected** exceeded the average response time threshold of 5000 ms, highlighting potential optimization areas for high traffic.

By analyzing these results, we can further refine system performance and scalability to enhance user experience.