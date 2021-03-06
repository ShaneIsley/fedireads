''' template filters '''
from django import template

from fedireads import models


register = template.Library()

@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d.get(k) or 0

@register.filter(name='stars')
def stars(number):
    ''' turn integers into stars '''
    try:
        number = int(number)
    except (ValueError, TypeError):
        number = 0
    return ('★' * number) + '☆' * (5 - number)

@register.filter(name='description')
def description_format(description):
    ''' handle the various OL description formats '''
    if isinstance(description, dict) and 'value' in description:
        description = description['value']
    if '----------' in description:
        description = description.split('----------')[0]

    return description.strip()

@register.filter(name='author_bio')
def bio_format(bio):
    ''' clean up OL author bios '''
    if isinstance(bio, dict) and 'value' in bio:
        bio = bio['value']
    bio = bio.split('\n')
    return bio[0].strip()


@register.filter(name='username')
def get_user_identifier(user):
    ''' use localname for local users, username for remote '''
    return user.localname if user.localname else user.username


@register.simple_tag(takes_context=True)
def shelve_button_identifier(context, book):
    ''' check what shelf a user has a book on, if any '''
    try:
        shelf = models.ShelfBook.objects.get(
            shelf__user=context['user'],
            book=book
        )
    except models.ShelfBook.DoesNotExist:
        return 'to-read'
    identifier = shelf.shelf.identifier
    if identifier == 'to-read':
        return 'reading'
    elif identifier == 'reading':
        return 'read'
    return 'to-read'


@register.simple_tag(takes_context=True)
def shelve_button_text(context, book):
    ''' check what shelf a user has a book on, if any '''
    try:
        shelf = models.ShelfBook.objects.get(
            shelf__user=context['user'],
            book=book
        )
    except models.ShelfBook.DoesNotExist:
        return 'Want to read'
    identifier = shelf.shelf.identifier
    if identifier == 'to-read':
        return 'Start reading'
    elif identifier == 'reading':
        return 'I\'m done!'
    return 'Want to read'


@register.simple_tag(takes_context=True)
def current_shelf(context, book):
    ''' check what shelf a user has a book on, if any '''
    try:
        shelf = models.ShelfBook.objects.get(
            shelf__user=context['user'],
            book=book
        )
    except models.ShelfBook.DoesNotExist:
        return None
    return shelf.name

