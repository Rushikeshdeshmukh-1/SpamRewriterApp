"""
LLM Rewriter Module
Author: [Your Name]
Description: Handles email rewriting using Google's Gemini API
"""

import google.generativeai as genai
import os
from typing import Optional, Dict, Any
import time
import logging

class EmailRewriter:
    """
    A class to handle email rewriting using Google's Gemini API
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the EmailRewriter with Gemini API

        Args:
            api_key (str): Google AI API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set GOOGLE_AI_API_KEY environment variable or pass it directly.")

        # Set up logging first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Configure the API
        genai.configure(api_key=self.api_key)

        # Initialize the model with fallback options
        self.model = self._initialize_model()

    def _initialize_model(self):
        """
        Initialize the Gemini 2.5 Flash model
        """
        model_name = 'models/gemini-2.5-flash'

        try:
            self.logger.info(f"Initializing model: {model_name}")
            model = genai.GenerativeModel(model_name)

            # Test the model with a simple request
            test_response = model.generate_content("Hello")
            if test_response.text:
                self.logger.info(f"Successfully initialized model: {model_name}")
                return model
            else:
                raise ValueError("Model test failed - no response generated")

        except Exception as e:
            error_msg = f"Failed to initialize {model_name}: {str(e)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    def create_rewrite_prompt(self, email_text: str, user_instructions: str = "") -> str:
        """
        Create a well-engineered prompt for email rewriting

        Args:
            email_text (str): The original email text
            user_instructions (str): Custom instructions from user

        Returns:
            str: The complete prompt for the LLM
        """
        base_prompt = """You are an expert email writer. Your task is to rewrite the given email to make it more professional, formal, and appropriate for business communication.

Follow these guidelines:
1. Maintain the core message and intent
2. Use professional language and tone
3. Correct any grammar or spelling errors
4. Remove spam-like characteristics (excessive caps, multiple exclamation marks, etc.)
5. Make it concise yet complete
6. Ensure proper email etiquette"""

        if user_instructions.strip():
            custom_instructions = f"\n\nAdditional custom instructions: {user_instructions}"
        else:
            custom_instructions = ""

        full_prompt = f"""{base_prompt}{custom_instructions}

Original Email:
{email_text}

Please rewrite this email following the guidelines above. Only return the rewritten email, no additional comments."""

        return full_prompt

    def rewrite_email(self, email_text: str, user_instructions: str = "") -> Dict[str, Any]:
        """
        Rewrite an email using Gemini API

        Args:
            email_text (str): The original email text
            user_instructions (str): Custom rewriting instructions

        Returns:
            Dict: Contains 'success', 'rewritten_text', 'error', 'processing_time'
        """
        start_time = time.time()

        try:
            # Input validation
            if not email_text or not email_text.strip():
                return {
                    'success': False,
                    'rewritten_text': '',
                    'error': 'Email text cannot be empty',
                    'processing_time': 0
                }

            # Create the prompt
            prompt = self.create_rewrite_prompt(email_text, user_instructions)
            self.logger.info("Sending request to Gemini API...")

            # Generate response
            response = self.model.generate_content(prompt)

            if response.text:
                processing_time = time.time() - start_time
                self.logger.info(f"Email rewritten successfully in {processing_time:.2f} seconds")

                return {
                    'success': True,
                    'rewritten_text': response.text.strip(),
                    'error': None,
                    'processing_time': processing_time
                }
            else:
                return {
                    'success': False,
                    'rewritten_text': '',
                    'error': 'No response generated from API',
                    'processing_time': time.time() - start_time
                }

        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Error during rewriting: {str(e)}"
            self.logger.error(error_msg)

            return {
                'success': False,
                'rewritten_text': '',
                'error': error_msg,
                'processing_time': processing_time
            }

    def list_available_models(self) -> list:
        """
        List all available models for debugging

        Returns:
            list: Available model names
        """
        try:
            models = genai.list_models()
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
                    self.logger.info(f"Available model: {model.name}")
            return available_models
        except Exception as e:
            self.logger.error(f"Error listing models: {str(e)}")
            return []
        """
        Test if the API connection is working
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            test_response = self.model.generate_content("Hello, this is a test.")
            return bool(test_response.text)
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Example usage (your teammates can use this as reference)

    # Initialize the rewriter (make sure to set your API key)
    # You can get a free API key from: https://makersuite.google.com/app/apikey

    # Option 1: Set environment variable
    # os.environ['GOOGLE_AI_API_KEY'] = 'your-api-key-here'
    # rewriter = EmailRewriter()

    # Option 2: Pass directly (not recommended for production)
    # rewriter = EmailRewriter(api_key='your-api-key-here')

    # For demo purposes - pass your API key directly
    try:
        # Replace 'your-api-key-here' with your actual Google AI API key
        rewriter = EmailRewriter(api_key='AIzaSyApRtIWlXf8Ya_bImiYSk0g66CCphZFf3I')

        # Test email (typical spam-like email)
        test_email = """
        URGENT!!! MONEY MAKING OPPORTUNITY!!!
        
        hey there!!!
        
        i have amazing opportunity for you to make $$$$ FAST!!! 
        just click this link and get rich quick!!!
        
        dont miss out!!! limited time only!!!
        
        contact me asap!!!
        """

        # Test the rewriter
        result = rewriter.rewrite_email(test_email, "Make it sound like a professional business proposal")

        if result['success']:
            print("Original Email:")
            print(test_email)
            print("\n" + "="*50 + "\n")
            print("Rewritten Email:")
            print(result['rewritten_text'])
            print(f"\nProcessing time: {result['processing_time']:.2f} seconds")
        else:
            print(f"Error: {result['error']}")

    except ValueError as e:
        print(f"Setup Error: {e}")
        print("\nTo use this module, you need to:")
        print("1. Get a Google AI API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as environment variable: GOOGLE_AI_API_KEY")
        print("3. Or pass it directly to EmailRewriter(api_key='your-key')")