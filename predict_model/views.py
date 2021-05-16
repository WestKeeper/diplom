import os
from django.shortcuts import render, HttpResponse, redirect
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from predict_model import forms as pred_forms
import numpy as np
import pandas as pd
import joblib

PREP_FILE_CHOICES_DICT = {}
PARAMS_TEMPLATE = ['Форма обучения_Заочная',
 'Форма обучения_Очная',
 'Форма обучения_Очно-заочная',
 'Квалификация_Бакалавр',
 'Квалификация_Магистр',
 'Квалификация_Специалист',
 'Курс_1',
 'Курс_2',
 'Курс_3',
 'Курс_4',
 'Курс_5',
 'Профиль_Автоматизация теплоэнергетических процессов',
 'Профиль_Автоматизация технологических процессов и производств (в нефтегазовой отрасли)',
 'Профиль_Автоматизация технологических процессов и производств в машиностроении',
 'Профиль_Автоматизация технологических процессов и производств в нефтяной и газовой промышленности',
 'Профиль_Автоматизация технологических процессов и производств в теплоэнергетике и теплотехнике',
 'Профиль_Аддитивные технологии',
 'Профиль_Анализ и контроль в биотехнологических и фармацевтических производствах',
 'Профиль_Безопасность и нераспространение ядерных материалов',
 'Профиль_Биомедицинская инженерия',
 'Профиль_Биотехнические и медицинские аппараты и системы',
 'Профиль_Биотехнология',
 'Профиль_Бурение нефтяных и газовых скважин',
 'Профиль_Бухгалтерский учет, анализ и аудит',
 'Профиль_Высоковольтные электроэнергетика и электротехника',
 'Профиль_Вычислительные машины, комплексы, системы и сети',
 'Профиль_Геоинформационные системы',
 'Профиль_Геологическая съемка, поиски и разведка месторождений твердых полезных ископаемых',
 'Профиль_Геология месторождений стратегических металлов',
 'Профиль_Геология нефти и газа',
 'Профиль_Геофизические методы исследования скважин',
 'Профиль_Геоэкология',
 'Профиль_Защита в чрезвычайных ситуациях',
 'Профиль_Землеустройство',
 'Профиль_Изотопные технологии и материалы',
 'Профиль_Инженерное предпринимательство',
 'Профиль_Инженерные изыскания в области природообустройства',
 'Профиль_Инжиниринг нефтегазоперерабатывающих и нефтехимических производств',
 'Профиль_Интеллектуальные робототехнические и мехатронные системы',
 'Профиль_Интеллектуальные системы автоматизации и управления',
 'Профиль_Информационно-измерительная техника и технологии',
 'Профиль_Информационно-измерительная техника и технологии неразрушающего контроля',
 'Профиль_Информационно-коммуникационные технологии',
 'Профиль_Информационно-телекоммуникационные системы и технологии (Networks and Communications)',
 'Профиль_Информационные системы и технологии в бизнесе',
 'Профиль_Информационные системы и технологии в неразрушающем контроле и безопасности',
 'Профиль_Информационные технологии в электроэнергетике',
 'Профиль_Информационные технологии управления производственными процессами',
 'Профиль_Киберфизическая автоматизация высокотехнологичных процессов и производств',
 'Профиль_Компьютеризация измерений и контроля',
 'Профиль_Компьютерное моделирование',
 'Профиль_Компьютерный анализ и интерпретация данных',
 'Профиль_Конструирование технологического оборудования',
 'Профиль_Конструкторско-технологическое обеспечение автоматизированных машиностроительных производств',
 'Профиль_Котлы, камеры сгорания и парогенераторы АЭС',
 'Профиль_Математические методы в экономике',
 'Профиль_Математическое моделирование и компьютерные вычисления',
 'Профиль_Материаловедение и технологии материалов',
 'Профиль_Материаловедение и технология материалов в машиностроении',
 'Профиль_Машины и аппараты химических производств',
 'Профиль_Машины и оборудование нефтяных и газовых промыслов',
 'Профиль_Машины и технологии сварочного производства',
 'Профиль_Машины и технология высокоэффективных процессов обработки материалов',
 'Профиль_Медицинские информационные системы и телемедицина',
 'Профиль_Надежность газонефтепроводов и хранилищ',
 'Профиль_Наноструктурные материалы',
 'Профиль_Нефтегазопромысловая геология',
 'Профиль_Обеспечение эффективности технологических процессов жизненного цикла изделий',
 'Профиль_Оборудование и технология сварочного производства',
 'Профиль_Оптико-электронные приборы и системы',
 'Профиль_Основные процессы химических производств и химическая кибернетика',
 'Профиль_Перспективные химические и биомедицинские технологии',
 'Профиль_Плазменно-пучковые и электроразрядные технологии',
 'Профиль_Поиски и разведка подземных вод и инженерно-геологические изыскания',
 'Профиль_Предпринимательство в инновационной деятельности',
 'Профиль_Приборостроение',
 'Профиль_Приборы и методы контроля качества и диагностики',
 'Профиль_Прикладная электронная инженерия',
 'Профиль_Прикладной системный инжиниринг',
 'Профиль_Применение математических методов к решению инженерных и экономических задач',
 'Профиль_Проектирование и эксплуатация атомных станций',
 'Профиль_Производственный менеджмент',
 'Профиль_Производство и транспортировка электрической энергии',
 'Профиль_Производство изделий из наноструктурных материалов',
 'Профиль_Промышленная теплоэнергетика',
 'Профиль_Промышленная томография сложных систем',
 'Профиль_Промышленная электроника',
 'Профиль_Промышленный дизайн',
 'Профиль_Пучковые и плазменные технологии',
 'Профиль_Радиационная безопасность человека и окружающей среды',
 'Профиль_Разработка и эксплуатация нефтяных и газовых месторождений',
 'Профиль_Разработка интернет-приложений',
 'Профиль_Разработка программно-информационных систем',
 'Профиль_Разработка трудноизвлекаемых запасов углеводородов',
 'Профиль_Релейная защита и автоматизация электроэнергетических систем',
 'Профиль_Релейная защита и автоматика энергосистем',
 'Профиль_Системная инженерия программного обеспечения',
 'Профиль_Системы автоматизации физических установок и их элементы',
 'Профиль_Системы управления технологическими процессами и физическими установками',
 'Профиль_Строительство глубоких нефтяных и газовых скважин в сложных горно-геологических условиях',
 'Профиль_Тепловые и атомные электрические станции',
 'Профиль_Тепловые электрические станции',
 'Профиль_Техника и физика высоких напряжений',
 'Профиль_Технологии больших данных',
 'Профиль_Технологии водородной энергетики',
 'Профиль_Технологии наукоемких производств в машиностроении',
 'Профиль_Технологии проектирования, производства и диагностирования энергетического оборудования',
 'Профиль_Технологии промышленной теплотехники',
 'Профиль_Технологии радиационной безопасности',
 'Профиль_Технологическое брокерство',
 'Профиль_Технология и оборудование химических и нефтехимических производств',
 'Профиль_Технология и техника разведки месторождений полезных ископаемых',
 'Профиль_Технология нефтегазохимии и полимерных материалов',
 'Профиль_Технология тугоплавких неметаллических и силикатных материалов',
 'Профиль_Технология, оборудование и автоматизация машиностроительных производств',
 'Профиль_Управление в производственных системах',
 'Профиль_Управление земельными ресурсами',
 'Профиль_Управление качеством в производственно-технологических системах',
 'Профиль_Управление комплексной техносферной безопасностью',
 'Профиль_Управление режимами электроэнергетических систем',
 'Профиль_Управление роботами и мехатронными системами',
 'Профиль_Управление ядерной энергетической установкой',
 'Профиль_Физика атомного ядра и частиц',
 'Профиль_Физика кинетических явлений',
 'Профиль_Физика конденсированного состояния вещества',
 'Профиль_Фотонные технологии и светотехническая инженерия',
 'Профиль_Химическая технология высокомолекулярных соединений',
 'Профиль_Химическая технология керамики и композиционных материалов',
 'Профиль_Химическая технология материалов ЯТЦ',
 'Профиль_Химическая технология материалов ядерно-топливного цикла',
 'Профиль_Химическая технология органических веществ',
 'Профиль_Химическая технология подготовки и переработки нефти и газа',
 'Профиль_Химическая технология природных энергоносителей и углеродных материалов',
 'Профиль_Химическая технология синтетических биологически активных веществ, химико-фармацевтических препаратов и косметических средств',
 'Профиль_Химическая технология топлива и газа',
 'Профиль_Химические технологии в биологии и медицине',
 'Профиль_Химический инжиниринг',
 'Профиль_Химия и технология биологически активных веществ',
 'Профиль_Цифровой маркетинг',
 'Профиль_Чистая вода',
 'Профиль_Экологические проблемы окружающей среды',
 'Профиль_Экономика и управление на предприятии',
 'Профиль_Экономика и управление на предприятии нефтегазовой отрасли',
 'Профиль_Экономика предприятий и организаций',
 'Профиль_Эксплуатация и обслуживание оборудования газокомпрессорных станций',
 'Профиль_Эксплуатация и обслуживание объектов добычи нефти',
 'Профиль_Эксплуатация и обслуживание объектов транспорта и хранения нефти, газа и продуктов переработки',
 'Профиль_Эксплуатация и обслуживание объектов транспорта и хранения углеводородов',
 'Профиль_Электрические станции',
 'Профиль_Электрические станции и подстанции, высоковольтная техника',
 'Профиль_Электроизоляционная, кабельная и конденсаторная техника',
 'Профиль_Электроизоляционные системы и кабельная техника',
 'Профиль_Электромеханика',
 'Профиль_Электромеханические и электротехнические системы автономных объектов',
 'Профиль_Электрооборудование и электрохозяйство предприятий, организаций и учреждений',
 'Профиль_Электрооборудование летательных аппаратов',
 'Профиль_Электропривод и автоматизация электротехнических комплексов и систем',
 'Профиль_Электропривод и автоматика',
 'Профиль_Электроснабжение',
 'Профиль_Электроснабжение и автоматизация объектов нефтегазовой промышленности',
 'Профиль_Электроснабжение промышленных предприятий и городов',
 'Профиль_Электроэнергетические системы и сети',
 'Профиль_Энергосберегающие режимы электрических источников питания и электротехнических установок',
 'Профиль_Ядерная медицина (медицинская физика)',
 'Профиль_Ядерные реакторы и энергетические установки',
 'Выпуск. отдел._Исследовательская школа химических и биомедицинских технологий',
 'Выпуск. отдел._Научно-образовательный центр Б.П. Вейнберга',
 'Выпуск. отдел._Научно-образовательный центр И.Н.Бутакова',
 'Выпуск. отдел._Научно-образовательный центр Н.М.Кижнера',
 'Выпуск. отдел._Отделение автоматизации и робототехники',
 'Выпуск. отдел._Отделение геологии',
 'Выпуск. отдел._Отделение информационных технологий',
 'Выпуск. отдел._Отделение контроля и диагностики',
 'Выпуск. отдел._Отделение материаловедения',
 'Выпуск. отдел._Отделение нефтегазового дела',
 'Выпуск. отдел._Отделение социально-гуманитарных наук',
 'Выпуск. отдел._Отделение химической инженерии',
 'Выпуск. отдел._Отделение экспериментальной физики',
 'Выпуск. отдел._Отделение электронной инженерии',
 'Выпуск. отдел._Отделение электроэнергетики и электротехники',
 'Выпуск. отдел._Отделение ядерно-топливного цикла',
 'Выпуск. отдел._Школа инженерного предпринимательства',
 'Обуч. подразд._Инженерная школа информационных технологий и робототехники',
 'Обуч. подразд._Инженерная школа неразрушающего контроля и безопасности',
 'Обуч. подразд._Инженерная школа новых производственных технологий',
 'Обуч. подразд._Инженерная школа природных ресурсов',
 'Обуч. подразд._Инженерная школа энергетики',
 'Обуч. подразд._Инженерная школа ядерных технологий',
 'Обуч. подразд._Исследовательская школа химических и биомедицинских технологий',
 'Обуч. подразд._Школа инженерного предпринимательства',
 'Форма финансирования_на договорной основе',
 'Форма финансирования_на основе бюджетного финансирования',
 'Форма финансирования_по целевому приёму',
 'Гражданство_Алжирская Народная Демократическая Республика',
 'Гражданство_Арабская Республика Египет',
 'Гражданство_Без гражданства',
 'Гражданство_Государство Израиль',
 'Гражданство_Демократическая Республика Конго',
 'Гражданство_Йеменская Республика',
 'Гражданство_Киргизская Республика',
 'Гражданство_Китайская Народная Республика',
 'Гражданство_Королевство Марокко',
 'Гражданство_Монголия',
 'Гражданство_Народная Республика Бангладеш',
 'Гражданство_Переходное Исламское Государство Афганистан',
 'Гражданство_Республика Айзербайджан',
 'Гражданство_Республика Беларусь',
 'Гражданство_Республика Боливия',
 'Гражданство_Республика Гана',
 'Гражданство_Республика Гватемала',
 'Гражданство_Республика Замбия',
 'Гражданство_Республика Зимбабве',
 'Гражданство_Республика Индия',
 'Гражданство_Республика Индонезия',
 'Гражданство_Республика Ирак',
 'Гражданство_Республика Казахстан',
 'Гражданство_Республика Казахстан, Российская Федерация',
 'Гражданство_Республика Колумбия',
 'Гражданство_Республика Конго',
 'Гражданство_Республика Корея',
 'Гражданство_Республика Мозамбик',
 'Гражданство_Республика Молдова',
 'Гражданство_Республика Намибия',
 'Гражданство_Республика Судан',
 'Гражданство_Республика Таджикистан',
 'Гражданство_Республика Таджикистан, Российская Федерация',
 'Гражданство_Республика Узбекистан',
 'Гражданство_Российская Федерация',
 'Гражданство_Социалистическая Республика Вьетнам',
 'Гражданство_Туркменистан',
 'Гражданство_Украина',
 'Гражданство_Федеративная Республика Бразилия',
 'Гражданство_Федеративная Республика Нигерия',
 'Гражданство_Эстонская Республика',
 'Гражданство_Южно-Африканская Республика',
 'Пол_Женский',
 'Пол_Мужской',
 'Академ отпуск (действующий) - да / нет_Да',
 'Академ отпуск (действующий) - да / нет_Нет']

