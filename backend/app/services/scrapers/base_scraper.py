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
    
    async def fetch_team_matches(self, team_number: str, event_id: str = None) -> Dict[str, Any]:
        """Fetch team matches from RobotEvents V5RC API
        
        Returns:
            Dict with keys:
            - 'matches': List of match dictionaries
            - 'team_info': Dict with team information (name, organization, region, etc.)
        """
        
        cache_key = f"robotevents_{team_number}_{event_id or 'all'}"
        cached = self.cache.get(cache_key)
        if cached:
            print(f"✓ Using cached data for team {team_number}")
            return cached
        
        # Check if API key is configured
        api_key = settings.ROBOTEVENTS_API_KEY if hasattr(settings, 'ROBOTEVENTS_API_KEY') else None
        
        print(f"\n{'='*60}")
        print(f"🔍 Attempting to fetch data for team: {team_number}")
        print(f"   Event filter: {event_id or 'ALL'}")
        print(f"   API Key configured: {'Yes' if api_key and api_key.strip() else 'No'}")
        print(f"   API Key preview: {api_key[:20] + '...' if api_key and len(api_key) > 20 else 'None'}")
        print(f"{'='*60}\n")
        
        if not api_key or api_key.strip() == "":
            print("⚠️  No RobotEvents API Key configured")
            print("💡 To use real data, apply for API key at:")
            print("   https://www.robotevents.com/api/v2/accessRequest/create")
            print("❌ Returning empty match list (no mock data)")
            # Return empty list instead of mock data
            return {"matches": [], "team_info": None}
        
        try:
            print(f"🔄 Attempting to fetch real data from RobotEvents API...")
            result = await self._fetch_from_api(team_number, event_id)
            matches = result.get("matches", [])
            team_info = result.get("team_info")
            print(f"✓ Successfully fetched {len(matches)} matches from RobotEvents")
            print(f"✓ Data source: REAL API DATA")
            if team_info:
                print(f"✓ Team info: {team_info.get('team_name')} - {team_info.get('organization')}")
        except Exception as e:
            print(f"❌ Failed to fetch from RobotEvents API: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error details: {str(e)}")
            print("❌ Returning empty match list (no fallback to mock data)")
            # Return empty list instead of mock data
            result = {"matches": [], "team_info": None}
        
        self.cache.set(cache_key, result)
        return result
    
    async def _fetch_from_api(self, team_number: str, event_id: str = None) -> Dict[str, Any]:
        """Fetch real data from RobotEvents V5RC API
        
        Returns dict with 'matches' and 'team_info'
        """
        matches = []
        team_info = None
        
        print(f"   📡 Connecting to RobotEvents API...")
        print(f"   API URL: {self.API_URL}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Step 1: Search for team
            headers = {
                "Authorization": f"Bearer {settings.ROBOTEVENTS_API_KEY if hasattr(settings, 'ROBOTEVENTS_API_KEY') else ''}",
                "Accept": "application/json"
            }
            
            print(f"   🔍 Step 1: Searching for team {team_number}...")
            
            # Search team by number
            # 注意: 不使用 program 参数，因为 RobotEvents API 在使用该参数时可能返回空结果
            team_response = await client.get(
                f"{self.API_URL}/teams",
                params={
                    "number": team_number
                    # program 信息会在返回的队伍数据中包含
                },
                headers=headers
            )
            
            print(f"   📊 Team search response: {team_response.status_code}")
            
            if team_response.status_code != 200:
                print(f"   ❌ Team search failed with status {team_response.status_code}")
                print(f"   Response: {team_response.text[:200]}")
                raise Exception(f"Team search failed: {team_response.status_code} - {team_response.text[:100]}")
            
            teams_data = team_response.json()
            if not teams_data.get("data"):
                print(f"   ❌ No teams found for {team_number}")
                raise Exception(f"Team {team_number} not found in RobotEvents database")
            
            team = teams_data["data"][0]
            team_id = team["id"]
            team_name = team.get("team_name", "Unknown")
            
            # Extract team information
            location = team.get("location", {})
            team_info = {
                "team_number": team.get("number", team_number),
                "team_name": team_name,
                "robot_name": team.get("robot_name"),
                "organization": team.get("organization", "Unknown"),
                "region": f"{location.get('city', '')}, {location.get('region', '')}".strip(", ") or "Unknown",
                "grade": team.get("grade")
            }
            
            print(f"   ✓ Found team: {team_name} (ID: {team_id})")
            print(f"   📍 Location: {team_info['region']}")
            print(f"   🏢 Organization: {team_info['organization']}")
            print(f"   🔍 Step 2: Fetching matches for team ID {team_id}...")
            
            # Step 2: Get team's matches using correct endpoint
            # Correct endpoint: /teams/{team_id}/matches
            # 只获取 2025-2026 赛季的数据 (Season ID: 197 - Push Back)
            matches_params = {
                "season[]": "197",  # VEX V5 Robotics Competition 2025-2026: Push Back
                "per_page": 250  # 每页最多250场比赛
            }
            
            # Only add event filter if event_id is provided and not "ALL"
            if event_id and event_id.upper() != "ALL":
                matches_params["event[]"] = event_id
                print(f"   🎯 Filtering by season 2025-2026 (ID: 197), event: {event_id}")
            else:
                print(f"   🎯 Fetching season 2025-2026 matches (Push Back)")
            
            matches_response = await client.get(
                f"{self.API_URL}/teams/{team_id}/matches",
                params=matches_params,
                headers=headers
            )
            
            print(f"   📊 Matches fetch response: {matches_response.status_code}")
            
            if matches_response.status_code != 200:
                print(f"   ❌ Matches fetch failed with status {matches_response.status_code}")
                print(f"   Response: {matches_response.text[:200]}")
                raise Exception(f"Matches fetch failed: {matches_response.status_code} - {matches_response.text[:100]}")
            
            matches_data = matches_response.json()
            total_matches = len(matches_data.get("data", []))
            
            print(f"   ✓ Received {total_matches} matches from API")
            print(f"   🔄 Parsing match data...")
            
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
        
        print(f"   ✓ Parsed {len(matches)} matches successfully")
        
        # Return both team info and matches
        return {
            "matches": matches,
            "team_info": team_info
        }
    
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
