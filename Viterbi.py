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
    tag_count = Counter()
    tag_given_tag_count = defaultdict(Counter)
    word_given_tag_count = defaultdict(Counter)

    for tag_list, words_list in zip(tags, words):
        prev_tag = "BOS"
        for tag, word in zip(tag_list, words_list):
            if "|" in tag:
                tag = tag.split("|")[1]
            # print(tag)
            if prev_tag == "BOS":
                tag_count["BOS"] += 1
            tag_count[tag] += 1
            word_given_tag_count[word][tag] += 1
            tag_given_tag_count[prev_tag][tag] += 1
            prev_tag = tag

    # print(f"tag_count: {tag_count}")
    # print('_'*50)
    # print(f"tag_given_tag_count: {tag_given_tag_count}")
    # print('_' * 50)
    # print(f"word_given_tag_count: {word_given_tag_count['said']}")
    # print('_' * 50)

    return tag_count, word_given_tag_count, tag_given_tag_count


def viterbi(test_sentences, tag_count, word_given_tag_count, tag_given_tag_count):
    score = defaultdict(float)
    backptr = defaultdict(str)
    unique_tags = list(tag_count.keys())
    predicted_tag_list_of_lists = []

    for sentence in test_sentences:

        predicted_tag_list = []
        # Initialization Step
        for tag in unique_tags:
            if tag != "BOS":
                prob_first_word_given_tag = word_given_tag_count[sentence[0]].get(tag, 0) / tag_count.get(tag, 1)
                prob_tag_given_bos = tag_given_tag_count["BOS"].get(tag, 0) / tag_count.get("BOS", 1)

                score[(tag, sentence[0])] = prob_first_word_given_tag * prob_tag_given_bos
                backptr[(tag, 0)] = "BOS"

        # Iteration Step
        for w in range(1, len(sentence)):
            for tag in unique_tags:
                if tag != "BOS":
                    max_score = -1
                    max_tag = None
                    prob_w_tag = word_given_tag_count[sentence[w]].get(tag, 0) / (tag_count.get(tag, 1))

                    for prev_tag in unique_tags:
                        if prev_tag != "BOS":
                            prob_tag_given_prevtag = tag_given_tag_count[prev_tag].get(tag, 0) / (
                                tag_count.get(prev_tag, 1))
                            current_score = score.get((prev_tag, sentence[w - 1]), 0) * prob_tag_given_prevtag
                            if current_score > max_score:
                                max_score = current_score
                                max_tag = prev_tag

                    score[(tag, sentence[w])] = prob_w_tag * max_score
                    backptr[(tag, sentence[w])] = max_tag

        # Sequence Identification Step
        max_final_score = -1
        max_final_tag = None
        for tag in unique_tags:
            if tag != "BOS":
                final_score = score.get((tag, sentence[-1]), 0)
                if final_score > max_final_score:
                    max_final_score = final_score
                    max_final_tag = tag

        current_tag = max_final_tag
        for w in range(len(sentence) - 1, -1, -1):
            predicted_tag_list.insert(0, current_tag)
            current_tag = backptr[(current_tag, sentence[w])]
        predicted_tag_list_of_lists.append(predicted_tag_list)

    tagged_sentences = []
    for senten, tags in zip(test_sentences, predicted_tag_list_of_lists):
        tagged_sentence = ' '.join([f"{word}/{tag}" for word, tag in zip(senten, tags)])
        tagged_sentences.append(tagged_sentence)

    return predicted_tag_list_of_lists, tagged_sentences


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


def write_to_file(tagged_sentences, file_name="POS.test.out"):
    with open(file_name, 'w') as f:
        for sentence in tagged_sentences:
            f.write(sentence + '\n')


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

    tag_count, word_given_tag_count, tag_given_tag_count = counts(tag_list, word_list)

    predicted_tag_list, tagged_sentences = viterbi(test_sentences, tag_count, word_given_tag_count, tag_given_tag_count)

    if train_file != "POS.train.large":
        write_to_file(tagged_sentences)
    accuracy = calculate_accuracy(test_tag_list, predicted_tag_list)

    print(f"Accuracy: {accuracy} %")


if __name__ == "__main__":
    main()
