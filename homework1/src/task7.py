import requests
# https://www.youtube.com/watch?v=IAXhhXI3qTQ (Some applications for requests that may be applicable to credibility of links)

def request_website_status(url):
    '''Verifies if a website link is online or offline. Returns a True statement if it is online, otherwise False.'''
    response = requests.get(url)

    if response.status_code == 200:
        # data = response.json()
        # print(data)
        return True
    else:
        return False
    