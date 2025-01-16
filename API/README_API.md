# API - README

<div align="justify">

### Overview

This document consolidates the testing strategies, CI/CD pipelines, and coverage reports for the various submodules of the API module in the application. Each section provides an overview of the respective module, its test cases, and execution results.

---

## **1. AllPaths Module**

### Description

The AllPaths module is responsible for querying and displaying all paths between nodes in a graph database. It integrates with Neo4j and Flask for backend and frontend functionalities.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_allpaths.py
  coverage report
  ```

### Tests Performed

- **Mocking and Path Validation:** Mock objects simulate Neo4j nodes, relationships, and paths, verifying the functionality of the `find_all_paths` method in the `QueryHandler`.
- **POST Request Testing:** Ensures that the application redirects appropriately when data is incomplete.
- **Display Route Testing:** Validates rendering of node relationships in valid scenarios, and handles invalid parameter scenarios gracefully.

### Results

- **Total Tests:** 3
- **Passes:** 3
- **Failures:** 0
- **Coverage:** 64%

| File                           | Lines | Uncovered | Coverage |
| ------------------------------ | ----- | --------- | -------- |
| AllPaths/api/__init__.py | 3     | 0         | 100%     |
| AllPaths/api/routes.py         | 38    | 30        | 21%      |
| AllPaths/app.py                | 48    | 13        | 73%      |
| AllPaths/query_handler.py      | 17    | 11        | 35%      |
| AllPaths/settings.py           | 4     | 0         | 100%     |
| tests/test_allpaths.py         | 46    | 2         | 96%      |

---

## **2. HighDegreeConnections Module**

### Description

This module handles the analysis of graph nodes with high degrees of connectivity. It interfaces with AWS Lambda and Neo4j for distributed computation.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_highdegreeconnections.py
  coverage report
  ```

### Tests Performed

- **Lambda Handler Validation:** Tests successful and failed Lambda function calls for various parameter scenarios.
- **Query Validation:** Ensures correct graph queries are executed, testing node retrieval by degree and connectivity.
- **Environment Configuration:** Verifies that essential environment variables for Neo4j connectivity are set correctly.

### Results

- **Total Tests:** 4
- **Passes:** 4
- **Failures:** 0
- **Coverage:** 80%

| File                                   | Lines | Uncovered | Coverage |
| -------------------------------------- | ----- | --------- | -------- |
| HighDegreeConnections/query_handler.py | 23    | 10        | 57%      |
| HighDegreeConnections/settings.py      | 4     | 0         | 100%     |
| tests/test_highdegreeconnections.py    | 49    | 5         | 90%      |

---

## **3. IsolatedNodes Module**

### Description

The IsolatedNodes module identifies nodes with no connections in the graph and provides results via AWS Lambda.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_isolatednodes.py
  coverage report
  ```

### Tests Performed

- **Lambda Integration Testing:** Verifies the Lambda function returns appropriate responses for valid and invalid inputs.
- **Neo4j Driver Mocking:** Tests the `query_isolated_nodes` method with a mocked Neo4j driver to retrieve isolated nodes.
- **Error Handling:** Simulates exceptions during Lambda invocations and validates the application's error responses.

---

### Results

- **Total Tests:** 4
- **Passes:** 4
- **Failures:** 0
- **Coverage:** 90%

| File                             | Lines | Uncovered | Coverage |
| -------------------------------- | ----- | --------- | -------- |
| IsolatedNodes/lambda_function.py | 17    | 0         | 100%     |
| tests/test_isolatednodes.py      | 66    | 9         | 86%      |

---

## **4. main_web Module**

### Description

The main_web module serves as the central hub for interacting with all other modules via a unified web interface.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_main_web.py
  coverage report
  ```

### Tests Performed

- **Route Validation:** Confirms that the main index route of the application responds correctly and renders the expected HTML structure.

### Results

- **Total Tests:** 1
- **Passes:** 1
- **Failures:** 0
- **Coverage:** 90%

| File                   | Lines | Uncovered | Coverage |
| ---------------------- | ----- | --------- | -------- |
| main_web/app.py        | 9     | 1         | 89%      |
| tests/test_main_web.py | 12    | 1         | 92%      |

---

## **5. MaxDistance Module**

