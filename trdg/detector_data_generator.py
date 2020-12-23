import os
import random as rnd

from PIL import Image, ImageFilter

from trdg import computer_text_generator, background_generator, distorsion_generator

try:
    from trdg import handwritten_text_generator
except ImportError as e:
    print("Missing modules for handwritten text generation.")

def create_strings_from_dict(length, lang_dict,allow_variable=True):
    """
        Create all strings by picking X random word in the dictionnary
    """

    dict_len = len(lang_dict)
    current_string = ""
    for _ in range(0, rnd.randint(1, length) if allow_variable else length):
        current_string += lang_dict[rnd.randrange(dict_len)]
    return current_string


class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(
        cls,
        index,
        strdict,
        font,
        out_dir,
        size,
        extension,
        skewing_angle,
        random_skew,
        blur,
        random_blur,
        background_type,
        distorsion_type,
        distorsion_orientation,
        is_handwritten,
        name_format,
        width,
        alignment,
        text_color,
        orientation,
        space_width,
        character_spacing,
        margins,
        fit,
        output_mask,
        word_split,
        image_dir,
        stroke_width=0, 
        stroke_fill="#282828",
        image_mode="RGB", 
    ):
        background_height = 800
        background_width = 600
        row_number = 25
        row_number_range = [i+1 for i in range(row_number)]
        row_height = int(background_height / row_number)
        row_text_maxlength = 40
        font_size_range = list(range(int(row_height/2),int(row_height+1)))
        #############################
        # Generate background image #
        #############################
        if background_type == 0:
            background_img = background_generator.gaussian_noise(
                background_height, background_width
            )
        elif background_type == 1:
            background_img = background_generator.plain_white(
                background_height, background_width
            )
        elif background_type == 2:
            background_img = background_generator.quasicrystal(
                background_height, background_width
            )
        else:
            background_img = background_generator.image(
                background_height, background_width, image_dir
            )
        # background_mask = Image.new(
        #     "RGB", (background_width, background_height), (0, 0, 0)
        # )

        bbox = []
        texts = []
        row_hastxt = []
        for _ in range(rnd.choice(row_number_range)):
            rowid = rnd.choice(row_number_range)
            while rowid  in row_hastxt:
                rowid = rnd.choice(row_number_range)
            row_hastxt.append(rowid)
            ##########################
            # Create picture of text #
            ##########################
            text = create_strings_from_dict(row_text_maxlength,strdict)
            texts.append(text)
            font_size = rnd.choice(font_size_range)
            image, mask = computer_text_generator.generate(
                text,
                font,
                text_color,
                font_size,
                orientation,
                space_width,
                character_spacing,
                fit,
                word_split,
                stroke_width, 
                stroke_fill,
            )
            random_angle = rnd.randint(0 - skewing_angle, skewing_angle)

            rotated_img = image.rotate(
                skewing_angle if not random_skew else random_angle, expand=1
            )

            rotated_mask = mask.rotate(
                skewing_angle if not random_skew else random_angle, expand=1
            )

            #############################
            # Apply distorsion to image #
            #############################
            if distorsion_type == 0:
                distorted_img = rotated_img  # Mind = blown
                # distorted_mask = rotated_mask
            elif distorsion_type == 1:
                distorted_img, distorted_mask = distorsion_generator.sin(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            elif distorsion_type == 2:
                distorted_img, distorted_mask = distorsion_generator.cos(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            else:
                distorted_img, distorted_mask = distorsion_generator.random(
                    rotated_img,
                    rotated_mask,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2),
                )
            ##################################
            # Resize image to desired format #
            ##################################

            # Horizontal text
            
            if orientation == 0:
                new_width = int(
                    distorted_img.size[0]
                    * (float(font_size) / float(distorted_img.size[1]))
                )
                if new_width <= background_width:
                    resized_img = distorted_img.resize(
                        (new_width, font_size), Image.ANTIALIAS
                    )
                    # resized_mask = distorted_mask.resize((new_width, font_size), Image.NEAREST)
                else:
                    new_height = int(distorted_img.size[1]
                        * (float(background_width) / float(distorted_img.size[0]))
                    )
                    resized_img = distorted_img.resize(
                        (background_width, new_height), Image.ANTIALIAS
                    )
                    resized_mask = distorted_img.resize(
                        (background_width, new_height), Image.NEAREST
                    )
            # Vertical text
            elif orientation == 1:
                # new_height = int(
                #     float(distorted_img.size[1])
                #     * (float(size - horizontal_margin) / float(distorted_img.size[0]))
                # )
                # resized_img = distorted_img.resize(
                #     (size - horizontal_margin, new_height), Image.ANTIALIAS
                # )
                # resized_mask = distorted_mask.resize(
                #     (size - horizontal_margin, new_height), Image.NEAREST
                # )
                # background_width = size
                # background_height = new_height + vertical_margin
                raise ValueError("Vertical text")
            else:
                raise ValueError("Invalid orientation")

            #############################
            # Place text with alignment #
            #############################
            top_left_x =  rnd.choice(range(0,max(1,background_width-resized_img.size[0])))
            top_left_y =  (rowid * row_height) + rnd.choice(range(0,max(1,row_height-font_size)))
            bbox.append([top_left_x,top_left_y,top_left_x+resized_img.size[0],top_left_y+resized_img.size[1]])
            background_img.paste(
                resized_img,
                (top_left_x, top_left_y),
                resized_img,
            )

        #######################
        # Apply gaussian blur #
        #######################

        gaussian_filter = ImageFilter.GaussianBlur(
            radius=blur if not random_blur else rnd.randint(0, blur)
        )
        final_image = background_img.filter(gaussian_filter)
        # final_mask = background_mask.filter(gaussian_filter)
        
        ############################################
        # Change image mode (RGB, grayscale, etc.) #
        ############################################
        
        final_image = final_image.convert(image_mode)
        # final_mask = final_mask.convert(image_mode) 

        #####################################
        # Generate name for resulting image #
        #####################################
        # We remove spaces if space_width == 0
        if space_width == 0:
            text = text.replace(" ", "")
        if name_format == 0:
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))
        elif name_format == 1:
            image_name = "{}_{}.{}".format(str(index), text, extension)
            mask_name = "{}_{}_mask.png".format(str(index), text)
        elif name_format == 2:
            image_name = "{}.{}".format(str(index), extension)
            mask_name = "{}_mask.png".format(str(index))
        else:
            print("{} is not a valid name format. Using default.".format(name_format))
            image_name = "{}_{}.{}".format(text, str(index), extension)
            mask_name = "{}_{}_mask.png".format(text, str(index))

        # Save the image
        if out_dir is not None:
            final_image.save(os.path.join(out_dir, image_name))
            # if output_mask == 1:
                # final_mask.save(os.path.join(out_dir, mask_name))
        else:
            # if output_mask == 1:
            #     return final_image, final_mask
            return final_image,bbox,texts
            
        #################################
