from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Mark, Chastisement
import random
from datetime import datetime
from datacenter.models import Commendation, Lesson, Schoolkid, Subject


def fix_marks(schoolkid):
    """Функция исправления оценки. Укажите имя ученика"""
    try:
        choosed_schoolkid = Schoolkid.objects.filter(full_name__startswith=schoolkid).get()
        Mark.objects.filter(schoolkid=choosed_schoolkid[0], points__in=[2, 3]).update(points=5)
    except ObjectDoesNotExist:
        print("Такого ученика не существует")
    except MultipleObjectsReturned:
        print('Слишко много учеников с таким именем')


def remove_chastisements(schoolkid):
    """Функция удаления плохого комментария. Укажите имя ученика"""
    try:
        choosed_schoolkid = Schoolkid.objects.filter(full_name__startswith=schoolkid)
        Chastisement.objects.filter(schoolkid=choosed_schoolkid[0]).delete()
    except ObjectDoesNotExist:
        print("Такого ученика не существует")
    except MultipleObjectsReturned:
        print('Слишко много учеников с таким именем')


def create_commendation(name, subject):
    """Функция слздания хорошего комментария. Укажите имя ученика и предмет"""
    commendation_types = {
        1: 'Молодец',
        2: 'Отлично',
        3: 'Хорошо',
        4: 'Гораздо лучше, чем я ожидал!',
        5: 'Ты меня приятно удивил!',
        6: 'Великолепно!',
        7: 'Прекрасно!',
        8: 'Ты меня очень обрадовал!',
        9: 'Именно этого я давно ждал от тебя!',
        10: 'Сказано здорово – просто и ясно!',
        11: 'Ты, как всегда, точен!',
        12: 'Очень хороший ответ!',
        13: 'Талантливо!',
        14: 'Ты сегодня прыгнул выше головы!',
        15: 'Я поражен!',
        16: 'Уже существенно лучше!',
        17: 'Потрясающе!',
        18: 'Замечательно!',
        19: 'Прекрасное начало!',
        20: 'Так держать!',
        21: 'Ты на верном пути!',
        22: 'Здорово!',
        23: 'Это как раз то, что нужно!',
        24: 'Я тобой горжусь!',
        25: 'С каждым разом у тебя получается всё лучше!',
        26: 'Мы с тобой не зря поработали!',
        27: 'Я вижу, как ты стараешься!',
        28: 'Ты растешь над собой!',
        29: 'Ты многое сделал, я это вижу!',
        30: 'Теперь у тебя точно все получится!'}
    random_commendation = commendation_types[random.randint(1, 30)]
    try:
        schoolkid = Schoolkid.objects.filter(full_name__startswith=name)[0]
    except ObjectDoesNotExist:
        print("Такого ученика не существует")
    except MultipleObjectsReturned:
        print('Слишко много учеников с таким именем')

    try:
        subject_name = Subject.objects.filter(title=subject)[0]
    except ObjectDoesNotExist:
        print("Введите корректный предмет")

        lessons_6a = Lesson.objects.filter(subject__title=subject, year_of_study=6, group_letter="А")
        last_lesson = Lesson.objects.filter(subject__title=subject, year_of_study=6, group_letter="А").order_by(
            "date").last().date
        Commendation.objects.create(text=random_commendation, created=datetime.fromisoformat(str(last_lesson)),
                                    schoolkid=schoolkid, subject=subject_name, teacher=lessons_6a[0].teacher)


