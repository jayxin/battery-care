import psutil
import time
from plyer import notification
import sys

class BatteryMonitor:
    def __init__(self):
        # 是否运行
        self.running = True
        # 是否已发送低电量通知
        self.notified_low = False
        # 是否已发送高电量通知
        self.notified_high = False
        # 低电量阈值
        self.low_threshold = 30
        # 高电量阈值
        self.high_threshold = 80
        # 检查间隔(秒)
        self.check_interval = 60

    def send_notification(self, title, message):
        """发送系统通知"""
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10,  # 通知显示10秒
                app_name="Battery Care"
            )
        except Exception as e:
            print(f"Failed to send notification: {e}")

    def get_battery_info(self):
        """获取电池信息"""
        battery = psutil.sensors_battery()
        if battery is None:
            return None, None, None

        percent = battery.percent
        is_plugged = battery.power_plugged
        return percent, is_plugged, battery

    def check_and_notify(self):
        """检查电量并发送通知"""
        percent, is_plugged, battery = self.get_battery_info()

        if percent is None:
            return

        # 电量低于低电量阈值且未通知过
        if percent <= self.low_threshold and not self.notified_low:
            message = f"Current power: {percent}%\nIt is recommended to charge immediately!"
            if not is_plugged:
                self.send_notification("Warning: power lower than threshold.", message)
                self.notified_low = True
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] power lower than threshold: {percent}%")

        # 电量高于高电量阈值且未通知过
        elif percent >= self.high_threshold and not self.notified_high:
            if is_plugged:
                message = f"Current power: {percent}%\nIt is recommended to unplug the power!"
                self.send_notification("Warning: power higher than threshold.", message)
                self.notified_high = True
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] power higher than threshold: {percent}%")

        # 重置通知标志(当电量回到中间范围时)
        elif self.low_threshold < percent < self.high_threshold:
            self.notified_low = False
            self.notified_high = False

        # 若充电状态改变，重置标志
        if is_plugged and percent > self.low_threshold:
            self.notified_low = False
        if not is_plugged and percent < self.high_threshold:
            self.notified_high = False

    def monitor_loop(self):
        """监控循环"""
        print(f"Started battery monitoring.")
        print(f"Power range: [{self.low_threshold}%, {self.high_threshold}%]")
        print(f"Operating cycle: {self.check_interval} seconds")
        print("Press Ctrl+C to exit\n")

        while self.running:
            try:
                self.check_and_notify()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                print(f"Error monitoring: {e}")
                time.sleep(self.check_interval)

    def stop(self):
        """停止监控"""
        self.running = False
        print("\nStopped battery monitoring.")
        sys.exit(0)
