import tensorflow as tf
import tensorflow.python.keras as keras

MODEL_PATH = '/dlModel'


def processData():  # DB 안의 데이터를 모델 학습에 맞게 전처리하여 리턴
    '''
        전처리
    '''
    X = []
    Y = []
    return (X, Y)


def trainModel():  # 모델을 생성하여 훈련하여 리턴

    X, Y = processData()

    model = keras.models.Sequential([
        # ....레이어들
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam')
    model.fit(X, Y, epochs=100, verbose=0)

    return model


def predictDirection(model, data):  # True: Down, False: Up
    return model.predict_classes(data)


def changeAirCondition(data, down: bool = True):  # 공조 장치를 제어하는 함수
    '''
        공조 장치 제어 코드
    '''
    return data


def optimizeEnvironment(data):  # 현재 상태 데이터로 부터 최적의 온도를 찾아 조절한다.
    prevDir = None
    currDir = None
    model = None

    try:  # 모델이 존재하면 불러오고 아니면 새로 만든다.
        model = keras.models.load_model(MODEL_PATH)
    except:
        model = trainModel()
        keras.models.save_model(model, MODEL_PATH)

    while(prevDir == currDir):  # 온도 조절의 방향이 바뀌면 최적 지점에 도달한 것으로 판단
        dir = predictDirection(model, data)
        data = changeAirCondition(data, dir)

        prevDir = currDir
        currDir = dir
