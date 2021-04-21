from django.conf import settings


def convert_hex_color_to_name(hex_color):
    hex_color = hex_color.replace('#', '')

    if hex_color in settings.COLORS:
        return settings.COLORS[hex_color]

    max_color = 16777215
    color = '000000'
    for key in settings.COLORS.keys():
        red = int(hex_color[:2], 16) - int(key[:2], 16)
        green = int(hex_color[2:4], 16) - int(key[2:4], 16)
        blue = int(hex_color[4:], 16) - int(key[4:], 16)

        # d = (r1 - r2)^2 + (g1 - g2)^2 + (b1 - b2)^2
        color_distance = (red * red) + (green * green) + (blue * blue)

        if color_distance <= max_color:
            max_color = color_distance
            color = key

    return settings.COLORS[color]
