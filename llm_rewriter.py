"""
LLM Rewriter Module - Simplified Version
Author: Your Name
Description: Email rewriting using Google's Gemini API
"""

import google.generativeai as genai
import time
import logging


class EmailRewriter:
    """Email rewriter using Gemini 2.5 Flash"""

    def __init__(self, api_key: str):
        """Initialize with API key"""
        if not api_key:
            raise ValueError("API key is required")

        # Configure API and initialize model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("EmailRewriter initialized with Gemini 2.5 Flash")

    def rewrite_email(self, email_text: str, user_instructions: str = "") -> dict:
        """
        Rewrite email professionally

        Args:
            email_text: Original email
            user_instructions: Custom instructions (optional)

        Returns:
            dict: {'success', 'rewritten_text', 'error', 'processing_time'}
        """
        start_time = time.time()

        try:
            if not email_text.strip():
                return {
                    'success': False,
                    'rewritten_text': '',
                    'error': 'Email text cannot be empty',
                    'processing_time': 0
                }

            # Create prompt
            base_prompt = """Rewrite this email to be professional, formal, and appropriate for business communication.
- Maintain the core message
- Use professional language
- Correct grammar and spelling
- Remove spam characteristics
- Make it concise and clear"""

            if user_instructions.strip():
                base_prompt += f"\n\nAdditional instructions: {user_instructions}"

            prompt = f"{base_prompt}\n\nOriginal Email:\n{email_text}\n\nRewritten Email:"

            # Generate response
            response = self.model.generate_content(prompt)

            if response.text:
                return {
                    'success': True,
                    'rewritten_text': response.text.strip(),
                    'error': None,
                    'processing_time': time.time() - start_time
                }
            else:
                return {
                    'success': False,
                    'rewritten_text': '',
                    'error': 'No response from API',
                    'processing_time': time.time() - start_time
                }

        except Exception as e:
            return {
                'success': False,
                'rewritten_text': '',
                'error': str(e),
                'processing_time': time.time() - start_time
            }


# Example usage
if __name__ == "__main__":
    # Replace with your API key
    api_key = "AIzaSyApRtIWlXf8Ya_bImiYSk0g66CCphZFf3I"

    try:
        rewriter = EmailRewriter(api_key=api_key)

        # Test email
        test_email = """URGENT!!! MONEY MAKING OPPORTUNITY!!!

hey there!!!

i have amazing opportunity for you to make $$$$ FAST!!! 
just click this link and get rich quick!!!

dont miss out!!! limited time only!!!

contact me asap!!!"""

        print("Original Email:")
        print(test_email)
        print("\n" + "=" * 50 + "\n")

        # Rewrite
        result = rewriter.rewrite_email(test_email, "Make it professional for business")

        if result['success']:
            print("Rewritten Email:")
            print(result['rewritten_text'])
            print(f"\nProcessing time: {result['processing_time']:.2f}s")
        else:
            print(f"Error: {result['error']}")

    except Exception as e:
        print(f"Setup Error: {e}")
        print("\nTo use this module:")
        print("1. Get API key from: https://aistudio.google.com/")
        print("2. Replace 'your-api-key-here' with your actual key")