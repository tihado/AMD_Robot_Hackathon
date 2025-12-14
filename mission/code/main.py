from voice_assistant import VoiceAssistant
from robot import Robot
import threading


def main():
    assistant = VoiceAssistant(speak_enabled=True)
    robot = Robot(dummy=False)

    assistant.speak("Hello! How can I assist you today?")
    while True:
        command = assistant.listen()
        if command == "" or not command:
            continue

        # Use OpenAI for response
        response = assistant.ask_openai(command)
        print(f"Assistant: {response}")

        if response.action == "bye":
            assistant.speak(response.response_text)
            print("Bye bye!")
            break

        if response.action == "feed":
            # Run speak and robot.run in parallel
            speak_thread = threading.Thread(
                target=assistant.speak, args=(response.response_text,)
            )
            robot_thread = threading.Thread(target=robot.run, args=("feed",))

            speak_thread.start()
            robot_thread.start()

            # Wait for both threads to complete
            speak_thread.join()
            robot_thread.join()
        else:
            assistant.speak(response.response_text)


if __name__ == "__main__":
    main()
