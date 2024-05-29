import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
from queue import Queue

class VideoPlayerApp:
    def __init__(self, master, emotion_queue):
        self.master = master
        self.emotion_queue = emotion_queue
        self.current_emotion = "normal"
        self.play_video_flag = True  # 控制视频播放线程是否运行的标志

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()

        # 计算窗口大小
        self.window_width = int(self.screen_width * 8/10)
        self.window_height = int(self.screen_height * 8/10)

        # 计算窗口居中位置
        self.window_x = (self.screen_width - self.window_width) // 2
        self.window_y = (self.screen_height - self.window_height) // 2

        # 创建窗口
        self.master.geometry(f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}")
        self.master.title("MOSS人工智能语音交互")

        # 获取动态路径
        self.BASE_DIR = os.path.dirname(__file__)
        self.video_dir = os.path.join(self.BASE_DIR, 'MOSS_Expressions')

        # 创建一个字典来存储视频文件的路径
        self.video_paths = self.load_video_paths()
        
        if not self.video_paths:
            print("No video files found in directory:", self.video_dir)
            return

        # 加载默认视频
        self.load_video(self.current_emotion)
        
        # 创建视频播放区域
        self.video_label = tk.Label(self.master)
        self.video_label.pack(fill=tk.BOTH, expand=tk.YES)

        # 绑定窗口大小调整事件
        self.master.bind("<Configure>", self.on_resize)

        # 开始播放视频
        self.play_video()

    def load_video_paths(self):
        video_paths = {}
        for file_name in os.listdir(self.video_dir):
            if file_name.endswith(".mp4"):  # 确保只包含视频文件
                emotion = os.path.splitext(file_name)[0]  # 假设文件名是情绪名
                video_paths[emotion] = os.path.join(self.video_dir, file_name)
        return video_paths

    def load_video(self, emotion):
        print("Loading video for emotion:", emotion)
        self.video_path = self.video_paths.get(emotion, self.video_paths.get("normal"))
        if not self.video_path:
            print("No video file found for emotion:", emotion)
            return
        self.video_cap = cv2.VideoCapture(self.video_path)
        self.fps = int(self.video_cap.get(cv2.CAP_PROP_FPS))
        self.video_width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Loaded video:", self.video_path)

    def on_resize(self, event):
        # 更新窗口宽高
        self.window_width = event.width
        self.window_height = event.height

    def play_video(self):
        if not self.play_video_flag:
            return

        if not self.emotion_queue.empty():
            new_emotion = self.emotion_queue.get()
            if new_emotion == "terminate":
                self.play_video_flag = False  # 设置标志为 False，退出播放线程
                self.master.destroy()
                return

        ret, frame = self.video_cap.read()
        if ret:
            # 调整视频尺寸以适应窗口
            frame = cv2.resize(frame, (self.window_width, self.window_height))
            # 将 OpenCV 图像转换为 Tkinter 图像
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            # 在 Label 上显示视频帧
            self.video_label.configure(image=photo)
            self.video_label.image = photo
            # 继续播放下一帧
            self.master.after(1000 // self.fps, self.play_video)
        else:
            # 视频播放结束，释放资源
            self.video_cap.release()

    def close_window(self):
        # 在窗口关闭时释放视频资源并发送终止信号到情绪队列
        self.play_video_flag = False  # 设置标志为 False
        self.emotion_queue.put("terminate")  # 发送终止信号
        self.video_cap.release()  # 释放视频资源
        self.master.destroy()  # 关闭窗口

def run_video_player(emotion_queue):
    root = tk.Tk()
    app = VideoPlayerApp(root, emotion_queue)
    root.protocol("WM_DELETE_WINDOW", app.close_window)  # 绑定窗口关闭事件处理器
    root.mainloop()
