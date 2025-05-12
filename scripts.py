from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
import random

COMPLIMENTS = [
        'Хвалю!',
        'Молодец!',
        'Сказано здорово - просто ясно!',
        'Я поражен!',
        'Ты растешь над собой!'
    ]


def fix_marks(schoolkid):
    schoolkid = get_schoolkid(schoolkid)
    if schoolkid is None:
        return
    bad_grades = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    print('Плохие оценки исправлены.')
    return


def remove_chastisements(schoolkid):
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastisements.delete()
    print('Замечания удалены.')
    return


def create_commendation(schoolkid, subject_name):
    lessons=Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject__title=subject_name).order_by('date').first()
    if lesson is None:
        print("Нет уроков по данному предмету")
        return
            
    Commendation.objects.create(schoolkid=schoolkid, teacher=lesson.teacher,subject=lesson.subject,created=lesson.date,text=random.choice(COMPLIMENTS))


def get_schoolkid(full_name):
    try:
        return Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.DoesNotExist:
        print("Такого ученика не существует")
        return None
    except Schoolkid.MultipleObjectsReturned:
        print("Нашёл два и более ученика")
        return None
