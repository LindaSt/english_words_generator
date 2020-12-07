import argparse
from multiprocessing import Pool, cpu_count

import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont
import os
import itertools
import glob

from utils.transforms import shear_y, shear_x


def main(words_path, fonts_folder, output_path, train_amount, test_amount, val_amount):
    word_list = create_word_list(words_path)

    font_list = glob.glob(os.path.join(fonts_folder, '*.ttf'))

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    pool = Pool(processes=cpu_count())

    pool.starmap(generate_files, zip(word_list,
                                     range(len(word_list)),
                                     itertools.repeat(font_list),
                                     itertools.repeat(output_path),
                                     itertools.repeat(test_amount),
                                     itertools.repeat(train_amount),
                                     itertools.repeat(val_amount)))

    pool.close()


def generate_files(word, i, font_list, output_path, test_amount, train_amount, val_amount):
    print('create files for char {}'.format(i))

    create_image('train', output_path, word, i, font_list, train_amount)
    create_image('val', output_path, word, i, font_list, val_amount)
    create_image('test', output_path, word, i, font_list, test_amount)


def create_image(subset, output_path, char, i, font_list, amount):
    for j in range(amount):
        font = ImageFont.truetype(sample_font(font_list), 140 + random.randint(-40, 40))
        draw_word_and_save_file(char, font, output_path, subset, i, j)


def sample_font(font_list):
    return np.random.choice(font_list, 1)[0]


def draw_word_and_save_file(char, font, output_path, cat, char_class, image_number=None):
    word_size = get_word_size(font, char)
    word_height = word_size[1]
    word_width = word_size[0]

    bg_height = int(word_height*2.5)
    bg_width = int(word_width*2)
    bg = Image.new('L', (bg_width, bg_height), color=255)

    # bottom middle
    # TODO fix this to make it a bit more centred
    text_x = int((bg_width - word_width) / 2) + random.randint(-int(bg_width*0.1), int(bg_height*0.05))
    text_y = int((bg_height - word_height) / 2) + random.randint(-int(bg_height*0.05), int(bg_height*0.05))

    # draw the word on the image
    word_img = draw_text_on_bg(char, font, bg, text_x, text_y)

    # save the image
    folder_name = os.path.join(output_path, cat, str(char_class))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    fname = os.path.join(folder_name, cat + '_' + str(image_number) + '.png')
    word_img.save(fname)


def create_word_list(words_path):
    my_file = open(words_path, "r")
    content_list = my_file.readlines()
    return [w.strip() for w in content_list]


def draw_text_on_bg(word, font, pil_img, x, y):
    """
    Draw word in the center of background
    :param word: word to draw
    :param font: font to draw word
    :param pil_img: background PIL image
    :return:
        pil_img: word image
    """
    offset = font.getoffset(word)

    draw = ImageDraw.Draw(pil_img)

    word_color = 0

    draw_text_wrapper(draw, word, x - offset[0], y - offset[1], font, word_color)

    # add rotation
    #rot = random.randint(-2, 2)
    #pil_img = pil_img.rotate(rot, expand=1, fillcolor=255)
    # add shearing
    pil_img = shear_x(pil_img, 0.08)
    pil_img = shear_y(pil_img, 0.08)

    # np_img = np.array(rotated).astype(np.float32)
    # word_size = get_word_size(font, word)
    # word_height = word_size[1]
    # word_width = word_size[0]
    # text_box_pnts = [
    #     [x, y],
    #     [x + word_width, y],
    #     [x + word_width, y + word_height],
    #     [x, y + word_height]
    # ]

    return pil_img


def get_word_size(font, word):
    """
    Get word size removed offset
    :param font: truetype
    :param word:
    :return:
        size: word size, removed offset (width, height)
    """
    offset = font.getoffset(word)
    size = font.getsize(word)
    size = (size[0] - offset[0], size[1] - offset[1])
    return size


def draw_text_wrapper(draw, text, x, y, font, text_color):
    draw.text((x, y), text, fill=text_color, font=font)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--words_path', required=True, type=str,
                        help='Path to the word list text file')
    parser.add_argument('--fonts_folder', required=True, type=str,
                        help='Path to the font folder')
    parser.add_argument('--output_path', required=True, type=str,
                        help='Path to the output folder')
    parser.add_argument('--train_amount', type=int, default=10,
                        help='The amount of train images for each word')
    parser.add_argument('--test_amount', type=int, default=1,
                        help='The amount of test images for each word')
    parser.add_argument('--val_amount', type=int, default=1,
                        help='The amount of val images for each word')

    args = parser.parse_args()

    main(args.words_path, args.fonts_folder, args.output_path, args.train_amount, args.test_amount, args.val_amount)
    print("Fishished!")
