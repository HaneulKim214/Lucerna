import os, time
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from util import validate_dates
from prompts import prompt_templates as pt
from typing import Dict, Any, Optional, List, Union

from dotenv import load_dotenv
load_dotenv(override=True)

# ??? WHat is ABC?
class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    # @abstractmethod
    # def generate_content(self, prompt: str, **kwargs) -> str:
    #     """Generate content using the LLM.
    #
    #     Args:
    #         prompt: The text prompt to send to the LLM
    #         **kwargs: Additional provider-specific parameters
    #
    #     Returns:
    #         Generated text response
    #     """
    #     pass
    #
    # @abstractmethod
    # def get_model_name(self) -> str:
    #     """Get the name of the current model being used.
    #
    #     Returns:
    #         Model name as a string
    #     """
    #     pass

class GeminiProvider(LLMProvider):
    """Gemini model list: https://ai.google.dev/gemini-api/docs/models"""

    def __init__(self, model_version: str = "gemini-2.0-flash"):
        """Initialize the Gemini provider.

        Args:
            model_version: The version of the Gemini model to use
        """
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel(model_version)
        self.model_version = model_version

    def generate_content(self, prompt: str, generation_config, **kwargs) -> str:
        response = self.model.generate_content(prompt, generation_config=generation_config,
                                               **kwargs)
        return response.text

    def get_model_list():
        genai.list


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, model_version: str = "gpt-4.1"):
        """Initialize the OpenAI provider.
        OpenAI model versions: https://platform.openai.com/docs/models
            - reasoning: o3, o4-mini, etc...
            - chat: GPT-4.1, ChatGPT-4o
            - cost optimized: o4-mini, GPT-4.1 mini, GPT-4.1 nano
        Args:
            model_version: The version of the OpenAI model to use
        """
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model_version = model_version

    def generate_content(self, prompt: str, generation_config, **kwargs) -> str:
        # Extract OpenAI specific parameters or use defaults
        # temperature = kwargs.get('temperature', 0.7)
        # max_tokens = kwargs.get('max_tokens', 1000)

        response = self.client.chat.completions.create(
            model=self.model_version,
            # tools=[{"type": "web_search_preview"}],
            messages=[{"role": "user", "content": prompt}]
            # , temperature=temperature
            # ,max_tokens=max_tokens
        )

        return response.choices[0].message.content


class LLMFactory:
    """Factory class for creating LLM providers."""
    @staticmethod
    def create_provider(provider: str, model_version: Optional[str] = None) -> LLMProvider:
        provider = provider.lower()
        if provider == "gemini":
            if model_version:
                return GeminiProvider(model_version)
            return GeminiProvider()
        elif provider == "openai":
            if model_version:
                return OpenAIProvider(model_version)
            return OpenAIProvider()
        else:
            raise ValueError(f"Provider '{provider}' is not supported")


class Lucerna:
    """Main interface for the AI robo advisor."""

    def __init__(self, provider: str = "gemini", model_version: Optional[str] = None):
        """Initialize the Lucerna advisor.

        Args:
            provider: The LLM provider to use ("gemini", "openai", or "anthropic")
            model_version: Optional specific model version to use
        """
        if not model_version:
            model_version = 'default'
        self.llm = LLMFactory.create_provider(provider, model_version)
        
        print(f"LLM successfully configured with: {provider.upper()}: {model_version}")

    def explain_company(self, company, custom_prompt=None, generation_config={}) -> str:
        """Explain services for a given company.

        Args:
            company: The company name to explain services for
            custom_prompt: Optional custom prompt to use instead of the default
            config: Dict or config class

        Returns:
            Generated explanation as text
        """
        if custom_prompt:
            prompt = custom_prompt
        else:
            # Assuming pt.prompt_service_info is defined elsewhere
            # You would replace this with your actual prompt template
            prompt = pt.prompt_company_info
        
        return self.llm.generate_content(prompt.format(company=company),
                                        generation_config)

    def get_investment_advice(self,
                              risk_profile: str,
                              investment_horizon: str,
                              goals: List[str],
                              custom_prompt: Optional[str] = None) -> str:
        """Get personalized investment advice.

        Args:
            risk_profile: The risk tolerance profile (e.g., "conservative", "moderate", "aggressive")
            investment_horizon: The time period for the investment (e.g., "5 years", "10 years")
            goals: List of financial goals
            custom_prompt: Optional custom prompt to override the default

        Returns:
            Generated investment advice as text
        """
        if custom_prompt:
            prompt = custom_prompt
        else:
            goals_text = ", ".join(goals)
            prompt = (
                f"Provide investment advice for someone with a {risk_profile} risk profile, "
                f"an investment horizon of {investment_horizon}, and the following financial goals: {goals_text}."
            )

        return self.llm.generate_content(prompt)

    def analyze_portfolio(self,
                          portfolio: Dict[str, float],
                          market_conditions: str,
                          custom_prompt: Optional[str] = None) -> str:
        """Analyze an investment portfolio.

        Args:
            portfolio: Dictionary mapping asset names to their allocation percentages
            market_conditions: Description of current market conditions
            custom_prompt: Optional custom prompt to override the default

        Returns:
            Generated portfolio analysis as text
        """
        if custom_prompt:
            prompt = custom_prompt
        else:
            portfolio_text = ", ".join([f"{asset}: {percentage}%" for asset, percentage in portfolio.items()])
            prompt = (
                f"Analyze the following investment portfolio given the current market conditions.\n\n"
                f"Portfolio: {portfolio_text}\n\n"
                f"Market Conditions: {market_conditions}"
            )

        return self.llm.generate_content(prompt)

    def switch_provider(self, provider: str, model_version: Optional[str] = None) -> None:
        """Switch to a different LLM provider.

        Args:
            provider: The new LLM provider to use
            model_version: Optional specific model version to use
        """
        self.llm = LLMFactory.create_provider(provider, model_version)
        print(f"Switched to {provider} provider with model: {self.llm.get_model_name()}")