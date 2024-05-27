import threading
from queue import Queue
from VoiceInteractions import VoiceAssistant
from ScreenView import run_video_player

def start_voice_assistant(emotion_queue):
    assistant = VoiceAssistant(emotion_queue)
    assistant.run()

def start_video_player(emotion_queue):
    run_video_player(emotion_queue)

if __name__ == "__main__":
    emotion_queue = Queue()

    video_thread = threading.Thread(target=start_video_player, args=(emotion_queue,))
    voice_thread = threading.Thread(target=start_voice_assistant, args=(emotion_queue,))

    video_thread.start()
    voice_thread.start()

    video_thread.join()
    voice_thread.join()
