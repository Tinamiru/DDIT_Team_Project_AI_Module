import numpy as np
from tensorflow import keras
from keras import datasets, models, layers
from keras.utils import to_categorical
from module.dr_crown_dao import DrCrownDao

class Recommend:
    def __init__(self):
        self.de = DrCrownDao()
        self.model1 = keras.models.load_model('D:/Dr_Crown_AI/module/model/brushing.h5')
        self.model2 = keras.models.load_model('D:/Dr_Crown_AI/module/model/paste.h5')
        self.model3 = keras.models.load_model('D:/Dr_Crown_AI/module/model/brush.h5')
        self.model4 = keras.models.load_model('D:/Dr_Crown_AI/module/model/gargel.h5')
        
        self.brushingList = self.de.getRecommend("A001")
        self.brushList = self.de.getRecommend("A002")
        self.pasteList = self.de.getRecommend("A003")
        self.gargleList = self.de.getRecommend("A004")
        
    def getTeethByPatient(self,p_id):
        # p_id = "1"
        
        timeNum = self.de.getTime(p_id)
        age = self.de.getAge(timeNum)
        result = self.de.getPatientData(p_id)
        # print("age",age)        
        # print("result",result)
        datas = []
        
        if age <= 6:
            datas.append(0)
            datas.append(0)
        elif age > 6 and age <= 30:
            datas.append(0)
            datas.append(1)
        elif age > 30 and age <= 50:
            datas.append(1)
            datas.append(0)
        elif age > 50:
            datas.append(1)
            datas.append(1)
        for i in result:
            if i=='y':
                datas.append(1)
            else:
                datas.append(0)
        # print("datas",datas)
        
        
        
        train_images_a = [datas]
        
        # print("train_images_a",train_images_a)

        train_images_n = np.array(train_images_a)
        # print(train_images_n.shape)
        self.model1.predict(train_images_n)
        self.model2.predict(train_images_n)
        self.model3.predict(train_images_n)
        self.model4.predict(train_images_n)
        
        predictions1 = self.model1.predict(train_images_n)
        predictions2 = self.model2.predict(train_images_n)
        predictions3 = self.model3.predict(train_images_n)
        predictions4 = self.model4.predict(train_images_n)

        idx1 =np.argmax(predictions1[0])
        idx2 =np.argmax(predictions2[0])
        idx3 =np.argmax(predictions3[0])
        idx4 =np.argmax(predictions4[0])
        # print("idx",idx)
        # print("teethList",self.teethList)
        
        return(self.brushingList[idx1],self.pasteList[idx2],self.brushList[idx3],self.gargleList[idx4])
    