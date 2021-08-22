import time
from enum import Enum
import configparser
import sys
from datetime import timedelta
import platform
import os
import __strings__ as strings


class PomodoroType(Enum):
    WORK = 1
    BREAK = 2
    REST = 3


class Pomodoro:
    config = configparser.ConfigParser()
    current_pomodoro = PomodoroType.WORK
    pomodoro_count = 0

    def __init__(self) -> None:
        self.current_pomodoro: PomodoroType = PomodoroType.WORK
        self.config.read('config.cfg')

    def get_current_pomodoro_name(self):
        if self.current_pomodoro == PomodoroType.WORK:
            return "Рабочий"
        elif self.current_pomodoro == PomodoroType.REST:
            return "Отдых"
        else:
            return "Перерыв"

    def get_time(self, type: PomodoroType):
        if type == PomodoroType.WORK:
            return int(self.config.get("pomodoro", "work_time"))
        elif type == PomodoroType.REST:
            return int(self.config.get("pomodoro", "rest_time"))
        elif type == PomodoroType.BREAK:
            return int(self.config.get("pomodoro", "break_time"))

    def get_total_time(self):
        return self.pomodoro_count*self.get_time(PomodoroType.WORK)

    def start(self):
        os.system("clear")
        print(strings.hello.format(self.get_time(PomodoroType.WORK)/60, self.get_time(PomodoroType.BREAK)/60, self.get_time(PomodoroType.REST)/60))
        print(strings.start)
        while True:
            command = input()
            if command.strip().lower() == "start":
                self.pomodoro()
            elif command.strip().lower() == "exit":
                print(f"За сеанс ты отработал {timedelta(self.get_total_time())}. Пока!")
                break
            elif command.strip().lower() == "info":
                self.info()

    def pomodoro(self):
        os.system("clear")
        timing = time.time()
        while True:
            if time.time() - timing > self.get_time(self.current_pomodoro):
                message = self.get_ending_string(self.current_pomodoro)
                self.notification("Ваш помидор", message)
                print(message)
                break
            else:
                os.system("clear")
                sys.stdout.write("\r\033[1mТекущий помодор {0}: {1}/{2}\033[0m".format(self.get_current_pomodoro_name(), str(timedelta(seconds=time.time()-timing))[:7], timedelta(seconds=self.get_time(self.current_pomodoro))))
                sys.stdout.flush()
                time.sleep(0.5)

    def info(self):
        os.system("clear")
        print("\033[1mИнформация\033[0m")
        print(f"\033[1mТекущий помодор\033[0m: {self.get_current_pomodoro_name()}")
        print(f"\033[1mВсего помидоров выполнено\033[0m: {self.pomodoro_count}")
        print(f"\033[1mОтработано: \033[0m{self.get_total_time()}")

    def get_ending_string(self, type: PomodoroType):
        if (type == PomodoroType.WORK):
            self.pomodoro_count += 1
            if self.pomodoro_count % 4 == 0:
                self.current_pomodoro = PomodoroType.REST
                return "\nРабочий помидор закончен. Впереди {} минут отдыха".format(self.get_time(self.current_pomodoro)/60)
            else:
                self.current_pomodoro = PomodoroType.BREAK
                return "\nРабочий помидор закончен. Впереди {} минут перерыва".format(self.get_time(self.current_pomodoro)/60)
        elif (type == PomodoroType.BREAK):
            self.current_pomodoro = PomodoroType.WORK
            return "\nПерерыв закончен. Впереди {} минут работы".format(self.get_time(self.current_pomodoro)/60)
        elif (type == PomodoroType.REST):
            self.current_pomodoro = PomodoroType.WORK
            return "\nОтдых закончен. Впереди {} минут работы".format(self.get_time(self.current_pomodoro)/60)

    @classmethod
    def notification(self, title, message):
        duration = 3  # seconds
        freq = 293  # Hz
        os.system('play -nq synth {} sine {}'.format(duration, freq))
        if platform.system() == "Linux":
            command = f'notify-send {message} {title}'
        elif platform.system() == "Darwin":
            command = f'''osascript -e 'display notification "{message}" with title "{title}"'''
        os.system(command)


if __name__ == "__main__":
    pomodoro = Pomodoro()
    pomodoro.start()
