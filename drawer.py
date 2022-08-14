from PIL import Image, ImageFont, ImageDraw


def draw(strs, size):
    """
    在一页空白图片上画上strs所示的文字
    :param strs: 文字
    :param size: 尺寸
    :return: 得到的图片
    """
    font = ImageFont.truetype('assets/font/DEJAVUSANSMONO_0.TTF', 12)
    step_h = 14
    w, h = 2, 0
    img = Image.new("RGB", size, (255, 255, 255))
    img_w, img_h = size
    im_draw = ImageDraw.Draw(img)
    for s in strs:
        im_draw.text((w, h), s, font=font, fill='#000000')
        h += step_h
        if h > img_h:
            break
    return img
