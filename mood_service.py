import os
import logging
import google.generativeai as genai
import google.generativeai as genai
import json
from collections import Counter

logger = logging.getLogger(__name__)

class MoodService:
    def __init__(self):
        """Initialize the mood analysis service with Gemini AI"""
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            
            genai.configure(api_key=api_key)
            logger.info("MoodService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MoodService: {e}")
            self.client = None
    
    def analyze_news_mood(self, articles):
        """Analyze the overall mood and trending topics from news articles"""
        if not self.client:
            logger.error("Gemini client not initialized")
            return self._get_fallback_mood_data(articles)
        
        if not articles or len(articles) == 0:
            return self._get_fallback_mood_data(articles)
        
        try:
            # Extract titles and descriptions for analysis
            article_texts = []
            for article in articles:
                title = article.get('title', '')
                description = article.get('description', '')
                if title:
                    article_texts.append(f"Title: {title}")
                if description:
                    article_texts.append(f"Description: {description}")
            
            if not article_texts:
                return self._get_fallback_mood_data(articles)
            
            # Combine texts for analysis
            combined_text = "\n".join(article_texts[:20])  # Limit to first 20 to avoid token limits
            
            # Analyze mood and trends
            mood_data = self._analyze_sentiment_and_trends(combined_text)
            
            # Add article count and trending topics
            mood_data['total_articles'] = len(articles)
            mood_data['trending_topics'] = self._extract_trending_topics(articles)
            mood_data['topic_analysis'] = self._analyze_topic_distribution(articles)
            
            return mood_data
            
        except Exception as e:
            logger.error(f"Error analyzing news mood: {e}")
            return self._get_fallback_mood_data(articles)
    
    def _analyze_sentiment_and_trends(self, text):
        """Use Gemini to analyze sentiment and overall mood"""
        try:
            prompt = f"""
            Analyze the overall sentiment and mood of these XR/AR/VR/3D development news articles.
            
            Article content:
            {text}
            
            Please provide analysis in JSON format with:
            1. mood: one of ["positive", "negative", "neutral", "excited", "cautious"]
            2. confidence: float between 0 and 1
            3. mood_description: brief explanation of the overall mood
            4. key_themes: list of 3-5 main themes or topics detected
            
            Focus on technology trends, developer sentiment, industry outlook, and innovation pace.
            """
            
           model = genai.GenerativeModel("gemini-1.5-flash")
           response = model.generate_content(prompt)
            
            if response.text:
                result = json.loads(response.text)
                return {
                    'mood': result.get('mood', 'neutral'),
                    'confidence': float(result.get('confidence', 0.5)),
                    'mood_description': result.get('mood_description', 'Mixed sentiment in technology news'),
                    'key_themes': result.get('key_themes', [])
                }
            else:
                raise ValueError("Empty response from Gemini")
                
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                'mood': 'neutral',
                'confidence': 0.5,
                'mood_description': 'Unable to analyze mood - using neutral sentiment',
                'key_themes': []
            }
    
    def _extract_trending_topics(self, articles):
        """Extract trending topics from article titles"""
        try:
            # Common XR/3D keywords to look for
            keywords = [
                'Unity', 'Blender', 'AR', 'VR', 'Meta Quest', 'Apple Vision',
                'AI', 'Machine Learning', '3D Modeling', 'Game Development',
                'WebXR', 'Mixed Reality', 'Spatial Computing', 'Neural Networks',
                'OpenXR', 'USD', 'Metaverse', 'Digital Twin', 'Simulation'
            ]
            
            keyword_counts = Counter()
            
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                combined = f"{title} {description}"
                
                for keyword in keywords:
                    if keyword.lower() in combined:
                        keyword_counts[keyword] += 1
            
            # Return top trending topics (mentioned in multiple articles)
            trending = [keyword for keyword, count in keyword_counts.most_common(10) if count >= 1]
            return trending[:8]  # Limit to top 8
            
        except Exception as e:
            logger.error(f"Error extracting trending topics: {e}")
            return []
    
    def _analyze_topic_distribution(self, articles):
        """Analyze the distribution of different technology topics"""
        try:
            topic_categories = {
                'Unity Development': ['unity', 'unity3d', 'unity engine'],
                'Blender/3D Art': ['blender', '3d modeling', '3d artist', '3d graphics'],
                'AR Development': ['ar', 'augmented reality', 'arcore', 'arkit'],
                'VR Development': ['vr', 'virtual reality', 'oculus', 'meta quest'],
                'Game Development': ['game development', 'indie game', 'game engine'],
                'AI/ML': ['artificial intelligence', 'machine learning', 'neural', 'ai']
            }
            
            topic_counts = {category: 0 for category in topic_categories.keys()}
            total_matches = 0
            
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                combined = f"{title} {description}"
                
                for category, keywords in topic_categories.items():
                    for keyword in keywords:
                        if keyword in combined:
                            topic_counts[category] += 1
                            total_matches += 1
                            break  # Count each article only once per category
            
            # Calculate percentages
            topic_analysis = []
            if total_matches > 0:
                for category, count in topic_counts.items():
                    if count > 0:
                        percentage = round((count / total_matches) * 100, 1)
                        topic_analysis.append({
                            'topic': category,
                            'count': count,
                            'percentage': percentage
                        })
            
            # Sort by count and return top topics
            topic_analysis.sort(key=lambda x: x['count'], reverse=True)
            return topic_analysis[:6]
            
        except Exception as e:
            logger.error(f"Error in topic analysis: {e}")
            return []
    
    def _get_fallback_mood_data(self, articles):
        """Return fallback mood data when AI analysis fails"""
        return {
            'mood': 'neutral',
            'confidence': 0.0,
            'mood_description': 'Mood analysis not available',
            'total_articles': len(articles) if articles else 0,
            'trending_topics': [],
            'topic_analysis': [],
            'key_themes': []
        }
