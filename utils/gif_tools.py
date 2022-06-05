import numpy as np
import cv2
import os
from PIL import Image
from PIL import ImageSequence
import moviepy.editor as mp


class GifTools:
    @staticmethod
    def generate_frame(img_shape, frame, gif_sec, background=(0, 0, 0), alpha_channel=False, alpha_value=255):
        """
        生成gif圖像的單張圖片，指定圖像尺寸大小、幀數、秒數
        :param img_shape: 欲生成的圖像大小
        :param frame: 幀數
        :param gif_sec: 秒數
        :param background: 背景顏色
        :param alpha_channel: 是否新增透明度通道
        :param alpha_value: 透明度通道底值；建議值0,255
        設為0代表圖層全通透，若用在gif上會看到前一張圖片的痕跡!請注意
        設為255代表圖層基底全遮蔽，便不會看到前一張圖片的痕跡
        :return: 單張圖片清單
        """
        # frame*sec等於gif圖所需的所有張數，後許可使用1 sec. N frame來讀取
        gif_list = []
        for i in range(frame * gif_sec):  # 生成所有幀
            mask = np.full(img_shape, background, dtype=np.uint8)  # 生成蒙版
            if alpha_channel:
                alpha_img = np.full(img_shape[:2], alpha_value, dtype=np.uint8)
                mask = cv2.merge([mask, alpha_img])
            gif_list.append(mask)
        return gif_list

    @staticmethod
    def show_gif(gif_list, frame_rate=30):
        """
        讀取cv2連續圖片清單，並展示gif圖像，按空白鍵關閉視窗
        :param gif_list:cv2連續圖片清單
        :param frame_rate:幀數，每秒顯示多少張圖片，預設為30幀
        :return: None
        """
        # 將幀數換算成每張圖像間隔時間，公式 = 1秒//幀數 = 1000毫秒//幀數
        interval_sec = 1000 // frame_rate
        loop = True  # 設定 loop 為 True
        while loop:
            for i in gif_list:
                cv2.imshow('show gif press blank key leave windows', i)  # 不斷讀取並顯示串列中的圖片內容
                if cv2.waitKey(interval_sec) == ord(" "):
                    loop = False  # 停止時同時也將 while 迴圈停止
                    break
        cv2.destroyAllWindows()

    @staticmethod
    def show_gif_with_pil_list(gif_list, frame_rate=30):
        """
        讀取pil連續圖片清單，並展示gif圖像，按空白鍵關閉視窗
        :param gif_list:cv2連續圖片清單
        :param frame_rate:幀數，每秒顯示多少張圖片，預設為30幀
        :return: 回傳轉換成cv2的圖片清單，看要不要用，不強制，因為直接使用pil儲存也可以
        """
        # 將幀數換算成每張圖像間隔時間，公式 = 1秒//幀數 = 1000毫秒//幀數
        interval_sec = 1000 // frame_rate
        cv2_gif_list = []
        for frame in gif_list:  # 先過檔一次，將PIL圖片清單轉成cv2清單
            frame = np.uint8(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGRA)  # 顏色從 RGBA 轉換為 BGRA
            cv2_gif_list.append(frame)

        loop = True  # 設定 loop 為 True
        while loop:
            for frame in cv2_gif_list:
                cv2.imshow('show gif press blank key leave windows', frame)  # 不斷讀取並顯示串列中的圖片內容
                if cv2.waitKey(interval_sec) == ord(" "):
                    loop = False  # 停止時同時也將 while 迴圈停止
                    break
        cv2.destroyAllWindows()
        return cv2_gif_list

    @staticmethod
    def cv2_img_list_save_gif(gif_list, save_file_name, frame_rate=30):
        """
        將cv2的圖片清單儲存成gif檔案，儲存幀率最高限制為50幀
        :param gif_list: cv2圖片清單
        :param save_file_name: 儲存檔名
        :param frame_rate: 每秒顯示多少幀(多少張數圖片)
        :return: 回傳檔案路徑 final_path
        """
        folder_dir = "./data"  # 儲存的資料夾
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        final_path = os.path.join(folder_dir, save_file_name)  # 最終檔案儲存路徑
        output = []
        interval_sec = 1000 // frame_rate
        for img in gif_list:
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 轉換成 PIL 格式(同時BGR轉RGB讓顯色與cv2呈現出來相同)
            output.append(img)  # 加入 output
        # duration 將每幀的顯示時間設置為duration以毫秒為單位。如果值太小，將被忽略。
        # duration 最小值只能設到20，等於幀數最高設置為50，若超過該限制，會變成預設間隔時間為100
        output[0].save(final_path, save_all=True, append_images=output[1:], loop=0, duration=interval_sec, disposal=0)
        return final_path

    @staticmethod
    def read_and_show_gif(path, frame_rate=30):
        """
        讀取gif檔案，並展示gif圖像，按空白鍵關閉視窗
        :param path:gif檔案路徑
        :param frame_rate:幀數，每秒顯示多少張圖片，預設為30幀
        :return:
        """
        interval_sec = 1000 // frame_rate
        gif = Image.open(path)
        img_list = []  # 建立儲存影格的空串列
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGBA')  # 轉換成 RGBA
            opencv_img = np.array(frame, dtype=np.uint8)  # 轉換成 numpy 陣列
            opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGBA2BGRA)  # 顏色從 RGBA 轉換為 BGRA
            img_list.append(opencv_img)  # 利用串列儲存該圖片資訊

        loop = True  # 設定 loop 為 True
        while loop:
            for i in img_list:
                cv2.imshow('show gif press blank key leave windows', i)  # 不斷讀取並顯示串列中的圖片內容
                if cv2.waitKey(interval_sec) == ord(" "):
                    loop = False  # 停止時同時也將 while 迴圈停止
                    break
        cv2.destroyAllWindows()

    @staticmethod
    def mp4_to_gif2(input_file):
        # moviepy將mp4轉gif
        clip_frame = mp.VideoFileClip(input_file)
        clip_frame.write_gif("output.gif")

    @staticmethod
    def gif_to_mp4(input_file):
        # moviepy將gif轉mp4
        clip_frame = mp.VideoFileClip(input_file)
        clip_frame.write_videofile("output.mp4")
