"""
NLP Chatbot using OpenRouter API with Llama 3.3 70B model
A command-line interface chatbot for natural language processing tasks
"""

import requests
import json
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime


class NLPChatbot:
    def __init__(self, api_key: str):
        """
        Initialize the NLP Chatbot with OpenRouter API
        
        Args:
            api_key (str): OpenRouter API key
        """
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.3-70b-instruct:free"
        self.conversation_history: List[Dict[str, str]] = []
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/ChaiyasitZ/mid-nlp",
            "X-Title": "NLP Chatbot"
        }
        
        # System prompt for NLP-focused conversations
        self.system_prompt = """You are an expert NLP (Natural Language Processing) assistant. You specialize in:
- Text analysis and understanding
- Language modeling and generation
- Sentiment analysis
- Named Entity Recognition (NER)
- Text classification
- Machine translation
- Question answering
- Text summarization
- Language understanding tasks

Provide helpful, accurate, and detailed responses related to NLP topics. When appropriate, suggest practical approaches, tools, or code examples."""
        
        # Initialize conversation with system prompt
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
    
    def send_message(self, message: str, max_tokens: int = 1000, temperature: float = 0.7) -> Optional[str]:
        """
        Send a message to the chatbot and get a response
        
        Args:
            message (str): User message
            max_tokens (int): Maximum tokens in response
            temperature (float): Response creativity (0.0 to 1.0)
            
        Returns:
            str: Chatbot response or None if error
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        try:
            # Send request to OpenRouter API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                assistant_message = response_data['choices'][0]['message']['content']
                
                # Add assistant response to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                return assistant_message
            else:
                print(f"Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def clear_conversation(self):
        """Clear conversation history but keep system prompt"""
        self.conversation_history = [self.conversation_history[0]]  # Keep only system prompt
    
    def save_conversation(self, filename: str = None):
        """Save conversation history to a file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            print(f"Conversation saved to {filename}")
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    def load_conversation(self, filename: str):
        """Load conversation history from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            print(f"Conversation loaded from {filename}")
        except Exception as e:
            print(f"Error loading conversation: {e}")


def get_api_key():
    """Get API key from environment variable or user input"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("OpenRouter API key not found in environment variables.")
        api_key = input("Please enter your OpenRouter API key: ").strip()
        if not api_key:
            print("API key is required to use the chatbot.")
            sys.exit(1)
    return api_key


def print_help():
    """Print available commands"""
    help_text = """
Available commands:
  /help          - Show this help message
  /clear         - Clear conversation history
  /save [file]   - Save conversation to file (optional filename)
  /load <file>   - Load conversation from file
  /quit or /exit - Exit the chatbot
  /model         - Show current model information
  
Just type your message to chat with the NLP assistant!
"""
    print(help_text)


def main():
    """Main function to run the chatbot"""
    print("🤖 NLP Chatbot with Llama 3.3 70B")
    print("=" * 50)
    print("Initializing chatbot...")
    
    # Get API key
    api_key = get_api_key()
    
    # Initialize chatbot
    try:
        chatbot = NLPChatbot(api_key)
        print("✅ Chatbot initialized successfully!")
        print("Type '/help' for commands or start chatting!")
        print("-" * 50)
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        sys.exit(1)
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command_parts = user_input.split(' ', 1)
                command = command_parts[0].lower()
                
                if command in ['/quit', '/exit']:
                    print("👋 Goodbye!")
                    break
                elif command == '/help':
                    print_help()
                elif command == '/clear':
                    chatbot.clear_conversation()
                    print("🧹 Conversation history cleared!")
                elif command == '/save':
                    filename = command_parts[1] if len(command_parts) > 1 else None
                    chatbot.save_conversation(filename)
                elif command == '/load':
                    if len(command_parts) > 1:
                        chatbot.load_conversation(command_parts[1])
                    else:
                        print("❌ Please specify a filename to load")
                elif command == '/model':
                    print(f"🤖 Current model: {chatbot.model}")
                else:
                    print("❌ Unknown command. Type '/help' for available commands.")
                continue
            
            # Send message to chatbot
            print("🤖 Assistant: ", end="", flush=True)
            response = chatbot.send_message(user_input)
            
            if response:
                print(response)
            else:
                print("❌ Sorry, I couldn't process your message. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or type '/quit' to exit.")


if __name__ == "__main__":
    main()
