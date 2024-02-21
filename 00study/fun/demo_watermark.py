from blind_watermark import WaterMark

# 嵌入水印
# bwm1 = WaterMark(password_img=1, password_wm=1)
# bwm1.read_img('pic/ori_img.jpg')
# wm = ' test watermark 20240206'
# bwm1.read_wm(wm, mode='str')
# bwm1.embed('pic/embedded.png')
# len_wm = len(bwm1.wm_bit)
# print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm)) # 198

# 提取水印

bwm1 = WaterMark(password_img=1, password_wm=1)
len_wm = 198
wm_extract = bwm1.extract('pic/embedded.png', wm_shape=len_wm, mode='str')
print(wm_extract)  # test watermark 20240206


# text_blind_watermark