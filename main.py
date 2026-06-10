from battery_monitor import BatteryMonitor
from control_panel import create_gui

def main():
    """主函数"""
    print("Select running mode:")
    print("1. Terminal Mode: notification only")
    print("2. GUI Mode: control panel")
    choice = input("Please select(1/2, default 1): ").strip()

    if choice == "2":
        create_gui()
    else:
        monitor = BatteryMonitor()

        # 自定义阈值
        custom = input(f"Change default threshold? (Low{monitor.low_threshold}% / High{monitor.high_threshold}%) [y/N]: ").strip().lower()
        if custom == 'y':
            try:
                low = int(input(f"Low battery threshold (10-50): "))
                high = int(input(f"High battery threshold (50-95): "))
                if 10 <= low <= 50 and 50 <= high <= 95:
                    monitor.low_threshold = low
                    monitor.high_threshold = high
                else:
                    print("Invalid input! Use default.")
            except:
                print("Invalid input! Use default.")

        try:
            monitor.monitor_loop()
        except KeyboardInterrupt:
            monitor.stop()

if __name__ == "__main__":
    main()
