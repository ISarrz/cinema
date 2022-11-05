class Eror(Exception):
    pass

eror = 'ОШИБКА'

class hall():
    def __init__(self, name, width, hight) -> None:
        self.places = [[[]] * width for i in range(hight)]
        self.width, self.hight, self.name = width, hight, name

    def print_info(self):
        print(f' Зал {self.name}')
        print('   ', '   '.join([str(i) for i in range(1, self.width + 1)]))
        for i in range(1, self.hight + 1):
            string = " ".join(['[' + str(g[1]) + ']' for g in self.places[i - 1]])
            print(f'{i}  {string}')
        print()
    
    def number_chairs(self):
        for i in range(self.hight):
            count = 1
            for g in range(self.width):
                if not(self.places[i][g] and self.places[i][g][1] == ' '):
                    self.places[i][g] = [i, count]
                    count += 1
    
    def change_hall(self):
        while True:
            print(f'\tСистема настройки зала "{self.name}"\n'
                   'Для удаления сидения: "удалить" {ряд}, {столбец}\n'
                   'Для добавления сидения: "добавить" {ряд}, {столбец}\n'
                   'Для добавления столбца слева: "Добавить слева"\n' 
                   'Для добавления столбца справа: "Добавить справа"\n'
                   'Для добавления ряда сверху: "Добавить сверху"\n'
                   'Для добавления ряда снизу: "Добавить снизу"\n'
                   'Для удаления столбца слева: "Удалить слева"\n' 
                   'Для удаления столбца справа: "Удалить справа"\n'
                   'Для удаления ряда сверху: "Удалить сверху"\n'
                   'Для удаления ряда снизу: "Удалить снизу"\n'
                   'Для выхода: "Выход"\n')
            self.print_info()
            answer = input().lower()
            try:
                if answer == 'выход':
                    break
                if len(answer.split()) == 3 and answer.split()[0].lower() == 'удалить':
                    rol, col = map(int, answer.split()[1:])
                    if not(1 <= col <= self.width) or not(1 <= rol <= self.hight):
                        raise Eror
                    self.places[rol - 1][col - 1] = ['', ' ']
                    self.number_chairs()
                elif len(answer.split()) == 3 and answer.split()[0].lower() == 'добавить':
                    rol, col = map(int, answer.split()[1:])
                    if not(1 <= col <= self.width) or not(1 <= rol <= self.hight):
                        raise Eror
                    self.places[rol - 1][col - 1] = ['', '']
                    self.number_chairs()
                elif answer == "добавить слева":
                    for i in range(self.hight):
                        rol = [['', '']]
                        rol.extend(self.places[i])
                        self.places[i] = rol
                    self.width += 1
                    self.number_chairs()
                elif answer == "добавить справа":
                    for i in range(self.hight):
                        rol = ['', '']
                        self.places[i].append(rol)
                    self.width += 1
                    self.number_chairs()
                elif answer == "добавить сверху":
                    rol = [[['', ''] for _ in range(self.width)]]
                    rol.extend(self.places)
                    self.places = rol
                    self.hight += 1
                    self.number_chairs()
                elif answer == "добавить снизу":
                    self.places.append([['', '']  for _ in range(self.width)])
                    self.hight += 1
                    self.number_chairs()
                elif answer == "удалить слева":
                    for i in range(self.hight):
                        self.places[i] = self.places[i][1:]
                    self.width -= 1
                    self.number_chairs()
                elif answer == "удалить справа":
                    for i in range(self.hight):
                        self.places[i] = self.places[i][:-1]
                    self.width -= 1
                    self.number_chairs()
                elif answer == "удалить сверху":
                    self.places = self.places[1:]
                    self.hight -= 1
                    self.number_chairs()
                elif answer == "удалить снизу":
                    self.places = self.places[:-1]
                    self.hight -= 1
                    self.number_chairs()
                
                else:
                    raise Eror
            except Exception:
                print(eror)