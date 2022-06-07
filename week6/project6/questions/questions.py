import math

import nltk
import os
import string
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 10


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
    for filename in filenames:
        print(filename)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            files[filename] = open(f, "r", encoding='utf-8').read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by converting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = string.punctuation
    document = document.casefold()
    tokens = [word for word in nltk.tokenize.word_tokenize(document)
              if word not in stopwords and word not in punctuation]
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_doc_appearances = dict()
    for title, document in documents.items():
        for word in document:
            if word not in word_doc_appearances:
                word_doc_appearances[word] = {title}
            else:
                word_doc_appearances[word].add(title)

    idfs = dict()
    for title, document in documents.items():
        for word in document:
            if word in idfs:
                continue

            idf = math.log(len(documents) / len(word_doc_appearances[word]))
            idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = {
        title: sum([file.count(word) * idfs[word] if word in idfs else 0 for word in query])
        for title, file in files.items()
    }

    return [title for title, _ in sorted(tfidfs.items(), key=lambda item: item[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = string.punctuation
    sentence_word_counts = {
        sentence: len([word for word in nltk.tokenize.word_tokenize(sentence)
                       if word not in stopwords and word not in punctuation])
        for sentence in sentences
    }

    # query_rank = {
    #     sentence: (sum([idfs[word] if word in idfs and word in sentence else 0 for word in query]),
    #                sum([sentence.count(word) for word in query]) / sentence_word_counts[sentence])
    #     for sentence in sentences
    # }

    query_rank = dict()
    for sentence in sentences:
        matching_word_measure = sum([idfs[word] if word in idfs and word in sentence else 0 for word in query])
        word_appearances = sum([sentence.count(word) for word in query])
        query_term_density = word_appearances / sentence_word_counts[sentence]
        query_rank[sentence] = (matching_word_measure, query_term_density)

    return [sentence for sentence, _ in sorted(query_rank.items(), key=lambda item: item[1], reverse=True)][:n]


if __name__ == "__main__":
    main()