### Description

The MaxDistance module calculates the longest path between two nodes based on steps or weight. It uses Neo4j for graph storage and querying.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_maxdistance.py
  coverage report
  ```

### Tests Performed

- **Longest Path Calculation:** Validates the `find_longest_path_by_steps` and `find_longest_path_by_weight` methods using mocked Neo4j queries.
- **Lambda Functionality:** Tests error handling for invalid parameters and modes in the Lambda handler.
- **Integration with QueryHandler:** Verifies correct responses when invoking Lambda functions through the `QueryHandler`.

---

### Results

- **Total Tests:** 5
- **Passes:** 5
- **Failures:** 0
- **Coverage:** 82%

| File                                          | Lines | Uncovered | Coverage |
| --------------------------------------------- | ----- | --------- | -------- |
| MaxDistance/lambda_package/lambda_function.py | 44    | 11        | 75%      |
| MaxDistance/webpage/query_handler.py          | 14    | 8         | 43%      |
| tests/test_maxdistance.py                     | 56    | 1         | 98%      |

---

## **6. NodeConnections Module**

### Description

This module manages graph nodes based on their degree of connectivity and provides APIs to retrieve node data within specific ranges.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_nodeconnections.py
  coverage report
  ```

### Tests Performed

- **Node Querying:** Tests retrieving nodes based on degree, degree range, and minimum degree using mocked Neo4j queries.
- **API Testing:** Validates the index route and ensures proper driver cleanup operations.
- **Mocked Graph Queries:** Ensures the module retrieves accurate data with mocked inputs and database interactions.

---

### Results

- **Total Tests:** 5
- **Passes:** 5
- **Failures:** 0
- **Coverage:** 58%

| File                             | Lines | Uncovered | Coverage |
| -------------------------------- | ----- | --------- | -------- |
| NodeConnections/api/routes.py    | 44    | 33        | 25%      |
| NodeConnections/query_handler.py | 32    | 23        | 28%      |
| NodeConnections/app.py           | 15    | 2         | 87%      |

---

## **7. ShortestPath Module**

### Description

The ShortestPath module identifies the shortest paths between nodes in a graph using Neo4j and provides results via APIs.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_shortestpath.py
  coverage report
  ```

### Tests Performed

- **Graph Management:** Tests creation and deletion of graph projections in Neo4j.
- **Shortest Path Queries:** Ensures the `find_shortest_path` method correctly handles empty and valid query results.
- **Node ID Retrieval:** Verifies accurate retrieval and mapping of node IDs in the database.

---

### Results

- **Total Tests:** 4
- **Passes:** 4
- **Failures:** 0
- **Coverage:** 82%

| File                          | Lines | Uncovered | Coverage |
| ----------------------------- | ----- | --------- | -------- |
| ShortestPath/query_handler.py | 41    | 11        | 73%      |
| tests/test_shortestpath.py    | 45    | 5         | 89%      |

---

## **8. StronglyConnected Module**

### Description

The StronglyConnected module identifies strongly connected components in a graph using Neo4j queries. It includes Flask-based APIs for visualization.

### Test Summary

- **Framework:** `unittest` with mocks
- **Execution Command:**
  ```bash
  cd API
  coverage run -m unittest tests/test_stronglyconnected.py
  coverage report
  ```

### Tests Performed

- **Route Testing:** Validates proper responses for the index route and various display route scenarios.
- **Query Validation:** Mocks Neo4j queries to ensure the functionality of methods in the `QueryHandler`.
- **Parameter Handling:** Tests missing and invalid parameters to validate error handling in display routes.

---

### Results

- **Total Tests:** 3
- **Passes:** 3
- **Failures:** 0
- **Coverage:** 58%

| File                               | Lines | Uncovered | Coverage |
| ---------------------------------- | ----- | --------- | -------- |
| StronglyConnected/api/routes.py    | 32    | 19        | 41%      |
| StronglyConnected/query_handler.py | 41    | 31        | 24%      |
| StronglyConnected/app.py           | 35    | 9         | 74%      |

---

### Final Remarks

Each module has been thoroughly tested, and CI/CD pipelines have been configured to ensure continuous validation. Future improvements include increasing test coverage, handling more edge cases, and centralizing coverage report reviews.
