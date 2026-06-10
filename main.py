from battery_monitor import BatteryMonitor
from control_panel import create_gui

def main():
    """主函数"""
    print("选择运行模式:")
    print("1. 终端(TUI)模式: 仅通知")
    print("2. 图形界面(GUI)模式: 提供控制面板")
    choice = input("请选择(1/2，默认1): ").strip()

    if choice == "2":
        create_gui()
    else:
        monitor = BatteryMonitor()

        # 自定义阈值
        custom = input(f"是否修改默认阈值？(低{monitor.low_threshold}% / 高{monitor.high_threshold}%) [y/N]: ").strip().lower()
        if custom == 'y':
            try:
                low = int(input(f"低电量阈值 (10-50): "))
                high = int(input(f"高电量阈值 (50-95): "))
                if 10 <= low <= 50 and 50 <= high <= 95:
                    monitor.low_threshold = low
                    monitor.high_threshold = high
                else:
                    print("输入无效, 使用默认值")
            except:
                print("输入无效, 使用默认值")

        try:
            monitor.monitor_loop()
        except KeyboardInterrupt:
            monitor.stop()

if __name__ == "__main__":
    main()
