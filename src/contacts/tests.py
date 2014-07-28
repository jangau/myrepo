import requests, random, string, re
from django.contrib.auth import login, authenticate
from django.test import Client, TestCase
from django.contrib.auth.models import User
def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def random_user(csrf_token):
    username = randomword(10)
    password = randomword(10)
    email = randomword(10)
    email += '@example.com'
    register_data = {'username':username, 'password1':password, 'csrfmiddlewaretoken':csrf_token, 'email':email, 'password2':password,}   
    return register_data
    
class Tests(TestCase):
    url = 'http://10.18.32.152/'
    user_data = {'username':'ceva', 'password':'ceva',}
#     def test1(self):
# #         this test will create a new user using http post
# #         the user is randomly generated
# #         after the register, we will be redirected to the profile page
# #         we can make assertions
#         client = requests.Session()
#         r = client.get(self.url+'register')
#         csrftoken = client.cookies['csrftoken']
#         self.user_data = random_user(csrftoken)
#         r = client.post(self.url+'register', data = self.user_data)
#         r = client.get(self.url+'home')
#         pattern = re.compile(r"(\w+)\'s Profile")
#         s = r.content
#         match = re.search(pattern, s)
#         created_name = match.group(1)
#         print created_name
#         self.assertEqual(created_name, self.user_data['username'])
        
    def test2(self):
        client = requests.Session()
        r = client.get(self.url+'login')
        csrftoken = client.cookies['csrftoken']
        login_data = {'username':self.user_data['username'], 'password':
                    self.user_data['password'], 'csrfmiddlewaretoken': csrftoken}
        r = client.post(self.url+'login/', data=login_data)
        print r.status_code
        r = client.get(self.url+'view/25/', )
        regex = re.compile(r"id=\"likes\"\>(\w+)")
        match = re.search (regex, r.content)
        print r.content
        print match.groups()
        like_no1 = int(match.group(1))
        r = client.get(self.url+'ajaxlike_json')
        csrftoken = client.cookies['csrftoken']
        r = client.post(self.url+'ajaxlike_json', data={'csrfmiddlewaretoken': csrftoken, 'client_id': '25'},)
        regex2 = re.compile(r"(\d+)")
        match = re.search (regex2, r.content)
        print match.group(1)
        self.assertEqual(like_no1 + 1, int(match.group(1)))