from django import template

register = template.Library()


def index(arr, i):
    return arr[i]


register.filter('index', index)
