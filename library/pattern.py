

class Pattern:
    """
    A Pattern class with the following operations:
        -   Read pixel color code from pattern file
        -   Mapping color code to rgb hex color.

        Constants:
            -   PALETTE: map of color code and rgb hex color.
            -   PIXELS_COUNT_CONSTRAINT: The number of pixels
                per pattern constraint.
    """

    RGB_HEX_RED = (255, 0, 0)
    RGB_HEX_GREEN = (0, 255, 0)
    RGB_HEX_BLUE = (0, 0, 255)
    RGB_HEX_BLACK = (0, 0, 0)
    PALETTE = {
        'r': RGB_HEX_RED,
        'g': RGB_HEX_GREEN,
        'b': RGB_HEX_BLUE
    }
    PIXELS_COUNT_CONSTRAINT = 64

    def __init__(self, pattern_file):
        self.pixels = list()
        try:
            self.read_pixels(pattern_file)
        except Exception:
            self.set_pixels_to_default()
        self.mapping_color_code_to_rgb_hex()

    def read_pixels(self, file):
        """
        Read the color codes from a file.

        Inputs:
            -   file: path to the pattern file
        """
        pixels = list()
        with open(file, 'r') as pattern_file:
            for line in pattern_file:
                buffer_pixels = [pixel.strip() for pixel in line.split(',')]
                pixels.extend(buffer_pixels)
        if len(pixels) != self.PIXELS_COUNT_CONSTRAINT:
            raise Exception
        else:
            self.pixels = pixels

    def set_pixels_to_default(self):
        """
        Set the pixels of this pattern's instance to default,
        which is all black.
        """
        self.pixels = (self.RGB_HEX_BLACK) * self.PIXELS_COUNT_CONSTRAINT

    def mapping_color_code_to_rgb_hex(self):
        """
        Mapping this pattern instance's color code to rgb hex code.
        """
        for i, color in enumerate(self.pixels):
            # return black if color code doesn't exist in palette
            self.pixels[i] = self.PALETTE.get(color, self.RGB_HEX_BLACK)

    def get_pixels(self):
        return self.pixels
