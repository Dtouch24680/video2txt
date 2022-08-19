import cv2
import numpy as np
import time
import os

import drawer
import getTxt
import cv2 as cv
import argparse


def arg_parse():
    parser = argparse.ArgumentParser(
        usage="python %(prog)s [参数名] [参数值]"
    )
    parser.add_argument(
        "--input", help="输入的视频或图片文件路径", required=True, type=str
    )
    parser.add_argument(
        "--output_dir", help="输出目录", default='./output', type=str
    )
    parser.add_argument(
        "--name", help="输出文件名", default='output.' + str(int(time.time())), type=str
    )
    parser.add_argument(
        "--mp4", help="是否输出MP4格式文件，仅在--pic参数为false时有效（默认avi）", action='store_true', default=False
    )
    parser.add_argument(
        "--times", help="视频转字符块分辨率下降的倍数，建议不小于4。该数值越小，处理越慢。（默认为6）", default=8, type=int
    )
    parser.add_argument(
        "--keep_audio", help="是否需要保留音频（默认保留）", action='store_true', default=True
    )
    parser.add_argument(
        "--pic", help="是否处理图片（要求--input参数指向一张图片。默认为否，表示处理文本）", action='store_true', default=False
    )
    parser.add_argument(
        "--mapping_str", help="与灰阶相映射的字符集，不建议改动，不支持中文字符", default='MN#HQ$OC?&>!:-. ', type=str
    )
    options, _ = parser.parse_known_args()  # _ 用于接受命令行中未定义的参数，不做处理
    return options


# 命令行参数构成的对象
opt = arg_parse()


def generate_video():
    video = cv.VideoCapture(opt.input)
    # 分辨率降低的倍数
    times = opt.times
    # 获取帧的宽高
    w, h = int(video.get(cv.CAP_PROP_FRAME_WIDTH)), int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    print('视频长' + str(w), '，宽' + str(h))
    # 获取原视频帧率
    fps = video.get(cv.CAP_PROP_FPS)
    # 获取帧数
    frame_count = video.get(cv.CAP_PROP_FRAME_COUNT)
    # 文字图片集合
    img_set = []
    cnt = 0

    # while video.isOpened():
    #     # 获取每一帧
    #     cnt += 1
    #     ret, frame = video.read()
    #     if ret:
    #     if cnt % 10 == 0:
    #         cv.imwrite(str(cnt) + '.jpg', frame)
    #
    # video.release()
    # return

    while video.isOpened():
        # 获取每一帧
        cnt += 1
        ret, frame = video.read()

        # if cnt == 1:
        #     cv.imwrite('origin.jpg', frame)
        #     frame = cv.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     cv.imwrite('plain.jpg', frame)
        #     frame_enhanced = getTxt.enhance_contrast(frame)
        #     cv.imwrite('enhance.jpg', frame_enhanced)
        #
        #     h, w = frame.shape  # 注意不是 w, h
        #     h_new, w_new = int(h / times), int(w / times)
        #
        #     frame_small = cv.resize(frame, (w_new, h_new))
        #     cv.imwrite('small.jpg', frame_small)
        #     frame_smaller = getTxt.down_sample(frame, times)
        #     cv.imwrite('smaller.jpg', frame_smaller)
        #     frame_txt = drawer.draw(getTxt.to_txt(frame, opt.mapping_str, times), (int(7 * w / times), int(7 * h / times)))
        #     cv.imwrite('txt.jpg', np.asarray(frame_txt))
        #
        #     frame_small_enhance = cv.resize(frame_enhanced, (w_new, h_new))
        #     cv.imwrite('small_enhance.jpg', frame_small_enhance)
        #     frame_smaller_enhance = getTxt.down_sample(frame_enhanced, times)
        #     cv.imwrite('smaller_enhance.jpg', frame_smaller_enhance)
        #     frame_txt_enhance = drawer.draw(getTxt.to_txt(frame_enhanced, opt.mapping_str, times), (int(7 * w / times), int(7 * h / times)))
        #     cv.imwrite('txt_enhance.jpg', np.asarray(frame_txt))
        #     video.release()
        #     return

        if ret:
            if cnt == 1:
                print('视频读取成功，正在处理...')
            # 将帧转为单通道图像
            frame = cv.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 获得该帧图像的txt文本
            strs = getTxt.to_txt(frame, opt.mapping_str, times)
            # 7也许可以通过精确计算得出，但这里我是调参得到的（随便尝试了几个整数）
            txt_frame = drawer.draw(strs, (int(7 * w / times), int(7 * h / times)))
            # Image类型需要转为一般数组
            img_set.append(np.asarray(txt_frame))

        else:
            break

        if cnt % 30 == 0:
            print('已处理' + str(cnt) + '/' + str(int(frame_count)) + '帧')

    # 图片合成视频
    print('正在合并图片...')

    output_dir = opt.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if opt.mp4:
        suffix = '.mp4'
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    else:
        suffix = '.avi'
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    nh, nw, _ = img_set[0].shape  # 注意这里的shape有三个维度，不是单通道
    full_name = os.path.join(output_dir, opt.name + suffix)
    res_video = cv2.VideoWriter(
        full_name,
        fourcc,
        int(fps + 0.5),  # 四舍五入转整
        (nw, nh)
    )

    for res_img in img_set:
        res_video.write(res_img)

    video.release()
    res_video.release()
    print("转换成功！视频保存为：" + full_name)


def generate_pic():
    # 读取单通道
    img = cv.imread(opt.input, 0)
    # 获得对应字符串集合
    strs = getTxt.to_txt(img, opt.mapping_str, opt.times)
    times = opt.times
    h, w = img.shape
    # 字符串写入新图片
    txt_img = np.asarray(drawer.draw(strs, (int(7 * w / times), int(7 * h / times))))
    output_dir = opt.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    full_name = os.path.join(output_dir, opt.name + '.jpg')
    cv.imwrite(full_name, txt_img)
    print("转换成功！图片保存为：" + full_name)


if __name__ == '__main__':
    if not opt.pic:
        generate_video()
    else:
        generate_pic()
