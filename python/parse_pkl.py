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

        print("<<<TABLE_START>>>") # start of HTML output

        if isinstance(obj, (pd.DataFrame, np.ndarray, list, tuple)):
            _parse_pkl(obj=obj, level=1, max_depth=3, file_path=file_path, ctf=False, pose=False)
        
        else:
            print(f"Unsupported .pkl data type: {type(obj).__name__}", file=sys.stderr)
            sys.exit(1)

        print("<<<TABLE_END>>>") # end of HTML output

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def _parse_pkl(obj, level=1, max_depth=3, file_path='', ctf=False, pose=False):
    if level > max_depth:
        print(f"<p>...</p>")
        return

    # string, int, float, bool
    if isinstance(obj, (str, int, float, bool)):
        print(f"<h{level}>{type(obj).__name__}</h{level}>")
        print(f"<p>{obj}</p>")
    
    # Pandas DataFrame
    elif isinstance(obj, pd.DataFrame):
        try:
            display_dataframe(df=obj, name=type(obj).__name__, level=level)
        
        except Exception as e:
            print(f"<p><i>Failed to render {type(obj).__name__}: {e}</i></p>")

    # NumPy ndarray
    elif isinstance(obj, np.ndarray):
        try:
            if obj.ndim == 1:
                display_dataframe(df=pd.DataFrame(obj), name=type(obj).__name__, level=level)
                
            elif obj.ndim == 2:
                df = pd.DataFrame(obj)

                # reformat (rename columns) if structure matches CTF data format
                if (
                    ctf or (
                        'ctf' in file_path and
                        level == 1 and
                        df.shape[1] == 9
                    )
                ):
                    print(f"<p><i>Formatted ndarray {str(list(df.shape))} as CTF data.</i></p>")
                    df.columns = [
                        'image size (pix)',
                        'pixel size (A/pix)',
                        'defocus U (A)',
                        'defocus V (A)',
                        'defocus angle (deg)',
                        'voltage (kV)',
                        'spherical aberration (mm)',
                        'amplitude contrast ratio',
                        'phase shift (deg)'
                    ]
                    display_dataframe(df=df, name='CTF', level=level)
                
                # reformat name if structure matches pose (translation) data format
                elif (
                    pose and
                    level == 2 and
                    df.shape[1] == 2
                ):
                    display_dataframe(df=df, name='translation', level=level)
                
                else:
                    display_dataframe(df=df, name=type(obj).__name__, level=level)

            elif obj.ndim == 3:
                # reformat name if structure matches pose (rotation) data format
                if (
                    pose and
                    level == 2 and
                    obj.shape[1] == 3 and
                    obj.shape[2] == 3
                ):
                    print(f"<h2>rotation {str(list(obj.shape))}</h2>")
                
                else:
                    print(f"<h{level}>{type(obj).__name__} {str(list(obj.shape))}</h{level}>")
                
                n_slices = obj.shape[0]
                
                if n_slices <= NDARRAY_DISPLAY_MAX_SLICES:
                    for i in range(0, n_slices):
                        display_dataframe(df=pd.DataFrame(obj[i]), name=f"{i}", level=level + 1)
                
                else:
                    n_slices_display = NDARRAY_DISPLAY_MAX_SLICES // 2
                    
                    for i in range(min(n_slices, n_slices_display)):
                        display_dataframe(df=pd.DataFrame(obj[i]), name=f"{i}", level=level + 1)
                        
                    print(f"<h{level + 1}>...</h{level + 1}>")

                    for i in range(-1 * n_slices_display, 0):
                        display_dataframe(df=pd.DataFrame(obj[i]), name=f"{n_slices + i}", level=level + 1)
            
            else:
                print(f"<p><i>Failed to render {type(obj).__name__}: {e}</i></p>")
        
        except Exception as e:
            print(f"<p><i>Failed to render {type(obj).__name__}: {e}</i></p>")

    # list, tuple
    elif isinstance(obj, (list, tuple)):
        # reformat if structure matches pose data format
        if (
            pose or (
                'pose' in file_path and
                isinstance(obj, tuple) and
                len(obj) == 2 and
                level == 1 and
                isinstance(obj[0], np.ndarray) and
                isinstance(obj[1], np.ndarray) and
                obj[0].ndim == 3 and
                obj[0].shape[1] == 3 and
                obj[0].shape[2] == 3 and
                obj[1].ndim == 2 and
                obj[1].shape[1] == 2 and
                obj[0].shape[0] == len(obj[1])
            )
        ):
            print(f"<p><i>Formatted tuple [2] of (ndarray [{len(obj[1])}, 3, 3], ndarray [{len(obj[1])}, 2]) as pose data.</i></p>")
            print(f"<h1>pose [{len(obj)}]</h1>")

            rotation = obj[0]
            translation = obj[1]

            _parse_pkl(obj=rotation, level=2, max_depth=max_depth, pose=True)
            _parse_pkl(obj=translation, level=2, max_depth=max_depth, pose=True)
        
        else:
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
