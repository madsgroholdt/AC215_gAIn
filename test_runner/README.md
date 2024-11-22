### Test Documentation

The testing of gAIn source code is two-fold. Firstly, integration tests are run on the relevant containers in gAIn's infrastructure to ensure that they all build correctly and that the user-interacting functions run properly. Secondly, non-containerized utility functions are tested using the pytest library. Future testing efforts may also be expanded to cover infrastructure functionality such as data_preprocessing and fine_tuning, but integration testing is currently focused on end-user interacting and other application-critical functions.

All test files are located in the tests folder, with the integration_tests folder intended to hold test functions for containerized functions.

### Unit Tests

In the unit test functionality, we test individual, auxiliary functions that are not part of a specific container.

- test_semantic_split.py: Contains tests for the semantic_split.py functionality used to preprocess text before pushing it to the vector database.
- integration_tests: Tests of containerized functions.

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

To run the integration tests - first navigate to the vector_db folder and run **sh docker-shell.sh**. Then in a separate terminal, navigate to the api_service folder and run **sh docker-shell.sh**. Then with those two containers running, run **pipenv run pytest tests/integration_tests/test_rag_chat.py**. This will run the file with tests for the rag llm functionality.

To run the system tests, simply run **pipenv run pytest tests/test_semantic_splitter.py** in the root directory of the project.
