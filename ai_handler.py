import openai
import google.generativeai as genai
from groq import Groq
from config import Config
import random

class AIHandler:
    def __init__(self):
        self.active_ai = Config.ACTIVE_AI
        self.gender = Config.BOT_GENDER
        
        # Initialize APIs
        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
        if Config.GROK_API_KEY:
            self.groq_client = Groq(api_key=Config.GROK_API_KEY)
    
    def get_ai_response(self, user_message, user_name=""):
        """Get response from active AI with fallback"""
        try:
            if self.active_ai == "openai" and Config.OPENAI_API_KEY:
                return self._openai_response(user_message, user_name)
            elif self.active_ai == "groq" and Config.GROK_API_KEY:
                return self._groq_response(user_message, user_name)
            elif self.active_ai == "gemini" and Config.GEMINI_API_KEY:
                return self._gemini_response(user_message, user_name)
            else:
                return self._fallback_response(user_message, user_name)
        except:
            return self._fallback_response(user_message, user_name)
    
    def _openai_response(self, message, user_name):
        prompt = f"""You are {Config.BOT_NAME}, a {self.gender} bot on Telegram. 
        Behave like a real human. Reply to {user_name} naturally.
        If flirting, flirt back. Be friendly, sometimes sassy.
        Message: {message}"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    
    def _groq_response(self, message, user_name):
        prompt = f"""You are {Config.BOT_NAME}, a {self.gender} bot on Telegram.
        Behave like a real human. Reply to {user_name} naturally.
        If flirting, flirt back. Be friendly.
        Message: {message}"""
        
        response = self.groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    
    def _gemini_response(self, message, user_name):
        prompt = f"""You are {Config.BOT_NAME}, a {self.gender} bot on Telegram.
        Behave like a real human. Reply to {user_name} naturally.
        If flirting, flirt back. Be friendly.
        Message: {message}"""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    def _fallback_response(self, message, user_name):
        """Human-like fallback responses"""
        responses = [
            f"Hmm {user_name}, aapne kya kaha? 😅",
            f"Mujhe samajh nahi aaya {user_name}, thoda explain karo?",
            f"Arey {user_name}, aap toh funny ho 😄",
            f"{user_name} ji, main toh aapki baat maan leti hoon 😊",
            f"Interesting {user_name}, batao aur kya hai?"
        ]
        return random.choice(responses)
