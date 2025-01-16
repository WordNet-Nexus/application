# DatalakeBuilder - README

## Module Description
DatalakeBuilder is a key component for processing and managing data. It includes tools for cleaning text, downloading books, and uploading data to a MongoDB database.

### Main Features:
1. **TextCleaner:** Cleans and processes text by removing punctuation, numbers, and stopwords.
2. **BookFetcher:** Initializes different book downloaders, such as AWS.
3. **MongoDBUploader:** Connects to a MongoDB database, uploads data, and creates collections.

## Instructions for Running Tests

### Prerequisites
- Python 3.11
- Dependencies listed in `requirements.txt` installed:
  ```bash
  pip install -r requirements.txt
  ```
- Required NLTK data downloaded:
  ```bash
  python -c "import nltk; nltk.download('stopwords')"
  ```

### About the `unittest` Framework
`unittest` is a Python standard library module for writing and running tests. It is based on the xUnit architecture and provides features such as:
- **Test case creation:** Allows developers to define test cases as methods within a class that inherits from `unittest.TestCase`.
- **Setup and teardown methods:** Includes `setUp` and `tearDown` methods for initializing and cleaning up resources before and after each test.
- **Assertions:** Provides various assertion methods (e.g., `assertEqual`, `assertTrue`, `assertRaises`) to validate test outcomes.
- **Test discovery:** Supports automatic discovery of test files and cases within a directory structure.
- **Command-line integration:** Allows execution of tests directly via the Python CLI using `python -m unittest`.

### Running the Tests
The tests are executed using the `unittest` framework.

1. Set the project environment variable:
   ```bash
   export PYTHONPATH=$GITHUB_WORKSPACE
   ```
2. Run the tests:
   ```bash
   python -m unittest discover -s DatalakeBuilder/tests
   ```
3. Generate the coverage report:
   ```bash
   coverage run -m unittest discover -s DatalakeBuilder/tests
   ```
4. View the coverage report:
   ```bash
   coverage report
   ```

## Test Objectives
The tests aim to:
1. **Ensure functional correctness:** Verify that implemented classes and methods behave as expected.
2. **Enhance robustness:** Validate proper handling of successful and erroneous scenarios.
3. **Support maintainability:** Facilitate future modifications through clear and concise tests.

## Test Details

### Tested Classes

#### 1. **TextCleaner** (in `src.clean.cleaner`):
- **Main Function:** Processes and cleans text by removing punctuation, numbers, and stopwords.
- **Tested Methods:**
  - `clean_text`: Ensures the text is cleaned correctly.
  - `process_documents`: Validates that text files are processed and return a word count.

#### 2. **BookFetcher** (in `src.bookFetcher.book_fetcher`):
- **Main Function:** Initializes various book downloaders (e.g., AWS).
- **Tested Methods:**
  - `initialize_downloader`: Ensures it returns a valid instance for a specified downloader.

#### 3. **MongoDBUploader** (in `src.uploader.mongodb_uploader`):
- **Main Function:** Connects to a MongoDB database and allows processed data uploads.
- **Tested Methods:**
  - `set_params`: Verifies that MongoDB connection parameters are set correctly.
  - `upload_data`: Confirms that data is uploaded successfully to the database.
  - `create_collection`: Validates the creation of a collection in the database if it does not exist.

### Execution Summary
- **Total Tests Executed:** 6
- **Successes:** 6
- **Failures:** 0
- **Total Execution Time:** ~0.042s

### Test Coverage
- **Overall Coverage:** 84%
- **File Details:**
  | File                                     | Lines  | Uncovered | Coverage |
  |------------------------------------------|--------|-----------|----------|
  | DatalakeBuilder/src/bookFetcher/aws_book_downloader.py | 19     | 13        | 32%      |
  | DatalakeBuilder/src/bookFetcher/book_fetcher.py       | 6      | 0         | 100%     |
  | DatalakeBuilder/src/bookFetcher/downloader.py         | 5      | 1         | 80%      |
  | DatalakeBuilder/src/clean/cleaner.py                  | 23     | 1         | 96%      |
  | DatalakeBuilder/src/uploader/mongodb_uploader.py      | 28     | 5         | 82%      |
  | DatalakeBuilder/tests/test_all.py                     | 52     | 1         | 98%      |

