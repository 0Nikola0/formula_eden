from django import template

register = template.Library()

# TODO podobro ke e "%20" -> " " -> "-"

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
        "Practice 1": "Вежбање 1",
        "Practice 2": "Вежбање 2",
        "Practice 3": "Вежбање 3",
        "Qualifying 1": "Квалификации дел 1",
        "Qualifying 2": "Квалификации дел 2",
        "Qualifying 3": "Квалификации дел 3",
        "Grid": "Постројување",
        "Race": "Трка",
        "FastestLap": "Крај на трка",
        # ========================== #
        "Monday": "Понеделник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четвтрок",
        "Friday": "Петок",
        "Saturday": "Сабота",
        "Sunday": "Недела",
        # ========================== #
    }.get(value)
