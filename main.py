from core.gold_experience_requiem import SutandoPowah
from utils.gif_tools import GifTools

if __name__ == '__main__':
    # Notice : if you use show_gif function, you need to press "blank key" to leave windows
    # 注意 : 如果您使用show_gif功能，您需要按“空白鍵”離開視窗
    # Example GIF
    example_shape = (1000, 1000)

    # 1. SutandoPowah.gold_experience_requiem；黃金體驗鎮魂曲風格gif
    gif_list = SutandoPowah.gold_experience_requiem(img_shape=(1000, 1200))
    GifTools.show_gif_with_pil_list(gif_list, frame_rate=30)
    # gif_list[0].save("./test.gif", save_all=True, append_images=gif_list[1:], loop=0, duration=50, disposal=0)
