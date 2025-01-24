import os, shutil
import time

"""
将照片按时间分割为各个文件夹
"""


# 获取path目录带指定后缀的文件的路径
def search_file(path, suffix_ls):
    "return all file_path with specific suffix in path，suffix_ls 后缀列表"
    dir_ls = os.listdir(path)  # 获取path目录下所有文件
    file_ls = []
    dict_ = []
    for dir_ in dir_ls:
        pathTmp = os.path.join(path, dir_)
        if os.path.isdir(pathTmp):  # 如是目录,则递归查找
            dict_ += search_file(pathTmp, suffix_ls)
        else:  # 不是目录,则比较后缀名
            suffix = os.path.splitext(dir_)[1]
            if suffix in suffix_ls:
                file_ls.append(dir_)
    return [{"path": path, "filename_ls": file_ls}] + dict_


# 获取文件的时间,返回time.struct_time格式
get_FileCreateTime = lambda filePath: time.localtime(max(os.path.getctime(filePath), 0))
get_FileAccessTime = lambda filePath: time.localtime(max(os.path.getatime(filePath), 0))
get_FileModifyTime = lambda filePath: time.localtime(max(os.path.getmtime(filePath), 0))


class dir_ls():

    def __init__(s, dir_=[]):
        s.dir_ls = dir_

    def touch(s, dir_):
        if dir_ in s.dir_ls:
            return True
        elif not os.path.isdir(dir_):
            os.mkdir(dir_)
            s.dir_ls.append(dir_)


def main():
    suffix_ls = ['.MP4', '.jpg', '.mp4', '.png', '.JPG', '.MOV', '.CR2']
    rule = "%Y_%m_%d"  # "%Y-%m-%d %H:%M:%S" 2016-03-20 11:45:39 #"%a %b"  Sat Mar
    root_path = input("please input the root path\n")
    target_path = input("please input the target_path\n")
    c_m_a = input("分类标准：m for modifytime \n c for createtime\n a for accesstime\n")
    if c_m_a == 'm':
        get_c_m_a_Time = get_FileModifyTime
    elif c_m_a == 'a':
        get_c_m_a_Time = get_FileAccessTime
    elif c_m_a == 'c':
        get_c_m_a_Time = get_FileCreateTime
    fileList = search_file(root_path, suffix_ls)
    print(fileList)
    copy_path_root = os.path.join(target_path, \
                                  'deal' + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())))
    os.mkdir(copy_path_root)  # 创建复制根文件夹
    root_cwd = os.getcwd()
    dir_ls_ins = dir_ls()
    for folder in fileList:
        os.chdir(folder["path"])
        for file in folder["filename_ls"]:
            c_m_a_time = get_c_m_a_Time(file)

            copy_path_y = os.path.join(copy_path_root, \
                                       str(c_m_a_time.tm_year))
            dir_ls_ins.touch(copy_path_y)  # 创建year文件夹
            copy_path_m_d = os.path.join(copy_path_y, \
                                         str(time.strftime(rule, c_m_a_time)))
            dir_ls_ins.touch(copy_path_m_d)  # 创建month_day文件夹
            print(os.getcwd())
            shutil.copy2(file, copy_path_m_d)  # 复制文件到新路径
    ##            shutil.move(file,copy_path_m_d)          #移动文件（不建议）
    os.chdir(root_cwd)


if __name__ == "__main__":
    main()
