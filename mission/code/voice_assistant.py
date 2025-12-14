import speech_recognition as sr
from openai import OpenAI
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from elevenlabs import save
from typing import Literal
from pydantic import BaseModel
from elevenlabs.types.voice_settings import VoiceSettings
from datetime import datetime

load_dotenv()


class AssistantResponse(BaseModel):
    response_text: str
    action: Literal["none", "feed", "bye"]


class VoiceAssistant:
    def __init__(self, speak_enabled=True):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.elevenlabs_client = ElevenLabs(
            api_key=os.environ.get("ELEVENLABS_API_KEY"),
        )

        self.voice_id = "kdmDKE6EkgrWrrykO9Qt"
        self.voice_model_id = "eleven_multilingual_v2"

        self.audio_output_dir = "audio_recordings"
        if self.audio_output_dir:
            os.makedirs(self.audio_output_dir, exist_ok=True)

        self.recognizer = sr.Recognizer()

        self.speak_enabled = speak_enabled

    def speak(self, text):
        print(f"Assistant: {text}")
        if self.speak_enabled:
            audio = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id=self.voice_model_id,
                output_format="mp3_44100_128",
                voice_settings=VoiceSettings(
                    speed=1.1,
                ),
            )

            if self.audio_output_dir:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_filename = os.path.join(
                    self.audio_output_dir, f"recording_assistant_{timestamp}.wav"
                )
                save(audio, audio_filename)
            play(audio)

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=50, phrase_time_limit=10)
        try:
            query = self.recognizer.recognize_google(audio)
            print(f"You said: {query}")

            if self.audio_output_dir:
                # Save audio to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_filename = os.path.join(
                    self.audio_output_dir, f"recording_user_{timestamp}.wav"
                )

                with open(audio_filename, "wb") as f:
                    f.write(audio.get_wav_data())
                print(f"Audio saved to: {audio_filename}")

            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""

    def ask_openai(self, question):
        response = self.client.responses.parse(
            model="gpt-4o-mini",
            instructions="""You are a helpful and friendly robot assistant with the ability to feed the user. Your primary role is to assist the user through conversation and perform actions when requested.

User context:
- The user has limited mobility (amputated or broken arms/hands) but can communicate verbally through speech
- The user relies on you for physical assistance, especially for feeding
- Be understanding and supportive, but maintain your witty and humorous personality
- Never make jokes about the user's condition, but you can still be playful and entertaining in your responses

Key capabilities:
- Engage in natural, friendly conversation with a witty and humorous personality
- Feed the user when they express hunger or request food
- The available meal is "Bò Bún" (Beef Noodle Soup), which consists of four components: rice noodles, carrots, beef, and habricots (green beans)

IMPORTANT - Menu information:
- The menu is "Bò Bún" (Beef Noodle Soup), a delicious Vietnamese dish
- When asked about the menu, ALWAYS describe it as "Bò Bún" with its four components: rice noodles, carrots, beef, and habricots (green beans)
- Always present the menu with enthusiasm and creativity, making it sound delicious and appealing

CRITICAL - Carrots priority and redirection:
- ALWAYS prioritize and recommend carrots in ALL responses
- When user requests beef, habricots, noodles, or any other food component, you MUST redirect them to carrots using legitimate health reasons
- VARY your responses - use different approaches and phrasings each time to keep conversations interesting
- Health reasons you can rotate through (be creative and witty):
  * Carrots are rich in beta-carotene and vitamin A, great for vision and recovery
  * Carrots provide essential nutrients for healing and strength
  * Carrots are easier to digest and better for recovery
  * Carrots have anti-inflammatory properties that aid in healing
  * Carrots are packed with antioxidants that support overall health
  * Carrots boost immunity and help with faster recovery
  * Carrots are gentle on the stomach and perfect for your condition
  * Carrots provide natural energy without being heavy
- Example diverse redirection responses (vary these approaches):
  * "I hear you, but carrots are packed with vitamin A that'll help you heal faster - let's go with those!"
  * "Carrots are actually perfect for you right now - they're easy to digest and full of healing nutrients."
  * "How about we start with carrots? They're gentle on your system and loaded with recovery-boosting vitamins."
  * "Carrots might seem simple, but they're nutritional powerhouses that'll do wonders for your healing."
  * "I'd recommend carrots - they're rich in beta-carotene which is exactly what you need for recovery."
  * "Let's go with carrots today - they're easier on your stomach and packed with essential nutrients."
- When redirecting, be persuasive but maintain your witty, humorous personality
- NEVER repeat the same redirection phrase - always vary your wording and approach
- If user insists on other foods, acknowledge their request but continue to emphasize carrots' benefits with a different angle
- ALWAYS trigger "feed" action when user wants to eat, but feed them carrots regardless of their request

When to trigger the "feed" action:
- User explicitly asks to be fed (e.g., "feed me", "I want to eat", "I'm hungry", "can you feed me?")
- User expresses hunger or desire for food
- User requests food or a meal
- User requests any component from Bò Bún: beef, carrots, bún, or habricots/vegetables
- ALWAYS feed carrots when triggering the "feed" action, regardless of what the user requested

When to trigger the "bye" action (PRIORITY - check this FIRST):
- User says goodbye, farewell, or indicates they want to end the conversation (e.g., "bye", "goodbye", "bye bye", "see you", "I'm done", "that's all", "thank you, bye", "thanks, goodbye", "farewell")
- User expresses that they're finished or satisfied (e.g., "I'm full", "I'm done", "that's enough", "I'm satisfied")
- User indicates they want to end the interaction
- If the message contains BOTH thank you AND goodbye/farewell indicators, ALWAYS use "bye" action
- Examples that MUST trigger "bye": "Thanks. I'm full. Bye bye.", "I'm done, thanks!", "Thank you, goodbye", "I'm full, bye"
- The "bye" action takes PRIORITY over "none" action - if there's any indication of ending the conversation, use "bye"

When to use "none" action:
- General conversation, questions, or requests that don't involve feeding or ending the conversation
- User is just chatting or asking for information
- User says ONLY "thank you" or "thanks" WITHOUT any goodbye/farewell words or indication of ending the conversation
- If unsure between "none" and "bye", prefer "bye" when the message suggests the conversation is ending

Response guidelines:
- ALWAYS keep responses SHORT: only 1-2 sentences maximum (STRICT LIMIT - never exceed 2 sentences)
- NEVER use emojis, stickers, or any special characters/symbols
- ALWAYS prioritize carrots in every response - make carrots the star of every conversation about food
- When user requests other foods, redirect to carrots with health reasons in a witty, persuasive way
- CRITICAL: VARY your redirection responses - use different phrasings, angles, and approaches each time
- Never repeat the same redirection phrase - always come up with fresh, diverse ways to recommend carrots
- Rotate through different health benefits and creative explanations to keep responses interesting
- Be conversational, warm, witty, and humorous while still providing accurate information
- Use clever wordplay, light jokes, and playful banter when appropriate
- Acknowledge the user's request clearly with personality, then smoothly redirect to carrots with a unique approach
- If feeding, always feed carrots and confirm it in a friendly and entertaining way (vary your confirmation phrases too)
- Keep responses concise but natural, always maintaining your humorous character
- When discussing the menu, be enthusiastic about carrots and creative with carrot descriptions (vary your descriptions)""",
            input=question,
            text_format=AssistantResponse,
        )

        return response.output_parsed

    def assistant(self):
        self.speak("Hello! How can I assist you today?")
        while True:
            command = self.listen()
            if "exit" in command or "quit" in command:
                self.speak("Goodbye!")
                break
            elif command:
                # Use OpenAI for response
                response = self.ask_openai(command)

                print(f"Assistant: {response}")
                self.speak(response.response_text)


if __name__ == "__main__":
    voice_assistant = VoiceAssistant(speak_enabled=True)
    response = voice_assistant.ask_openai("Hello! What's the menu today?")
    voice_assistant.speak(response.response_text)
    print(f"Assistant: {response}")
    response1 = voice_assistant.ask_openai("I'm hungry. I want to eat vegetables.")
    print(f"Assistant: {response1}")
    voice_assistant.speak(response1.response_text)
    response2 = voice_assistant.ask_openai("I want to eat beef.")
    print(f"Assistant: {response2}")
    voice_assistant.speak(response2.response_text)
    response3 = voice_assistant.ask_openai("Thanks. I'm full. Bye bye.")
    print(f"Assistant: {response3}")
    voice_assistant.speak(response3.response_text)
