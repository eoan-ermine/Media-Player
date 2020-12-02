import threading

from flask import Flask, request
import json

from src.gui.input_manager import InputManager
from src.gui.ui_manager import UIManager
from multiprocessing import Process


class Order:
    def __init__(self, command, args=[]):
        self.command = command
        self.args = args


class Command:
    def __init__(self, num_of_args, description, callback):
        self.num_of_args = num_of_args
        self.description = description
        self.callback = callback

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)


class ShellDaemon:
    def __init__(self, parent, host, port):
        self.parent = parent

        self.host = host
        self.port = port

    def run(self, i):
        app = Flask("Daemon #{}".format(i))

        def parse_order(order: str) -> Order:
            return Order(order["command"], order["args"])

        @app.route("/", methods=['POST'])
        def handle_order():
            if self.parent.execute(parse_order(request.get_json())):
                return json.dumps({"success": True}), 200
            return json.dumps({"success": False}), 400

        server = threading.Thread(target=app.run, args=(self.host, self.port))
        server.setDaemon(True)
        server.start()


class DaemonManager:
    def __init__(self):
        self.input_manager = InputManager.get_instance()
        self.ui_manager = UIManager.get_instance()

        self.commands = {
            "open_file": Command(1, "Открыть файл", self.open_file),
            "open_files": Command("Infinity", "Открыть файлы", self.open_files),
            "open_directory": Command(1, "Открыть директорию", self.open_directory),
            "exit": Command(0, "Выйти из медиаплеера", self.exit),

            "bit_slower": Command(0, "Сделать скорость немного медленнее", self.bit_slower),
            "slower": Command(0, "Сделать скорость медленнее", self.slower),
            "normal_speed": Command(0, "Установить нормальную скорость", self.normal_speed),
            "bit_faster": Command(0, "Сделать скорость немного быстрее", self.bit_faster),
            "faster": Command(0, "Сделать скорость быстрее", self.faster),

            "forward_time": Command(0, "Совершить скачок вперед", self.forward_time),
            "backward_time": Command(0, "Совершить скачок назад", self.backward_time),
            "at_time": Command(3, "Перейти к заданному времени", self.at_time),

            "play": Command(0, "Начать воспроизведение", self.play),
            "pause": Command(0, "Поставить воспроизведение на паузу", self.pause),
            "stop": Command(0, "Остановить воспроизведение", self.stop),
            "backward_media": Command(0, "Перейти к предыдущему в плейлисте медиафайлу", self.backward_media),
            "forward_media": Command(0, "Перейти к следующему в плейлисте медиафайлу", self.forward_media),

            "increase_volume": Command(0, "Сделать громкость больше", self.increase_volume),
            "decrease_volume": Command(0, "Сделать громкость меньше", self.decrease_volume),
            "mute": Command(0, "Выключить звук", self.mute),

            "show_fullscreen": Command(0, "Перейти в полноэкранный режим", self.show_fullscreen)
        }
        self.daemons = []

    def add_daemon(self, host: str, port: str):
        daemon = ShellDaemon(self, host, port)
        daemon.run(len(self.daemons))

        self.daemons.append(daemon)

    def execute(self, order: Order):
        command, args = [order.command, order.args]
        if command in self.commands:
            command_obj = self.commands[command]
            if command_obj.num_of_args in ("Infinity", len(args)):
                command_obj(*args)
            else:
                print("Invalid count of arguments")
                return False
        else:
            print("Invalid command")
            return False
        return True

    def open_file(self, filepath):
        self.input_manager.add_file(filepath)

    def open_files(self, *files):
        [self.input_manager.add_file(file) for file in files]

    def open_directory(self, folderpath):
        self.input_manager.add_folder(folderpath)

    def exit(self):
        self.input_manager.exit()

    def bit_slower(self):
        self.input_manager.set_playback_rate(self.input_manager.get_playback_rate() - 0.25)

    def slower(self):
        self.input_manager.set_playback_rate(self.input_manager.get_playback_rate() - 0.5)

    def normal_speed(self):
        self.input_manager.set_playback_rate(1.0)

    def bit_faster(self):
        self.input_manager.set_playback_rate(self.input_manager.get_playback_rate() + 0.25)

    def faster(self):
        self.input_manager.set_playback_rate(self.input_manager.get_playback_rate() - 0.5)

    def forward_time(self):
        self.input_manager.set_position(self.input_manager.get_position() + 10 * 1000)

    def backward_time(self):
        self.input_manager.set_position(self.input_manager.get_position() - 10 * 1000)

    def at_time(self, seconds):
        self.input_manager.set_position(seconds * 1000)

    def play(self):
        self.input_manager.play()

    def pause(self):
        self.input_manager.pause()

    def stop(self):
        self.input_manager.stop()

    def backward_media(self):
        self.input_manager.previous_media()

    def forward_media(self):
        self.input_manager.next_media()

    def increase_volume(self):
        self.input_manager.set_volume(self.input_manager.get_volume() + 10)

    def decrease_volume(self):
        self.input_manager.set_volume(self.input_manager.get_volume() - 10)

    def mute(self):
        self.input_manager.mute(True if self.input_manager.is_muted() else False)

    def show_fullscreen(self):
        self.ui_manager.show_fullscreen()
