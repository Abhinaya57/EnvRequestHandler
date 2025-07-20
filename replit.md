# XR News Aggregator

## Overview

This is a Flask-based web application that aggregates and distributes XR technology news from multiple sources. The application searches for articles about XR/AR/VR/Metaverse AND gaming/3D development tools from the past 48 hours, ensuring at least 5-20 articles daily. It automatically fetches news articles from NewsAPI, formats them for email distribution, and sends daily updates to configured recipients.

## User Preferences

Preferred communication style: Simple, everyday language.
AI Provider: Gemini AI Pro instead of OpenAI for all AI features.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with Python
- **Scheduler**: APScheduler for automated daily news delivery at 8 AM
- **Services**: Modular service-oriented architecture with separate NewsService and EmailService classes
- **Configuration**: Environment variable-based configuration for API keys and email settings

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap with dark theme from Replit CDN
- **Icons**: Feather icons for consistent UI elements
- **JavaScript**: Vanilla JavaScript for interactive features and UI enhancements

## Key Components

### Core Services
1. **NewsService** (`news_service.py`)
   - Integrates with NewsAPI to fetch articles
   - Configurable keyword search for niche tech topics
   - Article filtering and formatting capabilities
   - Multiple targeted searches: Searches for specific keyword combinations like "AR development", "Unity 3D", "Blender modeling", etc.
   - Ensures relevant articles: Each search targets specific development topics for better relevance
   - Time range: No time restrictions - all relevant articles with publication dates shown
   - Page size: 20 articles per fetch to ensure adequate daily coverage

2. **EmailService** (`email_service.py`)
   - Gmail SMTP integration for email delivery
   - Support for multiple recipients
   - Email validation and error handling
   - Formatted HTML/text email content

3. **SummarizerService** (`summarizer_service.py`)
   - Gemini AI Pro integration for article summarization
   - Generates 5-point professional takeaways for XR/gaming developers
   - Uses Gemini 2.5 Flash model for fast, efficient summarization
   - Fallback summary generation for error handling

4. **Flask Application** (`app.py`)
   - Web interface for news display and configuration
   - Background scheduler for automated daily emails
   - Route handlers for manual actions (refresh, send email)
   - AI summarization API endpoints for dashboard integration

### Web Interface
- **Dashboard**: Display of latest news articles with stats and AI-powered summaries
- **Configuration**: Email settings, API key management, and Gemini AI testing interface
- **Actions**: Manual refresh, email sending, and on-demand AI summarization capabilities

## Data Flow

1. **Automated Schedule**: Background job runs daily at 8 AM
2. **News Fetching**: Multiple NewsAPI calls with specific keyword combinations to ensure each topic is covered (no time restrictions)
3. **Article Processing**: Filter and format articles for email
4. **Email Distribution**: Send formatted content to recipient list
5. **Web Interface**: Display current articles and allow manual actions

## External Dependencies

### APIs and Services
- **NewsAPI**: Primary news source (requires API key)
- **Gmail SMTP**: Email delivery service (requires app password)
- **Gemini AI Pro**: Article summarization and analysis (requires Gemini API key)

### Frontend Libraries
- **Bootstrap**: UI framework with Replit dark theme
- **Feather Icons**: Icon library for consistent visual elements

### Python Packages
- **Flask**: Web framework
- **APScheduler**: Task scheduling
- **Requests**: HTTP client for API calls
- **SMTP**: Built-in email functionality

## Environment Configuration

Required environment variables:
- `NEWS_API_KEY`: NewsAPI authentication key
- `EMAIL_USER`: Gmail account for sending emails
- `EMAIL_PASS`: Gmail app password
- `EMAIL_TO`: Comma-separated recipient email addresses
- `GEMINI_API_KEY`: Google Gemini AI API key for article summarization
- `SESSION_SECRET`: Flask session security key (optional, defaults to dev key)

## Deployment Strategy

### Local Development
- Flask development server with debug mode
- Host: 0.0.0.0, Port: 5000
- Entry point: `main.py`

### Production Considerations
- Environment variables must be properly configured
- Gmail app passwords required for email functionality
- Scheduler runs in background thread
- Graceful shutdown handling for scheduler cleanup

### Architecture Benefits
- **Modularity**: Separate services for easy testing and maintenance
- **Automation**: Set-and-forget daily news delivery
- **Flexibility**: Configurable keywords and recipients
- **User-Friendly**: Web interface for management and manual actions
- **Reliability**: Error handling and logging throughout the application

### Recent Changes

#### July 20, 2025 - Major Feature Addition: News Mood Dashboard & Gamified Learning Paths
- **News Mood Dashboard**: Added AI-powered sentiment analysis using Gemini 2.5 Flash to analyze overall mood and trending topics from XR/3D development news
  - Shows sentiment classification (positive, negative, neutral, excited, cautious) with confidence scores
  - Extracts and displays top trending topics from article titles
  - Provides topic analysis with percentage breakdowns (Unity, Blender, AR/VR development, etc.)
  - Real-time mood analysis with refresh functionality
- **Gamified Learning Paths**: Implemented comprehensive gamification system for XR/3D/Game development learning
  - 6 learning paths: AR Developer, VR Developer, Unity Developer, 3D Artist (Blender), Game Developer, XR Developer
  - Each path has 5 levels with specific XP requirements and topic focuses:
    - Level 1: Fundamentals (0 XP) - Basics and getting started
    - Level 2: Intermediate (100 XP) - Core skills and interactions
    - Level 3: Applications (250 XP) - Building projects and real applications
    - Level 4: Advanced (500 XP) - Optimization, advanced techniques
    - Level 5: Expert (1000 XP) - Research, leadership, custom solutions
  - Complete learning resources for each level with direct links to:
    - Official documentation (Unity, Blender, ARCore, ARKit, Unreal Engine)
    - University courses and professional tutorials
    - Industry best practices and certification programs
    - Open source projects and research papers
  - 10 different achievements users can unlock (News Explorer, Daily Reader, Topic Master, etc.)
  - XP system: +5 XP for reading articles, +3 XP for generating AI summaries
  - Progress tracking with daily streaks, total articles read, and level progression
  - Real-time notifications for XP gains, achievements, and level ups
  - Interactive learning navigation with "Learn Current Topics" and "View Full Path" buttons
- **User Experience**: Enhanced navigation with new dashboard links and seamless integration between features
- **Technical Implementation**: Created MoodService and GamificationService with Gemini AI integration and local JSON storage for user progress
- **User Feedback**: User expressed high satisfaction with the final learning path implementation featuring complete progression and real learning resources

#### July 20, 2025 - Keyword Search Strategy Improvement
- **Issue Resolved**: Previous search was returning many irrelevant articles not matching user's specific interests
- **Solution Implemented**: Changed from single complex search to 8 separate targeted searches for each keyword category:
  - "AR development" OR "augmented reality development"
  - "VR development" OR "virtual reality development" 
  - "Unity 3D" OR "Unity engine" OR "Unity development"
  - "Blender 3D" OR "Blender modeling" OR "Blender tutorial"
  - "Meta Quest" OR "Oculus Quest" OR "VR headset"
  - "3D modeling" OR "3D design" OR "3D graphics"
  - "game development" OR "indie game" OR "game engine"
  - "graphics design" OR "3D artist" OR "digital art"
- **Result**: Now fetching 33 unique articles with most articles being relevant to user's keywords
- **User Feedback**: "this time most of the news articles are related to my keywords" - Success confirmed

### Potential Enhancements
- Database integration for article storage and user management
- Multiple news source support beyond NewsAPI
- Advanced filtering and categorization options
- User subscription management
- Analytics and engagement tracking