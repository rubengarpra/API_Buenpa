from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
import requests
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

router = APIRouter(prefix="/news",
                   tags=["news"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

URL = "https://buenpastor.es/noticias/"


class New(BaseModel):
    id: int
    image: str
    title: str
    date: str
    link: str


@router.get('/')
async def news():
    response = scrape_url(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup.find('title').text)
    news_list = []
    news_info = soup.find_all('div', class_='col-12 col-lg-6 col-md-6')
    if not news_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Noticias no encontradas")
    i = 1
    for new_info in news_info:
        image = new_info.find('img')['src']
        title = new_info.find('h3', class_='post-title')
        date = new_info.find('p', class_='post-date').text
        link = title.find('a')['href']

        new = New(id=i, image=image,
                  title=title.text, date=date, link=link)
        news_list.append(new)
        i += 1
    return news_list


def scrape_url(url):
    delays = [2, 3, 4]  # Adjust delay values as needed
    user_agent = UserAgent().chrome  # Choose a random user-agent

    while True:
        try:
            headers = {'User-Agent': user_agent}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            # Process the response data here
            return response
        except requests.exceptions.RequestException as e:
            delay = random.choice(delays)
            print(f"Encountered error: {e}. Waiting for {delay} seconds...")
            time.sleep(delay)

