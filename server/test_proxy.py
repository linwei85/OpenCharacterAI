import requests
import httpx

# write a main function that calls the proxy
def main():
    proxy = "socks5h://127.0.0.1:12777"
    proxy2 = "socks5://127.0.0.1:12777"
    target_url = "https://www.youtube.com/"

    '''
    # test1
    resp = requests.get(target_url, proxies=dict(http=proxy,https=proxy))
    #resp = requests.get(target_url)

    # print the response
    print(resp.text)
    '''

    #test2
    client = httpx.Client(proxies={"http://": proxy2, "https://": proxy2})
    #client = httpx.Client()

    resp = client.get(target_url)
    print(resp.text)

if __name__ == '__main__':
    main()