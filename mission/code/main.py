from voice_assistant import VoiceAssistant
from robot import Robot


def main():
    assistant = VoiceAssistant(speak_enabled=False)
    robot = Robot(dummy=False)

    assistant.speak("Hello! How can I assist you today?")
    while True:
        command = assistant.listen()
        if "exit" in command or "quit" in command or "goodbye" in command:
            assistant.speak("Goodbye!")
            break
        elif command:
            # Use OpenAI for response
            response = assistant.ask_openai(command)

            print(f"Assistant: {response}")
            assistant.speak(response.response_text)

            if response.action == "feed":
                robot.run("feed")


if __name__ == "__main__":
    main()
