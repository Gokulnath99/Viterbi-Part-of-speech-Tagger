import sys
from collections import defaultdict, Counter


def read_file(file_name):
    with open(file_name, 'r') as f:
        corpus = f.readlines()
    word_tags_lists = []
    for sentence in corpus:
        word_tags_lists.append(sentence.split())

    return word_tags_lists


def counts(tags, words):
    word_given_tag_count = defaultdict(Counter)

    for tag_list, words_list in zip(tags, words):
        prev_tag = "BOS"
        for tag, word in zip(tag_list, words_list):
            if "|" in tag:
                tag = tag.split("|")[1]
            word_given_tag_count[word][tag] += 1

    # print(f"word_given_tag_count: {word_given_tag_count}")
    # print('_' * 50)

    return word_given_tag_count


def calculate_accuracy(test_tag_list, predicted_tag_list):
    correct_count = 0
    total_count = 0

    for test_tags, predicted_tags in zip(test_tag_list, predicted_tag_list):
        for test_tag, predicted_tag in zip(test_tags, predicted_tags):
            total_count += 1
            if test_tag == predicted_tag:
                correct_count += 1

    accuracy = (correct_count / total_count * 100) if total_count else 0
    return accuracy


def baseline(test_sentences, word_given_tag_count):
    predicted_tag_list_of_lists = []

    for sentence in test_sentences:
        predicted_tag_list = []
        for word in sentence:
            if word_given_tag_count[word]:
                predicted_tag = word_given_tag_count[word].most_common(1)[0][0]
            else:
                predicted_tag = "NN"
            predicted_tag_list.append(predicted_tag)
        predicted_tag_list_of_lists.append(predicted_tag_list)

    return predicted_tag_list_of_lists


def main():
    train_file = sys.argv[1]
    test_file = sys.argv[2]

    word_tags_lists = read_file(train_file)
    test_word_tags_lists = read_file(test_file)

    tag_list = []
    word_list = []

    for word_tag_list in word_tags_lists:
        tag = []
        words = []
        for word_tag in word_tag_list:
            if '/' in word_tag:
                words.append(word_tag.split('/')[:-1][0])
                tag.append(word_tag.split('/')[-1])
        word_list.append(words)
        tag_list.append(tag)

    test_tag_list = []
    test_sentences = []
    for word_tag_list in test_word_tags_lists:
        list_of_sentence = []
        list_of_tag = []
        for word_tag in word_tag_list:
            list_of_sentence.append(word_tag.split('/')[:-1][0])
            list_of_tag.append(word_tag.split('/')[-1])
        test_sentences.append(list_of_sentence)
        test_tag_list.append(list_of_tag)

    word_given_tag_count = counts(tag_list, word_list)

    predicted_tag_list = baseline(test_sentences, word_given_tag_count)

    accuracy = calculate_accuracy(test_tag_list, predicted_tag_list)

    print(f"Accuracy: {accuracy} %")


if __name__ == "__main__":
    main()
