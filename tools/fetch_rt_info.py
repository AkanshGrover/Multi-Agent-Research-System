import requests, feedparser, re
from datetime import datetime, timedelta

class InfoFetcherRT:
    def __init__(self):
        self.session = requests.Session()
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
            r = self.session.get(url, params=params, headers=headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return None
        
    def fetch_rss(self, url, limit=5):
        try:
            feed = feedparser.parse(url)

            items = []

            for entry in feed.entries[:limit]:

                date = None
                if getattr(entry, "published_parsed", None):
                    date = datetime(*entry.published_parsed[:6])
                elif getattr(entry, "updated_parsed", None):
                    date = datetime(*entry.updated_parsed[:6])

                items.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "summary": entry.get("summary", ""),
                    "published": date,
                    "source": feed.feed.get("title", "rss")
                })

            return items
        except Exception as e:
            print(f"RSS Error ({url}): {e}")
            return []
    
    def are_related(self, topic, text):
        topic_words = set(re.findall(r'\w+', topic.lower()))
        text_words = set(re.findall(r'\w+', text.lower()))

        overlap = len(topic_words & text_words)

        return overlap >= max(1, int(len(topic_words) * 0.3))
    
    def fetch_tech_news(self, topic, limit=10):
        news = []

        per_feed = max(3, limit // len(self.rss_feeds))

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

        for p in data.get("data", {}).get("children", [])[:limit]:
            d = p["data"]
            posts.append({
                "title": d.get("title", ""),
                "url": "https://reddit.com" + d.get("permalink", ""),
                "score": d.get("score", 0),
                "comments": d.get("num_comments", 0),
                "created": datetime.fromtimestamp(d.get("created_utc", 0)),
                "subreddit": subreddit,
                "source": "reddit"
            })

        return posts
    
    def fetch_github(self, topic, page=1):
        try:
            url = "https://api.github.com/search/repositories"
    
            params = {
                "q": topic,
                "per_page": 20,
                "page": page
            }
    
            data = self.get_json(url, params=params)
    
            if not data:
                return []
    
            repos = []
    
            for repo in data.get("items", []):
                repos.append({
                    "name": repo.get("full_name", ""),
                    "full_name": repo.get("full_name", ""),
                    "description": repo.get("description", ""),
                    "html_url": repo.get("html_url", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "language": repo.get("language", ""),
                    "created_at": repo.get("created_at", ""),
                    "updated_at": repo.get("updated_at", ""),
                    "source": "github"
                })
    
            return repos
        except Exception as e:
            print(f"Github Error: {e}")
            return []
    
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
    
    def deduplicate(self, items, key):
        seen = set()
        unique = []

        for item in items:
            value = item.get(key)

            if value and value not in seen:
                seen.add(value)
                unique.append(item)

        return unique
    
    def fetch_all(self, topic, github_page=1, so_page=1):
        news = self.fetch_tech_news(topic)
        reddit = []

        for sub in self.reddit_sources:
            reddit += self.fetch_reddit(sub, 2)

        github = self.fetch_github(topic, github_page)
        stackoverflow = self.fetch_stackoverflow([topic], so_page)

        news = self.deduplicate(news, "link")
        reddit = self.deduplicate(reddit, "url")
        github = self.deduplicate(github, "html_url")
        stackoverflow = self.deduplicate(stackoverflow, "link")

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
    
# if __name__ == "__main__":
#     fetcher = InfoFetcherRT()

#     topic = "Retrieval-Augmented Generation in Large Language Models"
#     results = fetcher.fetch_all(topic)
#     for source_name, items in results["sources"].items():
#         print(f"\n=== {source_name.upper()} ===")
        
#         for i, item in enumerate(items, 1):
#             title = (item.get("title") or item.get("name") or "No Title")
            
#             print(f"{i}. {title}")