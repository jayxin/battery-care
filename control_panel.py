import tkinter as tk
from tkinter import ttk
import threading
from battery_monitor import BatteryMonitor

def create_gui():
    """创建图形界面"""
    root = tk.Tk()
    root.title("电池监控")
    root.geometry("500x400")
    root.resizable(False, False)

    monitor = BatteryMonitor()

    # 设置阈值
    tk.Label(root, text="电量阈值设置", font=("Arial", 14, "bold")).pack(pady=10)

    frame1 = tk.Frame(root)
    frame1.pack(pady=5)
    tk.Label(frame1, text="低电量阈值:").pack(side=tk.LEFT, padx=5)
    low_var = tk.IntVar(value=30)
    low_spin = tk.Spinbox(frame1, from_=10, to=50, textvariable=low_var, width=10)
    low_spin.pack(side=tk.LEFT, padx=5)
    tk.Label(frame1, text="%").pack(side=tk.LEFT)

    frame2 = tk.Frame(root)
    frame2.pack(pady=5)
    tk.Label(frame2, text="高电量阈值:").pack(side=tk.LEFT, padx=5)
    high_var = tk.IntVar(value=80)
    high_spin = tk.Spinbox(frame2, from_=50, to=95, textvariable=high_var, width=10)
    high_spin.pack(side=tk.LEFT, padx=5)
    tk.Label(frame2, text="%").pack(side=tk.LEFT)

    frame3 = tk.Frame(root)
    frame3.pack(pady=5)
    tk.Label(frame3, text="检查间隔:").pack(side=tk.LEFT, padx=5)
    interval_var = tk.IntVar(value=60)
    interval_spin = tk.Spinbox(frame3, from_=10, to=300, textvariable=interval_var, width=10)
    interval_spin.pack(side=tk.LEFT, padx=5)
    tk.Label(frame3, text="秒").pack(side=tk.LEFT)

    # 实时显示电量
    tk.Label(root, text="当前电池状态", font=("Arial", 14, "bold")).pack(pady=(20,10))

    percent_label = tk.Label(root, text="电量: --%", font=("Arial", 24))
    percent_label.pack()

    status_label = tk.Label(root, text="状态: --", font=("Arial", 12))
    status_label.pack(pady=5)

    def update_status():
        """更新状态显示"""
        percent, is_plugged, _ = monitor.get_battery_info()
        if percent is not None:
            percent_label.config(text=f"电量: {percent}%")
            if is_plugged:
                status_label.config(text="状态: 充电中", fg="green")
            else:
                status_label.config(text="状态: 使用电池", fg="red")
        root.after(1000, update_status)

    def start_monitor():
        """启动监控"""
        monitor.low_threshold = low_var.get()
        monitor.high_threshold = high_var.get()
        monitor.check_interval = interval_var.get()

        # 在新线程中运行监控
        monitor_thread = threading.Thread(target=monitor.monitor_loop, daemon=True)
        monitor_thread.start()

        # 禁用启动按钮
        start_btn.config(state=tk.DISABLED, text="监控运行中")
        # 启用停止按钮
        stop_btn.config(state=tk.NORMAL)

    def stop_monitor():
        """停止监控"""
        monitor.stop()
        # 启用启动按钮
        start_btn.config(state=tk.NORMAL, text="启动监控")
        # 禁用停止按钮
        stop_btn.config(state=tk.DISABLED)

    # 按钮
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=20)
    # 启动按钮, 默认启用
    start_btn = tk.Button(btn_frame, text="启动监控", command=start_monitor, bg="lightgreen", fg="black", padx=20)
    start_btn.pack(side=tk.LEFT, padx=10)
    # 停止按钮, 默认禁用
    stop_btn = tk.Button(btn_frame, text="停止监控", command=stop_monitor, state=tk.DISABLED, bg="pink", fg="black", padx=20)
    stop_btn.pack(side=tk.LEFT, padx=10)

    # 启动状态更新
    update_status()

    # 关闭窗口时的处理
    def on_closing():
        if monitor.running:
            monitor.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
