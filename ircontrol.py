import tkinter as tk
from tkinter import ttk
import serial
import time

class IRRemoteGUI:
    def __init__(self, port='COM8'):
        self.ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(2)
        
        self.root = tk.Tk()
        self.root.title("赤外線リモコン")
        self.root.geometry("400x500")
        
        # DENON コンポ
        denon_frame = ttk.LabelFrame(self.root, text="DENON コンポ", padding=10)
        denon_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(denon_frame, text="電源", command=self.denon_power, width=15).pack(side="left", padx=5)
        ttk.Button(denon_frame, text="Vol +", command=self.denon_vol_up, width=10).pack(side="left", padx=5)
        ttk.Button(denon_frame, text="Vol -", command=self.denon_vol_down, width=10).pack(side="left", padx=5)
        
        # TCL テレビ
        tv_frame = ttk.LabelFrame(self.root, text="TCL テレビ", padding=10)
        tv_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(tv_frame, text="電源", command=self.tv_power, width=15).pack(pady=2)
        ttk.Button(tv_frame, text="入力切替", command=self.tv_input, width=15).pack(pady=2)
        
        # 十字キー
        nav_frame = tk.Frame(tv_frame)
        nav_frame.pack(pady=10)
        
        ttk.Button(nav_frame, text="↑", command=self.tv_up, width=8).grid(row=0, column=1, pady=2)
        ttk.Button(nav_frame, text="↓", command=self.tv_down, width=8).grid(row=2, column=1, pady=2)
        ttk.Button(nav_frame, text="OK", command=self.tv_ok, width=8).grid(row=1, column=1, pady=2)
        
        # ログ
        log_frame = ttk.LabelFrame(self.root, text="ログ", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, height=10, width=50)
        self.log_text.pack(fill="both", expand=True)
        
    def send_command(self, command):
        self.ser.write((command + '\n').encode())
        time.sleep(0.1)
        if self.ser.in_waiting:
            response = self.ser.readline().decode().strip()
            self.log_text.insert(tk.END, f"{response}\n")
            self.log_text.see(tk.END)
    
    def denon_power(self):
        self.send_command("DENON_POWER")
    
    def denon_vol_up(self):
        self.send_command("DENON_VOL_UP")
    
    def denon_vol_down(self):
        self.send_command("DENON_VOL_DOWN")
    
    def tv_power(self):
        self.send_command("TV_POWER")
    
    def tv_input(self):
        self.send_command("TV_INPUT")
    
    def tv_up(self):
        self.send_command("TV_UP")
    
    def tv_down(self):
        self.send_command("TV_DOWN")
    
    def tv_ok(self):
        self.send_command("TV_OK")
    
    def run(self):
        self.root.mainloop()
        self.ser.close()

if __name__ == "__main__":
    app = IRRemoteGUI(port='COM8')  # ポートを環境に合わせて変更
    app.run()