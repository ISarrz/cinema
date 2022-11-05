from classes import cinema, hall

# дописать класс филмов
# дописать продажу билетов
class Eror(Exception):
    pass

eror = 'ОШИБКА'
class movie():
    def __init__(self,name) -> None:
        self.name = name
        self.cinemas = []





    
class Interface():
    def __init__(self) -> None:
        self.cinemas = []
        self.movies = []
    
    def buy(self):
        pass

    def settings(self):
        while True:
            print('\nСитема настройки кинотеатров\n'
                  'Для настрйки фильмов: Настройка фильмов\n'
                  'Для добавления кинотеатра: Добавить {название кинотеатра}\n'
                  'Для удаления кинотеатра: Удалить {название кинотеатра}\n'
                  'Для выбора кинотеатра: Выбрать {название кинотеатра}\n'
                  'Для выхода: Выход\n')
            print('Кинотеатры:')
            for i in self.cinemas:
                i.print_info()
            print()
            answer = input().lower()
            try:
                if answer == 'выход':
                    break
                if answer.split()[0] == 'добавить':
                    self.cinemas.append(cinema(answer.split()[1:]))
                elif answer.split()[0] == 'удалить':
                    for i in range(len(self.cinemas)):
                        if self.cinemas[i].name == ' '.join(answer.split()[1:]):
                            del self.cinemas[i]
                            break
                elif answer.split()[0] == 'выбрать':
                    for i in range(len(self.cinemas)):
                        if self.cinemas[i].name == ' '.join(answer.split()[1:]):
                            self.cinemas[i].change_cinema()
                            break
                else:
                    raise Eror
            except Exception:
                print(eror)

    
    def run(self, buy, settings):
        while True:
            print('Для покупки билета введите: "Купить билет"\n'
                  'Для настройки введите: "Настройка"\n'
                  'Для выхода: Выход\n')
            answer = input().lower()
            try:
                if answer == 'купить билет':
                    buy()
                elif answer == 'настройка':
                    settings() 
                elif answer == 'выход':
                    break
                else:
                    print('Ошибка\n')
            except Exception:
                print(eror)

def main():
    interface = Interface()
    interface.run(interface.buy, interface.settings)


if __name__ == '__main__':
    main()