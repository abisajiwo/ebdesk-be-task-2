import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

urls = [
    'https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl'
]

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(urls[0])
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')

    channel_id=[]
    judul=[]
    channel_name=[]
    publish=[]

    id = 1

    for a in soup.findAll('div', class_='text-wrapper style-scope ytd-video-renderer')[:30]:
        titles = a.find('yt-formatted-string', class_='style-scope ytd-video-renderer')
        channel_names = a.find('a', class_='yt-simple-endpoint style-scope yt-formatted-string')
        view_n_release = a.findAll('span', class_='style-scope ytd-video-meta-block')
        releases = view_n_release[1]

        judul.append(titles.text)
        channel_id.append(id)
        channel_name.append(channel_names.text)
        publish.append(releases.text)

        id += 1

    print(judul)
    print(publish)
    print(channel_name)
    print(channel_id)

    cv = pd.DataFrame({'Channel_id':channel_id, 'Title':judul, 'Channel_name':channel_name, 'Publish':publish})
    cv.to_csv('youtube.csv', index=False, encoding='utf-8')

main()

