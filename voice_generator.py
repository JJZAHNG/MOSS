import os
from openai import OpenAI
from aip import AipSpeech

class VoiceGenerator:
    def __init__(self):
        # 初始化 OpenAI API
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_base_url = "https://pro.aiskt.com/v1"
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")
        self.openai_client = OpenAI(api_key=self.openai_api_key, base_url=self.openai_base_url)
        
        # 初始化百度 API
        self.baidu_app_id = os.getenv('BAIDU_APP_ID')
        self.baidu_api_key = os.getenv('BAIDU_API_KEY')
        self.baidu_secret_key = os.getenv('BAIDU_SECRET_KEY')
        if not self.baidu_app_id or not self.baidu_api_key or not self.baidu_secret_key:
            raise ValueError("Baidu API credentials are not set. Please set the environment variables BAIDU_APP_ID, BAIDU_API_KEY, and BAIDU_SECRET_KEY.")
        self.baidu_client = AipSpeech(self.baidu_app_id, self.baidu_api_key, self.baidu_secret_key)

        # 语音文件保存路径
        self.voice_dir = os.path.join(os.path.dirname(__file__), 'MOSS_Voices')

    def generate_openai_voice(self, text, filename):
        print(f"Generating OpenAI voice for text: {text}")
        response = self.openai_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        file_path = os.path.join(self.voice_dir, filename)
        response.stream_to_file(file_path)
        print(f"OpenAI voice saved to {file_path}")

    def generate_baidu_voice(self, text, filename):
        print(f"Generating Baidu voice for text: {text}")
        result = self.baidu_client.synthesis(text, 'zh', 1, {
            'vol': 5,  # 音量
            'spd': 5,  # 语速
            'pit': 5,  # 音调
            'per': 4   # 发音人选择
        })
        file_path = os.path.join(self.voice_dir, filename)
        if not isinstance(result, dict):
            with open(file_path, 'wb') as f:
                f.write(result)
            print(f"Baidu voice saved to {file_path}")
        else:
            print("Baidu voice synthesis failed:", result)

if __name__ == "__main__":
    generator = VoiceGenerator()
    user_filename = input("请输入要覆盖的文件名（包括扩展名，例如 myvoice.mp3）：")
    user_text = input("请输入要合成语音的文本：")
    
    # 选择合成引擎，可以是 'openai' 或 'baidu'
    engine_choice = input("请选择语音合成引擎（openai 或 baidu）：").strip().lower()
    if engine_choice == 'openai':
        generator.generate_openai_voice(user_text, user_filename)
    elif engine_choice == 'baidu':
        generator.generate_baidu_voice(user_text, user_filename)
    else:
        print("无效的语音合成引擎选择。请选择 'openai' 或 'baidu'。")
