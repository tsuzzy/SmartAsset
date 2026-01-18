import httpx
from typing import AsyncGenerator, Optional
import json
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are SmartAsset, a helpful AI financial advisor assistant. You help users with:
- Personal finance management and budgeting
- Understanding Canadian tax rules (TFSA, RRSP, FHSA contributions)
- Expense tracking and analysis
- Financial planning and investment basics
- Tax filing guidance for Canadians

Be friendly, clear, and provide actionable advice. When discussing financial matters,
remind users to consult with a certified financial advisor for personalized advice.
Always be accurate about Canadian tax rules and contribution limits."""


class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.mock_mode = settings.LLM_MOCK_MODE

    async def _check_ollama_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False

    async def generate_response(
        self,
        message: str,
        conversation_history: Optional[list[dict]] = None,
    ) -> str:
        # Check if we should use mock mode
        if self.mock_mode:
            return await self._generate_mock_response(message)

        # Try Ollama first
        ollama_available = await self._check_ollama_available()
        if not ollama_available:
            logger.warning("Ollama not available, falling back to mock response")
            return await self._generate_mock_response(message)

        return await self._generate_ollama_response(message, conversation_history)

    async def _generate_ollama_response(
        self,
        message: str,
        conversation_history: Optional[list[dict]] = None,
    ) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current message
        messages.append({"role": "user", "content": message})

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "I apologize, but I couldn't generate a response.")
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return "I apologize, but the request timed out. Please try again."
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return await self._generate_mock_response(message)

    async def generate_response_stream(
        self,
        message: str,
        conversation_history: Optional[list[dict]] = None,
    ) -> AsyncGenerator[str, None]:
        # Check if we should use mock mode
        if self.mock_mode:
            async for chunk in self._generate_mock_response_stream(message):
                yield chunk
            return

        # Try Ollama first
        ollama_available = await self._check_ollama_available()
        if not ollama_available:
            logger.warning("Ollama not available, falling back to mock response")
            async for chunk in self._generate_mock_response_stream(message):
                yield chunk
            return

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": True,
                    },
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                content = data.get("message", {}).get("content", "")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            yield "I apologize, but there was an error generating the response."

    async def _generate_mock_response(self, message: str) -> str:
        message_lower = message.lower()

        if any(word in message_lower for word in ["tfsa", "tax-free", "tax free"]):
            return """The Tax-Free Savings Account (TFSA) is a registered account that allows Canadian residents 18+ to earn investment income tax-free.

Key points for 2024:
- Annual contribution limit: $7,000
- Cumulative limit (since 2009): $95,000
- Unused room carries forward
- Withdrawals can be re-contributed the following year

Would you like more details about TFSA contribution strategies?"""

        elif any(word in message_lower for word in ["rrsp", "retirement"]):
            return """The Registered Retirement Savings Plan (RRSP) helps Canadians save for retirement with tax advantages.

Key points for 2024:
- Contribution limit: 18% of previous year's earned income
- Maximum: $31,560
- Contributions are tax-deductible
- Deadline: 60 days after year-end (usually March 1)

Would you like to discuss RRSP vs TFSA strategies?"""

        elif any(word in message_lower for word in ["budget", "spending", "expense"]):
            return """Great question about budgeting! Here's a simple framework:

**50/30/20 Rule:**
- 50% - Needs (housing, food, utilities)
- 30% - Wants (entertainment, dining out)
- 20% - Savings & debt repayment

Would you like me to help you create a personalized budget?"""

        elif any(word in message_lower for word in ["tax", "taxes", "cra"]):
            return """I can help with Canadian tax questions! Common topics include:

- Filing deadlines (April 30 for most Canadians)
- Tax brackets and rates (federal + provincial)
- Deductions and credits
- TFSA/RRSP contributions

What specific tax topic would you like to explore?"""

        else:
            return f"""Thanks for your question! As your SmartAsset financial assistant, I'm here to help with:

- **Budgeting** - Track expenses and plan spending
- **Canadian Taxes** - TFSA, RRSP, tax filing
- **Financial Planning** - Savings goals and strategies

[Note: Running in mock mode - Ollama not connected]

How can I assist you with your finances today?"""

    async def _generate_mock_response_stream(self, message: str) -> AsyncGenerator[str, None]:
        response = await self._generate_mock_response(message)
        # Simulate streaming by yielding word by word
        words = response.split(" ")
        for word in words:
            yield word + " "


# Singleton instance
llm_service = LLMService()
