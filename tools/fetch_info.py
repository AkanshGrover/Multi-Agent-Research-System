from datetime import datetime, timedelta
import requests, arxiv

class InfoFetcher:
    def __init__(self):
        self.cs_categories = [
            'cs.AI',      # Artificial Intelligence
            'cs.CC',      # Computational Complexity
            'cs.CE',      # Computational Engineering, Finance, and Science
            'cs.CG',      # Computational Geometry
            'cs.CL',      # Computation and Language
            'cs.CR',      # Cryptography and Security
            'cs.CV',      # Computer Vision and Pattern Recognition
            'cs.CY',      # Computers and Society
            'cs.DB',      # Databases
            'cs.DC',      # Distributed, Parallel, and Cluster Computing
            'cs.DL',      # Digital Libraries
            'cs.DM',      # Discrete Mathematics
            'cs.DS',      # Data Structures and Algorithms
            'cs.ET',      # Emerging Technologies
            'cs.FL',      # Formal Languages and Automata Theory
            'cs.GL',      # General Literature
            'cs.GR',      # Graphics
            'cs.GT',      # Computer Science and Game Theory
            'cs.HC',      # Human-Computer Interaction
            'cs.IR',      # Information Retrieval
            'cs.IT',      # Information Theory
            'cs.LG',      # Machine Learning
            'cs.LO',      # Logic in Computer Science
            'cs.MA',      # Multiagent Systems
            'cs.MM',      # Multimedia
            'cs.MS',      # Mathematical Software
            'cs.NA',      # Numerical Analysis
            'cs.NE',      # Neural and Evolutionary Computing
            'cs.NI',      # Networking and Internet Architecture
            'cs.OH',      # Other Computer Science
            'cs.OS',      # Operating Systems
            'cs.PF',      # Performance
            'cs.PL',      # Programming Languages
            'cs.RO',      # Robotics
            'cs.SC',      # Symbolic Computation
            'cs.SD',      # Sound
            'cs.SE',      # Software Engineering
            'cs.SI',      # Social and Information Networks
            'cs.SY',      # Systems and Control
            'cs.TH',      # Hardware Architecture
            'cs.UR',      # Human-Computer Interaction
        ]

        self.cs_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
            'computer vision', 'natural language processing', 'nlp', 'data science',
            'software engineering', 'programming', 'algorithm', 'data structure',
            'database', 'cybersecurity', 'cryptography', 'blockchain', 'distributed system',
            'cloud computing', 'web development', 'mobile development', 'devops',
            'computer science', 'information technology', 'computing', 'technology',
            'software', 'hardware', 'networking', 'operating system', 'computer graphics',
            'human computer interaction', 'hci', 'robotics', 'automation', 'ai',
            'ml', 'dl', 'cv', 'nlp', 'api', 'framework', 'library', 'tool',
            'platform', 'architecture', 'design pattern', 'optimization', 'performance',
            'scalability', 'reliability', 'security', 'privacy', 'data mining',
            'big data', 'analytics', 'visualization', 'user interface', 'ux', 'ui'
        ]

    def is_cs_topic(self, topic):
        topic = topic.lower()
        return any(keyword in topic for keyword in self.cs_keywords)#returns true if any word of topic existis in the cs_keywords

    def calculate_relevance(self, topic, title, text):#just checks whether the info gayjered is apt for the stuff we need it for
        topic_words = set(topic.lower().split())
        content_words = set((title + " " + text).lower().split())

        if not topic_words:
            return 0.0

        overlap = len(topic_words & content_words)

        score = overlap / len(topic_words)

        if topic.lower() in (title + " " + text).lower():
            score += 0.3

        return min(score, 1.0)
    
    def fetch_hn(self, topic, max_results = 10):#hackernews
        url = "https://hn.algolia.com/api/v1/search"
        params = {
            'query': topic,
            'tags': 'story',
            'hitsPerPage': max_results,
            'numericFilters': f'created_at_i>{int((datetime.now() - timedelta(days=30)).timestamp())}'
        }

        posts = []

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()

            for hit in data.get('hits', []):
                post_data = {
                    'title': hit.get('title', ''),
                    'url': hit.get('url', ''),
                    'points': hit.get('points', 0),
                    'comments': hit.get('num_comments', 0),
                    'created_at': datetime.fromtimestamp(hit.get('created_at_i', 0)),
                    'source': 'Hacker News',
                    'relevance_score': self.calculate_relevance(topic, hit.get('title', ''), '')
                }
                posts.append(post_data)
        
        except Exception as e:
            print("Error fetching from hackernews")

        return posts

    def fetch_arxiv(self, topic, limit = 20):
        search = arxiv.Search(
            query=topic,
            max_results=limit,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers = []

        try:
            for paper in search.results():

                if not any(cat in paper.categories for cat in self.cs_categories):#checks whether the category is present in your defined list ofceategories
                    continue

                papers.append({
                    "title": paper.title,
                    "authors": [a.name for a in paper.authors],
                    "abstract": paper.summary,
                    "published": paper.published,
                    "url": paper.entry_id,
                    "pdf_url": paper.pdf_url,
                    "source": "arxiv",
                    "relevance_score": self.calculate_relevance(
                        topic,
                        paper.title,
                        paper.summary
                    )
                })

        except Exception as e:
            print("Error fetching from arxiv")

        return papers
    
    def get_domain_specific_insights(self, topic):
        insights = {
            'domain': 'Computer Science & Information Technology',
            "suggested_categories": set(),
            "research_directions": set(),
            "key_technologies": set(),
            'recent_trends': []
        }
        
        # Analyze topic for domain-specific insights
        topic_lower = topic.lower()
        
        # AI/ML related
        if any(keyword in topic_lower for keyword in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning']):
            insights['suggested_categories'].update(['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL'])
            insights['research_directions'].update(['Neural Networks', 'Deep Learning', 'Computer Vision', 'NLP'])
            insights['key_technologies'].update(['TensorFlow', 'PyTorch', 'Transformers', 'GANs'])
        
        # Software Engineering
        if any(keyword in topic_lower for keyword in ['software', 'programming', 'development', 'engineering']):
            insights['suggested_categories'].update(['cs.SE', 'cs.PL', 'cs.DS'])
            insights['research_directions'].update(['Software Architecture', 'Code Quality', 'Testing', 'DevOps'])
            insights['key_technologies'].update(['Git', 'Docker', 'Kubernetes', 'CI/CD'])
        
        # Cybersecurity
        if any(keyword in topic_lower for keyword in ['security', 'cybersecurity', 'cryptography', 'privacy']):
            insights['suggested_categories'].update(['cs.CR', 'cs.CY'])
            insights['research_directions'].update(['Cryptography', 'Network Security', 'Privacy', 'Threat Detection'])
            insights['key_technologies'].update(['Blockchain', 'Zero-Knowledge Proofs', 'Encryption'])
        
        # Data Science
        if any(keyword in topic_lower for keyword in ['data', 'analytics', 'database', 'big data']):
            insights['suggested_categories'].update(['cs.DB', 'cs.DS', 'cs.LG'])
            insights['research_directions'].update(['Data Mining', 'Big Data', 'Data Visualization', 'Analytics'])
            insights['key_technologies'].update(['Hadoop', 'Spark', 'Pandas', 'SQL'])
        
        insights["suggested_categories"] = list(insights["suggested_categories"])
        insights["research_directions"] = list(insights["research_directions"])
        insights["key_technologies"] = list(insights["key_technologies"])

        return insights
    

    def fetch_all(self, topic):
        arxiv_data = self.fetch_arxiv(topic)
        hn_data = self.fetch_hn(topic)
        insights = self.get_domain_specific_insights(topic)

        results = {
            "topic": topic,
            "is_cs_related": self.is_cs_topic(topic),
            "insights": insights,
            "sources": {
                "arxiv": arxiv_data,
                "hackernews": hn_data
            },
            "total_items": len(arxiv_data) + len(hn_data),
            "timestamp": datetime.now().isoformat()
        }

        return results