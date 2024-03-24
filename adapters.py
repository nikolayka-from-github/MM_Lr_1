# coding=utf-8
# from readers import SP3Reader  # , RINReader, Readers
import os

Mm = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def GetDWeek_06_01_1980(yyyy: int, mm: int, dd: int):
    t_y = yyyy - 1980
    c_y_plus = int(t_y / 4)
    if t_y % 4 != 0:
        c_y_plus += 1
    d_y = t_y * 365 + c_y_plus + GetDatInYear(yyyy=yyyy, mm=mm, dd=dd) - 6
    m_d = int(d_y / 7)
    d_n = d_y % 7

    return [m_d, d_n]


def GetDatInYear(yyyy: int, mm: int, dd: int):
    day_plus = 0
    int_flag = yyyy % 4
    if int_flag == 0:
        day_plus = 1
    d_m = 0
    for i in range(1, mm):
        d_m += Mm[i]
    if mm > 2:
        d_m += day_plus
    return d_m + dd


class Adapter:

    def __init__(self, url: str):
        self._url = url

    def get_data(self, path):
        return None

    def forming_path(self, data):
        return None


class SP3ReadAdapter(Adapter):
    _folder = "/MCC/PRODUCTS/"

    def __init__(self, url: str, data: str, obj):
        super().__init__(url)
        self._obj = obj
        self._data = data
        self._link = self.forming_path(data)

    def forming_path(self, data: str):
        data = self._data.split(".")
        day = GetDatInYear(yyyy=int(data[2]), mm=int(data[1]), dd=int(data[0]))
        week = GetDWeek_06_01_1980(yyyy=int(data[2]), mm=int(data[1]), dd=int(data[0]))
        full_path = self._url + self._folder
        if len(data[2]) == 4:
            data[2] = data[2][2:5]
        day = str(day)
        day = "0" * (3 - len(day)) + day
        full_path = full_path + data[2] + day + f"/final/Sta{week[0]}{week[1]}.sp3"
        return full_path

    def get_data(self, sat_id: str):
        data = self._obj.read(self._link)
        x = []
        y = []
        z = []
        time = data['Arr_Time']
        index_sat = data['Id_Sat'].index(sat_id)

        for i in time:
            pos = data[i][index_sat]
            x.append(pos[0])
            y.append(pos[1])
            z.append(pos[2])

        res_data = []
        res_data.append(x)
        res_data.append(y)
        res_data.append(z)
        res_data.append(time)
        return res_data


class RINReadAdapter(Adapter):
    _folder = "/MCC/BRDC/"

    def __init__(self, url: str, data: str, obj):
        super().__init__(url)
        self._obj = obj
        self._data = data
        self._link = self.forming_path(data)

    def forming_path(self, data: str):
        data = self._data.split(".")
        day = GetDatInYear(yyyy=int(data[2]), mm=int(data[1]), dd=int(data[0]))
        week = GetDWeek_06_01_1980(yyyy=int(data[2]), mm=int(data[1]), dd=int(data[0]))
        full_path = self._url + self._folder
        temp2_year = str(data[2][2:5])
        day = str(day)
        day = "0" * (3 - len(day)) + day + "0"
        full_path = full_path + data[2] + f"/Brdc{day}.{temp2_year}g"
        # print(full_path)
        return full_path

    def get_data(self, sat_id: str):
        data = self._obj.read(self._link)
        x = []
        y = []
        z = []
        time = data['Arr_Time']
        index_sat = data['Id_Sat'].index(sat_id)

        for i in time:
            pos = data[i][index_sat]
            x.append(pos[0])
            y.append(pos[1])
            z.append(pos[2])

        res_data = []
        res_data.append(x)
        res_data.append(y)
        res_data.append(z)
        res_data.append(time)
        return res_data
