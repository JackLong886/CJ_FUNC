import cv2
import numpy as np
import os
from osgeo import gdal, osr
import math


class IMAGE3:
    def __init__(self, filenameOrDs, read_type=gdal.GA_ReadOnly, is_print=False):
        self.output_dataset = None
        self.copy_dataset = None
        self.dataset = None
        self.read_type = read_type
        self.bit_depth = None
        self.statis = None
        self.in_file = None
        if isinstance(filenameOrDs, gdal.Dataset):
            self.dataset = filenameOrDs
        elif os.path.isfile(filenameOrDs):
            self.in_file = filenameOrDs
            self.dataset = gdal.Open(self.in_file, read_type)  # 打开文件
        else:
            raise KeyError('无法通过 {} 初始化IMAGE'.format(filenameOrDs))
        self.im_width = self.dataset.RasterXSize  # 栅格矩阵的列数
        self.im_height = self.dataset.RasterYSize  # 栅格矩阵的行数
        self.im_bands = self.dataset.RasterCount  # 波段数
        self.im_geotrans = self.dataset.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
        self.im_proj = self.dataset.GetProjection()  # 地图投影信息，字符串表示
        self.im_resx, self.im_resy = self.im_geotrans[1], self.im_geotrans[5]
        if is_print:
            print("in_file:{}".format(self.in_file))
            print("res_x:{}, res_y:{}".format(self.im_resx, self.im_resy))
            print("width:{}, height:{}, bands:{}".format(self.im_width, self.im_height, self.im_bands))
            print("im_geotrans:{}".format(self.im_geotrans))
            print("im_proj:{}".format(self.im_proj))

    def get_extent(self, extent=None, bands=None):
        if extent is None:
            x, y, s_size, y_size = 0, 0, self.im_width, self.im_height
        else:
            x, y, s_size, y_size = extent

        if not bands or bands == self.im_bands:
            return self.dataset.ReadAsArray(x, y, s_size, y_size)
        else:
            return self.dataset.ReadAsArray(x, y, s_size, y_size)[0:bands, :, :]

    def write2self_img(self, extent=None, im_data=None):
        assert self.read_type == gdal.GA_Update
        for i in range(self.im_bands):
            self.dataset.GetRasterBand(i + 1).WriteArray(im_data[i], xoff=extent[0], yoff=extent[1])
        self.dataset.FlushCache()

    def create_img(self, filename, out_bands=None, im_width=None, im_height=None,
                   im_proj=None, im_geotrans=None, datatype=None, block_size=(256, 256)):
        self.output_file = filename
        # 创建文件
        driver = gdal.GetDriverByName(self.get_frmt(filename))
        options = ['TILED=YES', 'BLOCKXSIZE={}'.format(block_size[0]), 'BLOCKYSIZE={}'.format(block_size[1])]
        if not datatype:
            datatype = self.dataset.GetRasterBand(1).DataType

        self.out_bands = self.im_bands if not out_bands else out_bands
        if im_width and im_height:
            self.output_dataset = driver.Create(filename, im_width, im_height, self.out_bands, datatype,
                                                options=options)
        else:
            self.output_dataset = driver.Create(filename, self.im_width, self.im_height, self.out_bands, datatype,
                                                options=options)
        if im_geotrans:
            self.output_dataset.SetGeoTransform(im_geotrans)
        else:
            self.output_dataset.SetGeoTransform(self.im_geotrans)  # 写入仿射变换参数
        if im_proj:
            self.output_dataset.SetProjection(im_proj)
        else:
            self.output_dataset.SetProjection(self.im_proj)  # 写入投影
        driver = None

    def write_extent(self, extent=None, im_data=None):
        if im_data is None: return 0
        (x, y, s_size, y_size) = extent if extent else (0, 0, self.im_width, self.im_height)
        if self.out_bands == 1:
            self.output_dataset.GetRasterBand(1).WriteArray(im_data, xoff=x, yoff=y)  # 写入数组数据
        else:
            for i in range(self.out_bands):
                self.output_dataset.GetRasterBand(i + 1).WriteArray(im_data[i], xoff=x, yoff=y)
        self.output_dataset.FlushCache()

    def compute_statistics(self, if_print=False, approx_ok=True):
        # min max mean std
        statis = []
        for i in range(self.im_bands):
            s = self.dataset.GetRasterBand(i + 1).ComputeStatistics(approx_ok)
            statis.append(s)
        if if_print:
            for i in range(len(statis)):
                print("min:{}, max:{}, mean:{}, std:{}".format(*statis[i]), flush=True)
        self.statis = statis
        return statis

    def gen_extents(self, x_winsize, y_winsize, win_std=None):
        if win_std is None:
            win_std = [x_winsize, y_winsize]
        frame = []
        x = 0
        y = 0
        while y < self.im_height:  # 高度方向滑窗
            if y + y_winsize >= self.im_height:
                y_left = self.im_height - y_winsize
                y_right = y_winsize
                y_end = True
            else:
                y_left = y
                y_right = y_winsize
                y_end = False

            while x < self.im_width:  # 宽度方向滑窗
                if x + x_winsize >= self.im_width:
                    x_left = self.im_width - x_winsize
                    x_right = x_winsize
                    x_end = True
                else:
                    x_left = x
                    x_right = x_winsize
                    x_end = False
                frame.append((x_left, y_left, x_right, y_right))
                x += win_std[0]
                if x_end:
                    break
            y += win_std[1]
            x = 0
            if y_end:
                break
        return frame

    def __del__(self):
        self.dataset = None
        self.copy_dataset = None
        self.output_dataset = None

    def copy_image(self, filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.copy_image_file = filename
        # 同类型间拷贝最快
        if not self.in_file:
            gdal.Translate(self.copy_image_file, self.dataset, format=self.get_frmt(self.copy_image_file))
        else:
            if os.path.splitext(os.path.basename(self.copy_image_file))[1] == \
                    os.path.splitext(os.path.basename(self.in_file))[1]:
                gdal.GetDriverByName(self.get_frmt(self.copy_image_file)).CopyFiles(self.copy_image_file, self.in_file)
            else:
                gdal.Translate(self.copy_image_file, self.in_file, format=self.get_frmt(self.copy_image_file))
        self.copy_dataset = gdal.Open(self.copy_image_file, gdal.GA_Update)
        if self.copy_dataset:
            os.chmod(self.copy_image_file, 0o755)  # 设置目标文件的权限
            print("文件复制成功！")
        else:
            raise KeyError("文件复制失败:{}".format(filename))

    def write2copy_image(self, extent, im_data):
        x, y, s_size, y_size = extent
        bands = self.copy_dataset.RasterCount
        if bands == 1:
            self.copy_dataset.GetRasterBand(1).WriteArray(im_data, xoff=x, yoff=y)  # 写入数组数据
        else:
            for i in range(bands):
                self.copy_dataset.GetRasterBand(i + 1).WriteArray(im_data[i], xoff=x, yoff=y)

    def get_4_extent(self, dataset=None):
        if not dataset:
            # 计算影像的四至范围
            x_min = self.im_geotrans[0]
            y_max = self.im_geotrans[3]
            x_max = x_min + self.im_geotrans[1] * self.im_width
            y_min = y_max + self.im_geotrans[5] * self.im_height
        else:
            # 获取影像的地理转换
            geotransform = dataset.GetGeoTransform()
            # 获取影像的宽度和高度
            width = dataset.RasterXSize
            height = dataset.RasterYSize
            # 计算影像的四至范围
            x_min = geotransform[0]
            y_max = geotransform[3]
            x_max = x_min + geotransform[1] * width
            y_min = y_max + geotransform[5] * height
        return x_min, y_min, x_max, y_max

    def get_frmt(self, img_path):
        self.suffix = os.path.splitext(os.path.basename(img_path))[1]
        if self.suffix in ['.tif', '.TIF', '.tiff', '.TIFF']:
            self.frmt = 'GTiff'
        elif self.suffix in ['.img', '.IMG']:
            self.frmt = 'HFA'
        elif self.suffix in ['.vrt', '.VRT']:
            self.frmt = 'VRT'
        else:
            raise KeyError('{}不是支持的文件格式'.format(self.suffix))
        return self.frmt

    def is_projected(self):
        proj_srs = osr.SpatialReference()
        proj_srs.ImportFromWkt(self.im_proj)
        return proj_srs.IsProjected()


def cv_imread(file_path, read_type=-1):
    """解决无法读取中文路径的问题"""
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), read_type)
    return cv_img
