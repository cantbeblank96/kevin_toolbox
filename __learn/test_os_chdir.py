# 问题：在使用 os.chdir 改变工作路径后，离开该作用域，工作路径是否会恢复到原始状态?
import os


def change_path(func=None):
    print(f"now in {os.getcwd()}")
    os.chdir("..")
    print(f"change to {os.getcwd()}")
    if func is not None:
        func()
    print(f"end in {os.getcwd()}")


if __name__ == '__main__':
    change_path(change_path)
    # now in / home / SENSETIME / xukaiming / Desktop / gitlab_repos / chunked_version_of_misc_module / __learn
    # change
    # to / home / SENSETIME / xukaiming / Desktop / gitlab_repos / chunked_version_of_misc_module
    # now in / home / SENSETIME / xukaiming / Desktop / gitlab_repos / chunked_version_of_misc_module
    # change
    # to / home / SENSETIME / xukaiming / Desktop / gitlab_repos
    # end in / home / SENSETIME / xukaiming / Desktop / gitlab_repos
    # end in / home / SENSETIME / xukaiming / Desktop / gitlab_repos
    # end in / home / SENSETIME / xukaiming / Desktop / gitlab_repos

    "结论：确实不会恢复到原始状态"
