import requests, feedparser
from datetime import datetime, timedelta

class InfoFetcherRT:
    def __init__(self):
        self.rss_feeds = {
            'hackernews': 'https://hnrss.org/frontpage',
            'reddit_programming': 'https://www.reddit.com/r/programming.rss',
            'reddit_machinelearning': 'https://www.reddit.com/r/MachineLearning.rss',
            'reddit_compsci': 'https://www.reddit.com/r/compsci.rss',
            'reddit_artificial': 'https://www.reddit.com/r/artificial.rss',
            'techcrunch': 'https://techcrunch.com/feed/',
            'arstechnica': 'https://feeds.arstechnica.com/arstechnica/index/',
            'wired': 'https://www.wired.com/feed/rss',
            'ieee_spectrum': 'https://spectrum.ieee.org/rss/fulltext',
            'acm_news': 'https://cacm.acm.org/rss/',
        }

        self.reddit_sources = [
            "MachineLearning",
            "programming",
            "technology",
            "computerscience"
        ]

    def get_json(self, url, params=None, headers=None):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return None
        
    def fetch_rss(self, url, limit=5):
        feed = feedparser.parse(url)

        items = []

        for entry in feed.entries[:limit]:

            date = None
            if getattr(entry, "published_parsed", None):
                date = datetime(*entry.published_parsed[:6])

            items.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "summary": entry.get("summary", ""),
                "published": date,
                "source": feed.feed.get("title", "rss")
            })

        return items
    
    def are_related(self, topic, text):
        topic_words = set(topic.lower().split())
        text_words = set(text.lower().split())

        overlap = len(topic_words & text_words)

        return overlap >= max(1, int(len(topic_words) * 0.3))
    
    def fetch_tech_news(self, topic, limit=10):
        news = []

        per_feed = max(1, limit // len(self.rss_feeds))

        for url in self.rss_feeds.values():
            for item in self.fetch_rss(url, per_feed):
                if self.are_related(topic, item["title"] + " " + item["summary"]):
                    news.append(item)

        return news[:limit]
    
    def fetch_reddit(self, subreddit, limit=5):
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"

        data = self.get_json(
            url,
            headers={"User-Agent": "cs-research-agent"}
        )

        if not data:
            return []

        posts = []

        for p in data["data"]["children"][:limit]:
            d = p["data"]
            posts.append({
                "title": d["title"],
                "url": "https://reddit.com" + d["permalink"],
                "score": d["score"],
                "comments": d["num_comments"],
                "created": datetime.fromtimestamp(d["created_utc"]),
                "subreddit": subreddit,
                "source": "reddit"
            })

        return posts
    
    def fetch_github(self, topic, page=1):
        url = "https://api.github.com/search/repositories"

        params = {
            "q": topic,
            "sort": "stars",
            "order": "desc",
            "per_page": 10,
            "page": page
        }

        data = self.get_json(url, params=params)

        if not data:
            return []

        repos = []

        for repo in data.get("items", []):
            repos.append({
                "name": repo["full_name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "updated": repo["updated_at"],
                "source": "github"
            })

        return repos
    
    def fetch_stackoverflow(self, tags, page=1):

        url = "https://api.stackexchange.com/2.3/questions"

        params = {
            "site": "stackoverflow",
            "order": "desc",
            "sort": "creation",
            "tagged": ";".join(tags),
            "pagesize": 5,
            "page": page,
            "fromdate": int((datetime.now() - timedelta(days=7)).timestamp())
        }

        data = self.get_json(url, params=params)

        if not data:
            return []

        questions = []

        for q in data.get("items", []):

            questions.append({
                "title": q["title"],
                "link": q["link"],
                "score": q["score"],
                "answers": q["answer_count"],
                "views": q["view_count"],
                "tags": q["tags"],
                "created": datetime.fromtimestamp(q["creation_date"]),
                "source": "stackoverflow"
            })

        return questions
    
    def fetch_all(self, topic, github_page=1, so_page=1):
        news = self.fetch_tech_news(topic)
        reddit = []

        for sub in self.reddit_sources:
            reddit += self.fetch_reddit(sub, 2)

        github = self.fetch_github(topic, github_page)
        stackoverflow = self.fetch_stackoverflow([topic], so_page)

        return {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "sources": {
                "tech_news": news,
                "reddit": reddit,
                "github": github,
                "stackoverflow": stackoverflow
            },
            "total_items": len(news) + len(reddit) + len(github) + len(stackoverflow)
        }