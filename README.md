# MOSS 人工智能语音交互系统

## 项目简介

MOSS2.0 是一个基于人工智能的语音交互系统，集成多个LLMs大模型，在1.0版本上 优化并增加了语音交互、情绪识别、人脸检测。该系统可以识别用户的情绪并展示对应的表情，并进行语音交互。

## 文件说明

```sh
1. main.py：主程序入口，启动语音助手和视频播放。

2. ScreenView.py：表情播放界面，实现情绪检测并播放相应表情。

3. VoiceInteractions.py：语音交互逻辑，实现语音识别、合成和对话功能。

4. config.ini：配置文件，存储 API 密钥等配置信息。

5. requirements.txt：依赖包文件，列出项目所需的 Python 包。

6. .gitignore：Git忽略文件，指定哪些文件和目录不应该被包含在版本控制中。
```


## 快速运行

### 1. 克隆仓库

```sh
git clone https://github.com/JJZHANG/MOSS.git
cd MOSS人工智能2.0
```

### 2. 安装依赖
确保你已经安装了 Python 3.12，然后运行以下命令安装所需依赖：

```sh
复制代码
pip install -r requirements.txt
```
### 3. 设置环境变量

在项目根目录创建一个 .env 文件，并添加以下内容（使用你的实际 API 密钥替换示例值）：

```sh
复制代码
# OpenAI
export OPENAI_API_KEY="your_openai_api_key"

# Baidu-aip
export BAIDU_APP_ID="your_baidu_app_id"
export BAIDU_API_KEY="your_baidu_api_key"
export BAIDU_SECRET_KEY="your_baidu_secret_key"
```

### 4. 运行程序

使用以下命令启动程序：

```sh
复制代码
python3 main.py
```

## 注意事项
确保环境变量已经正确设置。
确保所有依赖项已经安装。
确保配置文件 config.ini 中的 API 密钥和 ID 正确。(如果没有做第一步的话)
通过以上步骤，你应该能够成功运行 MOSS 人工智能语音交互系统。如果遇到任何问题，请随时联系我进行解决。



## 目录结构

```sh
MOSS人工智能2.0
├── pycache
├── Human
│ └── myvoices.mp3 # 录制的用户语音
├── MOSS_Expressions
│ ├── angry.mp4 # 愤怒情绪视频
│ ├── happy.mp4 # 开心情绪视频
│ ├── normal.mp4 # 正常情绪视频
│ └── sad.mp4 # 悲伤情绪视频
├── MOSS_Voices
│ ├── exit.mp3 # 退出语音
│ ├── init.mp3 # 初始化语音
│ ├── myvoices.mp3 # 用户录音文件
│ ├── robotVoices.mp3 # 机器人回答语音
│ └── starting.mp3 # 启动语音
├── .gitignore # Git忽略文件
├── config.ini # 配置文件
├── main.py # 主程序入口
├── requirements.txt # 依赖包文件
├── ScreenView.py # 视频播放界面
└── VoiceInteractions.py # 语音交互逻辑
```