# GraphDrawer - README

<div align="justify">

## Module Description
GraphDrawer is a Python-based module responsible for processing and managing graph-related data. It handles tasks like downloading, verifying, and storing data in systems such as MongoDB, Hazelcast, Neo4j, and Neptune.

### Main Features:
1. **AWSWordsDownloader:** Downloads word data from MongoDB and uploads it to Hazelcast.
2. **WordChecker:** Verifies word relationships, such as determining if two words differ by one letter.
3. **AWSStorageNeo4J:** Handles the storage of graph edges in a Neo4j database.
4. **AWSStorageNeptune:** Uploads graph nodes and edges to AWS Neptune using Gremlin queries.
5. **GraphStore:** An abstract class providing a blueprint for storing graph data.

## Instructions for Running Tests

### Prerequisites
- Python 3.11 installed.
- Dependencies listed in `requirements.txt` installed:
  ```bash
  pip install -r GraphDrawer/requirements.txt
  ```
- Install coverage for measuring test coverage:
  ```bash
  pip install coverage
  ```

### Running the Tests
The tests are executed using `unittest` with mocks for external dependencies.

1. Set the `PYTHONPATH` environment variable:
   ```bash
   export PYTHONPATH=$GITHUB_WORKSPACE
   ```
2. Run the tests:
   ```bash
   python -m unittest discover -s GraphDrawer/tests
   ```
3. Generate the coverage report:
   ```bash
   coverage run -m unittest discover -s GraphDrawer/tests
   coverage report
   ```

## Test Objectives
The tests aim to:
1. **Ensure functional correctness:** Verify that implemented classes and methods behave as expected.
2. **Enhance robustness:** Validate proper handling of successful and erroneous scenarios.
3. **Support maintainability:** Facilitate future modifications through clear and concise tests.

## Test Details

### Tested Components

1. **AWSWordsDownloader:**
   - **Tested Method:** `run`
   - **Functionality:** Validates the full flow of downloading words from MongoDB and uploading them to Hazelcast.

2. **WordChecker:**
   - **Tested Method:** `are_one_letter_apart`
   - **Functionality:** Ensures correct determination of word relationships.

3. **AWSStorageNeo4J:**
   - **Tested Method:** `upload_edges`
   - **Functionality:** Validates batch edge insertion into Neo4j.

4. **AWSStorageNeptune:**
   - **Tested Method:** `load_graph`
   - **Functionality:** Tests the upload of nodes and edges to Neptune using Gremlin queries.

5. **GraphStore:**
   - **Tested Method:** Abstract method `load_graph`
   - **Functionality:** Ensures that instantiating the abstract class directly raises an error.

### Mock Testing
Mocks simulate interactions with external systems:
- **MongoDB:** Simulates connection and data query operations.
- **Hazelcast:** Simulates cluster connections and map manipulations.
- **Neo4j:** Simulates sessions and Cypher query executions.
- **Neptune:** Simulates Gremlin queries via Boto3.

### Execution Summary
- **Total Tests Executed:** 5
- **Successes:** 5
- **Failures:** 0

### Coverage Results
The coverage results, as measured by `coverage.py`, are as follows:

| File                                      | Statements | Missed | Coverage |
|-------------------------------------------|------------|--------|----------|
| config/settings.py                        | 11         | 0      | 100%     |
| src/download_words/aws_words_downloaders.py | 47         | 18     | 62%      |
| src/download_words/downloaders.py         | 6          | 1      | 83%      |
| src/graph_builder/word_checker.py         | 14         | 2      | 86%      |
| src/storage/aws_storage_neo4j.py          | 31         | 12     | 61%      |
| src/storage/aws_storage_neptune.py        | 16         | 0      | 100%     |
| src/storage/graph_store.py                | 5          | 1      | 80%      |
| tests/test_graph_drawer.py                | 60         | 1      | 98%      |
| **Total**                                 | 190        | 35     | 82%      |

### Execution Output
```plaintext
----------------------------------------------------------------------
Ran 5 tests in 0.025s

OK
Response: <MagicMock name='client().execute_gremlin_query()' id='140041316262800'>
Connected to MongoDB and Hazelcast
Data uploaded to Hazelcast
```