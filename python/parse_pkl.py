import os
import sys
import pickle
import pandas as pd
import numpy as np

from utils import display_dataframe

NDARRAY_DISPLAY_MAX_SLICES = 10


# parse .pkl file
def parse_pkl(file_path):
    try:
        with open(file_path, 'rb') as f:
            obj = pickle.load(f)

        print("<<<TABLE_START>>>") # start of html output

        if isinstance(obj, (pd.DataFrame, np.ndarray, list, tuple)):
            _parse_pkl(obj)
        
        else:
            print(f"Unsupported .pkl data type: {type(obj).__name__}", file=sys.stderr)
            sys.exit(1)

        print("<<<TABLE_END>>>") # end of html output

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def _parse_pkl(obj, level=1, max_depth=3):
    if level > max_depth:
        print(f"<p>...</p>")
        return

    # string, int, float, bool
    if isinstance(obj, (str, int, float, bool)):
        print(f"<h{level}>{type(obj).__name__}</h{level}>")
        print(f"<p>{obj}</p>")
    
    # pandas dataframe
    elif isinstance(obj, pd.DataFrame):
        try:
            display_dataframe(df=obj, name=type(obj).__name__, level=level)
        
        except Exception as e:
            print(f"<p>Failed to render {type(obj).__name__}: {e}</p>")

    # numpy ndarray
    elif isinstance(obj, np.ndarray):
        try:
            if obj.ndim == 1:
                df = pd.DataFrame(obj)
                display_dataframe(df, name=type(obj).__name__, level=level)
                
            elif obj.ndim == 2:
                df = pd.DataFrame(obj)
                display_dataframe(df, name=type(obj).__name__, level=level)

            elif obj.ndim == 3:
                print(f"<h{level}>{type(obj).__name__} {str(list(obj.shape))}</h{level}>")
                
                n_slices = obj.shape[0]
                max_slices = 10

                for i in range(min(n_slices, max_slices)):
                    df = pd.DataFrame(obj[i])
                    display_dataframe(df, name=f"slice {i}", level=level + 1)

                if n_slices > NDARRAY_DISPLAY_MAX_SLICES:
                    print(f"<h{level + 1}>...</h{level + 1}>")
            
            else:
                print(f"<p>Failed to render {type(obj).__name__}: {e}</p>")
        
        except Exception as e:
            print(f"<p>Failed to render {type(obj).__name__}: {e}</p>")

    # list, tuple
    elif isinstance(obj, (list, tuple)):
        print(f"<h{level}>{type(obj).__name__} [{len(obj)}]</h{level}>")
        
        for o in obj:
            _parse_pkl(obj=o, level=level + 1, max_depth=max_depth)

    else:
        print(f"Unsupported .pkl data type: {type(obj).__name__}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_pkl.py <path_to_pkl_file>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    if path.endswith('.pkl') is False:
        print(f"Unsupported extension for file: {path}.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(path):
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    parse_pkl(path)


if __name__ == "__main__":
    main()
