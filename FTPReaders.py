from ftplib import FTP
import re
import wget


class FTPReader:
    _url = ""
    _name = ""

    def __init__(self, url, user_name, user_pass):
        self._ftp = FTP(url, encoding='cp1251')
        self._ftp.login(user=user_name, passwd=user_pass)

    def Read(self, name):
        return NotImplementedError(f"In the <{self.__name__}> class, the method must be redefined <Read>")
