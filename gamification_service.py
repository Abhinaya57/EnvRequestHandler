import os
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

class GamificationService:
    def __init__(self):
        """Initialize gamification service"""
        self.user_data_file = "user_progress.json"
        self.learning_paths = self._define_learning_paths()
        self.achievements = self._define_achievements()
        
    def _define_learning_paths(self):
        """Define learning paths for different XR/3D/Game development tracks"""
        return {
            "ar_developer": {
                "name": "AR Developer",
                "description": "Master Augmented Reality development",
                "icon": "smartphone",
                "color": "primary",
                "levels": [
                    {"level": 1, "title": "AR Basics", "xp_required": 0, "topics": ["AR fundamentals", "ARCore", "ARKit"]},
                    {"level": 2, "title": "AR Interactions", "xp_required": 100, "topics": ["Hand tracking", "Gesture recognition", "Spatial mapping"]},
                    {"level": 3, "title": "AR Applications", "xp_required": 250, "topics": ["AR games", "Industrial AR", "AR marketing"]},
                    {"level": 4, "title": "Advanced AR", "xp_required": 500, "topics": ["Computer vision", "SLAM", "AR cloud"]},
                    {"level": 5, "title": "AR Expert", "xp_required": 1000, "topics": ["AR research", "Custom AR engines", "AR leadership"]}
                ]
            },
            "vr_developer": {
                "name": "VR Developer",
                "description": "Become a Virtual Reality expert",
                "icon": "eye",
                "color": "success",
                "levels": [
                    {"level": 1, "title": "VR Fundamentals", "xp_required": 0, "topics": ["VR basics", "Unity VR", "Unreal VR"]},
                    {"level": 2, "title": "VR Interactions", "xp_required": 100, "topics": ["VR controllers", "Hand tracking", "Locomotion"]},
                    {"level": 3, "title": "VR Experiences", "xp_required": 250, "topics": ["VR games", "VR training", "Social VR"]},
                    {"level": 4, "title": "Advanced VR", "xp_required": 500, "topics": ["VR optimization", "Custom shaders", "VR physics"]},
                    {"level": 5, "title": "VR Master", "xp_required": 1000, "topics": ["VR research", "VR architecture", "VR innovation"]}
                ]
            },
            "unity_developer": {
                "name": "Unity Developer",
                "description": "Master Unity game engine",
                "icon": "box",
                "color": "warning",
                "levels": [
                    {"level": 1, "title": "Unity Basics", "xp_required": 0, "topics": ["Unity interface", "GameObjects", "Components"]},
                    {"level": 2, "title": "Unity Scripting", "xp_required": 100, "topics": ["C# basics", "MonoBehaviour", "Unity API"]},
                    {"level": 3, "title": "Game Development", "xp_required": 250, "topics": ["Game mechanics", "UI systems", "Audio"]},
                    {"level": 4, "title": "Advanced Unity", "xp_required": 500, "topics": ["Optimization", "Custom tools", "Networking"]},
                    {"level": 5, "title": "Unity Expert", "xp_required": 1000, "topics": ["Unity architecture", "Performance", "Team leadership"]}
                ]
            },
            "blender_artist": {
                "name": "3D Artist (Blender)",
                "description": "Become a 3D modeling and animation expert",
                "icon": "layers",
                "color": "info",
                "levels": [
                    {"level": 1, "title": "Blender Basics", "xp_required": 0, "topics": ["Blender interface", "Basic modeling", "Materials"]},
                    {"level": 2, "title": "3D Modeling", "xp_required": 100, "topics": ["Advanced modeling", "Sculpting", "Retopology"]},
                    {"level": 3, "title": "Animation", "xp_required": 250, "topics": ["Keyframe animation", "Rigging", "Character animation"]},
                    {"level": 4, "title": "Advanced 3D", "xp_required": 500, "topics": ["Geometry nodes", "Simulations", "Compositing"]},
                    {"level": 5, "title": "3D Master", "xp_required": 1000, "topics": ["Pipeline development", "3D innovation", "Teaching"]}
                ]
            },
            "game_developer": {
                "name": "Game Developer",
                "description": "Create engaging games across platforms",
                "icon": "play",
                "color": "danger",
                "levels": [
                    {"level": 1, "title": "Game Design", "xp_required": 0, "topics": ["Game mechanics", "Level design", "Player experience"]},
                    {"level": 2, "title": "Programming", "xp_required": 100, "topics": ["Game programming", "Engine basics", "Debug tools"]},
                    {"level": 3, "title": "Production", "xp_required": 250, "topics": ["Project management", "Team collaboration", "Publishing"]},
                    {"level": 4, "title": "Advanced Games", "xp_required": 500, "topics": ["AI systems", "Multiplayer", "Performance"]},
                    {"level": 5, "title": "Game Expert", "xp_required": 1000, "topics": ["Game architecture", "Industry trends", "Innovation"]}
                ]
            },
            "xr_developer": {
                "name": "XR Developer",
                "description": "Build mixed reality and cross-platform XR experiences",
                "icon": "globe",
                "color": "dark",
                "levels": [
                    {"level": 1, "title": "XR Fundamentals", "xp_required": 0, "topics": ["Mixed reality basics", "OpenXR", "WebXR"]},
                    {"level": 2, "title": "Cross-Platform XR", "xp_required": 100, "topics": ["Multi-device XR", "Shared experiences", "XR frameworks"]},
                    {"level": 3, "title": "XR Applications", "xp_required": 250, "topics": ["Enterprise XR", "Social XR", "XR for education"]},
                    {"level": 4, "title": "Advanced XR", "xp_required": 500, "topics": ["XR optimization", "Custom XR tools", "XR analytics"]},
                    {"level": 5, "title": "XR Expert", "xp_required": 1000, "topics": ["XR research", "XR platform development", "XR innovation"]}
                ]
            }
        }
    
    def _define_achievements(self):
        """Define achievements users can unlock"""
        return [
            {"id": "first_read", "name": "News Explorer", "description": "Read your first XR article", "icon": "book-open", "xp": 10},
            {"id": "daily_reader", "name": "Daily Reader", "description": "Read articles for 7 consecutive days", "icon": "calendar", "xp": 50},
            {"id": "topic_master", "name": "Topic Master", "description": "Read 20 articles about a specific topic", "icon": "target", "xp": 100},
            {"id": "trend_spotter", "name": "Trend Spotter", "description": "Discover 5 trending topics", "icon": "trending-up", "xp": 75},
            {"id": "knowledge_seeker", "name": "Knowledge Seeker", "description": "Use AI summary 25 times", "icon": "brain", "xp": 60},
            {"id": "tech_enthusiast", "name": "Tech Enthusiast", "description": "Read 100 total articles", "icon": "star", "xp": 200},
            {"id": "learning_path", "name": "Path Starter", "description": "Begin a learning path", "icon": "map", "xp": 30},
            {"id": "level_up", "name": "Level Up", "description": "Reach level 2 in any path", "icon": "arrow-up", "xp": 100},
            {"id": "multi_path", "name": "Multi-Talented", "description": "Progress in 3 different learning paths", "icon": "shuffle", "xp": 150},
            {"id": "expert", "name": "Expert", "description": "Reach level 5 in any path", "icon": "award", "xp": 500}
        ]
    
    def get_user_progress(self):
        """Load user progress from file"""
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r') as f:
                    return json.load(f)
            else:
                return self._create_new_user()
        except Exception as e:
            logger.error(f"Error loading user progress: {e}")
            return self._create_new_user()
    
    def _create_new_user(self):
        """Create new user progress data"""
        return {
            "total_xp": 0,
            "articles_read": 0,
            "summaries_generated": 0,
            "topics_discovered": [],
            "achievements_unlocked": [],
            "learning_paths": {path_id: {"current_level": 1, "xp": 0} for path_id in self.learning_paths.keys()},
            "daily_streak": 0,
            "last_active": None,
            "created_date": datetime.now().isoformat()
        }
    
    def save_user_progress(self, user_data):
        """Save user progress to file"""
        try:
            with open(self.user_data_file, 'w') as f:
                json.dump(user_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving user progress: {e}")
    
    def award_xp(self, user_data, xp_amount, activity):
        """Award XP to user and check for level ups and achievements"""
        user_data["total_xp"] += xp_amount
        logger.info(f"Awarded {xp_amount} XP for {activity}")
        
        # Check for new achievements
        new_achievements = self._check_achievements(user_data)
        
        # Update learning path levels
        updated_paths = self._update_learning_paths(user_data)
        
        return {
            "xp_awarded": xp_amount,
            "new_achievements": new_achievements,
            "level_ups": updated_paths
        }
    
    def _check_achievements(self, user_data):
        """Check if user has unlocked new achievements"""
        new_achievements = []
        
        for achievement in self.achievements:
            if achievement["id"] not in user_data["achievements_unlocked"]:
                if self._achievement_condition_met(achievement, user_data):
                    user_data["achievements_unlocked"].append(achievement["id"])
                    user_data["total_xp"] += achievement["xp"]
                    new_achievements.append(achievement)
                    logger.info(f"Achievement unlocked: {achievement['name']}")
        
        return new_achievements
    
    def _achievement_condition_met(self, achievement, user_data):
        """Check if achievement condition is met"""
        achievement_id = achievement["id"]
        
        if achievement_id == "first_read":
            return user_data["articles_read"] >= 1
        elif achievement_id == "daily_reader":
            return user_data["daily_streak"] >= 7
        elif achievement_id == "topic_master":
            return any(count >= 20 for count in user_data.get("topic_counts", {}).values())
        elif achievement_id == "trend_spotter":
            return len(user_data["topics_discovered"]) >= 5
        elif achievement_id == "knowledge_seeker":
            return user_data["summaries_generated"] >= 25
        elif achievement_id == "tech_enthusiast":
            return user_data["articles_read"] >= 100
        elif achievement_id == "learning_path":
            return any(path_data["xp"] > 0 for path_data in user_data["learning_paths"].values())
        elif achievement_id == "level_up":
            return any(path_data["current_level"] >= 2 for path_data in user_data["learning_paths"].values())
        elif achievement_id == "multi_path":
            active_paths = sum(1 for path_data in user_data["learning_paths"].values() if path_data["xp"] > 0)
            return active_paths >= 3
        elif achievement_id == "expert":
            return any(path_data["current_level"] >= 5 for path_data in user_data["learning_paths"].values())
        
        return False
    
    def _update_learning_paths(self, user_data):
        """Update learning path levels based on XP"""
        level_ups = []
        
        for path_id, path_data in user_data["learning_paths"].items():
            if path_id in self.learning_paths:
                path_info = self.learning_paths[path_id]
                current_level = path_data["current_level"]
                current_xp = path_data["xp"]
                
                # Check if user can level up
                while current_level < len(path_info["levels"]):
                    next_level_index = current_level  # 0-based index for next level
                    if next_level_index < len(path_info["levels"]):
                        required_xp = path_info["levels"][next_level_index]["xp_required"]
                        if current_xp >= required_xp:
                            current_level += 1
                            path_data["current_level"] = current_level
                            level_ups.append({
                                "path": path_info["name"],
                                "new_level": current_level,
                                "level_title": path_info["levels"][current_level - 1]["title"],
                                "next_topics": path_info["levels"][current_level - 1]["topics"] if current_level <= len(path_info["levels"]) else []
                            })
                        else:
                            break
                    else:
                        break
        
        return level_ups
    
    def track_article_read(self, user_data, article, topic_category=None):
        """Track when user reads an article"""
        user_data["articles_read"] += 1
        
        # Update daily streak
        today = datetime.now().date()
        last_active = user_data.get("last_active")
        
        if last_active:
            last_date = datetime.fromisoformat(last_active).date()
            if today == last_date:
                pass  # Same day, no change
            elif today == last_date + timedelta(days=1):
                user_data["daily_streak"] += 1
            else:
                user_data["daily_streak"] = 1  # Reset streak
        else:
            user_data["daily_streak"] = 1
        
        user_data["last_active"] = datetime.now().isoformat()
        
        # Track topic
        if topic_category:
            if "topic_counts" not in user_data:
                user_data["topic_counts"] = defaultdict(int)
            user_data["topic_counts"][topic_category] += 1
            
            if topic_category not in user_data["topics_discovered"]:
                user_data["topics_discovered"].append(topic_category)
        
        # Award XP and check achievements
        result = self.award_xp(user_data, 5, "reading article")
        self.save_user_progress(user_data)
        
        return result
    
    def track_summary_generated(self, user_data):
        """Track when user generates AI summary"""
        user_data["summaries_generated"] += 1
        result = self.award_xp(user_data, 3, "generating AI summary")
        self.save_user_progress(user_data)
        return result
    
    def get_learning_dashboard_data(self):
        """Get comprehensive data for learning dashboard"""
        user_data = self.get_user_progress()
        
        # Calculate user level based on total XP
        user_level = min(10, max(1, user_data["total_xp"] // 100 + 1))
        
        # Get progress for each learning path
        path_progress = {}
        for path_id, path_info in self.learning_paths.items():
            user_path_data = user_data["learning_paths"].get(path_id, {"current_level": 1, "xp": 0})
            current_level = user_path_data["current_level"]
            
            # Calculate progress to next level
            if current_level <= len(path_info["levels"]):
                current_level_info = path_info["levels"][current_level - 1]
                if current_level < len(path_info["levels"]):
                    next_level_info = path_info["levels"][current_level]
                    progress_percent = min(100, (user_path_data["xp"] / next_level_info["xp_required"]) * 100)
                    next_level_xp = next_level_info["xp_required"]
                else:
                    progress_percent = 100
                    next_level_xp = None
            else:
                current_level_info = path_info["levels"][-1]
                progress_percent = 100
                next_level_xp = None
            
            path_progress[path_id] = {
                "info": path_info,
                "current_level": current_level,
                "current_level_title": current_level_info["title"],
                "current_xp": user_path_data["xp"],
                "next_level_xp": next_level_xp,
                "progress_percent": progress_percent,
                "completed": current_level >= len(path_info["levels"])
            }
        
        # Get unlocked achievements
        unlocked_achievements = [
            achievement for achievement in self.achievements
            if achievement["id"] in user_data["achievements_unlocked"]
        ]
        
        return {
            "user_level": user_level,
            "total_xp": user_data["total_xp"],
            "articles_read": user_data["articles_read"],
            "daily_streak": user_data["daily_streak"],
            "learning_paths": path_progress,
            "achievements": unlocked_achievements,
            "total_achievements": len(self.achievements),
            "achievement_progress": len(unlocked_achievements) / len(self.achievements) * 100
        }