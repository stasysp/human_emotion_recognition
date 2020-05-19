from utils import tools
import argparse
import importlib
if __name__ == "__main__":
    tools = importlib.reload(tools)

    parser = argparse.ArgumentParser(description='Optional app description')
    # Optional argument
    parser.add_argument('--path_to_csv', type=str, help='Path to csv with scalled results (example: --path_to_csv "./path/to/result0-100000.csv")')
    parser.add_argument('--path_to_data_source', type=str, help='Path to ./public_youtube1120_mp3')
    parser.add_argument('--path_to_data_destination', type=str, help='Path to dir with /train, /val subdirs with folders for every emotions')

    args = parser.parse_args()

    if not '.csv' in args.path_to_csv:
        print("Unexpected arg: ".format(args.path_to_csv))

    print(args.path_to_csv)
    print(args.path_to_data_source)
    print(args.path_to_data_destination)

    tools.get_train_val(args.path_to_csv, args.path_to_data_source, args.path_to_data_destination)