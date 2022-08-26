from django import template

register = template.Library()


@register.filter
def zameni_procent_dvaese(value):
    '''
        Zamenuva "%20" so " "
    '''
    return value.replace("%20", " ")


@register.filter
def zameni_prazno_mesto(value):
    '''
        Zamenuva " " so "-"
    '''
    return value.replace(" ", "-")


@register.filter
def prevedi(value):
    '''
        Preveduva nekoi od angliskite zborovi na mkd (so dict() keys)
    '''
    return {
        # ========================= #
        "Complete": "Завршено",
        "Confirmed": "Потврдено",
        "Canceled": "Откажано",
        # ========================= #
        "Practice 1": "Тренинг 1",
        "Practice 2": "Тренинг 2",
        "Practice 3": "Тренинг 3",
        "Qualifying 1": "Квалификации дел 1",
        "Qualifying 2": "Квалификации дел 2",
        "Qualifying 3": "Квалификации дел 3",
        "Grid": "Доделување пол позиција",
        "Sprint Qualifying": "Спринт квалификување",
        "Race": "Трка",
        "FastestLap": "Подиум прослава",
        # ========================== #
        "Monday": "Понеделник",
        "Mon": "Пон",
        "Tuesday": "Вторник",
        "Tue": "Вто",
        "Wednesday": "Среда",
        "Wed": "Сре",
        "Thursday": "Четвтрок",
        "Thu": "Чет",
        "Friday": "Петок",
        "Fri": "Пет",
        "Saturday": "Сабота",
        "Sat": "Саб",
        "Sunday": "Недела",
        "Sun": "Нед",
        # ========================== #
    }.get(value)
