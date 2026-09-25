import requests
# https://www.youtube.com/watch?v=IAXhhXI3qTQ (Some applications for requests that may be applicable to credibility of links)

def request_website_status(url):
    '''Verifies if a website link is online or offline. Returns a True statement if it is online, otherwise False.'''
    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            return True
        return False
        
    except requests.RequestException:
        return False
    