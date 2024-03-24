class Client:
    def __init__(self, user_name: str, obj):
        self.user_name = user_name
        self.obj = obj
        self.data = {}
        self.sheet_time = {}

    def plot(self):
        # print(f"{self.user_name} reading  (:>)")
        print(self.data)
        # print(len(self.data[0.0]))
        # print(len(self.data["Id_Sat"]))
        pass

    def get_data(self, sat_id: str):
        self.data = self.obj.get_data(sat_id)
