from cj_func import cv_imread
import cv2
from skimage.metrics import structural_similarity as ssim


def get_ssim(img_path1, img_path2, k1=1, k2=1):
    image1 = cv_imread(img_path1, 0)  # 转为灰度图像
    image2 = cv_imread(img_path2, 0)

    # 获取两张图像的最小尺寸
    min_width = min(image1.shape[1], image2.shape[1])
    min_height = min(image1.shape[0], image2.shape[0])

    # 调整图像尺寸
    image1_resized = cv2.resize(image1, (min_width, min_height))
    image2_resized = cv2.resize(image2, (min_width, min_height))

    # 计算结构相似性指数，只考虑结构
    similarity = ssim(image1_resized, image2_resized, data_range=image2_resized.max() - image2_resized.min(), K1=k1,
                      K2=k2)

    print("Structural Similarity Index (Structure Only) after Alignment:", similarity)
    return similarity


if __name__ == '__main__':
    get_ssim(
        r"D:\LCJ\img_data\智能处理测试\精校消融实验\导出\rsift_sac1_filter\regis_GF1B.tif",
        r"D:\LCJ\img_data\智能处理测试\精校消融实验\导出\rsift_sac1_filter\regis_GF1.tif",
    )

    get_ssim(
        r"D:\LCJ\img_data\智能处理测试\精校消融实验\导出\rsift_sac1_nofilter\regis_GF1.tif",
        r"D:\LCJ\img_data\智能处理测试\精校消融实验\导出\rsift_sac1_nofilter\regis_GF1B.tif",
    )