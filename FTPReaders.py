from ftplib import FTP
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
        return NotImplementedError(f"In the <{self.__name__}> class, the method must be redefined <Read>")

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url


class SP3Reader(FTPReader):

    def __init__(self, url, user_name="anonymous", user_pass=""):
        super().__init__(url, user_name, user_pass)

    def Read(self, path, name):
        self._link = self._link + path + "/" + name
        if not os.path.exists(name):
            wget.download(self._link)
        else:
            print("Working with a file <...>")
        return 1


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
