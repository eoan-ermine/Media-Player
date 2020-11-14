from src.gui.input_manager import InputManager


class Command:
    def __init__(self, num_of_args, description, callback):
        self.num_of_args = num_of_args
        self.description = description
        self.callback = callback

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)


class AbstractShell:
    def __init__(self, header, footer):
        self.footer = footer
        self.header = header

        self.input_manager = InputManager.get_instance()
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

            "pause": Command(0, "Поставить воспроизведение на паузу", self.pause),
            "stop": Command(0, "Остановить воспроизведение", self.stop),
            "backward_media": Command(0, "Перейти к предыдущему в плейлисте медиафайлу", self.backward_media),
            "forward_media": Command(0, "Перейти к следующему в плейлисте медиафайлу", self.forward_media),

            "increase_volume": Command(0, "Сделать громкость больше", self.increase_volume),
            "decrease_volume": Command(0, "Сделать громкость меньше", self.decrease_volume),
            "mute": Command(0, "Выключить звук", self.mute),

            "show_fullscreen": Command(0, "Перейти в полноэкранный режим", self.show_fullscreen)
        }

        self.show_intro()

    def show_intro(self):
        print(self.header)
        print("+----[Команды дистанционного управления]")
        for name in self.commands:
            command = self.commands[name]
            print("{} - {} аргумента(ов) - {}".format(name, command.num_of_args, command.description))
        print("+----[конец справки]")

    def __del__(self):
        print(self.footer)

    def open_file(self):
        pass

    def open_files(self):
        pass

    def open_directory(self):
        pass

    def exit(self):
        pass

    def bit_slower(self):
        pass

    def slower(self):
        pass

    def normal_speed(self):
        pass

    def bit_faster(self):
        pass

    def faster(self):
        pass

    def forward_time(self):
        pass

    def backward_time(self):
        pass

    def at_time(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def backward_media(self):
        pass

    def forward_media(self):
        pass

    def increase_volume(self):
        pass

    def decrease_volume(self):
        pass

    def mute(self):
        pass

    def show_fullscreen(self):
        pass