from FTPReaders import SP3Reader, RINReader
from adapters import SP3ReadAdapter, RINReadAdapter
from client import Client
"""
# coding=utf-8
# from FTPReaders import SP3Reader
# from FTPReaders import RinexReader, SP3Reader
#
# Url = "ftp://ftp.glonass-iac.ru"
# Path = "MCC/PRODUCTS/23340/final"
# File_name = "Sta22913.sp3"
#
# Path_r = "MCC/BRDC/2024"
# File_name_r = "Brdc0670.24g"
#
# sp3 = SP3Reader(url=Url)
# data = sp3.reading(Path, File_name)

# in data:
# 'Arr_Time' ... list
# 'Numb_Sat' ... int
# 'Id_Sat' ... list
# data:
# 'Arr_time[0]': x_0, y_0, z_0
#                x_1, y_1, z_1
#                ...
#                x_('Numb_Sat' - 1), y_('Numb_Sat' - 1), z_('Numb_Sat' - 1)
# 'Arr_time[1]': ...
# ...
# 'Arr_time[end]': ...
"""

if __name__ == '__main__':
    __url = "ftp://ftp.glonass-iac.ru"
    __data__ = "27.08.2023"
    __user_name = "Yakimenko"

    full_path = "ftp://ftp.glonass-iac.ru/MCC/PRODUCTS/23360/final/Sta22942.sp3"

    sp3 = SP3Reader()
    sp3A = SP3ReadAdapter(url=__url, data=__data__, obj=sp3)

    rin = RINReader()
    rinA = RINReadAdapter(url=__url, data=__data__, obj=rin)
    cl = Client(user_name=__user_name, obj=sp3A)
    cl.get_data("R17")
    cl.plot()

