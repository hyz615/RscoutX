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


class RoboteventsScra per(BaseScraper):
    """Scraper for RobotEvents.com (example implementation)"""
    
    BASE_URL = "https://www.robotevents.com"
    
    async def fetch_team_matches(self, team_number: str, event_id: str) -> List[Dict[str, Any]]:
        """Fetch team matches from RobotEvents"""
        
        cache_key = f"robotevents_{team_number}_{event_id}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        # Since we don't have the actual API, return mock data
        # In production, you would:
        # 1. Use the RobotEvents API (if available)
        # 2. Or scrape the HTML with configurable rules
        
        matches = await self._fetch_mock_data(team_number, event_id)
        
        self.cache.set(cache_key, matches)
        return matches
    
    async def _fetch_mock_data(self, team_number: str, event_id: str) -> List[Dict[str, Any]]:
        """Return mock match data for demonstration"""
        
        # Simulate some matches
        mock_matches = []
        
        for i in range(5):
            match = {
                "match_id": f"Q{i+1}",
                "event_id": event_id,
                "event_name": f"VEX Event {event_id}",
                "match_date": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                "alliance": "red" if i % 2 == 0 else "blue",
                "score_for": 50 + i * 10,
                "score_against": 45 + i * 8,
                "result": "win" if (50 + i * 10) > (45 + i * 8) else "loss",
                "opponents": f"Team{1000 + i}, Team{2000 + i}",
                "rank_snapshot": i + 1
            }
            mock_matches.append(match)
        
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
        return RobotEventsScraper()
    elif scraper_type == "configurable":
        return ConfigurableHTMLScraper(config or {})
    else:
        raise ValueError(f"Unknown scraper type: {scraper_type}")
