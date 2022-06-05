import numpy as np
import random
from utils.gif_tools import GifTools
from utils.move_text_by_vector import MoveTextByVector
from PIL import Image


class SutandoPowah:
    @staticmethod
    def gold_experience_requiem(img_shape=(1280, 720), gif_sec=1):
        """
        安妮雅鎮魂曲!，類似黃金鎮魂曲的移動複製效果
        :param img_shape: 輸出的GIF圖像大小
        :param gif_sec:生成GIF的秒數
        :return:
        """
        width, height = img_shape
        gif_img_shape = (height, width, 3)
        gif_list = GifTools.generate_frame(gif_img_shape, frame=60, gif_sec=gif_sec, background=(255, 255, 255),
                                           alpha_channel=True, alpha_value=0)  # 生成gif底圖

        img_path1 = r"./database/anya_suki_anya_small.png"  # 提取指定資料夾的圖片  # 主程式要調用時請用這行
        img_path2 = r"./database/diablo.png"
        # img_path1 = r"../database/anya_suki_anya_small.png"  # 提取指定資料夾的圖片  # generate_dvd_bounce_gif要用時調用這行!!!
        # img_path2 = r"../database/diablo.png"
        # 初始參數設定
        # 建議匯入的圖片需要二值化，避免疊圖時產生雜訊
        img1 = Image.open(img_path1).convert("RGBA")  # 以PIL開啟讀取並操作透明度
        img2 = Image.open(img_path2).convert("RGBA")
        width, height = img2.size  # 讀出尺寸大小
        img2 = img2.resize((width//2, height//2))  # resize一半
        location1 = (0, 300)  # 起始位置
        location2 = (50, 0)
        # 生成隨機向量(暫時固定，可自行設定)
        vector = (random.randint(25, 25), random.randint(25, 25))

        new_gif_list = []  # 紀錄新生成的圖片清單
        location_list1 = []  # 紀錄座標
        location_list2 = []
        for frame in gif_list:  # 在每幀間繪圖
            # 可以開啟反彈，會很鬧==
            location1, vector = MoveTextByVector.vector_setting(np.uint8(frame), start_point=location1, vector=vector,
                                                                paste_img=np.uint8(img1), bounce_setting=False)
            location2, vector = MoveTextByVector.vector_setting(np.uint8(frame), start_point=location2, vector=vector,
                                                                paste_img=np.uint8(img2), bounce_setting=False)
            new_frame = Image.fromarray(frame, mode="RGBA")  # 將底圖轉換為PIL格式
            location_list1.append(location1)  # 紀錄每次繪圖的座標，畫新的圖的時候就依序在畫上去，如此便有疊加的效果了
            location_list2.append(location2)
            for loc in location_list2:
                new_frame.paste(img2, loc, img2)  # 已去背圖片(img)，貼上指定位置(loc)，遮罩(mask)為自己
            for loc in location_list1:
                new_frame.paste(img1, loc, img1)  # 已去背圖片(img)，貼上指定位置(loc)，遮罩(mask)為自己

            new_gif_list.append(new_frame)
        return new_gif_list


if __name__ == '__main__':
    _gif_list = SutandoPowah.gold_experience_requiem(img_shape=(1000, 1200))
    GifTools.show_gif_with_pil_list(_gif_list, frame_rate=30)
    # 回傳出PIL的清單，便可以直接儲存了
    # _gif_list[0].save("./test.gif", save_all=True, append_images=_gif_list[1:], loop=0, duration=50, disposal=0)
