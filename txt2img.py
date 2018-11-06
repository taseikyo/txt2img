#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-06 09:26:57
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
from PIL import Image, ImageDraw, ImageFont
import optparse
import re
import math

class Txt2Img:
    """Share your text as a image"""
    def __init__(self, out_img_name, font_family, save_dir):
        self.out_img_name = out_img_name
        self.font_family = font_family
        self.save_dir = save_dir
        self.user_font_size = 45 
        self.lrc_font_size = 30
        self.line_space = 30 
        self.lrc_line_space = 15
        self.text_color = '#fff'
        self.stroke = 5 
        self.share_img_width = 1080

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

    def save(self, title, lrc, filename = None):
        """MI Note"""
        user = title
        border_color = (220, 211, 196)
        text_color = (125, 101, 89)
        
        out_padding = 30
        padding = 45
        banner_size = 20

        user_font = ImageFont.truetype(self.font_family.split('.')[0]+'bd.ttc', self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)
        lyric_w, lyric_h = ImageDraw.Draw(Image.new(mode='RGB', 
                                        size=(1, 1))).textsize(lrc, font=lyric_font, spacing=self.line_space) # get lyric w, h

        max_line_w = self.share_img_width - out_padding*2 - padding*2

        if lrc.find('\n') > -1: # if '\n' finds, I won't check the words length 
            lrc_rows = len(lrc.split('\n'))
        elif lyric_w > max_line_w:
            lrc_rows = lyric_w // max_line_w + 1
            tmp = ''

            inc = int(math.ceil(len(lrc)//lrc_rows)) + 6 # words in a line

            for i in range(lrc_rows):
                tmp += lrc[i*inc: (i+1)*inc] + '\n'
            lrc = tmp
        else:
            lrc_rows = 1


        w = self.share_img_width

        if user:
            inner_h = padding*2 + self.user_font_size + self.line_space + \
                        self.lrc_font_size * lrc_rows + (lrc_rows - 1) * self.lrc_line_space
        else:
            inner_h = padding*2 + self.lrc_font_size * lrc_rows + (lrc_rows - 1) * self.lrc_line_space

        h = out_padding*2 + inner_h

        out_img = Image.new(mode='RGB', size=(w, h), color=(255, 255, 255))
        draw = ImageDraw.Draw(out_img)

        mi_img = Image.open('res/mi_note_default_background.png')
        mi_banner = Image.open('res/mi_note_default_banner.png').resize((banner_size, banner_size), resample=3)

        # add background
        for x in range(int(math.ceil(h/100))):
            out_img.paste(mi_img, (0, x*100))

        # add border
        def draw_rectangle(draw, rect, width):
            for i in range(width):
                draw.rectangle((rect[0] + i, rect[1] + i, rect[2] - i, rect[3] - i), outline=border_color)

        draw_rectangle(draw, (out_padding, out_padding, w - out_padding, h - out_padding ), 2)

        # add banner
        out_img.paste(mi_banner, (out_padding, out_padding))
        out_img.paste(mi_banner.transpose(Image.FLIP_TOP_BOTTOM), (out_padding, h - out_padding - banner_size + 1))
        out_img.paste(mi_banner.transpose(Image.FLIP_LEFT_RIGHT), (w - out_padding - banner_size + 1, out_padding))
        out_img.paste(mi_banner.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM), 
                        (w - out_padding - banner_size + 1, h - out_padding - banner_size + 1))

        # text
        if user:
            user_w, lyric_h = ImageDraw.Draw(Image.new(mode='RGB', 
                                size=(1, 1))).textsize(user, font=user_font, spacing=self.line_space)
            draw.text(((w - user_w)//2, out_padding + padding),  user, font=user_font, 
                        fill=text_color, spacing=self.line_space)
            draw.text((out_padding + padding, out_padding + padding + self.user_font_size + self.line_space), 
                        lrc, font=lyric_font, fill=text_color, spacing=self.lrc_line_space)
        else:
            draw.text((out_padding + padding, out_padding + padding), 
                        lrc, font=lyric_font, fill=text_color, spacing=self.lrc_line_space)

        self.saveImg(title, filename, out_img)

    def saveImg(self, user, filename, out_img):
        """save out_img object to local disk"""
        img_save_path = ''
        i = 0
        if filename:
            img_save_path = self.save_dir + '/' + filename + '.png'
            while os.path.exists(img_save_path):
                img_save_path = self.save_dir + '/' + filename + str(i) + '.png'
                i += 1
        elif user:
            img_save_path = self.save_dir + '/' + user + '.png'
            while os.path.exists(img_save_path):
                img_save_path= self.save_dir + '/' + user + str(i) + '.png'
                i += 1
        print('generated images path:', img_save_path)
        out_img.save(img_save_path)


def main():
    parser = optparse.OptionParser('usage: [-f <font path>] -t <pic style> -i <img file>\n\t' 
        '-w <some text> -u <user> -l <like count> -o <out img name>')
    parser.add_option('-t', dest='pic_style', type='int', help='1: share text like MI note; 2: netease share image')
    parser.add_option('-i', dest='img_file', type='string', help='your own image')
    parser.add_option('-f', dest='font_family', type='string', help='truetype font file path')
    parser.add_option('-w', dest='text', type='string', help='some text')
    parser.add_option('-u', dest='user', type='string', help='user name')
    parser.add_option('-o', dest='out_img_name', type='string', help='generated images name[if not set, the name will be USER]')
    
    (options, args) = parser.parse_args()
    pic_style = options.pic_style
    img_file = options.img_file
    font_family = options.font_family
    text = options.text
    user = options.user
    out_img_name = options.out_img_name

    if not font_family:
        font_family = 'res/msyh.ttc'

    if not pic_style:
        pic_style = 1
    if text:
        if user is None:
            out_img_name = 'Anonymous'
        if img_file is None:
            img_file = 'res/sundayday.jpg'
        img = Txt2Img(out_img_name, font_family, save_dir = 'img')
        if pic_style == 1:
            img.save(user, text.replace('\\n', '\n'), out_img_name)
    else:
        print('input -h/--help option for help')


if __name__ == '__main__':
    main()