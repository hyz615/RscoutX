from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx
import json
import time

from app.core.config import settings


class ScraperCache:
    """Simple in-memory cache for scraper results"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            entry = self._cache[key]
            if datetime.utcnow() < entry['expires']:
                return entry['data']
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl_minutes: int = None):
        ttl = ttl_minutes or settings.SCRAPER_CACHE_MINUTES
        self._cache[key] = {
            'data': data,
            'expires': datetime.utcnow() + timedelta(minutes=ttl)
        }
    
    def clear(self):
        self._cache.clear()


# Global cache instance
scraper_cache = ScraperCache()


class BaseScraper(ABC):
    """Base class for match data scrapers"""
    
    def __init__(self):
        self.timeout = settings.SCRAPER_TIMEOUT_SECONDS
        self.max_retries = settings.SCRAPER_MAX_RETRIES
        self.cache = scraper_cache
    
    @abstractmethod
    async def fetch_team_matches(self, team_number: str, event_id: str) -> List[Dict[str, Any]]:
        """Fetch match history for a team at an event"""
        pass
    
    async def _fetch_with_retry(self, url: str, headers: Optional[Dict] = None) -> str:
        """Fetch URL with retry logic"""
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, headers=headers or {})
                    response.raise_for_status()
                    return response.text
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to fetch {url} after {self.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
        return ""
    
    def _parse_with_rules(self, html: str, rules: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse HTML with configurable rules"""
        # Simple rule-based parser
        # Rules format: {"match_id": {"selector": "...", "attr": "..."}, ...}
        results = []
        
        # This is a simplified implementation
        # In production, you'd use BeautifulSoup or similar
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all match rows
            match_elements = soup.select(rules.get('row_selector', 'tr.match'))
            
            for elem in match_elements:
                match_data = {}
                for field, rule in rules.get('fields', {}).items():
                    try:
                        selector = rule.get('selector')
                        attr = rule.get('attr')
                        
                        found = elem.select_one(selector)
                        if found:
                            if attr == 'text':
                                match_data[field] = found.get_text(strip=True)
                            else:
                                match_data[field] = found.get(attr, '')
                    except:
                        match_data[field] = None
                
                if match_data:
                    results.append(match_data)
        except ImportError:
            # Fallback: return mock data if BeautifulSoup not available
            pass
        
        return results


