import os

content_s_ls, param_s_ls, expected_result_ls = [], [], []
count = 0
while True:
    try:
        exec(f'from .data_{count} import content_s, param_s')
        content_s_ls.append(content_s)
        param_s_ls.append(param_s)
        with open(os.path.join(os.path.dirname(__file__), f"data_{count}.md"), "r") as f:
            expected_result = f.read()
            expected_result_ls.append(expected_result)
        count += 1
    except:
        break
