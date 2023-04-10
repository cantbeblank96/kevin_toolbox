import os
import time
import argparse
import shutil

"""
使用本脚本进行打包和发布

# 打包 正式版
python pack.py

# 打包 dev 版本
python pack.py  --mode dev --validity_period 7776000  # 有效期3个月

# 发布
twine upload dist/*
"""

out_parser = argparse.ArgumentParser(description='pack and dist')
out_parser.add_argument('--mode', type=str, required=False, default="formal")
out_parser.add_argument('--validity_period', type=int, required=False, default=2592000)  # 默认为一个月有效期，自打包之时算起
out_parser.add_argument('--verbose', type=bool, required=False, default=True)  # 默认为一个月有效期，自打包之时算起
args = out_parser.parse_args().__dict__
assert args["mode"] in ["dev", "formal"]

root_dir = os.path.abspath(os.path.split(__file__)[0])

if args["mode"] == "dev":
    # modify __init__.py
    shutil.copy(src=os.path.join(root_dir, "kevin_toolbox", "__init__.py"),
                dst=os.path.join(root_dir, "kevin_toolbox", "__init__.py.bak"))
    with open(os.path.join(root_dir, "kevin_toolbox", "__init__.py"), "a") as f:
        f.write(
            f'''
import os

os.system(
    f'python {{os.path.split(__file__)[0]}}/env_info/check_version_and_update.py '
    f'--package_name kevin-toolbox-dev '
    f'--cur_version {{__version__}} --verbose {args["verbose"]}'
)

os.system(
    f'python {{os.path.split(__file__)[0]}}/env_info/check_validity_and_uninstall.py '
    f'--package_name kevin-toolbox-dev '
    f'--expiration_timestamp {int(time.time() + args["validity_period"])} --verbose {args["verbose"]}'
)
'''
        )

    # modify setup.cfg
    shutil.copy(src=os.path.join(root_dir, "setup.cfg"), dst=os.path.join(root_dir, "setup.cfg.bak"))
    with open(os.path.join(root_dir, "setup.cfg"), "r") as f:
        temp = f.read().split("kevin-toolbox", 1)
    with open(os.path.join(root_dir, "setup.cfg"), "w") as f:
        f.write("kevin-toolbox-dev".join(temp))

    # 打包
    for folder in ["build", "dist", "kevin_toolbox_dev.egg-info"]:
        shutil.rmtree(os.path.join(root_dir, folder), ignore_errors=True)
    os.system(f'cd {root_dir};python setup.py sdist bdist_wheel')

    # 恢复现场
    shutil.move(src=os.path.join(root_dir, "kevin_toolbox", "__init__.py.bak"),
                dst=os.path.join(root_dir, "kevin_toolbox", "__init__.py"))
    shutil.move(src=os.path.join(root_dir, "setup.cfg.bak"), dst=os.path.join(root_dir, "setup.cfg"))
else:
    # 打包
    for folder in ["build", "dist", "kevin_toolbox.egg-info"]:
        shutil.rmtree(os.path.join(root_dir, folder), ignore_errors=True)
    os.system(f'cd {root_dir};python setup.py sdist bdist_wheel')