class RoboteventsScraper(BaseScraper):
    """Scraper for RobotEvents.com V5RC API"""
    
    BASE_URL = "https://www.robotevents.com"
    API_URL = "https://www.robotevents.com/api/v2"
    
    async def fetch_team_matches(self, team_number: str, event_id: str = None) -> List[Dict[str, Any]]:
        """Fetch team matches from RobotEvents V5RC API"""
        
        cache_key = f"robotevents_{team_number}_{event_id or 'all'}"
        cached = self.cache.get(cache_key)
        if cached:
            print(f"✓ Using cached data for team {team_number}")
            return cached
        
        # Check if API key is configured
        api_key = settings.ROBOTEVENTS_API_KEY if hasattr(settings, 'ROBOTEVENTS_API_KEY') else None
        
        if not api_key or api_key.strip() == "":
            print("⚠️  No RobotEvents API Key configured")
            print("ℹ️  Using mock data for demonstration")
            print("💡 To use real data, apply for API key at:")
            print("   https://www.robotevents.com/api/v2/accessRequest/create")
            matches = await self._fetch_mock_data(team_number, event_id or "DEMO")
            self.cache.set(cache_key, matches)
            return matches
        
        try:
            print(f"🔄 Attempting to fetch real data from RobotEvents API...")
            matches = await self._fetch_from_api(team_number, event_id)
            print(f"✓ Successfully fetched {len(matches)} matches from RobotEvents")
        except Exception as e:
            print(f"❌ Failed to fetch from RobotEvents API: {e}")
            print("⚠️  Falling back to mock data")
            # Fallback to mock data for demo
            matches = await self._fetch_mock_data(team_number, event_id or "DEMO")
        
        self.cache.set(cache_key, matches)
        return matches
    
    async def _fetch_from_api(self, team_number: str, event_id: str = None) -> List[Dict[str, Any]]:
        """Fetch real data from RobotEvents V5RC API"""
        matches = []
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Step 1: Search for team
            headers = {
                "Authorization": f"Bearer {settings.ROBOTEVENTS_API_KEY if hasattr(settings, 'ROBOTEVENTS_API_KEY') else ''}",
                "Accept": "application/json"
            }
            
            # Search team by number
            team_response = await client.get(
                f"{self.API_URL}/teams",
                params={
                    "number": team_number,
                    "program": "V5RC"  # VEX V5 Robotics Competition
                },
                headers=headers
            )
            
            if team_response.status_code != 200:
                raise Exception(f"Team search failed: {team_response.status_code}")
            
            teams_data = team_response.json()
            if not teams_data.get("data"):
                raise Exception(f"Team {team_number} not found")
            
            team = teams_data["data"][0]
            team_id = team["id"]
            
            # Step 2: Get team's matches
            matches_params = {
                "team[]": team_id,
                "season[]": "181"  # Current season (adjust as needed)
            }
            
            if event_id:
                matches_params["event[]"] = event_id
            
            matches_response = await client.get(
                f"{self.API_URL}/matches",
                params=matches_params,
                headers=headers
            )
            
            if matches_response.status_code != 200:
                raise Exception(f"Matches fetch failed: {matches_response.status_code}")
            
            matches_data = matches_response.json()
            
            # Parse matches
            for match_entry in matches_data.get("data", []):
                # Determine alliance color
                red_alliance = match_entry.get("alliances", [{}])[0]
                blue_alliance = match_entry.get("alliances", [{}])[1] if len(match_entry.get("alliances", [])) > 1 else {}
                
                red_teams = [t["team"]["id"] for t in red_alliance.get("teams", [])]
                blue_teams = [t["team"]["id"] for t in blue_alliance.get("teams", [])]
                
                is_red = team_id in red_teams
                is_blue = team_id in blue_teams
                
                if not (is_red or is_blue):
                    continue
                
                alliance = "red" if is_red else "blue"
                score_for = red_alliance.get("score", 0) if is_red else blue_alliance.get("score", 0)
                score_against = blue_alliance.get("score", 0) if is_red else red_alliance.get("score", 0)
                
                # Determine result
                if score_for > score_against:
                    result = "win"
                elif score_for < score_against:
                    result = "loss"
                else:
                    result = "tie"
                
                # Get opponents
                opponent_teams = blue_teams if is_red else red_teams
                opponents = ", ".join([str(tid) for tid in opponent_teams])
                
                match = {
                    "match_id": match_entry.get("name", "Unknown"),
                    "event_id": match_entry.get("event", {}).get("code", event_id or "Unknown"),
                    "event_name": match_entry.get("event", {}).get("name", "Unknown Event"),
                    "match_date": match_entry.get("started", datetime.utcnow().isoformat()),
                    "alliance": alliance,
                    "score_for": score_for,
                    "score_against": score_against,
                    "result": result,
                    "opponents": opponents,
                    "rank_snapshot": None
                }
                matches.append(match)
        
        return matches
    
    async def _fetch_mock_data(self, team_number: str, event_id: str) -> List[Dict[str, Any]]:
        """Return mock match data for demonstration"""
        
        print(f"📊 Generating mock data for team {team_number}")
        print(f"   This is sample data for demonstration purposes")
        
        # Simulate some matches
        mock_matches = []
        
        for i in range(5):
            match = {
                "match_id": f"Q{i+1}",
                "event_id": event_id,
                "event_name": f"VEX Demo Event {event_id}",
                "match_date": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                "alliance": "red" if i % 2 == 0 else "blue",
                "score_for": 50 + i * 10,
                "score_against": 45 + i * 8,
                "result": "win" if (50 + i * 10) > (45 + i * 8) else "loss",
                "opponents": f"Team{1000 + i}, Team{2000 + i}",
                "rank_snapshot": i + 1
            }
            mock_matches.append(match)
        
        print(f"✓ Generated {len(mock_matches)} sample matches")
        return mock_matches


class ConfigurableHTMLScraper(BaseScraper):
    """Scraper with configurable parsing rules"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
    
    async def fetch_team_matches(self, team_number: str, event_id: str) -> List[Dict[str, Any]]:
        """Fetch and parse with configurable rules"""
        
        cache_key = f"configurable_{team_number}_{event_id}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Build URL from config
        url_template = self.config.get('url_template', '')
        url = url_template.format(team=team_number, event=event_id)
        
        # Fetch HTML
        html = await self._fetch_with_retry(url, self.config.get('headers'))
        
        # Parse with rules
        parsing_rules = self.config.get('parsing_rules', {})
        matches = self._parse_with_rules(html, parsing_rules)
        
        self.cache.set(cache_key, matches)
        return matches


# Scraper factory
def get_scraper(scraper_type: str = "robotevents", config: Optional[Dict] = None) -> BaseScraper:
    """Factory function to get scraper instance"""
    if scraper_type == "robotevents":
        return RoboteventsScraper()
    elif scraper_type == "configurable":
        return ConfigurableHTMLScraper(config or {})
    else:
        raise ValueError(f"Unknown scraper type: {scraper_type}")
