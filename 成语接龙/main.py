from idioms import VoiceAssistant, create_window
from queue import Queue

if __name__ == "__main__":
    emotion_queue = Queue()
    assistant = VoiceAssistant(emotion_queue)
    assistant.init_voice()
    create_window()
    assistant.run()
