import pathlib
import threading
from multiprocessing import Queue
import time
import pandas as pd
from enum import Enum

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support as score, f1_score

from dill import pickle
import dill


class TrainingThread (threading.Thread):
   def __init__(self, threadID, name, counter, model,fileLocation,feature_cols,q):

       threading.Thread.__init__(self)
       self.threadID = threadID
       self.name = name
       self.counter = counter
       self.model = model
       self.fileLocation = fileLocation
       self.feature_cols = feature_cols
       self.queue = q

   def run(self):
       print("------Thread Training Start :" + self.name)

       try:
           dataset = pd.read_excel(self.fileLocation)
           print(f"Data Sizing : {dataset.size}")


           inputKpiData = dataset[self.feature_cols]  # Features
           targetValue = dataset.Error_Bucket  # Target variable column name

          # splitting data for train & Test
           X_train, X_test, y_train, y_test = train_test_split(inputKpiData, targetValue, test_size=0.20, random_state=19)

          ## Training -  fit the model with data
           self.model.fit(X_train, y_train)

           y_pred = self.model.predict(X_test)

           precision, recall, fscore, support = score(y_test, y_pred , average='weighted')

          # f1score = precision + recall also as fscore
           fScore = f1_score(y_test, y_pred,average='weighted')
           accuracy = self.model.score(X_test,y_test)

           print('Thread Training :  precision: {}'.format(precision))
           print('Thread Training :  recall: {}'.format(recall))
           print('Thread Training :  f1 score: {}'.format(fscore))
           print('Thread Training :  support: {}'.format(support))
           print("------Thread Training :  FINISHED")

           completedStatus = {
               'status' : AlgoStatus.TRAINED,
               'accuracy' : accuracy,
               'f1score_weighted' : fScore,
               'trainedModel' : self.model
           }
           self.queue.put(completedStatus)
       except (Exception) as e:
           print(e)
           completedStatus = {
               'status': AlgoStatus.UNTRAINED,
               'accuracy': 0,
               'f1score_weighted': 0
           }
           self.queue.put(completedStatus)


class AlgoStatus(Enum):
    UNTRAINED = 1
    TRAINING = 2
    TRAINED = 3

