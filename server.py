import requests


class Server:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port

    def get_data(self):
        req = requests.get(f"http://{self.ip}:{self.port}/get_state")
        # print(req.json())
        # print(req.status_code)
        if req.status_code == 200:
            return req.json()
        else:
            print("Error getting data from server #{}".format(req.status_code))
            return -1
            
        
    def set_data(self, data):
        req = requests.post(f"http://{self.ip}:{self.port}/set_state", data=data, headers={"Content-Type": "application/json"})
        return req.status_code
    

    def get_history(self, count):
        req = requests.get(f"http://{self.ip}:{self.port}/get_history?count={count}")
        return req.json()
