import requests

def get_posts():
    # Define the API endpoint URL
    url = 'http://127.0.0.1:5000/db'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.RequestException as e:
        print('Request failed:', e)
        return None
    
print(get_posts())