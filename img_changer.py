import os
import traceback
from reportlab.pdfgen import canvas
from PIL import Image

class ImgChanger:
    def __init__(self):
        pass

    def get_image_size(self,image_name):
        img = Image.open(image_name)
        return img.size


    def convert_img_to_pdf(self,image_name, target_name):

        img = Image.open(image_name)
        image_width, image_height = img.size
        c = canvas.Canvas(target_name, pagesize=(image_width, image_height))
        c.drawImage(image_name, 0, 0, image_width, image_height)
        c.showPage()
        c.save()


    def convert_imgs_to_pdfs(self,default_dir, target_dir):

        for line in os.listdir(default_dir):
            image_abs_path = os.path.join(default_dir, line)
            if '.' in line:
                file_name, flag = line.rsplit('.')
                if flag in ('jpg', 'bmp', 'png'):
                    target_file_name = file_name + '.pdf'
                    target_file_abs_path = os.path.join(
                        target_dir, target_file_name)
                    self.convert_img_to_pdf(image_name=image_abs_path,
                                       target_name=target_file_abs_path)

    def convert_imgs_to_one_pdf(self,default_dir, target_file_name, flag = 'jpg',image_name_is_num=False):

        if not os.path.exists(target_file_name):
            assert flag in ('jpg','bmp','png'),'图片后缀必须为以下一种：jpg,bmp,png'

            # flag 图片后缀格式
            image_data = {}
            pdf_width = 0
            pdf_height = 0
            x = 0   # 图片放在画布中的横坐标
            y = 0   # 图片放在画布中的纵坐标

            for line in os.listdir(default_dir):
                if '.' in line:
                    head, tail = line.rsplit('.',1)

                    if image_name_is_num == True:
                        # 加一个断言来实现数字排序，如果平时转换图片，则不需要这个断言
                        # 图片名必须是数字
                        assert file_name.isdigit() == True, '图片名必须是数字，{} 不符合规范。'.format(line)

                    if tail == flag:
                        image_abs_path = os.path.join(default_dir, line)
                        size = self.get_image_size(image_abs_path)

                        width, height = size
                        if width > pdf_width:
                            pdf_width = width
                        if height > pdf_height:
                            pdf_height = height

                        image_data[line] = {}
                        image_data[line]['abs_path'] = image_abs_path
                        image_data[line]['size'] = size

            c = canvas.Canvas(filename=target_file_name,
                              pagesize=(pdf_width, pdf_height))

            image_name_list = image_data.keys()
            sorted_tmp = sorted([line.rsplit('.', 1)[0] for line in image_name_list], key=int)
            sorted_image_name_list = [line + '.{}'.format(flag) for line in sorted_tmp]
            for line in sorted_image_name_list:
                image_abs_path = image_data[line]['abs_path']
                w, h = image_data[line]['size']
                x = (pdf_width - w) / 2
                y = (pdf_height - h) / 2
                c.drawImage(image_abs_path, x, y, w, h)
                c.showPage()
            c.save()
        else:
            pass

if __name__ == '__main__':
    i = ImgChanger()
