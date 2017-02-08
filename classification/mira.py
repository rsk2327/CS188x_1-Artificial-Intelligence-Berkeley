# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        weights = []
        maxAccuracy = 0
        selectedC = Cgrid[0]
        finalWeights=0

        for c in Cgrid:
            self.initializeWeightsToZero()

            for iteration in range(self.max_iterations):
                for i in range(len(trainingData)):
                    y_value = self.classify([trainingData[i]])[0]
                    # print y_value
                    if y_value!=trainingLabels[i]:
                        t = (((self.weights[y_value] - self.weights[trainingLabels[i]])*trainingData[i]) + 1.0)/(2*(trainingData[i]*trainingData[i]))
                        t_final = min(t,c)

                        

                        for key in trainingData[i]:
                            # print "key : "+str(key)
                            # print self.weights[trainingLabels[i]][key]
                            # print trainingData[i][key]
                            self.weights[trainingLabels[i]][key] += trainingData[i][key]*t_final
                            # print self.weights[trainingLabels[i]][key]
                            # print "************"
                        for key in trainingData[i]:
                            self.weights[y_value][key] -= trainingData[i][key]*t_final

                        
           
            pred_labels = self.classify(validationData)
            accuracy = self.getAccuracy(pred_labels,validationLabels)
            
            

            if accuracy>maxAccuracy:

                maxAccuracy = accuracy
                selectedC = c
                finalWeights = self.weights

            weights.append(self.weights)

      
        self.weights = finalWeights



    def getAccuracy(self,pred,truth):

       
        count = 0
        for i in range(len(pred)):
            if pred[i]==truth[i]:
                count += 1

        return (count/float(len(pred)))

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


