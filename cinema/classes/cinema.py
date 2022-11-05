class cinema():
    def __init__(self, name) -> None:
        self.halls = []
        self.moves = []
        self.name = ' '.join(name)
    
    def append(self, hall):
        self.halls.append(hall)

    def add_movie(self, movie):
        pass

    def print_info(self):
        print(self.name)
    
    def change_cinema(self):
        while True:
            print(f'\nСистема найстроки кинотеатра "{self.name}"\n'
                   'Для добавления зала: Добавить {название зала} {ширина зала} {высота зала}\n'
                   'Для удаления зала: Удалить {название зала}\n'
                   'Для выбора зала: Выбрать {название зала}\n'
                   'Для изменения названия кинотеатра: Изменить {новое название}\n'
                   'Для выхода: Выход\n')
            print('Залы:')
            for i in range(len(self.halls)):
                print(self.halls[i].name)
            print()
            answer = input()
            try:
                if answer.lower() == 'выход':
                    break
                if answer.split()[0].lower() == 'добавить':
                    self.halls.append(hall(' '.join(answer.split()[1:-2]), int(answer.split()[-2]), int(answer.split()[-1])))
                    self.halls[-1].number_chairs()
                elif answer.split()[0].lower() == 'удалить':
                    for i in range(len(self.halls)):
                        if self.halls[i].name == ' '.join(answer.split()[1:]):
                            del self.halls[i]
                            break
                elif answer.split()[0].lower() == 'выбрать':
                    for i in range(len(self.halls)):
                        if self.halls[i].name == ' '.join(answer.split()[1:]):
                            self.halls[i].change_hall()
                            break
                elif answer.split()[0].lower() == 'изменить':
                    self.name = ' '.join(answer.split()[1:])
                else:
                    raise Eror
            except Exception:
                print(eror)