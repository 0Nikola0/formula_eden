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
