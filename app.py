import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from news_service import NewsService
from email_service import EmailService
from summarizer_service import SummarizerService
from mood_service import MoodService
from gamification_service import GamificationService
import atexit
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize services
news_service = NewsService()
email_service = EmailService()
summarizer_service = SummarizerService()
mood_service = MoodService()
gamification_service = GamificationService()

# Initialize scheduler
scheduler = BackgroundScheduler()

def send_daily_news():
    """Job function for automated daily news sending"""
    try:
        logger.info("Running automated daily news job")
        articles = news_service.fetch_niche_tech_news()
        if articles and len(articles) > 0:
            email_service.send_news_email(articles)
            logger.info("Daily news email sent successfully")
        else:
            logger.warning("No articles found for daily news")
    except Exception as e:
        logger.error(f"Error in daily news job: {e}")

# Schedule daily news at 8 AM
scheduler.add_job(
    func=send_daily_news,
    trigger=CronTrigger(hour=8, minute=0),
    id='daily_news_job',
    name='Send daily tech news',
    replace_existing=True
)

# Start scheduler
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def dashboard():
    """Main dashboard showing latest news"""
    try:
        articles, used_fallback = news_service.fetch_niche_tech_news()
        if used_fallback:
            flash("⚠️ Showing fallback articles due to NewsAPI rate limit.", 'warning')
        return render_template('dashboard.html', articles=articles)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        flash(f"Error loading news: {str(e)}", 'danger')
        return render_template('dashboard.html', articles=[])

@app.route('/refresh_news')
def refresh_news():
    """Manually refresh news articles"""
    try:
        articles, used_fallback = news_service.fetch_niche_tech_news()
        if used_fallback:
            flash("⚠️ Showing fallback articles due to NewsAPI rate limit.", 'warning')
        flash(f"Refreshed! Found {len(articles)} articles", 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        logger.error(f"Error refreshing news: {e}")
        flash(f"Error refreshing news: {str(e)}", 'danger')
        return redirect(url_for('dashboard'))

@app.route('/send_email')
def send_email_now():
    """Manually trigger email sending"""
    try:
        articles, used_fallback = news_service.fetch_niche_tech_news()
        if used_fallback:
            flash("⚠️ Showing fallback articles due to NewsAPI rate limit.", 'warning')
        if articles and len(articles) > 0:
            email_service.send_news_email(articles)
            flash("Email sent successfully!", 'success')
        else:
            flash("No articles to send", 'warning')
        return redirect(url_for('dashboard'))
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        flash(f"Error sending email: {str(e)}", 'danger')
        return redirect(url_for('dashboard'))

@app.route('/config')
def config():
    """Configuration page"""
    config_data = {
        'email_user': os.getenv('EMAIL_USER', ''),
        'email_to': os.getenv('EMAIL_TO', ''),
        'news_api_key': os.getenv('NEWS_API_KEY', ''),
        'keywords': news_service.get_keywords()
    }
    return render_template('config.html', config=config_data)

@app.route('/update_keywords', methods=['POST'])
def update_keywords():
    """Update search keywords"""
    try:
        keywords = request.form.get('keywords', '').strip()
        if keywords:
            news_service.set_keywords(keywords)
            flash("Keywords updated successfully!", 'success')
        else:
            flash("Keywords cannot be empty", 'danger')
        return redirect(url_for('config'))
    except Exception as e:
        logger.error(f"Error updating keywords: {e}")
        flash(f"Error updating keywords: {str(e)}", 'danger')
        return redirect(url_for('config'))

@app.route('/mood')
def news_mood():
    """News Mood dashboard showing trending topics and sentiment"""
    try:
        articles, used_fallback = news_service.fetch_niche_tech_news()
        if used_fallback:
            flash("⚠️ Showing fallback articles due to NewsAPI rate limit.", 'warning')
        mood_data = mood_service.analyze_news_mood(articles)
        return render_template('mood.html', mood_data=mood_data, articles=articles)
    except Exception as e:
        logger.error(f"Error loading mood dashboard: {e}")
        flash(f"Error loading mood data: {str(e)}", 'danger')
        return render_template('mood.html', mood_data={}, articles=[])

@app.route('/learning')
def learning_paths():
    """Gamified learning paths for XR/3D/Game development"""
    try:
        articles, used_fallback = news_service.fetch_niche_tech_news()
        if used_fallback:
            flash("⚠️ Showing fallback articles due to NewsAPI rate limit.", 'warning')
        learning_data = gamification_service.get_learning_dashboard_data()
        return render_template('learning.html', learning_data=learning_data, articles=articles)
    except Exception as e:
        logger.error(f"Error loading learning paths: {e}")
        flash(f"Error loading learning data: {str(e)}", 'danger')
        return render_template('learning.html', learning_data={}, articles=[])

@app.route('/api/articles')
def api_articles():
    """API endpoint for fetching articles"""
    try:
        articles, _ = news_service.fetch_niche_tech_news()
        return jsonify({'success': True, 'articles': articles, 'count': len(articles)})
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/mood')
def api_mood():
    """API endpoint for mood analysis"""
    try:
        articles, _ = news_service.fetch_niche_tech_news()
        mood_data = mood_service.analyze_news_mood(articles)
        return jsonify({'success': True, 'mood_data': mood_data})
    except Exception as e:
        logger.error(f"API mood error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/track_article_read', methods=['POST'])
def track_article_read():
    """Track when user reads an article for gamification"""
    try:
        data = request.json
        article_data = data.get('article', {})
        topic_category = data.get('topic_category')
        
        user_data = gamification_service.get_user_progress()
        result = gamification_service.track_article_read(user_data, article_data, topic_category)
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        logger.error(f"Error tracking article read: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/track_summary', methods=['POST'])
def track_summary():
    """Track when user generates AI summary for gamification"""
    try:
        user_data = gamification_service.get_user_progress()
        result = gamification_service.track_summary_generated(user_data)
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        logger.error(f"Error tracking summary: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test_email')
def test_email():
    """Test email configuration"""
    try:
        test_content = [{'title': 'Test Email', 'url': 'https://example.com', 'source': {'name': 'Test'}}]
        email_service.send_news_email(test_content, subject_prefix="TEST")
        flash("Test email sent successfully!", 'success')
        return redirect(url_for('config'))
    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        flash(f"Error sending test email: {str(e)}", 'danger')
        return redirect(url_for('config'))

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """API endpoint for generating article summaries with Gemini"""
    try:
        data = request.get_json()
        if not data or 'article' not in data:
            return jsonify({'success': False, 'error': 'Article data required'}), 400
        
        article = data['article']
        summary = summarizer_service.summarize_article(article)
        
        return jsonify({
            'success': True, 
            'summary': summary,
            'model': 'Gemini 2.5 Flash'
        })
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test_gemini')
def test_gemini():
    """Test Gemini AI integration"""
    try:
        # Test with a sample article
        test_article = {
            'title': 'Unity Announces New XR Development Tools',
            'description': 'Unity Technologies introduces advanced VR development capabilities for immersive gaming experiences.',
            'source': {'name': 'Unity Blog'}
        }
        
        summary = summarizer_service.summarize_article(test_article)
        flash(f"Gemini AI test successful! Generated summary: {summary[:100]}...", 'success')
        return redirect(url_for('config'))
    except Exception as e:
        logger.error(f"Error testing Gemini: {e}")
        flash(f"Gemini AI test failed: {str(e)}", 'danger')
        return redirect(url_for('config'))



if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
