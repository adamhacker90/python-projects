import requests

## Request with plain text
# url = "https://icanhazdadjoke.com/"
# response = requests.get(url, headers={"Accept": "text/plain"})

# print(response.text)



# # Request that is .json, can be used in python
# url = "https://icanhazdadjoke.com/"
# response = requests.get(url, headers={"Accept": "application/json"})

# data = response.json()
# print(data["joke"])




url = "https://icanhazdadjoke.com/search"
response = requests.get(
    url, 
    headers={"Accept": "application/json"},
    params={"term": "cat", "limit": 1}
    )

data = response.json()
print(data["results"])