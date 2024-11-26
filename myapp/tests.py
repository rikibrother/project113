from django.test import TestCase
import requests
# Create your tests here.


data = requests.get('http://127.0.0.1:8000/moviedata/')

# print(data.content)
print(data.status_code)