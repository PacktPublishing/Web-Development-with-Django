from django import template

register = template.Library()

@register.simple_tag
def greet_user(message, username):
    return "{greeting_message}, {user}!!!".format(greeting_message=message, user=username)

