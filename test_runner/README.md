### Test Documentation

The testing of gAIn source code is two-fold. Firstly, integration tests are run on the relevant containers in gAIn's infrastructure, to ensure that they all build correctly. Secondly, non-containerized utility functions are tested using the pytest library. Future testing efforts will include testing of functions in containerized applications as well, but because of the non-functional design of some of the code in each infrastructure container, such as data_scraping and data_preprocessing, this is not yet implemented.

All test files are located in the tests folder, with the integration_tests folder intended to hold future test functions for containerized functions.

### Unit Tests

In the unit test functionality, we test individual, auxiliary functions that are not part of a specific container.

- test_semantic_split.py: Contains tests for the semantic_split.py functionality used to preprocess text before pushing it to the vector database.
