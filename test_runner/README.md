### Test Documentation

The testing of gAIn source code is two-fold. Firstly, integration tests are run on the relevant containers in gAIn's infrastructure, to ensure that they all build correctly. Secondly, non-containerized utility functions are tested using the pytest library. Future testing efforts will include testing of functions in containerized applications as well, but because of the non-functional design of some of the code in each infrastructure container, such as data_scraping and data_preprocessing, this is not yet implemented.

All test files are located in the tests folder, with the integration_tests folder intended to hold future test functions for containerized functions.

### Unit Tests

In the unit test functionality, we test individual, auxiliary functions that are not part of a specific container.

- test_semantic_split.py: Contains tests for the semantic_split.py functionality used to preprocess text before pushing it to the vector database.
- integration_tests: Placeholder for future tests of containerized functions.

### CI Pipeline

Similarly to the testing, CI pipeline is done in two steps as well. We have added pre-commit hooks that run locally and fixes the following:

- trailing whitespace
- non-compliant file endings
- yaml file linting
- private key detection
- naming of python test files for pytest
- flake8 linting: Not auto-formatted, but prints relevant errors in staged files and enables developer to fix them before pushing to remote version control

Secondly, the same checks are run upon push to milestone4 and main branch, as a second layer of protection. If any of the tests fail, or the pre-commit hooks fail, an email is sent out to the developer - prompting them to clean up their code and repush their changes.

### Running tests locally

To run the integration tests and build the containers, run **docker-compose up** in the root directory of the project.

To run the system tests, simply run **pipenv run pytest** in the root directory of the project.
