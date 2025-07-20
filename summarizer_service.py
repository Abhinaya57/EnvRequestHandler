import os
import logging
import requests
import re
import google.generativeai as genai
from google.genai import types

logger = logging.getLogger(__name__)

class SummarizerService:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    def fetch_article_content(self, url):
        """Fetch article content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching article content: {e}")
            return None
    
    def extract_key_info(self, text):
        """Extract key information like companies, numbers, technologies from text"""
        if not text:
            return {}
        
        # Extract companies
        companies = re.findall(r'\b(?:NVIDIA|Google|Meta|Apple|Microsoft|Unity|Epic|Unreal|Blender|OpenAI|AMD|Intel)\b', text, re.IGNORECASE)
        
        # Extract numbers and percentages
        numbers = re.findall(r'\d+(?:\.\d+)?%?', text)
        
        # Extract technologies
        technologies = re.findall(r'\b(?:AR|VR|XR|AI|GPU|3D|metaverse|gaming|blockchain|NFT)\b', text, re.IGNORECASE)
        
        return {
            'companies': list(set(companies)),
            'numbers': numbers[:3],  # First 3 numbers
            'technologies': list(set(technologies))
        }

    def generate_fallback_summary(self, article_data):
        """Generate a fallback summary using article metadata"""
        title = article_data.get('title', '')
        description = article_data.get('description', '')
        source = article_data.get('source', {}).get('name', 'Unknown Source')
        
        # Extract key information
        key_info = self.extract_key_info(title + ' ' + description)
        
        # Extract key phrases and create summary points
        summary_points = []
        
        # Point 1: Main topic based on specific title content
        title_lower = title.lower()
        desc_lower = description.lower() if description else ''
        
        # More specific analysis based on actual content
        if 'nvidia' in title_lower:
            if 'stock' in title_lower or 'holdings' in title_lower:
                summary_points.append("1. Reports on NVIDIA stock performance and institutional investment changes")
            else:
                summary_points.append("1. Discusses NVIDIA's developments in AI and GPU technology")
        elif 'accessibility' in title_lower or 'accessible' in title_lower:
            if 'ar' in title_lower or 'lens' in title_lower:
                summary_points.append("1. Focuses on making AR technology accessible to visually impaired users")
            else:
                summary_points.append("1. Addresses accessibility improvements in technology design")
        elif 'lens' in title_lower and 'maps' in title_lower:
            summary_points.append("1. Examines AR integration in Google Maps through the Lens feature")
        elif key_info['companies']:
            summary_points.append(f"1. Covers developments at {', '.join(key_info['companies'][:2])}")
        elif key_info['technologies']:
            summary_points.append(f"1. Explores {', '.join(key_info['technologies'][:2]).upper()} technology trends")
        else:
            # Use first meaningful part of title
            title_words = title.split()[:6]
            summary_points.append(f"1. Analyzes {' '.join(title_words)}...")
        
        # Point 2: Specific details from description
        if description:
            if len(description) > 150:
                # Extract specific numbers or percentages
                if key_info['numbers']:
                    summary_points.append(f"2. Reports specific metrics: {', '.join(key_info['numbers'][:2])}")
                elif 'filing' in desc_lower and 'securities' in desc_lower:
                    summary_points.append("2. Based on official SEC filing and financial disclosure documents")
                elif 'institutional investor' in desc_lower:
                    summary_points.append("2. Analyzes institutional investment patterns and market confidence")
                elif 'case study' in title_lower:
                    summary_points.append("2. Presents detailed case study with practical implementation insights")
                else:
                    # Extract first sentence or meaningful chunk
                    first_sentence = description.split('.')[0] if '.' in description else description[:80]
                    summary_points.append(f"2. Details: {first_sentence}...")
            else:
                summary_points.append(f"2. Summary: {description}")
        else:
            summary_points.append("2. Provides industry insights and technical analysis")
        
        # Point 3: Professional relevance based on content
        if 'nvidia' in title_lower and 'stock' in title_lower:
            summary_points.append("3. Important for investors tracking AI and semiconductor market leaders")
        elif 'accessibility' in title_lower:
            summary_points.append("3. Valuable for UX designers creating inclusive AR/VR experiences")
        elif 'lens' in title_lower and 'maps' in title_lower:
            summary_points.append("3. Relevant for AR developers working on navigation applications")
        elif key_info['technologies']:
            tech_list = ', '.join(key_info['technologies'][:2])
            summary_points.append(f"3. Relevant for professionals working with {tech_list} technologies")
        else:
            summary_points.append("3. Relevant for professionals in XR/AR/VR and gaming industries")
        
        # Point 4: Market/Industry impact
        if 'stock' in title_lower or 'holdings' in title_lower:
            summary_points.append("4. Indicates continued institutional confidence in tech sector growth")
        elif 'accessibility' in title_lower:
            summary_points.append("4. Demonstrates commitment to inclusive technology development")
        elif 'challenges' in desc_lower:
            summary_points.append("4. Addresses key industry challenges and potential solutions")
        elif 'lessons' in desc_lower:
            summary_points.append("4. Shares valuable lessons from real-world implementation")
        else:
            summary_points.append("4. Discusses impact on future technology adoption and user experience")
        
        # Point 5: Source and credibility
        summary_points.append(f"5. Published by {source}, providing credible industry reporting")
        
        return "\n".join(summary_points)

    def summarize_article(self, article_data):
        """Generate 5 key takeaways from an article using Gemini AI Pro"""
        try:
            # Use article description and title for summarization
            content = f"Title: {article_data.get('title', '')}\n"
            content += f"Description: {article_data.get('description', '')}\n"
            content += f"Source: {article_data.get('source', {}).get('name', '')}"
            
            prompt = f"""You are an expert tech news summarizer. Extract exactly 5 key takeaways from the given article. 
            Format as a numbered list with concise, actionable points. Focus on the most important information for XR/AR/VR/gaming professionals.
            
            Please provide 5 key takeaways from this article:
            
            {content}"""
            
            # Using Gemini 2.5 Flash for fast, efficient summarization
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            summary = response.text.strip() if response.text else ""
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing article with Gemini: {e}")
            # Return fallback summary instead of error message
            return self.generate_fallback_summary(article_data)
    
    def get_article_summary(self, article_url, article_data):
        """Get summary for an article using URL and metadata"""
        try:
            # First try to get summary from article data
            summary = self.summarize_article(article_data)
            return summary
        except Exception as e:
            logger.error(f"Error getting article summary: {e}")
            return "Summary unavailable. Please read the full article."
