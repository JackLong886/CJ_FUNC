# 自动调整滑窗大小， 用于图像匹配
def adjust_winsize(res_img, res_baseimg, img_size, winsize_min=256, opt_blocksize=256):
    if img_size < 15000:
        winsize_img = winsize_min
    elif img_size < 30000:
        winsize_img = winsize_min * 2
    else:
        winsize_img = winsize_min * 4

    winsize_img = max(winsize_min, winsize_img)
    winsize_base = int(winsize_img * res_img / res_baseimg)

    if winsize_img < winsize_min:
        winsize_base = int(winsize_min * res_img / res_baseimg)
        winsize_img = winsize_base * res_baseimg / res_img
        winsize_img = int(winsize_img * 1. / opt_blocksize + 1) * opt_blocksize
        # winsize_base = int(winsize_img * res_img / res_baseimg)

    if winsize_base < winsize_min:
        winsize_img = winsize_min * res_baseimg / res_img
        winsize_img = int(winsize_img * 1. / opt_blocksize + 1) * opt_blocksize
        # winsize_base = int(winsize_img * res_img / res_baseimg)
    return winsize_img


if __name__ == '__main__':
    winsize_img, winsize_base = adjust_winsize(2, 2, 50000)
    print(winsize_img, winsize_base)
