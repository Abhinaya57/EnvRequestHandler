import os
import requests
import logging
from datetime import datetime
import time
import json

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
        self.keywords = "('AR' OR 'VR' OR 'MR' OR 'XR') AND ('3D Modeling' OR 'Game Development' OR Unity OR Blender OR 'Meta Quest' OR 'Graphics Design')"
        
    def get_keywords(self):
        """Get current search keywords"""
        return self.keywords
    
    def set_keywords(self, keywords):
        """Set new search keywords"""
        self.keywords = keywords
        logger.info(f"Keywords updated to: {keywords}")
    
    def fetch_niche_tech_news(self, page_size=5):
        """Fetch niche tech news from NewsAPI using multiple targeted searches"""
        if not self.api_key:
            logger.error("NEWS_API_KEY not found in environment variables")
            raise Exception("NEWS_API_KEY not configured")
        
        # Define specific keyword combinations for targeted searches
        keyword_searches = [
            '"AR development" OR "augmented reality development"',
            '"VR development" OR "virtual reality development"', 
            '"Unity 3D" OR "Unity engine" OR "Unity development"',
            '"Blender 3D" OR "Blender modeling" OR "Blender tutorial"',
            '"Meta Quest" OR "Oculus Quest" OR "VR headset"',
            '"3D modeling" OR "3D design" OR "3D graphics"',
            '"game development" OR "indie game" OR "game engine"',
            '"graphics design" OR "3D artist" OR "digital art"'
        ]
        
        all_articles = []
        
        for search_query in keyword_searches:
            try:
                params = {
                    'q': search_query,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': page_size,
                    'apiKey': self.api_key
                }
                
                logger.info(f"Searching for: {search_query}")
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    for article in articles:
                        if (article.get('title') and 
                            article.get('url') and 
                            article.get('title') != '[Removed]' and
                            article.get('description')):
                            
                            # Format the publication date nicely
                            published_date = article.get('publishedAt', '')
                            if published_date:
                                try:
                                    from datetime import datetime
                                    dt = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                                    formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                                except:
                                    formatted_date = published_date[:10]
                            else:
                                formatted_date = 'Unknown'
                            
                            cleaned_article = {
                                'title': article['title'],
                                'description': article.get('description', ''),
                                'url': article['url'],
                                'urlToImage': article.get('urlToImage'),
                                'publishedAt': article.get('publishedAt'),
                                'formattedDate': formatted_date,
                                'source': article.get('source', {}),
                                'author': article.get('author'),
                                'matchedKeyword': search_query
                            }
                            all_articles.append(cleaned_article)
                            
                else:
                    logger.warning(f"Search failed for '{search_query}' with status {response.status_code}")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error searching for '{search_query}': {e}")
                continue
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # Sort by publication date (newest first)
        unique_articles.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
        
        logger.info(f"Fetched {len(unique_articles)} unique articles from {len(keyword_searches)} keyword searches")
        if unique_articles:
            return unique_articles[:20], False  # Live articles
        else:
            fallback = self.load_fallback_articles()
            return fallback, True  # Fallback used

    
    def format_article_for_email(self, article, index):
        """Format a single article for email content"""
        title = article.get('title', 'No Title')
        url = article.get('url', '')
        source = article.get('source', {}).get('name', 'Unknown Source')
        
        formatted = f"{index}. {title}\n"
        formatted += f"   Source: {source}\n"
        formatted += f"   Link: {url}\n\n"
        
        return formatted
    
    def format_articles_for_email(self, articles):
        """Format all articles for email content"""
        if not articles:
            return "🛑 No niche tech news found today."
        
        content = "🧠 *Daily XR Technology News Update*\n\n"
        content += f"📅 Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
        content += f"⏰ Covering articles from the last 48 hours\n"
        content += f"📰 Found {len(articles)} articles from various sources\n\n"
        
        for i, article in enumerate(articles, 1):
            content += self.format_article_for_email(article, i)
        
        content += "\n---\n"
        content += "🔄 This is an automated daily update covering XR technology news from various sources.\n"
        content += f"📊 Search: Articles about XR/AR/VR/Metaverse AND Gaming/3D/Development tools\n"
        content += f"📅 Time Range: Last 48 hours\n"
        content += f"📈 Sources: News channels, tech blogs, industry publications, and more\n"
        
        return content
    
    def load_fallback_articles(self):
        """Load fallback articles from local JSON file"""
        fallback_path = os.path.join(os.path.dirname(__file__), "fallback_articles.json")
        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
                logger.warning("Loaded fallback articles due to NewsAPI failure.")
                return articles
        except Exception as e:
            logger.error(f"Error loading fallback articles: {e}")
            return []

    
