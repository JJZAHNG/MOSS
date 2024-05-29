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
        
        # 添加调试信息
        if API_KEY is None:
            raise ValueError("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")
        
        self.client = OpenAI(api_key=API_KEY, base_url=API_BASE)
        # 校验
        print('通行口令>>>' + self.client.api_key)
        print('通行路径>>>' + str(self.client.base_url))

        self.BASE_DIR = os.path.dirname(__file__)
        self.MY_VOICE_DIR = os.path.join(self.BASE_DIR, 'MOSS_Voices', 'myvoices.mp3')
        self.ROBOT_VOICE_DIR = os.path.join(self.BASE_DIR, 'MOSS_Voices', 'robotVoices.mp3')
        self.INIT_VOICE_DIR = os.path.join(self.BASE_DIR, 'MOSS_Voices', 'init.mp3')
        self.START_VOICE_DIR = os.path.join(self.BASE_DIR, 'MOSS_Voices', 'starting.mp3')
        self.EXIT_VOICE_DIR = os.path.join(self.BASE_DIR, 'MOSS_Voices', 'exit.mp3')

        # 百度 API 配置
        self.APP_ID = os.getenv('BAIDU_APP_ID')
        self.API_KEY = os.getenv('BAIDU_API_KEY')
        self.SECRET_KEY = os.getenv('BAIDU_SECRET_KEY')

        # 添加调试信息
        if None in [self.APP_ID, self.API_KEY, self.SECRET_KEY]:
            raise ValueError("Baidu API credentials are not set. Please set the environment variables BAIDU_APP_ID, BAIDU_API_KEY, and BAIDU_SECRET_KEY.")

        self.bd_client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

        self.messages = [
            {"role": "system", "content": "You are a helpful assistant. And all your response should be in this way: RESPONSE: & EMOTION"}
        ]

        self.emotion_queue = emotion_queue

    def init_voice(self):
        self._play_voice(self.START_VOICE_DIR)

    def exit_voice(self):
        self._play_voice(self.EXIT_VOICE_DIR)

    def _play_voice(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

    def my_record(self, rate=16000):
        recognizer = sr.Recognizer()
        with sr.Microphone(sample_rate=rate) as source:
            print("请说话>>>")
            audio = recognizer.listen(source, phrase_time_limit=10)
        with open(self.MY_VOICE_DIR, "wb") as f:
            f.write(audio.get_wav_data())
        print("VOICE INPUTTED")

    def watch_listen(self):
        with open(self.MY_VOICE_DIR, 'rb') as fp:
            voices = fp.read()
        try:
            result = self.bd_client.asr(voices, 'wav', 16000, {'dev_pid': 1537})
            result_text = result["result"][0]
            print("我听到你说： " + result_text)
            print('--------------------------间隔--------------------------')
            return result_text
        except KeyError as e:
            print(f"Error: {e}")
            print("Could not get access token.")
            return None

    def stt(self):
        with open(self.MY_VOICE_DIR, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format='text'
            )
        print('你问我：' + transcript)
        self.messages.append({"role": "user", "content": transcript})
        return transcript

    def conversation(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=self.messages,
        )
        res = response.choices[0].message
        print("MOSS回答： " + res.content)
        self.messages.append({"role": "assistant", "content": res.content})
        
        # 判断情绪
        emotion = self.detect_emotion(res.content)
        self.emotion_queue.put(emotion)
        
        return res.content

    def detect_emotion(self, response_content):
        # 这里添加你的情绪识别逻辑
        if "happy" in response_content:
            return "happy"
        elif "sad" in response_content:
            return "sad"
        elif "angry" in response_content:
            return "angry"
        else:
            return "neutral"

    def tts(self, inp):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=inp
        )
        response.stream_to_file(self.ROBOT_VOICE_DIR)
        self._play_voice(self.ROBOT_VOICE_DIR)

    def run(self):
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
                if spy_result and ("笨笨" in spy_result or "本本" in spy_result or "奔奔" in spy_result):
                    self.messages.append({"role": "user", "content": spy_result})
                    inp = self.conversation()
                    self.tts(inp)
                elif spy_result and ('goodbye' in spy_result or '退出' in spy_result or '再见' in spy_result):
                    self.exit_voice()
                    print('正在退出...')
                    break
                else:
                    continue
            except TypeError:
                print('ERROR VOICE INPUT --- NONE RECEIVED')
                continue
