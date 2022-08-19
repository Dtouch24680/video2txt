# video2txt
Render video as text using python

---
## Quick start
### 1. 下载源程序
git clone或下载zip压缩包解压，进入项目目录video2txt/
### 2. 环境配置（python3）
运行
```shell
pip install -r requirements.txt
```
直接安装依赖包：
+ opencv-python
+ numpy
+ pillow

若已有上述依赖则跳过
### 3. 输入
在assets文件夹下放入原始视频或图片文件(如demo.mp4)，文件名尽量不使用中文
### 4. 运行
直接运行：
```shell
python main.py --input './assets/demo.mp4' --times 10
```
查看参数详情：
```shell
python main.py --help
```
### 5. 输出
默认在output文件夹中