from django import template
register = template.Library()


@register.filter
def del_tag(tags, tag):
    tags = tags.split('+')
    if tag in tags:
        tags.remove(tag)
    tags = '+'.join(tags)
    if len(tags) == 0:
        tags = 'empty'
    return tags
