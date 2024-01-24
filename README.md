# Viterbi-Part-of-speech-Tagger

### Description

This repository contains the implementation of the Viterbi Algorithm for part-of-speech tagging, using the Penn Treebank tag set. The Viterbi algorithm, a dynamic programming approach, is used to assign the most probable sequence of tags to a given sequence of words in a sentence. This implementation is a key component of natural language processing tasks.

### Features

- **Viterbi Algorithm Implementation:** Python-based implementation of the Viterbi algorithm, specifically tailored for part-of-speech tagging.
- **Dataset Utilization:** Trains and tests on subsets of the Treebank dataset, including documents from various sources, manually annotated with part-of-speech tags.
- **Accuracy Measurement:** Compares the predicted tags against gold-standard tags to calculate the accuracy of the tagging system.
- **Output Generation:** Produces a file (`POS.test.out`) containing the test sentences with predicted part-of-speech tags.

### Usage

To run the program, use the following command:
```sh
python Viterbi.py POS.train POS.test
```
The program outputs the system accuracy in percentage and generates the `POS.test.out` file.

### Components

1. **Viterbi.py**: Main Python script implementing the Viterbi algorithm.
2. **baseline.py**: A baseline tagger for comparison purposes.

### Training and Testing

Two datasets are used:
- `POS.train` and `POS.test` for the initial training and testing.
- `POS.train.large` for training on a larger dataset and testing on the same `POS.test`.

### Requirements

- Python (with core libraries)
- Numpy (external libraries like Pandas and NLTK should not be used)
