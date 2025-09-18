import os
import sys
import starfile
import pandas as pd

from utils import display_dataframe


# parse .star file
def parse_star(path: str):
    try:
        obj = starfile.read(path)

        print("<<<TABLE_START>>>") # start of html output
        
        if isinstance(obj, dict):
            print(f"<h1>{type(obj).__name__} [{len(obj)}]</h1>")
            
            for name, df in obj.items():
                try:
                    display_dataframe(df=df, name=name, level=2)
                except Exception as e:
                    print(f"<p>Failed to render {type(obj).__name__}: {e}</p>")
                    
        elif isinstance(obj, pd.DataFrame):
            try:
                display_dataframe(df=obj, name='', level=1)
            except Exception as e:
                print(f"<p>Failed to render {type(obj).__name__}: {e}</p>")

        else:
            print(f"Unsupported .star data type: {type(obj).__name__}", file=sys.stderr)
            sys.exit(1)
        
        print("<<<TABLE_END>>>") # end of html output
    
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_star.py <path_to_star_file>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    if path.endswith('.star') is False:
        print(f"Unsupported extension for file: {path}.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(path):
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    parse_star(path)


if __name__ == "__main__":
    main()
