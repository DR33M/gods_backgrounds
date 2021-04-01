from django import template

register = template.Library()


@register.filter
def partition(old_list, args):
    columns, idx = args.split(',')
    try:
        columns = int(columns)
        old_list = list(old_list)
    except (ValueError, TypeError):
        return [old_list]
    new_list = [list() for i in range(columns)]
    for i, val in enumerate(old_list):
        new_list[i % columns].append(val)

    return new_list[int(idx)]
