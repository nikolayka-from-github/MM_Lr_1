# import re
import wget
import os.path
import math


class FTPReader:
    _url = ""
    _name = ""
    _user_name = ""
    _user_pass = ""
    _link = ""

    def __init__(self, url, user_name, user_pass):
        self._url = url
        self._user_name = user_name
        self._user_pass = user_pass
        self._link = url + "/"

    def Read(self, path, name):
        self._link = self._link + path + "/" + name
        if not os.path.exists(name):
            wget.download(self._link)
        # return NotImplementedError(f"In the <{self.__name__}> class, the method must be redefined <Read>")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url


class SP3Reader(FTPReader):
    __Numb_Sat = 0
    __Arr_Time = []
    __y_0 = 0
    __M_0 = 0
    __d_0 = 0
    __h_0 = 0
    __m_0 = 0
    __s_0 = 0.
    __All_dict = {}

    def __init__(self, url, user_name="anonymous", user_pass=""):
        super().__init__(url, user_name, user_pass)

    def Read(self, path, name):
        super().Read(path, name)
        with open(name) as file:
            str_id = ""
            temp_curr_time = 0.0
            while line := file.readline():
                line = line.split()
                if line[0][0] == 'P':
                    temp_arr_ = []
                    line = line[1:5]
                    for i in range(0, 4):
                        temp_arr_.append(float(line[i]))
                    self.__All_dict[temp_curr_time].append(temp_arr_)
                elif line[0] == '*':
                    temp_curr_time = (int(line[3]) - self.__d_0) * 24 + int(line[4]) + int(line[5]) / 60
                    self.__All_dict[temp_curr_time] = []
                    self.__Arr_Time.append(temp_curr_time)
                elif line[0] == '+':
                    if len(line) == 3:
                        str_id += line[2]
                    else:
                        str_id += line[1]
                elif len(line[0]) == 7:
                    self.__y_0 = int(line[0][3:7])
                    self.__M_0 = int(line[1])
                    self.__d_0 = int(line[2])
                    self.__h_0 = int(line[3])
                    self.__m_0 = int(line[4])
                    self.__s_0 = float(line[5])
        temp_id = []
        counter = 0
        temp_str = ''
        for i in str_id:
            if counter == 3:
                temp_id.append(temp_str)
                temp_str = ''
                counter = 0
            temp_str += i
            counter += 1
        temp_id.append(temp_str)

        self.__Numb_Sat = len(temp_id)
        self.__All_dict["Numb_Sat"] = self.__Numb_Sat
        self.__All_dict["Id_Sat"] = temp_id
        self.__All_dict["Arr_Time"] = self.__Arr_Time

        return self.__All_dict


class RinexReader(FTPReader):  # Only for GNSS!!!

    __y_0 = 0
    __M_0 = 0
    __d_0 = 0
    __h_0 = 0
    __m_0 = 0
    __s_0 = 0.

    def __init__(self, url, user_name="anonymous", user_pass=""):
        super().__init__(url, user_name, user_pass)

    @staticmethod
    def split_to_time(line):
        s = 0
        y = int(line[1])
        m_ = int(line[2])
        d = int(line[3])
        h = int(line[4])
        m = int(line[5])
        if len(line[6]) > 2:
            if line[6][1] == '-':
                s = float(line[6][0])
            else:
                s = float(line[6][0:2])
        elif len(line[6]) == 1:
            s = float(line[6])

        return y, m_, d, h, m, s

    @staticmethod
    def split_to_exp(line):
        for i in range(0, 4):
            v_len = len(line[i])
            pow_exp = int(line[i][v_len - 2:v_len])
            sign_pow_exp = -1
            if line[i][v_len - 3] == "+":
                sign_pow_exp = 1
            value__exp = float(line[i][0:v_len - 4])
            line[i] = value__exp*pow(10, sign_pow_exp*pow_exp)
        return line

    @staticmethod
    def split_to_f_value(line):
        temp_line = ""
        arr_line = []
        temp_srt_value = ""
        for i in line:
            temp_line += i
        counter = 0
        bool_d = False
        for i in temp_line:
            temp_srt_value += i
            if i == "D":
                bool_d = True
                continue
            if bool_d:
                counter += 1
            if counter == 3:
                arr_line.append(temp_srt_value)
                temp_srt_value = ""
                counter = 0
                bool_d = False
        return arr_line

    def Read(self, path, name):
        super().Read(path, name)
        with open(name) as file:
            str_id = ""
            temp_curr_time = []
            counter_broad = 1
            flag_broad = False
            init_time = False
            while line := file.readline():
                line = line.split()
                if line[0][0] == 'R':
                    flag_broad = True
                    if init_time:
                        init_time = False
                        [self.__y_0, self.__M_0, self.__d_0,
                         self.__h_0, self.__m_0,  self.__s_0] = self.split_to_time(line)
                    else:
                        line = self.split_to_time(line)
                elif flag_broad:
                    counter_broad += 1
                    if len(line) == 4:
                        line = self.split_to_exp(line)
                    else:
                        temp_line = self.split_to_f_value(line)
                        line = self.split_to_exp(temp_line)
                    if counter_broad == 4:
                        flag_broad = False

                print(line)
        print(self.__y_0)
        print(self.__M_0)
        print(self.__d_0)
        print(self.__h_0)
        print(self.__m_0)
        print(self.__s_0)
        return 1