def filedict_choice_update(path, filename):
    x = globals()
    x[filename] = {}
    tmp = os.listdir(path=path)
    inc = 1
    for el in tmp:
        x[filename][inc] = el
        inc += 1


def svc_model(request):
    filedict_choice_update('uploads/datasets_prepared', 'PREP_FILE_CHOICES_DICT')
    # prep_filename = ''
    if request.method == 'POST':
        form_model = pred_forms.MLModelForm(request.POST)
        if form_model.is_valid():
            cd = form_model.cleaned_data.get('prep_file_name')
            if str(cd) == '':
                return HttpResponse('Need to choose a file')
            else:
                prep_filename = PREP_FILE_CHOICES_DICT.get(
                    int(form_model.cleaned_data.get('prep_file_name')))  # a dictKey expected
            df = pd.read_excel(f"uploads/datasets_prepared/{prep_filename}")
            temp_list = prep_filename.split('.')[:-1]

            string = ''
            for element in temp_list:
                string += element

            x_train, x_test, y_train, y_test = get_train_test_samples(df)
            # answers = []
            # min_val = 5
            # max_val = 6
            # for i in range(min_val, max_val):
            #     clf = SVC(i).fit(x_train, y_train)
            #     answers.append(clf.score(x_test, y_test))
            # max_ans_idx = answers.index(max(answers)) + min_val
            clf = SVC(5).fit(x_train, y_train)
            save_model(clf)
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form_model = pred_forms.MLModelForm()
    # func_forms.filestorage_update_activator()
    return render(request, 'fileloader/index.html', {'form_model': form_model})


