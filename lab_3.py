from threading import Thread
import csv
import time
import psutil
import pynput.mouse
import codecs


class MetricsThread(Thread):
    def __init__(self, metric_name, interval):
        super().__init__()
        self.metric_name = metric_name
        self.interval = interval
        self.running = True

    def run(self):
        with codecs.open('metrics.csv', '+a', encoding='utf-8') as file:
            writer = csv.writer(file)

            while self.running:
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')

                if self.metric_name == 'CPU':
                    cpu_percent = psutil.cpu_percent()

                    writer.writerow([current_time, self.metric_name, cpu_percent])
                elif self.metric_name == 'Mouse':

                    mouse_listener = pynput.mouse.Listener(on_move=self.on_move)

                    mouse_listener.start()

                    time.sleep(self.interval)

                    mouse_listener.stop()

    def on_move(self, x, y):
        pass


cpu_thread = MetricsThread('CPU', 60)
mouse_thread = MetricsThread('Mouse', 60)

cpu_thread.start()
mouse_thread.start()

time.sleep(60)

cpu_thread.running = False
mouse_thread.running = False

cpu_thread.join()
mouse_thread.join()