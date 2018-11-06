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
            user_w, user_h = ImageDraw.Draw(Image.new(mode='RGB', 
                                size=(1, 1))).textsize(user, font=user_font, spacing=self.line_space)
            draw.text(((w - user_w)//2, out_padding + padding),  user, font=user_font, 
                        fill=text_color, spacing=self.line_space)
            draw.text((out_padding + padding, out_padding + padding + self.user_font_size + self.line_space), 
                        lrc, font=lyric_font, fill=text_color, spacing=self.lrc_line_space)
        else:
            draw.text((out_padding + padding, out_padding + padding), 
                        lrc, font=lyric_font, fill=text_color, spacing=self.lrc_line_space)

        self.saveImg(title, filename, out_img)

    def save1(self, title, lrc, filename = None):
        """netease cloud music share pic: 朱砂"""
        user = title
        text_color = (255, 255, 255)
        user_color = (213, 57, 50)
        
        top_padding = 45
        left_padding = 45
        bottom_padding = 200
        text_inner_padding = 10

        self.user_font_size = self.user_font_size-25

        user_font = ImageFont.truetype(self.font_family.split('.')[0]+'bd.ttc', self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family.split('.')[0]+'bd.ttc', self.lrc_font_size)

        user_w, user_h = ImageDraw.Draw(Image.new(mode='RGB', 
                            size=(1, 1))).textsize(user, font=user_font, spacing=self.line_space)

        lrc_rows = len(lrc.split('\n'))

        w = self.share_img_width - 400

        h = top_padding + self.user_font_size + top_padding + self.lrc_font_size * lrc_rows + (lrc_rows - 1) * self.lrc_line_space + bottom_padding

        out_img = Image.new(mode='RGB', size=(w, h), color=(213, 57, 50))
        draw = ImageDraw.Draw(out_img)

        # add title background
        draw.rectangle((left_padding, top_padding, left_padding+user_w+text_inner_padding*2, 
                    top_padding+user_h+text_inner_padding*2), fill='#fff')

        # text
        draw.text((left_padding+text_inner_padding, top_padding+text_inner_padding), user, font=user_font, 
                    fill=user_color, spacing=self.line_space)
        draw.text((left_padding, top_padding*2+user_h+text_inner_padding*2), 
                    lrc, font=lyric_font, fill=text_color, spacing=self.lrc_line_space)

        self.saveImg(title, filename, out_img)

    def save2(self, title, lrc, filename = None):
        """netease cloud music share pic: 信封"""
        user = '—— '+title
        text_color = '#282528'
        user_color = '#bbb8b9'
        
        banner_height = 20
        top_padding = 45
        left_padding = 45
        bottom_padding = 200

        self.lrc_font_size -= 10
        self.user_font_size = self.lrc_font_size

        user_font = ImageFont.truetype(self.font_family, self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        user_w, user_h = ImageDraw.Draw(Image.new(mode='RGB', 
                            size=(1, 1))).textsize(user, font=user_font, spacing=self.line_space)

        lrc_rows = len(lrc.split('\n'))

        w = self.share_img_width - 400

        h = banner_height + top_padding + self.lrc_font_size * lrc_rows + lrc_rows * self.lrc_line_space + user_h + bottom_padding

        out_img = Image.new(mode='RGB', size=(w, h), color='#fffeff')
        draw = ImageDraw.Draw(out_img)
        
        # add background
        pic_top = Image.open('res/netease_cloud_music_style2_top.png')
        pic_right = Image.open('res/netease_cloud_music_style2_right.png')

        for x in range(int(math.ceil(w/pic_top.size[0]))):
            out_img.paste(pic_top, (x*pic_top.size[0]-15, 0))
        
        out_img.paste(pic_right, (w-pic_right.size[0], banner_height*2))

        # text
        draw.text((left_padding, banner_height + top_padding), 
                    lrc, font=lyric_font, fill=text_color, spacing=self.lrc_line_space)

        draw.text((w-left_padding-user_w, h-bottom_padding), user, font=user_font, 
                    fill=user_color, spacing=self.line_space)

        self.saveImg(title, filename, out_img)

    def save3(self, title, lrc, filename = None):
        """netease cloud music share pic: 古书"""
        user, song  = title.split('·')
        text_color = '#282528'
        user_color = '#000'
        
        top_padding = 45
        left_padding = 45
        bottom_padding = 200
        circle_h = 20

        user_font = ImageFont.truetype(self.font_family.split('.')[0]+'bd.ttc', self.user_font_size)
        lyric_font = ImageFont.truetype(self.font_family, self.lrc_font_size)

        lyric_w, lyric_h = ImageDraw.Draw(Image.new(mode='RGB', 
                            size=(1, 1))).textsize(song, font=lyric_font, spacing=self.line_space)

        user_w, user_h = ImageDraw.Draw(Image.new(mode='RGB', 
                            size=(1, 1))).textsize(user, font=user_font, spacing=self.line_space)

        lrc_rows = len(lrc.split('\n'))

        w = self.share_img_width - 400

        h = top_padding + user_h + circle_h + self.lrc_line_space*2 + top_padding + self.lrc_font_size * (1 + lrc_rows) + (lrc_rows - 1) * self.lrc_line_space +  bottom_padding

        out_img = Image.new(mode='RGB', size=(w, h), color='#fff')
        draw = ImageDraw.Draw(out_img)

        # circle
        draw.arc((left_padding, top_padding+user_h+self.lrc_line_space+circle_h, left_padding+circle_h, top_padding+user_h+self.lrc_line_space+circle_h*2),
                    -360, 0, fill = (213, 57, 50), width=7)

        # text
        draw.text((left_padding, top_padding), user, font=user_font, 
                    fill=user_color, spacing=self.line_space)

        draw.text((left_padding, top_padding+user_h+self.line_space*2+circle_h), song, font=lyric_font, 
                    fill=text_color, spacing=self.line_space)

        draw.text((left_padding, top_padding+user_h+self.line_space*2+circle_h+lyric_h+top_padding), 
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
        elif pic_style == 2:
            img.save1(user, text.replace('\\n', '\n'), out_img_name)
        elif pic_style == 3:
            img.save2(user, text.replace('\\n', '\n'), out_img_name)
        elif pic_style == 4:
            img.save3(user, text.replace('\\n', '\n'), out_img_name)
    else:
        print('input -h/--help option for help')


if __name__ == '__main__':
    main()