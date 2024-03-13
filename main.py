import math
from FTPReaders import SP3Reader
from FTPReaders import RinexReader

Url = "ftp://ftp.glonass-iac.ru"
Path = "MCC/PRODUCTS/23340/final"
File_name = "Sta22913.sp3"

Path_r = "MCC/BRDC/2023"
File_name_r = "Brdc0420.23g"

sp3 = SP3Reader(url=Url)



sp3.Read(Path, File_name)

# rin = RinexReader(url=Url)
# rin.Read(Path_r, File_name_r)
