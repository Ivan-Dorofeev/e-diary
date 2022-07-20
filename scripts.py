from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Mark, Chastisement
from random import choice
from datetime import datetime
from datacenter.models import Commendation, Lesson, Schoolkid, Subject


def fix_marks(schoolkid_name):
    """Функция исправления оценки. Укажите имя ученика"""
    try:
        choosed_schoolkid = Schoolkid.objects.filter(full_name__startswith=schoolkid_name)[0]
        Mark.objects.filter(schoolkid=choosed_schoolkid, points__in=[2, 3]).update(points=5)
    except ObjectDoesNotExist:
        print("Такого ученика не существует")
    except MultipleObjectsReturned:
        print('Слишко много учеников с таким именем')


def remove_chastisements(schoolkid_name):
    """Функция удаления плохого комментария. Укажите имя ученика"""
    try:
        choosed_schoolkid = Schoolkid.objects.filter(full_name__startswith=schoolkid_name)[0]
        Chastisement.objects.filter(schoolkid=choosed_schoolkid).delete()
    except ObjectDoesNotExist:
        print("Такого ученика не существует")
    except MultipleObjectsReturned:
        print('Слишко много учеников с таким именем')


def create_commendation(schoolkid_name, subject_name, year_of_class, group_of_class):
    """Функция слздания хорошего комментария. Укажите имя ученика и предмет"""
    commendation_types = ['Молодец', 'Отлично', 'Хорошо', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                          'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
                          'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!',
                          'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                          'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!', 'Потрясающе!',
                          'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!', 'Здорово!',
                          'Это как раз то, что нужно!', 'Я тобой горжусь!',
                          'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
                          'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                          'Теперь у тебя точно все получится!']
    random_commendation = choice(commendation_types)
    try:
        schoolkid = Schoolkid.objects.filter(full_name__startswith=schoolkid_name)[0]
    except ObjectDoesNotExist:
        print("Такого ученика не существует")
    except MultipleObjectsReturned:
        print('Слишко много учеников с таким именем')

    try:
        subject = Subject.objects.filter(title=subject_name)[0]
    except ObjectDoesNotExist:
        print("Введите корректный предмет")

    try:
        lessons_of_class = Lesson.objects.filter(subject__title=subject_name, year_of_study=year_of_class,
                                                 group_letter=group_of_class)[0]
        last_lesson = Lesson.objects.filter(subject__title=subject_name, year_of_study=year_of_class,
                                            group_letter=group_of_class).order_by("date").last().date
    except ObjectDoesNotExist:
        print("Неверно указан класс. Проверьте, что он указан на на русском языке.")

        Commendation.objects.create(text=random_commendation, created=datetime.fromisoformat(str(last_lesson)),
                                    schoolkid=schoolkid, subject=subject, teacher=lessons_of_class.teacher)
