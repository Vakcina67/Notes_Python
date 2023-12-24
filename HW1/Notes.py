from datetime import datetime
import json
import os

notes_filename = 'Notes.json'


# Проверка наличия заметки по введенному идентификатору
def note_check(id_note):
    if not file_check():
        return False
    for note in note_list_get():
        if note['Идентификатор: '] == id_note:
            return True
    return False


# Проверка наличия файла с заметками
def file_check():
    f_path = os.path.abspath(notes_filename)
    if os.path.exists(f_path) and os.stat(f_path).st_size != 0:
        with open(notes_filename, 'r', encoding='utf-8') as f:
            smth = json.load(f)
            if isinstance(smth, list):
                return True
            else:
                return False
    else:
        return False


# Получение списка заметок из файла
def note_list_get():
    if file_check():
        with open(notes_filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print('Файл не существует или пустой.')


# Создание заметки
def note_create():
    note_id = input('Введите название(идентификатор) заметки: ')
    while note_check(note_id):
        note_id = input('Заметка с введенным идентификатором уже существует.'
                        'Введите другой идентификатор: ')
    note_paragraph = input('Введите заголовок заметки: ')
    note_message = input('Введите текст заметки: ')
    note_datetime = datetime.now()

    note_dict = {'Идентификатор: ': note_id,
                 'Заголовок: ': note_paragraph,
                 'Текст заметки: ': note_message,
                 'Дата изменения: ': note_datetime.date().strftime('%d.%m.%Y'),
                 'Время изменения: ': note_datetime.time().strftime('%H:%M:%S')}
    if file_check():
        renew = note_list_get()
        renew.append(note_dict)
        with open(notes_filename, 'w', encoding='utf-8') as f:
            json.dump(renew, f)
        print('Заметка создана и сохранена!')
    else:
        note_list = [note_dict]
        with open(notes_filename, 'w', encoding='utf-8') as f:
            json.dump(note_list, f)
        print('Заметка создана и сохранена!')


# Чтение всего списка заметок
def note_all_read():
    if file_check():
        print('Заметки из файла: ')
        for note in note_list_get():
            print(note)
    else:
        print('Файл не существует или пустой.')


# Получение заметки по идентификатору
def note_get(n_id):
    if note_check(n_id):
        for note in note_list_get():
            if n_id == note['Идентификатор: ']:
                return note
    else:
        print('Такой заметки не существует или файл пустой.')


# Изменение заметки
def note_change():
    n_id = input('Введите идентификатор заметки, которую хотите изменить: ')
    if note_check(n_id):
        n_list = note_list_get()
        note = note_get(n_id)
        n_list.remove(note)
        note['Заголовок: '] = input('Введите новый заголовок заметки: ')
        note['Текст заметки: '] = input('Введите новый текст заметки: ')
        note_datetime = datetime.now()
        note['Дата изменения: '] = note_datetime.date().strftime('%d.%m.%Y')
        note['Время изменения: '] = note_datetime.time().strftime('%H:%M:%S')
        n_list.append(note)
        with open(notes_filename, 'w', encoding='utf-8') as f:
            json.dump(n_list, f)
        print('Заметка создана и сохранена!')
    else:
        print('Такой заметки не существует или файл пустой.')


# Удаление заметки
def note_delete():
    n_id = input('Введите идентификатор заметки, которую хотите удалить: ')
    if note_check(n_id):
        new_list = note_list_get()
        new_list.remove(note_get(n_id))
        with open(notes_filename, 'w', encoding='utf-8') as f:
            json.dump(new_list, f)
        print('Заметка успешно удалена!')
    else:
        print('Такой заметки не существует или файл пустой.')


# выборка по дате
def date_get():
    format_1 = "%d.%m.%Y"
    date_min = input('Введите начальную дату для сортировки'
                     ' в формате дд.мм.гггг: ')
    try:
        res = bool(datetime.strptime(date_min, format_1))
    except ValueError:
        res = False
    if res:
        date_max = input('Введите конечную дату для сортировки'
                         ' в формате дд.мм.гггг: ')
        try:
            res = bool(datetime.strptime(date_max, format_1))
        except ValueError:
            res = False
        if res:
            for note in note_list_get():
                if date_min <= note['Дата изменения: '] <= date_max:
                    print(note)
        else:
            print('Дата введена некорректно!')
            return False
    else:
        print('Дата введена некорректно!')
        return False


b = True
print('Добрый день! Вас приветствует редактор заметок. Ниже приведен список команд.')
while b:
    i = 0
    try:
        i = int(input('1. Создание и сохранение заметки в файл\n'
                      '2. Чтение заметки\n'
                      '3. Чтение списка заметок\n'
                      '4. Редактирование заметки\n'
                      '5. Удаление заметки\n'
                      '6. Чтение списка заметок по выбранной дате\n'
                      '7. Выход из редактора\n'
                      'Введите номер команды, которую хотите выполнить: '))
    except ValueError as e:
        print(f'Вы ввели не число! Ошибка: {e}')

    if i == 1:
        note_create()
    elif i == 2:
        _id = input('Введите идентификатор заметки, которую хотите прочитать: ')
        print(note_get(_id))
    elif i == 3:
        note_all_read()
    elif i == 4:
        note_change()
    elif i == 5:
        note_delete()
    elif i == 6:
        date_get()
    elif i == 7:
        b = False
