#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-06 09:26:57
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : Python3.7

"""
由用户自己管理换行，脚本不负责
"""


import os
import re
import math
import optparse
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class Txt2Img:
    """Share your text as a image"""

    def __init__(self, img_file, out_img_name, font_family, save_dir):
        self.img_file = img_file
        self.out_img_name = out_img_name
        self.font_family = font_family
        self.save_dir = save_dir
        self.user_font_size = 45
        self.lrc_font_size = 30
        self.line_space = 30
        self.lrc_line_space = 15
        self.stroke = 5
        self.share_img_width = 1080

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

    def save1(self, title, lrc):
        """MI Note"""
        border_color = (220, 211, 196)
        text_color = (125, 101, 89)

        out_padding = 30
        padding = 45
        banner_size = 20

        user_font = ImageFont.truetype(
            self.font_family.split(".")[0] + "bd.ttc", self.user_font_size
        )
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        if lrc.find("\n") > -1:
            lrc_rows = len(lrc.split("\n"))
        else:
            lrc_rows = 1

        w = self.share_img_width

        if title:
            inner_h = (
                padding * 2
                + self.user_font_size
                + self.line_space
                + self.lrc_font_size * lrc_rows
                + (lrc_rows - 1) * self.lrc_line_space
            )
        else:
            inner_h = (
                padding * 2
                + self.lrc_font_size * lrc_rows
                + (lrc_rows - 1) * self.lrc_line_space
            )

        h = out_padding * 2 + inner_h

        out_img = Image.new(mode="RGB", size=(w, h), color=(255, 255, 255))
        draw = ImageDraw.Draw(out_img)

        mi_img = Image.open("assets/mi_note_default_background.png")
        mi_banner = Image.open("assets/mi_note_default_banner.png").resize(
            (banner_size, banner_size), resample=3
        )

        # add background
        for x in range(int(math.ceil(h / 100))):
            out_img.paste(mi_img, (0, x * 100))

        # add border
        def draw_rectangle(draw, rect, width):
            for i in range(width):
                draw.rectangle(
                    (rect[0] + i, rect[1] + i, rect[2] - i, rect[3] - i),
                    outline=border_color,
                )

        draw_rectangle(
            draw, (out_padding, out_padding, w - out_padding, h - out_padding), 2
        )

        # add banner
        out_img.paste(mi_banner, (out_padding, out_padding))
        out_img.paste(
            mi_banner.transpose(Image.FLIP_TOP_BOTTOM),
            (out_padding, h - out_padding - banner_size + 1),
        )
        out_img.paste(
            mi_banner.transpose(Image.FLIP_LEFT_RIGHT),
            (w - out_padding - banner_size + 1, out_padding),
        )
        out_img.paste(
            mi_banner.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM),
            (w - out_padding - banner_size + 1, h - out_padding - banner_size + 1),
        )

        if title:
            user_w, user_h = ImageDraw.Draw(
                Image.new(mode="RGB", size=(1, 1))
            ).textsize(title, font=user_font, spacing=self.line_space)
            draw.text(
                ((w - user_w) // 2, out_padding + padding),
                title,
                font=user_font,
                fill=text_color,
                spacing=self.line_space,
            )
            draw.text(
                (
                    out_padding + padding,
                    out_padding + padding + self.user_font_size + self.line_space,
                ),
                lrc,
                font=lyric_font,
                fill=text_color,
                spacing=self.lrc_line_space,
            )
        else:
            draw.text(
                (out_padding + padding, out_padding + padding),
                lrc,
                font=lyric_font,
                fill=text_color,
                spacing=self.lrc_line_space,
            )

        self.save_img(out_img)

    def save2(self, title, lrc):
        """netease cloud music: 朱砂"""
        text_color = (255, 255, 255)
        user_color = (213, 57, 50)

        top_padding = 45
        left_padding = 45
        bottom_padding = 200
        text_inner_padding = 10

        self.user_font_size = self.user_font_size - 25

        user_font = ImageFont.truetype(
            self.font_family.split(".")[0] + "bd.ttc", self.user_font_size
        )
        lyric_font = ImageFont.truetype(
            self.font_family.split(".")[0] + "bd.ttc", self.lrc_font_size
        )

        user_w, user_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            title, font=user_font, spacing=self.line_space
        )

        lrc_rows = len(lrc.split("\n"))

        w = self.share_img_width - 400

        h = (
            top_padding
            + self.user_font_size
            + top_padding
            + self.lrc_font_size * lrc_rows
            + (lrc_rows - 1) * self.lrc_line_space
            + bottom_padding
        )

        out_img = Image.new(mode="RGB", size=(w, h), color=(213, 57, 50))
        draw = ImageDraw.Draw(out_img)

        # add title background
        draw.rectangle(
            (
                left_padding,
                top_padding,
                left_padding + user_w + text_inner_padding * 2,
                top_padding + user_h + text_inner_padding * 2,
            ),
            fill="#fff",
        )

        # text
        draw.text(
            (left_padding + text_inner_padding, top_padding + text_inner_padding),
            title,
            font=user_font,
            fill=user_color,
            spacing=self.line_space,
        )
        draw.text(
            (left_padding, top_padding * 2 + user_h + text_inner_padding * 2),
            lrc,
            font=lyric_font,
            fill=text_color,
            spacing=self.lrc_line_space,
        )

        self.save_img(out_img)

    def save3(self, title, lrc):
        """netease cloud music: 信封"""
        user = "—— " + title
        text_color = "#282528"
        user_color = "#bbb8b9"

        banner_height = 20
        top_padding = 45
        left_padding = 45
        bottom_padding = 200

        self.lrc_font_size -= 10
        self.user_font_size = self.lrc_font_size

        user_font = ImageFont.truetype(self.font_family, self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        user_w, user_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            user, font=user_font, spacing=self.line_space
        )

        lrc_rows = len(lrc.split("\n"))

        w = self.share_img_width - 400

        h = (
            banner_height
            + top_padding
            + self.lrc_font_size * lrc_rows
            + lrc_rows * self.lrc_line_space
            + user_h
            + bottom_padding
        )

        out_img = Image.new(mode="RGB", size=(w, h), color="#fffeff")
        draw = ImageDraw.Draw(out_img)

        # add background
        pic_top = Image.open("assets/netease_cloud_music_style2_top.png")
        pic_right = Image.open("assets/netease_cloud_music_style2_right.png")

        for x in range(int(math.ceil(w / pic_top.size[0]))):
            out_img.paste(pic_top, (x * pic_top.size[0] - 15, 0))

        out_img.paste(pic_right, (w - pic_right.size[0], banner_height * 2))

        # text
        draw.text(
            (left_padding, banner_height + top_padding),
            lrc,
            font=lyric_font,
            fill=text_color,
            spacing=self.lrc_line_space,
        )

        draw.text(
            (w - left_padding - user_w, h - bottom_padding),
            user,
            font=user_font,
            fill=user_color,
            spacing=self.line_space,
        )

        self.save_img(out_img)

    def save4(self, title, lrc):
        """netease cloud music: 古书"""
        user, song = title.split("·")
        text_color = "#282528"
        user_color = "#000"

        top_padding = 45
        left_padding = 45
        bottom_padding = 200
        circle_h = 20

        user_font = ImageFont.truetype(
            self.font_family.split(".")[0] + "bd.ttc", self.user_font_size
        )
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        lyric_w, lyric_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            song, font=lyric_font, spacing=self.line_space
        )

        user_w, user_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            user, font=user_font, spacing=self.line_space
        )

        lrc_rows = len(lrc.split("\n"))

        w = self.share_img_width - 400

        h = (
            top_padding
            + user_h
            + circle_h
            + self.lrc_line_space * 2
            + top_padding
            + self.lrc_font_size * (1 + lrc_rows)
            + (lrc_rows - 1) * self.lrc_line_space
            + bottom_padding
        )

        out_img = Image.new(mode="RGB", size=(w, h), color="#fff")
        draw = ImageDraw.Draw(out_img)

        # circle
        draw.arc(
            (
                left_padding,
                top_padding + user_h + self.lrc_line_space + circle_h,
                left_padding + circle_h,
                top_padding + user_h + self.lrc_line_space + circle_h * 2,
            ),
            -360,
            0,
            fill=(213, 57, 50),
            width=7,
        )

        # text
        draw.text(
            (left_padding, top_padding),
            user,
            font=user_font,
            fill=user_color,
            spacing=self.line_space,
        )

        draw.text(
            (left_padding, top_padding + user_h + self.line_space * 2 + circle_h),
            song,
            font=lyric_font,
            fill=text_color,
            spacing=self.line_space,
        )

        draw.text(
            (
                left_padding,
                top_padding
                + user_h
                + self.line_space * 2
                + circle_h
                + lyric_h
                + top_padding,
            ),
            lrc,
            font=lyric_font,
            fill=text_color,
            spacing=self.lrc_line_space,
        )

        self.save_img(out_img)

    def save5(self, title, lrc):
        """netease cloud music: 磨砂"""
        user = title
        text_color = "#fff"
        user_color = "#fff"

        top_padding = 140
        left_padding = 50
        pic_width = 650
        pic_padding = 20

        bottom_padding = 120

        self.user_font_size += 15
        self.lrc_font_size += 10

        user_font = ImageFont.truetype(
            self.font_family.split(".")[0] + "bd.ttc", self.user_font_size
        )
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        user_w, user_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            user, font=user_font, spacing=self.line_space
        )

        lrc_rows = len(lrc.split("\n"))

        pic = Image.open(self.img_file)

        pw, ph = pic.size

        resize_pic = pic.resize((pic_width, pic_width * ph // pw), resample=3)

        rw, rh = resize_pic.size

        w = self.share_img_width

        out_img = pic.filter(ImageFilter.GaussianBlur(60)).resize(
            (w, 1920 if w * ph // pw < 1920 else w * ph // pw), resample=3
        )

        ow, oh = out_img.size

        draw = ImageDraw.Draw(out_img)

        h = (
            top_padding
            + rh
            + pic_padding
            + user_h
            + pic_padding
            + self.lrc_font_size * lrc_rows
            + lrc_rows * self.lrc_line_space
            + bottom_padding
        )

        # paste pic
        out_img.paste(resize_pic, ((w - rw) // 2, top_padding))

        draw.line(
            (
                (w - user_w) // 2,
                top_padding + rh + pic_padding + user_h + 10,
                (w + user_w) // 2,
                top_padding + rh + pic_padding + user_h + 10,
            ),
            fill=user_color,
        )

        # text
        draw.text(
            ((w - user_w) // 2, top_padding + rh + pic_padding),
            user,
            font=user_font,
            fill=user_color,
            spacing=self.line_space,
        )

        draw.text(
            (left_padding, top_padding + rh + pic_padding + user_h + pic_padding * 2),
            lrc,
            font=lyric_font,
            fill=text_color,
            spacing=self.lrc_line_space,
        )

        self.save_img(out_img)

    def save6(self, title, lrc):
        """bili wall paper: lighth/dark"""
        user = "——「" + title + "」"
        if self.img_file[-5] == "t":
            text_color = (74, 69, 99)
            bottom_padding = 1020
            left_padding = 150
        else:
            text_color = (255, 255, 255)
            bottom_padding = 920
            left_padding = 120

        top_padding = 650

        self.lrc_font_size += 20

        user_font = ImageFont.truetype(self.font_family, self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        user_w, user_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            user, font=user_font, spacing=self.line_space
        )

        out_img = Image.open(self.img_file)

        draw = ImageDraw.Draw(out_img)

        draw.text(
            (left_padding, top_padding),
            lrc,
            font=lyric_font,
            fill=text_color,
            spacing=self.lrc_line_space + 20,
        )

        draw.text(
            (out_img.size[0] - user_w - left_padding, out_img.size[1] - bottom_padding),
            user,
            font=user_font,
            fill=text_color,
        )

        self.save_img(out_img)

    def save7(self, lrc):
        """film style"""
        text_color = "#fff"

        self.lrc_font_size = 42

        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        lyric_w, lyric_h = ImageDraw.Draw(Image.new(mode="RGB", size=(1, 1))).textsize(
            lrc, font=lyric_font, spacing=self.line_space
        )  # get lyric w, h

        # load pic
        pic = Image.open(self.img_file)

        pw, ph = pic.size

        if pw < 1920:
            pic = pic.resize((1920, 1920 * ph // pw), resample=3)
            pw, ph = pic.size

        w, h = pw, int(ph * 1.24)

        out_img = Image.new(mode="RGB", size=(w, h), color=(0, 0, 0))
        draw = ImageDraw.Draw(out_img)

        # paste pic
        out_img.paste(pic, (0, int(ph * 0.12)))

        # text
        padding = 10  # (ph*0.12-lyric_h)//2
        draw.text(
            ((w - lyric_w) // 2, int(ph * 1.13) + padding),
            lrc,
            font=lyric_font,
            fill=text_color,
            spacing=self.lrc_line_space,
        )

        self.save_img(out_img)

    def save_img(self, out_img):
        """save out_img object to local disk"""
        img_save_path = (
            f"{self.save_dir}/{self.out_img_name}.png"
            if self.out_img_name
            else f"{self.save_dir}/out_img_name.png"
        )
        is_to_save = True
        if os.path.exists(img_save_path):
            print(f"{img_save_path} exists!")
            promp = input("Overwrite existing file? [y/n] ")
            if not promp in ("Y", "y"):
                is_to_save = False
        if is_to_save:
            out_img.save(img_save_path)
            print(f"generated images path: {img_save_path}")


def main():
    parser = optparse.OptionParser(
        "usage: [-f <font path>] -t <pic style> -i <img file>\n\t"
        "-w <some text> -u <user/title> -l <like count> -o <out img name>"
    )
    parser.add_option(
        "-t",
        dest="pic_style",
        type="int",
        help=(
            "1: Mi-note style; 2~5: netease-cloud-music lyric style;"
            "6: bilibili wallpaper style; 7: film style."
        ),
    )
    parser.add_option("-i", dest="img_file", type="string", help="image path")
    parser.add_option(
        "-f", dest="font_family", type="string", help="truetype font path"
    )
    parser.add_option("-w", dest="text", type="string", help="some text you like")
    parser.add_option("-u", dest="user", type="string", help="user name/title")
    parser.add_option(
        "-o", dest="out_img_name", type="string", help="generated images name",
    )

    (options, args) = parser.parse_args()
    pic_style = options.pic_style
    img_file = options.img_file
    font_family = options.font_family
    text = options.text
    user = options.user
    out_img_name = options.out_img_name

    if not font_family:
        font_family = "assets/msyh.ttc"

    if not pic_style:
        pic_style = 1

    if text:
        if not img_file:
            img_file = "assets/sundayday.jpg"

        # image will be saved as img/{out_img_name}
        img = Txt2Img(img_file, out_img_name, font_family, save_dir="img")

        if pic_style == 1:
            img.save1(user, text.replace("\\n", "\n"))
        elif pic_style == 2:
            img.save2(user, text.replace("\\n", "\n"))
        elif pic_style == 3:
            img.save3(user, text.replace("\\n", "\n"))
        elif pic_style == 4:
            img.save4(user, text.replace("\\n", "\n"))
        elif pic_style == 5:
            img.save5(user, text.replace("\\n", "\n"))
        elif pic_style == 6:
            img.save6(user, text.replace("\\n", "\n"))
        elif pic_style == 7:
            img.save7(text.replace("\\n", "\n"))
    else:
        print("input -h/--help option for help")


if __name__ == "__main__":
    main()
