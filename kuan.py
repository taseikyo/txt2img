#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Date    : 2021-01-09 15:26:05
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8

import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


def fefive_phone(year=2020):
    """
    一事无成手机壁纸
    """
    # 壁纸宽高，底色
    w, h = 1080, 2340
    color = (0, 0, 0)
    text_color = (255, 255, 255)

    font_family = "calibri"
    year_size = 90
    text_size = 65

    out_img = Image.new(mode="RGB", size=(w, h), color=color)
    draw = ImageDraw.Draw(out_img)

    year_font = ImageFont.truetype(font_family, year_size)
    text_font = ImageFont.truetype(font_family, text_size)

    year_text = f"{year} -- {datetime.now().year}"
    five_text = f"{datetime.now().year-year} years, you still have nothing"

    year_w, year_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
        year_text, font=year_font
    )
    text_w, _ = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
        five_text, font=text_font
    )

    # 年份的 y 位置
    year_y = 650
    line_space = 30
    draw.text(
        ((w - year_w) // 2, year_y),
        year_text,
        font=year_font,
        fill=text_color,
    )
    draw.text(
        ((w - text_w) // 2, year_y + year_h + line_space),
        five_text,
        font=text_font,
        fill=text_color,
    )

    if not os.path.exists("img"):
        os.mkdir("img")
    out_img.save(f"img/{year}.png")
    print(f"generated images path: img/{year}.png")


def fefive_pc(year=2020, align="center"):
    """
    电脑壁纸

    @align: ["center", "rb", "rt", "lb", lt]
    五个可选参数，分别为 居中 右下 右上 左下 左上
    right-bottom -> rb
    """
    # 壁纸宽高，底色
    w, h = 1920, 1080
    color = (0, 0, 0)
    text_color = (255, 255, 255)

    font_family = "calibri"
    year_size = 90
    text_size = 65

    out_img = Image.new(mode="RGB", size=(w, h), color=color)
    draw = ImageDraw.Draw(out_img)

    year_font = ImageFont.truetype(font_family, year_size)
    text_font = ImageFont.truetype(font_family, text_size)

    year_text = f"{year} -- {datetime.now().year}"
    five_text = f"{datetime.now().year-year} years, you still have nothing"

    year_w, year_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
        year_text, font=year_font
    )
    text_w, text_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
        five_text, font=text_font
    )

    line_space = 30
    right_padding = 100
    left_padding = 100
    bottom_padding = 150
    top_padding = 150
    # 年份的 y 位置
    if align == "rb":
        year_y = h - line_space - year_h - text_h - bottom_padding
        year_x = w - year_w - right_padding
        text_x = w - text_w - right_padding
    elif align == "rt":
        year_y = top_padding
        year_x = w - year_w - right_padding
        text_x = w - text_w - right_padding
    elif align == "lb":
        year_y = h - line_space - year_h - text_h - bottom_padding
        year_x = left_padding
        text_x = left_padding
    elif align == "lt":
        year_y = top_padding
        year_x = left_padding
        text_x = left_padding
    else:
        year_y = (h - line_space - year_h) // 2
        year_x = (w - year_w) // 2
        text_x = (w - text_w) // 2

    draw.text(
        (year_x, year_y),
        year_text,
        font=year_font,
        fill=text_color,
    )
    draw.text(
        (text_x, year_y + year_h + line_space),
        five_text,
        font=text_font,
        fill=text_color,
    )

    if not os.path.exists("img"):
        os.mkdir("img")
    out_img.save(f"img/{year}_pc.png")
    print(f"generated images path: img/{year}_pc.png")


if __name__ == "__main__":
    [fefive_phone(i) for i in range(1980, 2021)]
    fefive_pc(1949, "rb")
