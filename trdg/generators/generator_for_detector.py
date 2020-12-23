import os
import random

from ..detector_data_generator import FakeTextDataGenerator
from ..utils import load_dict, load_fonts


class GeneratorForDetector:
    """Generator that uses a given list of strings"""

    def __init__(
        self,
        strdict,
        count=-1,
        fonts=[],
        language="en",
        # size=32,
        skewing_angle=0,
        random_skew=False,
        blur=0,
        random_blur=False,
        background_type=0,
        distorsion_type=0,
        distorsion_orientation=0,
        is_handwritten=False,
        width=-1,
        # alignment=1,
        text_color="#282828",
        orientation=0,
        space_width=1.0,
        character_spacing=0,
        margins=(5, 5, 5, 5),
        fit=False,
        output_mask=False,
        word_split=False,
        image_dir=os.path.join(
            "..", os.path.split(os.path.realpath(__file__))[0], "images"
        ),
        stroke_width=0, 
        stroke_fill="#282828",
        image_mode="RGB",
    ):
        self.count = count
        # self.strings = strings
        self.strdict = load_dict(strdict)
        self.fonts = fonts
        if len(fonts) == 0:
            self.fonts = load_fonts(language)
        self.language = language
        # self.size = size
        self.skewing_angle = skewing_angle
        self.random_skew = random_skew
        self.blur = blur
        self.random_blur = random_blur
        self.background_type = background_type if isinstance(background_type,list) else [background_type]
        self.distorsion_type = distorsion_type if isinstance(distorsion_type, list) else [distorsion_type]
        self.distorsion_orientation = distorsion_orientation
        self.is_handwritten = is_handwritten
        self.width = width
        # self.alignment = alignment
        self.text_color = text_color
        self.orientation = orientation
        self.space_width = space_width if isinstance(space_width,list) else [character_spacing]
        self.character_spacing = character_spacing if isinstance(character_spacing,list) else [character_spacing]
        self.margins = margins
        self.fit = fit
        self.output_mask = output_mask
        self.word_split = word_split
        self.image_dir = image_dir
        self.generated_count = 0
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill
        self.image_mode = image_mode 

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.generated_count == self.count:
            raise StopIteration
        self.generated_count += 1
        return FakeTextDataGenerator.generate(
                self.generated_count,
                self.strdict,
                self.fonts[(self.generated_count - 1) % len(self.fonts)],
                None,
                None,
                None,
                self.skewing_angle,
                self.random_skew,
                self.blur,
                self.random_blur,
                random.choice( self.background_type),
                random.choice( self.distorsion_type),
                self.distorsion_orientation,
                self.is_handwritten,
                0,
                self.width,
                None,
                self.text_color,
                self.orientation,
                random.choice( self.space_width),
                random.choice( self.character_spacing),
                self.margins,
                self.fit,
                self.output_mask,
                self.word_split,
                self.image_dir,
                self.stroke_width,
                self.stroke_fill,
                self.image_mode, 
            )
