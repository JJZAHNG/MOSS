import pygame
import os
import time
import speech_recognition as sr
from openai import OpenAI
from aip import AipSpeech
from queue import Queue

class VoiceAssistant:
    def __init__(self, emotion_queue):
        pygame.init()
        pygame.mixer.init()
        API_KEY = os.getenv('OPENAI_API_KEY')
        API_BASE = "https://pro.aiskt.com/v1"

        if API_KEY is None:
            raise ValueError("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")

        self.client = OpenAI(api_key=API_KEY, base_url=API_BASE)
        print('通行口令>>>', self.client.api_key)
        print('通行路径>>>', str(self.client.base_url))

        self.BASE_DIR = os.path.dirname(__file__)
        self.WELCOME_DIR = os.path.join(self.BASE_DIR, 'welcome.mp3')
        self.HUMAN_TURN = os.path.join(self.BASE_DIR, 'HumanTurn.mp3')
        self.BYEBYE = os.path.join(self.BASE_DIR, 'byebye.mp3')
        self.ROBOT_TURN = os.path.join(self.BASE_DIR, 'RobotTurn.mp3')

        self.APP_ID = os.getenv('BAIDU_APP_ID')
        self.API_KEY = os.getenv('BAIDU_API_KEY')
        self.SECRET_KEY = os.getenv('BAIDU_SECRET_KEY')

        if None in [self.APP_ID, self.API_KEY, self.SECRET_KEY]:
            raise ValueError(
                "Baidu API credentials are not set. Please set the environment variables BAIDU_APP_ID, BAIDU_API_KEY, and BAIDU_SECRET_KEY.")

        self.bd_client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        self.messages = [
            {
                "role": "assistant",
                "content": "你是一个非常厉害的成语接龙玩家，非常擅长成语接龙（可以用谐音字）"
            }
        ]

        self.emotion_queue = emotion_queue

    def init_voice(self):
        self._play_voice(self.WELCOME_DIR)

    def exit_voice(self):
        self._play_voice(self.BYEBYE)

    def _play_voice(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

    def my_record(self, rate=16000):
        recognizer = sr.Recognizer()
        with sr.Microphone(sample_rate=rate) as source:
            print("你 的 回 合 > > > ")
            audio = recognizer.listen(source, phrase_time_limit=10)
        with open(self.HUMAN_TURN, "wb") as f:
            f.write(audio.get_wav_data())
        print("VOICE INPUTTED")

    def watch_listen(self):
        try:
            with open(self.HUMAN_TURN, 'rb') as fp:
                voices = fp.read()
            result = self.bd_client.asr(voices, 'wav', 16000, {'dev_pid': 1537})
            if result and 'result' in result and result['result']:
                result_text = result["result"][0]
                print("我 听 到 你 说 ： " + result_text)
                print('--------------------------间 隔--------------------------')
                return result_text
            else:
                print("监听识别结果为空或无效。")
                return None
        except KeyError as e:
            print(f"Error: {e}")
            print("Could not get access token.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def stt(self):
        try:
            with open(self.HUMAN_TURN, "rb") as audio_file:
                transcript_response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format='json'
                )
            transcript = transcript_response.text
            print('MOSS 理解：', transcript)
            self.messages.append({"role": "user", "content": transcript})
            return transcript
        except Exception as e:
            print(f"MOSS 语音转文本过程中发生错误：{e}")
            return None

    def conversation(self):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=self.messages,
            )
            content = response.choices[0].message.content.strip()
            print("MOSS回答： " + content)
            self.messages.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            print(f"OpenAI 对话过程中发生错误：{e}")
            return None

    def tts(self, inp):
        if inp is None:
            print("文本内容为空，无法进行语音合成。")
            return
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=inp
            )
            response.stream_to_file(self.ROBOT_TURN)
            self._play_voice(self.ROBOT_TURN)
        except Exception as e:
            print(f"MOSS 语音合成过程中发生错误：{e}")

    def run(self):
        print("--- 欢迎来到 「成语接龙」 挑战赛 ---")
        self.init_voice()
        while True:
            try:
                if not self.emotion_queue.empty():
                    termination_signal = self.emotion_queue.get()
                    if termination_signal == "terminate":
                        print("Terminating the voice assistant...")
                        self.exit_voice()
                        break

                self.my_record()
                spy_result = self.watch_listen()
                if spy_result:
                    if "笨笨" in spy_result or "本本" in spy_result or "奔奔" in spy_result:
                        print(f"触发关键词，MOSS正在处理：{spy_result}")
                        transcript = self.stt()
                        if transcript:
                            response_content = self.conversation()
                            self.tts(response_content)
                        else:
                            print('MOSS 语音转文本结果为空。')
                    elif 'goodbye' in spy_result or '退出' in spy_result or '再见' in spy_result:
                        self.exit_voice()
                        print('正在退出...')
                        break
                else:
                    print('ERROR VOICE INPUT --- NONE RECEIVED')
                    continue
            except TypeError:
                print('ERROR VOICE INPUT --- NONE RECEIVED')
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                continue


if __name__ == "__main__":
    emotion_queue = Queue()
    assistant = VoiceAssistant(emotion_queue)
    assistant.run()