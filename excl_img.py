# 如果希望图片名称直接使用URL的最后部分作为文件名（即去掉协议、域名和路径，仅保留URL末尾的部分），可以使用
# urlparse
# 模块来实现。以下是对上述代码进行相应修改后的版本：
import os
import pandas as pd
from urllib.parse import urlparse
import requests
from io import BytesIO

# 读取Excel文件（假设链接在第一列）
excel_file = '1111.xlsx'
df = pd.read_excel(excel_file, header=None)

# 图片保存的目标文件夹路径设为当前目录下的'img'文件夹
image_folder = os.path.join(os.getcwd(), 'img')

# 判断目标文件夹是否存在，如果不存在则创建
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

failed_links = []
total_failed = 0
total_success = 0
total_count = len(df.index)
current_count = 1

# 遍历每一行数据，假设链接在第一列（索引为0）
for index, row in df.iterrows():
    # 获取图片链接
    image_url = row[0]

    # 解析URL以获取文件名
    parsed_url = urlparse(image_url)
    image_name = os.path.basename(parsed_url.path) or "image.jpg"  # 若URL没有路径，则默认为'image.jpg'

    # 下载图片
    response = requests.get(image_url)

    if response.status_code == 200:
        # 创建图片完整保存路径
        image_path = os.path.join(image_folder, image_name)

        # 将图片内容写入文件
        with open(image_path, 'wb') as f:
            f.write(response.content)

        total_success += 1
        print(f'({current_count}/{total_count}) 图片下载成功并保存为：{image_name}')
        current_count += 1
    else:
        total_failed += 1
        failed_links.append((index, image_url))
        print(f'({current_count}/{total_count}) 无法从{image_url}下载图片，状态码：{response.status_code}')
        current_count += 1

print(f'\n所有图片下载完毕。\n共{total_success}条链接下载成功，{total_failed}条链接下载失败。')

# 输出失败的链接列表
if total_failed > 0:
    print("\n失败的链接如下：")
    for idx, link in failed_links:
        print(f"行号: {idx}, 链接: {link}")

# 这段代码会根据URL的最后一部分来命名下载的图片，并且在输出日志时显示下载进度信息和失败链接列表。如果URL中没有明确的文件名部分，它将默认使用
# image.jpg
# 作为文件名。