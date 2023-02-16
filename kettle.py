import threading
import sched
import time
from myAsyncSched import myAsyncSched
import logging
from config import timing, temp_boilling


logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w", 
                    format="%(asctime)s %(levelname)s %(message)s")

class Kettle():
    def __init__(self, water: float):
        """Инициализирует экземпляр класс Kettle
        
        Keyword arguments:
        water -- float
        
        """
        self.water = water # количество воды
        logging.info(f"'Количество воды'-{self.water}")
        self.state = "ВЫКЛ" # состояние
        logging.info(f"'Состояние'-{self.state}")
        self.temp = 0 # температура
        logging.info(f"'Начальная температура'-{self.temp}")
        self.schedul = sched.scheduler(time.time, time.sleep)
        self.asyncSched = myAsyncSched()
        self.loop_thread = threading.Thread(target=self.asyncSched.run)
        self.loop_thread.daemon = True
        self.loop_thread.start()
        self.schedul_event = ''


    def change_temperature(self, inData, start):
        """Изменяет температуру воды

        Args:
            inData (_type_): аргументы
            start (_type_): время инициализации экземпляра класса
        """
        self.temp = self.temp + temp_boilling//timing
        print(self.temp)
        logging.info(f"'Температура'-{self.temp}")
        if self.temp > temp_boilling:
            self.off_kettle('Вскипел')
            logging.info('Чайник вскипел')
        


    def on_kettle(self):
        """Включение чайника
        
        """
        self.state = 'ВКЛ'
        print('состояние: ', self.state)
        logging.info(f"'Состояние'-{self.state}")
        for i in range(time):
            self.asyncSched.addTask(i, self.change_temperature, 1)
            


    def off_kettle(self, text='Остановлен'):
        """Выключение чайника
        
        Args:
            text -- состояние чайника
        """
        self.state = text
        print('состояние: ', self.state)
        logging.info(f"'Состояние'-{self.state}")
        self.asyncSched.stop()



