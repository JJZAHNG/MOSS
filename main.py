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

    # 启动语音助手的线程
    voice_thread = threading.Thread(target=start_voice_assistant, args=(emotion_queue,))
    voice_thread.start()

    # 在主线程中运行视频播放器
    run_video_player(emotion_queue)

    # 等待语音助手线程结束
    voice_thread.join()

    # 在主线程中检查是否需要终止程序
    if not emotion_queue.empty():
        termination_signal = emotion_queue.get()
        if termination_signal == "terminate":
            print("Terminating the program...")
            exit()
