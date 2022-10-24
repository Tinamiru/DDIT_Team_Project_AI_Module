import cx_Oracle
import datetime
import math

class DrCrownDao:
    def __init__(self):
        self.conn = cx_Oracle.connect('team3_202204F/java@112.220.114.130:1521/xe')
 
        self.curs = self.conn.cursor()
        
    # 추천 라벨링 배열
    def getRecommend(self,r_code):
        sql = f"""select OSR_NAME
                from OS_RECOMMEND
                where osc_code = '{r_code}'
                order by OSR_NUMBER
                """
                
        arr = []
        
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        
        for row in rows:
            arr.append(row[0])
        return arr
    
    def getPatientData(self,brush_code):
        sql = f"""
                SELECT  cd.cd_gums AS "치주질환",
                        cd.cd_tartar AS "치석",
                        cd.cd_ORT AS "교정" ,
                        cd.cd_PRS AS "보철물"
                FROM PATIENT P
                JOIN CURE_DETAIL CD
                ON P.P_NO = CD.P_NO
                WHERE P.P_NO = {brush_code}
                order by cd.cd_regdate desc
                """
        
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        arr=[]
        for row in rows:
            arr.append(row[1])
        
        return rows[0]
        
        self.curs.execute(sql)
        rows = self.curs.fetchall()
        arr=[]
        for row in rows:
            arr.append(row[1])
        
        return rows[0]    

    def getTime(self,id):
        sql = f"""
                SELECT p_bir
                FROM PATIENT
                WHERE P_NO = {id}
                """
        self.curs.execute(sql)
        rows = self.curs.fetchone()
        return rows
    
    def getAge(self,time):
        dt_now = datetime.datetime.now()
        p_year = dt_now - time[0]
        
        return math.trunc(p_year.days/365)
    
    
    
    # def getYN(self,datas, age):
    #
    #     data = []
    #
    #     if age <= 6:
    #         data += 0,0,0,0
    #     elif age > 6 and age <= 30:
    #         data += 0,1,0,0
    #     elif age > 30 and age <= 50:
    #         data += 0,0,1,0
    #     elif age > 50:
    #         data += 0,0,0,1
    #
    #     for i in datas:
    #         if i == "y":
    #             data += [1]
    #         else:
    #             data += [0]
    #
    #     return data # 5가지 여부
    
    def __del__(self):
        # pass
        self.curs.close()
        self.conn.close()
        
