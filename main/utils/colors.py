def get_closest_color(color_hex, colors_queryset):
    color_hex = color_hex.replace('#', '')
    max_color = 16777215
    color_obj = None
    for obj in colors_queryset:
        clean_color_hex = obj.hex.replace('#', '')
        red = int(color_hex[:2], 16) - int(clean_color_hex[:2], 16)
        green = int(color_hex[2:4], 16) - int(clean_color_hex[2:4], 16)
        blue = int(color_hex[4:], 16) - int(clean_color_hex[4:], 16)

        # d = (r1 - r2)^2 + (g1 - g2)^2 + (b1 - b2)^2
        color_distance = (red * red) + (green * green) + (blue * blue)

        if color_distance <= max_color:
            max_color = color_distance
            color_obj = obj

    return color_obj
