import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as file:

        int_fields = {"Administrative", "Informational", "ProductRelated", "Month", "OperatingSystems", "Browser",
                      "Region", "TrafficType", "VisitorType", "Weekend"}
        float_fields = {"Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates",
                        "ExitRates", "PageValues", "SpecialDay"}
        month_map = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "June": 6, "Jul": 7, "Aug": 8, "Sep": 9,
                     "Oct": 10, "Nov": 11, "Dec": 12}
        visitor_map = {"Returning_Visitor": 1}

        csv_reader = csv.reader(file, delimiter=',')
        is_header = True
        labels = []
        evidence = []
        for line in csv_reader:
            if is_header:
                headers = line
                is_header = False
            else:
                row = []
                for i in range(len(headers)):
                    header = headers[i]
                    item = line[i]

                    if header in int_fields:
                        if header == "Month":
                            row.append(month_map[item])
                        elif header == "VisitorType":
                            row.append(visitor_map.get(item, 0))
                        elif header == "Weekend":
                            row.append(1 if item == "TRUE" else 0)
                        else:
                            row.append(int(item))
                    elif header in float_fields:
                        row.append(float(item))
                    elif header == "Revenue":
                        labels.append(1 if item == "TRUE" else 0)
                    else:
                        raise Exception(f"Unidentified header '{header}' in dataset.")

                if len(row) != 17:
                    raise Exception(f"Evidence row is of length '{len(evidence)}'. Should be '17'.")
                evidence.append(row)

    if len(evidence) != len(labels):
        raise Exception(f"Evidence length '{len(evidence)}' differs to Labels length '{len(labels)}'.")

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    total_positives = 0
    correct_positives = 0
    total_negatives = 0
    correct_negatives = 0

    for label, prediction in zip(labels, predictions):

        if label == 1:
            total_positives += 1
            if prediction == 1:
                correct_positives += 1
        else:
            total_negatives += 1
            if prediction == 0:
                correct_negatives += 1

    sensitivity = correct_positives / total_positives
    specificity = correct_negatives / total_negatives

    return sensitivity, specificity


if __name__ == "__main__":
    main()
