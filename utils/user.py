def is_moderator(user):
    return user.groups.filter(name='images-moderators').exists()
