import customtkinter as ctk
import time
import winsound
import threading

class MiniModePomodoro:
    def __init__(self):
        # --- 1. 基础窗口设置 ---
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("番茄钟")
        self.root.geometry("300x280")
        self.root.resizable(False, False)

        # 核心变量
        self.running = False
        self.time_left = 0
        self.mini_window = None # 用于存储悬浮窗对象
        
        # 绑定变量：主窗口和悬浮窗共享这个时间显示
        self.time_var = ctk.StringVar(value="25") 
        self.status_var = ctk.StringVar(value="保持专注")

        # --- 2. 主界面布局 ---
        self.label_hint = ctk.CTkLabel(self.root, text="设置时间 (分钟)", text_color="gray")
        self.label_hint.pack(pady=(30, 5))

        self.entry_time = ctk.CTkEntry(
            self.root, 
            textvariable=self.time_var, 
            font=("Roboto Medium", 70),
            width=220,
            height=80,
            justify="center",
            fg_color="transparent",
            border_width=0
        )
        self.entry_time.pack(pady=10)

        self.btn_start = ctk.CTkButton(
            self.root, 
            text="开始专注 (进入悬浮模式)", 
            command=self.start_timer, 
            width=180,
            height=40,
            fg_color="#2CC985", 
            hover_color="#229965",
            font=("微软雅黑", 14, "bold")
        )
        self.btn_start.pack(pady=30)

        self.root.mainloop()

    # --- 逻辑功能区 ---

    def start_timer(self):
        if not self.running:
            # 1. 验证输入
            user_input = self.time_var.get()
            if not user_input.isdigit():
                return
            
            minutes = int(user_input)
            if minutes <= 0: return

            # 2. 设置状态
            self.work_time = minutes * 60
            self.time_left = self.work_time
            self.running = True
            
            # 3. 切换界面：隐藏主窗口，打开悬浮窗
            self.root.withdraw() 
            self.open_mini_window()
            
            # 4. 开始后台倒计时
            threading.Thread(target=self.run_countdown, daemon=True).start()

    def open_mini_window(self):
        """创建右上角的悬浮小窗口"""
        self.mini_window = ctk.CTkToplevel()
        
        # 1. 去掉标题栏和边框 (无边框模式)
        self.mini_window.overrideredirect(True)
        # 2. 永远置顶
        self.mini_window.attributes('-topmost', True)
        
        # 3. 计算位置：屏幕右上角
        screen_width = self.root.winfo_screenwidth()
        # 设定悬浮窗宽高
        w, h = 220, 70 
        # x坐标 = 屏幕宽 - 窗口宽 - 20像素间距
        x = screen_width - w - 20 
        y = 20
        self.mini_window.geometry(f"{w}x{h}+{x}+{y}")
        self.mini_window.configure(fg_color="#1a1a1a") # 深色背景

        # 4. 悬浮窗布局
        # 左侧：时间
        lbl_mini_time = ctk.CTkLabel(
            self.mini_window, 
            textvariable=self.time_var, # 共享变量
            font=("Roboto Medium", 40),
            text_color="#2CC985"
        )
        lbl_mini_time.pack(side="left", padx=(20, 10))

        # 右侧：文字和停止按钮
        right_frame = ctk.CTkFrame(self.mini_window, fg_color="transparent")
        right_frame.pack(side="left", pady=5)

        lbl_keep = ctk.CTkLabel(right_frame, text="保持专注", font=("微软雅黑", 12))
        lbl_keep.pack()

        # 一个小的停止按钮，用来还原界面
        btn_stop = ctk.CTkButton(
            right_frame, 
            text="⏹", 
            width=30, 
            height=20,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.stop_and_restore
        )
        btn_stop.pack(pady=2)

    def run_countdown(self):
        while self.running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            self.time_var.set(time_str) # 这里更新，主窗口和悬浮窗都会变
            
            time.sleep(1)
            self.time_left -= 1
        
        if self.time_left == 0 and self.running:
            self.time_var.set("00:00")
            self.finish_work()

    def stop_and_restore(self):
        """手动点击停止按钮"""
        self.running = False
        self.close_mini_window()

    def finish_work(self):
        """倒计时自然结束"""
        self.running = False
        winsound.Beep(1000, 500)
        winsound.Beep(1500, 500)
        self.close_mini_window()

    def close_mini_window(self):
        """关闭悬浮窗，恢复主窗口"""
        if self.mini_window:
            self.mini_window.destroy()
            self.mini_window = None
        
        # 恢复主窗口显示
        self.root.deiconify() 
        self.time_var.set("25") # 重置时间

if __name__ == "__main__":
    MiniModePomodoro()