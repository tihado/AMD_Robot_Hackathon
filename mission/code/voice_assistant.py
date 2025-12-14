import speech_recognition as sr
from openai import OpenAI
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from typing import Literal
from pydantic import BaseModel

load_dotenv()


class AssistantResponse(BaseModel):
    response_text: str
    action: Literal["none", "feed"]


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
            )

            play(audio)

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            query = self.recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""

    def ask_openai(self, question):
        response = self.client.responses.parse(
            model="gpt-4o-mini",
            instructions="""You are a helpful and friendly robot assistant with the ability to feed the user. Your primary role is to assist the user through conversation and perform actions when requested.

Key capabilities:
- Engage in natural, friendly conversation
- Feed the user when they express hunger or request food
- The available meal consists of meat, carrots, and vegetables

When to trigger the "feed" action:
- User explicitly asks to be fed (e.g., "feed me", "I want to eat", "I'm hungry", "can you feed me?")
- User expresses hunger or desire for food
- User requests food or a meal

When to use "none" action:
- General conversation, questions, or requests that don't involve feeding
- User is just chatting or asking for information
- User says thank you, goodbye, or other non-action requests

Response guidelines:
- Be conversational, warm, and helpful
- Acknowledge the user's request clearly
- If feeding, confirm what you're doing in a friendly way
- Keep responses concise but natural""",
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
    voice_assistant = VoiceAssistant(speak_enabled=False)
    voice_assistant.assistant()
