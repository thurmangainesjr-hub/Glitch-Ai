"""
GLITCH LLM SERVICE
AI model integration layer
"""

import os
from typing import Dict, Any, Optional
import httpx
import json


class LLMService:
    """
    Service for interacting with LLM APIs.
    Supports OpenAI, Anthropic, and local models.
    """

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.default_provider = os.getenv("LLM_PROVIDER", "openai")
        self.default_model = os.getenv("LLM_MODEL", "gpt-4")

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        provider: str = None,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate a response from the LLM.
        """
        provider = provider or self.default_provider
        model = model or self.default_model

        if provider == "openai":
            return await self._openai_generate(
                prompt, system_prompt, model, temperature, max_tokens
            )
        elif provider == "anthropic":
            return await self._anthropic_generate(
                prompt, system_prompt, model, temperature, max_tokens
            )
        else:
            # Fallback to mock response for testing
            return self._mock_response(prompt)

    async def _openai_generate(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using OpenAI API."""
        if not self.openai_key:
            return self._mock_response(prompt)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=120.0
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return self._mock_response(prompt)

    async def _anthropic_generate(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate using Anthropic API."""
        if not self.anthropic_key:
            return self._mock_response(prompt)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.anthropic_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model or "claude-3-opus-20240229",
                    "max_tokens": max_tokens,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=120.0
            )

            if response.status_code == 200:
                data = response.json()
                return data["content"][0]["text"]
            else:
                return self._mock_response(prompt)

    async def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze a prompt and return structured data.
        """
        system = """Analyze the request and return a JSON object with:
- project_type: web_app|mobile_app|api|automation|other
- features: list of required features
- tech_stack: recommended technologies
- complexity: simple|medium|complex
- agents: list of required agent types

Return ONLY valid JSON."""

        response = await self.generate(prompt, system)

        # Try to parse JSON from response
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except json.JSONDecodeError:
            pass

        # Default analysis
        return {
            "project_type": "web_app",
            "features": ["basic CRUD", "user interface"],
            "tech_stack": {"frontend": "React", "backend": "FastAPI"},
            "complexity": "medium",
            "agents": ["architect", "fullstack_dev"]
        }

    def _mock_response(self, prompt: str) -> str:
        """
        Generate a mock response when no API is available.
        """
        return f"""# GLITCH Development Response

Based on your request, here's a generated implementation:

## Architecture Overview
- Modular, scalable design
- RESTful API backend
- Modern frontend framework
- Secure authentication

## Implementation

```python
# Example backend code
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
async def root():
    return {{"message": "GLITCH API Running"}}

@app.post("/items")
async def create_item(item: Item):
    return {{"item": item, "status": "created"}}
```

```javascript
// Example frontend code
import React from 'react';

function App() {{
  return (
    <div className="app">
      <h1>GLITCH Application</h1>
      <p>Generated by GLITCH AI Dev System</p>
    </div>
  );
}}

export default App;
```

## Next Steps
1. Review the architecture
2. Customize for your needs
3. Deploy to production

---
Generated by GLITCH - AI Development Orchestration System
"""
