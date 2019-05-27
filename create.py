import argparse
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont
import cv2
import os
from tqdm import tqdm


def main(alphabet_path, output_path):
    alphabet = create_alphabet(alphabet_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    font = ImageFont.truetype('./data/font/msyh.ttc', 72)

    for i, char in tqdm(zip(range(len(alphabet)), alphabet), ncols=150):
        create_train_image(output_path, char, i, font)
        create_val_image(output_path, char, i, font)
        create_test_image(output_path, char, i, font)


def create_test_image(output_path, char, i, font):
    bg = np.full((224, 244), 255)
    bg_width = bg.shape[1]

    word_size = get_word_size(font, char)
    word_height = word_size[1]
    word_width = word_size[0]

    # bottom middle
    text_x = int((bg_width - word_width) / 2)
    text_y = bg_width - word_height - 25
    draw_word_and_save_file(bg, char, font, i, output_path, text_x, text_y, "test")


def create_val_image(output_path, char, i, font):
    bg = np.full((224, 244), 255)
    bg_height = bg.shape[0]
    bg_width = bg.shape[1]

    word_size = get_word_size(font, char)
    word_height = word_size[1]
    word_width = word_size[0]

    # right middle

    text_x = bg_width - word_width
    text_y = int((bg_height - word_height) / 2)
    draw_word_and_save_file(bg, char, font, i, output_path, text_x, text_y, "val")


def create_train_image(output_path, char, i, font):
    # middle, top middle, left middle
    bg1 = np.full((224, 244), 255)

    bg_height = bg1.shape[0]
    bg_width = bg1.shape[1]

    word_size = get_word_size(font, char)
    word_height = word_size[1]
    word_width = word_size[0]

    # middle offset
    text_x = int((bg_width - word_width) / 2)
    text_y = int((bg_height - word_height) / 2)
    draw_word_and_save_file(bg1, char, font, i, output_path, text_x, text_y, "train")

    # left offset
    bg2 = np.full((224, 244), 255)

    text_x = 10
    text_y = int((bg_height - word_height) / 2)
    draw_word_and_save_file(bg2, char, font, i, output_path, text_x, text_y, "train")

    # top offset
    bg3 = np.full((224, 244), 255)

    text_x = int((bg_width - word_width) / 2)
    text_y = 10
    draw_word_and_save_file(bg3, char, font, i, output_path, text_x, text_y, "train")


def draw_word_and_save_file(bg3, char, font, i, output_path, text_x, text_y, cat):
    word_img, _, _ = draw_text_on_bg(char, font, bg3, text_x, text_y)
    folder_name = os.path.join(output_path, cat, str(i))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    fname = os.path.join(folder_name, cat + '_' + str(i) + '.jpg')
    cv2.imwrite(fname, word_img)


def create_alphabet(alphabet_path):
    alphabet = ' '
    with open(alphabet_path, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            alphabet += line.strip()
    return alphabet


def draw_text_on_bg(word, font, bg, x, y):
    """
    Draw word in the center of background
    :param word: word to draw
    :param font: font to draw word
    :param bg: background numpy image
    :return:
        np_img: word image
        text_box_pnts: left-top, right-top, right-bottom, left-bottom
    """

    word_size = get_word_size(font, word)
    word_height = word_size[1]
    word_width = word_size[0]

    offset = font.getoffset(word)

    pil_img = Image.fromarray(np.uint8(bg))
    draw = ImageDraw.Draw(pil_img)

    word_color = get_word_color(bg, x, y, word_height, word_width)

    draw_text_wrapper(draw, word, x - offset[0], y - offset[1], font, word_color)

    np_img = np.array(pil_img).astype(np.float32)

    text_box_pnts = [
        [x, y],
        [x + word_width, y],
        [x + word_width, y + word_height],
        [x, y + word_height]
    ]

    return np_img, text_box_pnts, word_color


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


def get_word_color(bg, text_x, text_y, word_height, word_width):
    """
    Only use word roi area to get word color
    """
    offset = 10
    ymin = text_y - offset
    ymax = text_y + word_height + offset
    xmin = text_x - offset
    xmax = text_x + word_width + offset

    word_roi_bg = bg[ymin: ymax, xmin: xmax]

    bg_mean = int(np.mean(word_roi_bg) * (2 / 3))
    word_color = random.randint(0, bg_mean)
    return word_color


def draw_text_wrapper(draw, text, x, y, font, text_color):
    """
    :param x/y: 应该是移除了 offset 的
    """
    draw.text((x, y), text, fill=text_color, font=font)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--alphabet_path', required=True, type=str,
                        help='Path to the alphabet')
    parser.add_argument('--output_path', required=True, type=str,
                        help='Path to the output folder')

    args = parser.parse_args()

    main(args.alphabet_path, args.output_path)
