import requests
import sys
import threading

def list_average(lst): 
    return sum(lst) / len(lst) 

def request_loop(url:str):
    if not url.startswith("http") or not url.startswith("https"):
        url = "http://" + url

    while True:
        try:
            requests.get(url)
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You must specify what url you want to request and how many concurrent requests you want.")
        print("Usage: python http_requester.py <URL_TO_REQUEST> <NB_OF_CONCURRENT_REQUESTS>")
        exit(1)
    else:
        try:
            url = str(sys.argv[1])
            nb_concurrent_request = int(sys.argv[2])
        except:
            print("You must specify what url you want to request and how many concurrent requests you want.")
            print("Usage: python http_requester.py <URL_TO_REQUEST> <NB_OF_CONCURRENT_REQUESTS>")
            exit(1)

    for i in range(nb_concurrent_request):
        threading.Thread(target=request_loop, args=[url]).start()