def model_predict(params_dict: dict, model_name):
    model = load_model(model_name)
    df = pd.DataFrame(params_dict)
    data_dummy = pd.get_dummies(df)
    dummy_values = np.zeros(239).tolist()
    params_keys = list(data_dummy.columns)
    for param in params_keys:
        if param not in PARAMS_TEMPLATE:
            print("Входные данные не соответствуют требуемым")
        else:
            dummy_values[PARAMS_TEMPLATE.index(param)] = 1

    stud_class = model.predict([dummy_values])
    return stud_class


def get_train_test_samples(df):
    data_dummy = pd.get_dummies(df)
    target = data_dummy['Класс']
    data_dummy.drop(['Класс'], axis=1, inplace=True)
    values = data_dummy.values
    X_train, X_test, y_train, y_test = train_test_split(values, target, test_size=0.33, random_state=42)
    return X_train, X_test, y_train, y_test


def predict(model, sample):
    return model.predict(sample)


def save_model(model):
    with open('uploads/INCREMENTER.txt', 'r') as reader:
        number = int(reader.read(1))
        inc = number + 1
    with open('uploads/INCREMENTER.txt', 'w') as writer:
        writer.write(str(inc))

    model_name = f'SVC-{number}'
    _ = joblib.dump(model, f"uploads/models/{model_name}.joblib.pkl")


def load_model(model_name):
    return joblib.load(f"uploads/models/{model_name}")
