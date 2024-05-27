import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os

class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
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
        BASE_DIR = os.path.dirname(__file__)
        video_path = os.path.join(BASE_DIR, 'MOSS_Expressions', 'MOSS_expression.mp4')

        # 读取视频
        self.video_path = video_path
        self.video_cap = cv2.VideoCapture(self.video_path)
        
        # 获取视频的帧率和尺寸
        self.fps = int(self.video_cap.get(cv2.CAP_PROP_FPS))
        self.video_width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 创建视频播放区域
        self.video_canvas = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.video_canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # 绑定窗口大小调整事件
        self.master.bind("<Configure>", self.on_resize)

        # 开始播放视频
        self.play_video()

    def on_resize(self, event):
        # 更新窗口宽高
        self.window_width = event.width
        self.window_height = event.height

    def play_video(self):
        ret, frame = self.video_cap.read()
        if ret:
            # 调整视频尺寸以适应窗口
            frame = cv2.resize(frame, (self.window_width, self.window_height))
            # 将 OpenCV 图像转换为 Tkinter 图像
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            # 在画布上显示视频帧
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.video_canvas.image = photo
            # 继续播放下一帧
            self.master.after(1000 // self.fps, self.play_video)
        else:
            # 视频播放结束，释放资源
            self.video_cap.release()

def main():
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
