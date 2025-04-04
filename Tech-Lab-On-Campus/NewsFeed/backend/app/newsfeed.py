"""Module for retrieving newsfeed information."""

from dataclasses import dataclass
from datetime import datetime
from app.utils.redis import REDIS_CLIENT


@dataclass
class Article:
    """Dataclass for an article."""

    author: str
    title: str
    body: str
    publish_date: datetime
    image_url: str
    url: str


def get_all_news() -> list[Article]:
    """Get all news articles from the datastore."""
    # 1. Use Redis client to fetch all articles
    articles = REDIS_CLIENT.get_entry("all_articles")
    # 2. Format the data into articles
    res = []
    for article in articles:
        res.append(Article(article['author'], article['title'], article['text'],datetime.strptime(article['published'], '%Y-%m-%dT%H:%M:%S.%f%z'), article['external_links'], article['url']))
    # 3. Return a list of the articles formatted 
    return res


def get_featured_news() -> Article | None:
    """Get the featured news article from the datastore."""
    # 1. Get all the articles
    articles = get_all_news()
    # 2. Return as a list of articles sorted by most recent date
    articles.sort(key=lambda x: x.publish_date, reverse=True)
    return articles
