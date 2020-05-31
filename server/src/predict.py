
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle
import os

def extract_features(word_list):
    return dict([(word, True) for word in word_list])

def train(model_path):

    print('Training....')
    # Load positive and negative reviews  
    positive_fileids = movie_reviews.fileids('pos')
    negative_fileids = movie_reviews.fileids('neg')

    features_positive = [(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in positive_fileids]
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in negative_fileids]


    # Split the data into train and test (80/20)
    threshold_factor = 0.8
    threshold_positive = int(threshold_factor * len(features_positive))
    threshold_negative = int(threshold_factor * len(features_negative))

    features_train = features_positive[:threshold_positive]+features_negative[:threshold_negative]
    features_test = features_positive[threshold_positive:]+features_negative[threshold_negative:]

    print("Number of training datapoints: ", len(features_train))
    print("Number of test datapoints: ", len(features_test)) 


    classifier = NaiveBayesClassifier.train(features_train)
    print("Accuracy of the classifier: ", nltk.classify.util.accuracy(classifier, features_test))

    print("Top ten most informative words: ")

    for item in classifier.most_informative_features()[:10]:
        print(item[0])

    save_classifier = open("naivebayes.pickle","wb")
    pickle.dump(classifier, save_classifier)
    save_classifier.close()

    return classifier


model_path = "naivebayes.pickle"
train_allow = not(os.path.exists(model_path))

if train_allow:
    classifier = train(model_path)
else:
    print("Loading model from file")
    classifier_f = open(model_path, "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()




def predict(input_reviews, comparer, allow_print = True):
    accuracies = []
    if allow_print:
        print("Predictions: ")
    total_score = 0

    for review in input_reviews:
        if allow_print:
            print("\nReview:", review)

        probdist = classifier.prob_classify(extract_features(review.split()))
        pred_sentiment = probdist.max()

        if allow_print:
            print(pred_sentiment)

        score = 0
        if pred_sentiment == "Positive":
            score = 1
        elif pred_sentiment == "Negative":
            score = -1
        
        score *= comparer
        accuracies.append(score)
        total_score += score

        #print("Probability: ", round(probdist.prob(pred_sentiment), 2))
    if allow_print:
        print(accuracies)

    avg = total_score / len(accuracies)

    return avg


