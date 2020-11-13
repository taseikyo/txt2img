#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-30 20:47:40
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : python3.8


"""
感觉 [豆瓣2019年度榜单](https://book.douban.com/annual/2019) 中给出的书签
样式挺好看的 感觉做网易云热评也好看 于是把背景和几个素材扣下来了

至于为什么不在 txt2img.py 上继续添加 感觉那代码写得太垃圾了...
"""

import os
import re
import math
import optparse
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def douban2019(text, user, ss_name, out_img_name, font_family):
    """生成豆瓣2019榜单样式的网易云热评
    text: 热评
    user: 用户名
    ss_name: 歌名与歌手名
    out_img_name: 生成图片名
    """
    text_color = "#2e2e2e"
    text_font_size = 16
    text_line_space = 30
    line_space = 30
    share_img_width = 500
    pen_padding = 10
    padding = 30

    text_font = ImageFont.truetype(font_family, text_font_size)
    text_w, text_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
        text, font=text_font, spacing=line_space
    )

    w = share_img_width
    h = share_img_width

    out_img = Image.new(mode="RGB", size=(w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(out_img)

    bg_img = Image.open("assets/file-1575626352.png")
    out_img.paste(bg_img, (0, 0))

    pen_img = Image.open("assets/file-1575626423.png")
    pen_w = 80
    pen_h = pen_img.size[1] * pen_w // pen_img.size[0]
    pen_img = pen_img.resize((pen_w, pen_h), resample=3)
    out_img.paste(pen_img, (pen_padding, pen_padding), mask=pen_img)

    icon_w = 18
    icon_x = padding + pen_w
    icon_y = padding
    icon_img = Image.open("assets/douban-icon.png").resize((icon_w, icon_w), resample=3)
    out_img.paste(icon_img, (icon_x, icon_y), mask=icon_img)


    text_x = icon_x
    text_y = icon_y + icon_w * 2

    max_line_w = share_img_width - text_x - padding

    # 这个 width 是指一行多少字 绝了 我还以为是宽度
    lines = textwrap.wrap(text, width=22)
    for line in lines:
        width, height = text_font.getsize(line)
        draw.text((text_x, text_y), line, font=text_font, fill=text_color, spacing=text_line_space)
        text_y += height + pen_padding * 2

    user = f"—— {user}"
    user_y = text_y + padding
    user_x = share_img_width - padding - text_font.getsize(user)[0]
    draw.text((user_x, user_y), user, font=text_font, fill=text_color, spacing=text_line_space)

    ss_name_y = text_y + padding + text_font.getsize(user)[1] + pen_padding
    ss_name_x = share_img_width - padding - text_font.getsize(ss_name)[0]
    draw.text((ss_name_x, ss_name_y), ss_name, font=text_font, fill=text_color, spacing=text_line_space)

    out_img.save(out_img_name)


def main():
    parser = optparse.OptionParser(
        "usage: [-f <font path>] -w <text> -u <user>\n\t-s <song name & singer> -o <out img name>"
    )
    parser.add_option("-w", dest="text", type="string", help="some text")
    parser.add_option("-u", dest="user", type="string", help="user name")
    parser.add_option(
        "-s", dest="song_singer_name", type="string", help="song name & singer"
    )
    parser.add_option(
        "-o", dest="out_img_name", type="string", help="generated image name",
    )
    parser.add_option(
        "-f", dest="font_family", type="string", help="truetype font file path"
    )

    options, args = parser.parse_args()

    text = options.text
    user = options.user
    song_singer_name = options.song_singer_name
    out_img_name = options.out_img_name
    font_family = options.font_family

    if text:
        if not out_img_name:
            out_img_name = "tmp.png"
        if not user:
            user = "Anonymous"
        if not song_singer_name:
            song_singer_name = "Anonymous"
        if not font_family:
            font_family = "assets/msyh.ttc"

        douban2019(text, user, song_singer_name, out_img_name, font_family)
    else:
        print("input -h/--help option for help")


if __name__ == "__main__":
    main()
