import wget
import os.path


class Readers:
    def __init__(self, user_name="anon", user_pass=""):
        self.user_name = user_name
        self.user_pass = user_pass
        self.file_name = ""

    def downloading(self, path):
        self.file_name = path.split("/")[-1]
        if not os.path.exists(self.file_name):
            wget.download(path)

    def read(self, path):
        return None


class SP3Reader(Readers):
    __Numb_Sat = 0
    __Arr_Time = []
    __y_0 = 0
    __M_0 = 0
    __d_0 = 0
    __h_0 = 0
    __m_0 = 0
    __s_0 = 0.
    __All_dict = {}
    __NUMB = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def my_split(self, line: str):
        new_line = []
        new_line.append(line[0:4].replace(" ", ""))
        new_line.append(line[4:18].replace(" ", ""))
        new_line.append(line[18:32].replace(" ", ""))
        new_line.append(line[32:46].replace(" ", ""))
        new_line.append(line[46:60].replace(" ", ""))
        # print(f"///{line[0:4]}///")
        # print(f"///{line[4:18]}///")
        # print(f"///{line[18:32]}///")
        # print(f"///{line[32:46]}///")
        # print(f"///{line[46:60]}///")
        return new_line

    def split_to_float(self, line):
        temp_arr = []
        temp_str = ""
        i_ = ""
        for i in line:
            if i == "-" and i_ in self.__NUMB:
                temp_arr.append(temp_str)
                temp_str = ""
            temp_str += i
            i_ = i
        temp_arr.append(temp_str)
        return temp_arr

    def __init__(self, user_name="anon", user_pass=""):
        super().__init__(user_name, user_pass)

    def read(self, path):
        super().downloading(path)
        # print(self.file_name)
        with open(self.file_name) as file:
            str_id = ""
            temp_curr_time = 0.0
            while line := file.readline():
                temp_line = line
                line = line.split()

                if line[0][0] == 'P':
                    temp_arr_ = []
                    line = self.my_split(temp_line)[1:5]
                    for i in range(0, 4):
                        # '22525.703927-153056.312033'
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


class RINReader(Readers):
    __All_dict = {}
    __Arr_Time = []
    __y_0 = 0
    __M_0 = 0
    __d_0 = 0
    __h_0 = 0
    __m_0 = 0
    __s_0 = 0.

    def __init__(self, user_name: str = "anon", user_pass: str = ""):
        super().__init__(user_name=user_name, user_pass=user_pass)

    # @property
    # def URL(self):
    #     return self.__url
    #
    # @URL.setter
    # def URL(self, url: str):
    #     self.__url = url

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
            line[i] = value__exp * pow(10, sign_pow_exp * pow_exp)
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

    def read(self, path):
        super().downloading(path)
        initialize_time = True
        initialize_id = True

        reading_data = False
        id_sheet = []
        time_sheet = []

        # current_time = 0.
        current_time_temp = 0.
        # previous_time = 0.
        counter_broad = 0
        temp_arr_pos = []
        with open(self.file_name) as file:
            while line := file.readline():
                line = line.split()

                if line[0][0] == 'R':
                    reading_data = True

                    if initialize_time:
                        initialize_time = False
                        [self.__y_0, self.__M_0, self.__d_0,
                         self.__h_0, self.__m_0, self.__s_0] = self.split_to_time(line)
                        current_time_temp = (self.__d_0 - self.__d_0) * 24 + self.__h_0 + self.__m_0 / 60
                        id_sheet.append(line[0])
                        time_sheet.append(current_time_temp)
                        self.__All_dict[current_time_temp] = []
                    else:
                        line_temp = self.split_to_time(line)
                        current_time_temp = (line_temp[2] - self.__d_0) * 24 + line_temp[3] + line_temp[4] / 60
                        if not (current_time_temp in self.__All_dict):
                            self.__All_dict[current_time_temp] = []
                            time_sheet.append(current_time_temp)
                            initialize_id = False
                        if initialize_id:
                            id_sheet.append(line[0])
                elif reading_data:
                    counter_broad += 1
                    if len(line) == 4:
                        line = self.split_to_exp(line)
                    else:
                        temp_line = self.split_to_f_value(line)
                        line = self.split_to_exp(temp_line)

                    temp_arr_pos.append(line[0])
                    if counter_broad == 3:
                        # flag_broad = False
                        reading_data = False
                        self.__All_dict[current_time_temp].append(temp_arr_pos)
                        temp_arr_pos = []
                        counter_broad = 0
        self.__All_dict["Numb_Sat"] = len(id_sheet)
        self.__All_dict["Id_Sat"] = id_sheet
        self.__All_dict["Arr_Time"] = time_sheet
        # print(self.__All_dict["Numb_Sat"])
        # print(self.__All_dict["Id_Sat"])
        # print(self.__All_dict["Arr_Time"])
        # self.__All_dict[current_time_temp]     self.__All_dict[0.25]
        # print(current_time_temp, len(self.__All_dict[current_time_temp]),  self.__All_dict[23.75])
        # print(time_sheet)
        # print(id_sheet)
        return self.__All_dict
