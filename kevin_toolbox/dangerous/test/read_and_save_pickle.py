import pickle
import argparse

out_parser = argparse.ArgumentParser(description='parse_bin_folder')
out_parser.add_argument('--input_file', type=str, required=True)
out_parser.add_argument('--output_file', type=str, required=True)
args = out_parser.parse_args().__dict__
print(args)

# read
with open(args["input_file"], "rb") as f:
    var = pickle.load(f)

with open(args["output_file"], "wb") as f:
    pickle.dump(var, f)
