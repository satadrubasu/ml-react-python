from processors.lrprocessor import LogisticRegressionAlgo


class ModelLR():
    processor = LogisticRegressionAlgo.get_instance()

    try:
        processor.startTrainWithFile()
    except (Exception ) as e:
        print(e)

    try:
        processor.predict()
    except (Exception ) as e:
        print(e)

    try:
        processor.saveTrainedModel()
    except (Exception ) as e:
        print(e)

    try:
        processor.loadTrainedModel()
    except (Exception ) as e:
        print(e)

    processor.getStatus()

    processor.getInfo()