import extcolors
import imagehash
from PIL import Image as PIL_Image, ImageSequence, ImageOps
from django.conf import settings

from .models import Color
from main.utils.colors import convert_hex_color_to_name
import logging

logger = logging.getLogger(__name__)


class ImageService:
    def __init__(self, file=None):
        self.data = {}
        if file:
            self.file = file
            self.image_file = PIL_Image.open(file)
            self.image_file_et = ImageOps.exif_transpose(self.image_file)

    def get_hash(self):
        self.data['image_hash'] = imagehash.phash(self.image_file, 31).__str__()
        return self.data['image_hash']

    def get_resolution(self):
        self.data['width'], self.data['height'] = self.image_file_et.width, self.image_file_et.height,
        return [self.data['width'], self.data['height']]

    def get_ratio(self):
        self.data['ratio'] = round((self.image_file_et.width / self.image_file_et.height), 2)
        return self.data['ratio']

    def get_size(self):
        # Bytes to MB
        self.data['size'] = round((self.file.size / 1024 / 1024), 2)
        return self.data['size']

    def get_extension(self):
        self.data['extension'] = self.image_file.format
        return self.data['extension']

    def is_animated(self):
        index = 0
        for frame in ImageSequence.Iterator(self.image_file):
            index += 1
            if index > 1:
                return True

        return False

    def add_colors(self, image):
        width_ratio = self.get_ratio()

        output_size = {
            'width': round(width_ratio * settings.IMAGE_COLORS_MAX_WIDTH),
            'height': settings.IMAGE_COLORS_MAX_WIDTH
        }

        image_file = self.image_file.resize((output_size['width'], output_size['height']))

        image_colors, pixel_count = extcolors.extract_from_image(image_file)

        colors = Color.objects.all().values_list('hex', flat=True)

        hex_colors = []
        add_colors = []
        for image_color in image_colors:
            if (image_color[1] / pixel_count) * 100 > settings.IMAGE_MINIMUM_PERCENTAGE_OF_DOMINANT_COLORS:
                color = '#%02x%02x%02x' % image_color[0]
                hex_colors.append(color)
                if color not in colors:
                    add_colors.append(Color(hex=color, similar_color=convert_hex_color_to_name(color)))

        Color.objects.bulk_create(add_colors)
        image.colors.add(*Color.objects.filter(hex__in=hex_colors))

    def resize_preview_image(self, image):
        height_ratio = self.data['height'] / self.data['width']

        if self.image_file_et.width > settings.IMAGE_PREVIEW_WIDTH:
            output_size = (settings.IMAGE_PREVIEW_WIDTH, round(round(height_ratio, 2) * settings.IMAGE_PREVIEW_WIDTH))
            image_file = self.image_file_et.resize(output_size)
            image_file.save(image.preview_image.path)
