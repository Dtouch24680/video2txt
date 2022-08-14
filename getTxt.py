import cv2 as cv
import numpy as np


def down_sample(img, times):
    """
    将图片缩小一定倍数
    :param img 图片
    :param times 缩小倍数
    :return: 缩小后的图片
    """
    h, w = img.shape  # 注意不是 w, h
    h_new, w_new = int(h / (2 * times)), int(w / times)
    return cv.resize(img, (w_new, h_new))


def enhance_contrast(img):
    """
    用线性增强提高图片的对比度
    :param img: 图片
    :return: 增强后的结果
    """
    i_max = np.max(img)
    i_min = np.min(img)
    if i_max == i_min:
        # 返回原图
        return img.astype(np.uint8)
    o_min, o_max = 0, 255
    a = float(o_max - o_min) / (i_max - i_min)
    b = o_min - a * i_min
    enhanced_img = a * img + b
    return enhanced_img.astype(np.uint8)


def to_txt(img, mapping_str, times):
    """
    将图像转换成文字信息，每个字符串为一行
    :param img: 图片
    :param mapping_str: 用于与色阶相映射的字符
    :param times: 缩小的倍数
    :return: 所有的字符数组
    """
    img = down_sample(img, times)
    img = enhance_contrast(img)
    res_strs = []
    # 每个区间的宽度
    section_w = 256 / len(mapping_str)
    for line in img:
        line_str = ''
        for ele in line:
            line_str += mapping_str[int(ele / section_w)]
        res_strs.append(line_str)
    return res_strs
