from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
import requests
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

router = APIRouter(prefix="/events",
                   tags=["events"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

URL = "https://buenpastor.es/eventos/"


class Event(BaseModel):
    id: int
    title: str
    date: str
    time: str
    link: str


@router.get('/')
async def events():
    response = scrape_url(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup.find('title').text)
    events_list = []
    events_info = soup.find('div', class_='event-list')
    articles = soup.find_all('article')
    if not events_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Eventos no encontrados")
    # print(articles)
    i = 1
    for article in articles:
        date = get_date(article.find('p', class_='ss-date'))
        body_content = article.find('div', class_='event-content')
        title = body_content.find('h3', class_='event-title').text
        time = body_content.find('p', class_='ss-time').text.strip()
        link = body_content.find('a', class_='btn btn-light')['href']

        print(title)
        print(time)
        print(link)
        event = Event(id=i, title=title,
                      date=date, time=time, link=link)
        events_list.append(event)
        i += 1
    return events_list


def scrape_url(url: str):
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


def get_date(article_date):
    day = article_date.find('span', class_='date').text
    month = article_date.find('span', class_='month').text.split('\'')
    return f"{day}-{month[0]}-{month[1]}"
