import requests
import unittest

url = "http://127.0.0.1:5002"

class Test(unittest.TestCase):

    def test_register(self):
        r = requests.get(url + "/register")
        assert r.status_code == 200

    def test_simulator(self):
        r = requests.get(url + "/simulator")
        assert r.status_code == 200

    def test_create_user(self):
        r = requests.post(
            url + "/register/create",
            json={
                "data": {
                    "username":"jimena1515",
                    "password":"aA.123",
                    "password_check":"aA.123"
                }
            },
            headers={"Content-Type": "application/json"},
        )
        assert r.status_code == 200
    
    def test_login(self):
        r = requests.post(
            url + "/login/enter",
            json={
                "data": {
                    "username":"jimena1515",
                    "password":"aA.123"
                }
            },
            headers={"Content-Type": "application/json"},
        )
        assert r.status_code == 200

    def test_admin(self):
        r = requests.get(url + "/admin")
        assert r.status_code == 200

if __name__ == '__main__':
    unittest.main()