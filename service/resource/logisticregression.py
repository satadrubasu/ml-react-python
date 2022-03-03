from flask_restful import Resource,reqparse
from processors.lrprocessor import LogisticRegressionAlgo

class LogRegression(Resource):

    processor = LogisticRegressionAlgo.get_instance()


    parser = reqparse.RequestParser()
    ##parser will only pick the elements mentioned below
    parser.add_argument('fileLocation',
                        type=str,
                        required=False,
                        help="fileLocation - point to a file location for server to train."
                        )
    parser.add_argument('fileName',
                        type=str,
                        required=False,
                        help="fileName - "
                        )
    parser.add_argument('inputKey',
                        type=dict,
                        required=False,
                        help="inputKey - to hold nested json of all input args needed for prediction"
                        )

    # [/info /status / predict / serialize ]
    def get(self,name):
        actions = ['info','status','predict','save','load']
        resp = {}
        print(f" Action called - {name}")

        parsed_data = LogRegression.parser.parse_args()

        if name=='info':
            resp = LogRegression.processor.getInfo()
            print(f"Response Info : {resp}")

        elif name=='status':
            resp = LogRegression.processor.getStatus()
            print(f"Status Info : {resp}"),200

        elif name=='predict':
            print(f"predict called :")
            inputMap = parsed_data['inputKey']
            print(type(inputMap))
            if not inputMap:
                return {"errorMessage": "Expected input key values withing parent key = inputKey"}, 400
            try:
                resp = LogRegression.processor.predict(inputMap)
            except (Exception ) as e:
                return {"errorMessage": str(e)}, 500

        elif name=='save':
            print(f"save called :")
            try:
                fileName = parsed_data['fileName']
                if not fileName:
                    return {"errorMessage": "Expected file name value for key = fileName"}, 400
                print(f'File Name : {fileName}')
                resp = LogRegression.processor.saveTrainedModel(fileName)
            except (Exception ) as e:
                return {"errorMessage": str(e) } ,500

        elif name=='load':
            try:
                fileName = parsed_data['fileName']
                if not fileName:
                    return {"errorMessage": "Expected file name value for key = fileName"}, 400
                print(f'File Name : {fileName}')
                resp = LogRegression.processor.loadTrainedModel(fileName)
                print(f"predict called : {resp}")
            except (Exception) as e:
                return {"errorMessage": str(e)}, 500
        else:
            return {'errorMessage':f'Incorrect Algo get method actions ! {str(actions)}'}, 400

        return resp,200

    # train - fileLocation = Server absolute path holding the xlsx data file
    # pretrain - fileLocation = Server absolute path holding the serialized file

    def post(self,name):  ## name - from Url
        parsed_data = LogRegression.parser.parse_args()
        try:
            fileLocation = parsed_data['fileLocation']
            if name=='train':
                resp = LogRegression.processor.startTrainWithFile(fileLocation)
            elif name=='pretrain':
                resp = LogRegression.processor.loadTrainedModel(fileLocation)

        except (Exception ) as e:
            return{"errorMessage":f"An Error occured processing the request = {e}"},500 # Internal server error

        ## Returning JSON Object
        responseDict = {"msg":"Training Accepted. In progress .. "}
        return responseDict , 201 # Created
