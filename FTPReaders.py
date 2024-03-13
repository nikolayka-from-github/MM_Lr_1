import re
import wget
import os.path


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
        # print(self.__Numb_Sat)
        # print(temp_id)
        self.__All_dict["Numb_Sat"] = self.__Numb_Sat
        self.__All_dict["Id_Sat"] = temp_id
        self.__All_dict["Arr_Time"] = self.__Arr_Time
        print(self.__All_dict["Arr_Time"])

        return self.__All_dict


class RinexReader(FTPReader):

    def __init__(self, url, user_name="anonymous", user_pass=""):
        super().__init__(url, user_name, user_pass)

    def Read(self, path, name):
        self._link = self._link + path + "/" + name
        if not os.path.exists(name):
            wget.download(self._link)
        else:
            print("Working with a file <...>")
        return 1
