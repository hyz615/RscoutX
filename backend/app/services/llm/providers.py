from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import httpx

from app.core.config import settings


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text from prompt"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using OpenAI API"""
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Ollama API"""
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }
        
        url = f"{self.base_url}/api/generate"
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get('response', '')


def get_llm_provider() -> BaseLLMProvider:
    """Factory function to get LLM provider"""
    provider_type = settings.LLM_PROVIDER.lower()
    
    if provider_type == "openai":
        return OpenAIProvider()
    elif provider_type == "ollama":
        return OllamaProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_type}")