class LogisticRegressionAlgo:
    __instance = None

    @staticmethod
    def get_instance():
        if LogisticRegressionAlgo.__instance == None:
            LogisticRegressionAlgo()
        return LogisticRegressionAlgo.__instance

    def __init__(self):
        if LogisticRegressionAlgo.__instance != None:
            raise Exception("Singleton..")
        else:

            self.name = "LogisticRegression"
            self.model = LogisticRegression()
            self.feature_cols = ["Node Count", "CPU_Usage", "Mem_Usage", "Hertz", "MEM_GB", "CPU_Count", "Hardisk_HDD1", "Total_TPS"]
            self.modelAccuracyPercentage = 0
            self.modelF1scorePercentage = 0
            self.status = AlgoStatus.UNTRAINED
            self.trainingThreadCounter = 0
            self.queue = Queue()
            LogisticRegressionAlgo.__instance  = self

    @staticmethod
    def updateStatus():
        print(f"updateStatus before method processing from Queue status")
        #print(f"Queue Size : {LogisticRegressionAlgo.__instance.queue.qsize}")
        if not LogisticRegressionAlgo.__instance.queue.empty():
            fetchStatus = LogisticRegressionAlgo.__instance.queue.get()

            print(fetchStatus)
            if fetchStatus:
                if fetchStatus.keys().__contains__('trainedModel'):
                    LogisticRegressionAlgo.__instance.model = fetchStatus['trainedModel']
                if fetchStatus.keys().__contains__('status'):
                    LogisticRegressionAlgo.__instance.status = fetchStatus['status']
                if fetchStatus.keys().__contains__('accuracy'):
                    LogisticRegressionAlgo.__instance.modelAccuracyPercentage = fetchStatus['accuracy']
                if fetchStatus.keys().__contains__('f1score_weighted'):
                    LogisticRegressionAlgo.__instance.modelF1scorePercentage = fetchStatus['f1score_weighted']

        print(f"updateStatus- END")

    @staticmethod
    def startTrainWithFile(fileLocation="/Users/satbasu/Downloads/ml_data-lr-test.xlsx"):
        # TODO : validate all keysets
        if LogisticRegressionAlgo.__instance.status == AlgoStatus.TRAINING:
            raise Exception("Training in Progress PLEASE WAIT !!")

        solitaryThread = TrainingThread(1,"trainingThread",
                                        LogisticRegressionAlgo.__instance.trainingThreadCounter+1,
                                        LogisticRegressionAlgo.__instance.model,
                                        fileLocation,
                                        LogisticRegressionAlgo.__instance.feature_cols,
                                        LogisticRegressionAlgo.__instance.queue)

        LogisticRegressionAlgo.__instance.status = AlgoStatus.TRAINING
        solitaryThread.start()
        print("Thread for training has been started , end of the method")

        # try:
        #     dataset = pd.read_excel(fileLocation)
        #     print(f"Data Sizing : {dataset.size}" )
        # except (Exception) as e:
        #     print(e)
        #     raise(e)
        #
        # LogisticRegressionAlgo.__instance.status = AlgoStatus.TRAINING
        # inputKpiData = dataset[LogisticRegressionAlgo.__instance.feature_cols]  # Features
        # targetValue = dataset.Error_Bucket  # Target variable column name
        #
        # # splitting data for train & Test
        # X_train, X_test, y_train, y_test = train_test_split(inputKpiData, targetValue, test_size=0.20, random_state=19)
        #
        # ## Training -  fit the model with data
        # LogisticRegressionAlgo.__instance.model.fit(X_train, y_train)
        #
        # y_pred = LogisticRegressionAlgo.__instance.model.predict(X_test)
        # # TODO - y_pred vs y_train accuracy
        # precision, recall, fscore, support = score(y_test, y_pred)
        #
        # # f1score = precision + recall also as fscore
        # LogisticRegressionAlgo.__instance.modelF1scorePercentage = f1_score(y_test, y_pred)
        # LogisticRegressionAlgo.__instance.modelAccuracyPercentage = LogisticRegressionAlgo.__instance.model.score(X_test, y_test)
        #
        # print('Training :  precision: {}'.format(precision))
        # print('Training :  recall: {}'.format(recall))
        # print('Training :  f1 score: {}'.format(fscore))
        # print('Training :  support: {}'.format(support))
        #print(f"### time taken in mins {(end_time_main-start_time_main)/60}")


    # Predict for a single row - ensure [[ data ]]
    @staticmethod
    def predict(inputMap):
        LogisticRegressionAlgo.__instance.updateStatus()
        if LogisticRegressionAlgo.__instance.status == AlgoStatus.TRAINING:
            raise Exception("Training in Progress cant predict now.. ")

        # orderedInputList will be loaded in sequence as defined in feature_cols
        orderedInputList = []
        index = 0
        try:
            for orderedKeyColumnName in LogisticRegressionAlgo.__instance.feature_cols:
                value = inputMap[orderedKeyColumnName]
                print(f"Value = {value} for Key = {orderedKeyColumnName}")
                orderedInputList.insert(index,value)
                index+=1
        except (Exception) as e:
            raise e
        # TODO : wrap the input list into array of array
        #y_predicted = LogisticRegressionAlgo.__instance.model.predict(orderedInputList)
        #return y_predicted
        return {"message" : "Prediction Done", "value": 200}

    @staticmethod
    def saveTrainedModel(name="lr_algo_save"):
        LogisticRegressionAlgo.__instance.updateStatus()
        if LogisticRegressionAlgo.__instance.status == AlgoStatus.TRAINING:
            raise Exception("Training in Progress cant save serialized file now")
        filename = name + ".dill"
        cwd = pathlib.Path.cwd()
        fullFilePath = str(cwd) + '/' + filename
        print(f"Saving Trained model to location : {fullFilePath}")
        try:
            with open(filename, "wb") as f:
                dill.dump(LogisticRegressionAlgo.__instance.model, f)
        except Exception as e:
            print(f"Unable to serialize Algo to file {fullFilePath}")
            raise Exception(f"Unable to serialize Algo to file {fullFilePath} : {e}")
        return {"message":f"Serialized to location {fullFilePath} on server host"}

    @staticmethod
    def loadTrainedModel(serialFileLocation):
        LogisticRegressionAlgo.__instance.updateStatus()
        if LogisticRegressionAlgo.__instance.status == AlgoStatus.TRAINING:
            raise Exception("Training in Progress cant load serialized file now")
        # TODO: proper implementation
        try:
            with open(serialFileLocation, "rb") as f:
                print(f"Loading model from serialFile {serialFileLocation}, using dill")
                LogisticRegressionAlgo.__instance.status = AlgoStatus.TRAINING
                LogisticRegressionAlgo.__instance.model = dill.load(f)
        except (Exception) as e:
            raise e
        print("Finished Loading model from serialFile onto memory")
        LogisticRegressionAlgo.__instance.status = AlgoStatus.TRAINED
        return {"message":f"Finished Loading model by dill load - {serialFileLocation}"}


    @staticmethod
    def getStatus():
        print(f"## Status Requested : {LogisticRegressionAlgo.__instance.status.name}")
        LogisticRegressionAlgo.__instance.updateStatus()

        while not LogisticRegressionAlgo.__instance.queue.empty():
            print(LogisticRegressionAlgo.__instance.queue.get())
        respDict = {'status': LogisticRegressionAlgo.__instance.status.name}
        return respDict

    @staticmethod
    def getInfo():
        print(f"## Info Requested : {LogisticRegressionAlgo.__instance.status}")
        LogisticRegressionAlgo.__instance.updateStatus()
        infoMapdict = {
            'name': LogisticRegressionAlgo.__instance.name ,
            'feature_cols': LogisticRegressionAlgo.__instance.feature_cols,
            'status': LogisticRegressionAlgo.__instance.status.name,
            'accuracy': LogisticRegressionAlgo.__instance.modelAccuracyPercentage,
            'f1score': LogisticRegressionAlgo.__instance.modelF1scorePercentage
        }
        return infoMapdict




