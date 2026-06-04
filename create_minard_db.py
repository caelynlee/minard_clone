import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        with open("data/minard.txt") as f:
            lines = f.readlines()

        #載入欄位名稱
        column_names = lines[2].split()  #txt檔案中第三行是欄位名稱

        #調整欄位名稱
        patterns_to_be_replaced = {"(","$",")",","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern,"")
            adjusted_column_names.append(column_name)
        self.lines = lines   
        self.column_names_city = adjusted_column_names[:3] #前3個欄位是城市資料
        self.column_names_temperature = adjusted_column_names[3:7] #第4-6個欄位是溫度資料
        self.column_names_troops = adjusted_column_names[7:] #第7個欄位後是軍隊資料
    def create_city_dataframe(self):            #載入城市資料
        i = 6  #index是從0開始的，所以第7行的index是6
        longtitudes, latitudes, cities = [], [], []
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]
            longtitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1
        city_data = (longtitudes, latitudes, cities)  # 後面要做成dataframe,所以放到tuple裡面
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df
    def create_temperature_dataframe(self):        #載入溫度資料
        i =6
        longtitudes, temperatures, days, dates = [], [], [], []
        while i <= 14: #溫度資料只到15列
            lines_split = self.lines[i].split()
            longtitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:          #第11行的日期資料是遺漏值，所以要依據資料邏輯特別處理
                dates.append("Nov 24")
            else:
                date_str = lines_split[6] +" "+ lines_split[7]  #日期資料是月份、日期分開兩個欄位，所以要把它們合併成一個字串
                dates.append(date_str)
            i += 1
        temperature_data = (longtitudes, temperatures, days, dates)
        temperature_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[column_name] = data
        return temperature_df
    def create_troop_dataframe(self):      #載入軍隊資料
        i= 6
        longtitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longtitudes.append(float(lines_split[-5]))
            i += 1
        troop_data = (longtitudes, latitudes, survivals, directions, divisions)
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troops, troop_data):
            troop_df[column_name] = data
        return troop_df
    def create_database(self):           #建立資料庫連線
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities": city_df,
            "temperatures": temperature_df,
            "troops": troop_df
        }
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")

create_minard_db = CreateMinardDB()      #初始化類別
create_minard_db.create_database()