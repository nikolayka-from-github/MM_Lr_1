# from FTPReaders import SP3Reader
from FTPReaders import RinexReader, SP3Reader

Url = "ftp://ftp.glonass-iac.ru"
Path = "MCC/PRODUCTS/23340/final"
File_name = "Sta22913.sp3"

Path_r = "MCC/BRDC/2024"
File_name_r = "Brdc0670.24g"

sp3 = SP3Reader(url=Url)
data = sp3.Read(Path, File_name)


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

rin = RinexReader(url=Url)
# data = rin.Read_1(Path_r, File_name_r)
print(data)
id_sat = 'R24'
index_sat = data['Id_Sat'].index(id_sat)
arr_time = data['Arr_Time']

print(id_sat, index_sat)
# print(arr_time)


for time in data['Arr_Time']:
    print(data[time][index_sat])



# Test arr:
