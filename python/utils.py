import pandas as pd

DATAFRAME_DISPLAY_MAX_ROWS = 100
DATAFRAME_DISPLAY_MAX_COLS = 100


# display pandas dataframe as html table
def display_dataframe(df, name='', level=1):
    if level is None:
        print(f"<p>{name} {str(list(df.shape))}</p>")
    else:
        print(f"<h{level}>{name} {str(list(df.shape))}</h{level}>")
    
    html = df.to_html(border=1, header=True, index=True, escape=True, justify='left', show_dimensions=False, max_rows=DATAFRAME_DISPLAY_MAX_ROWS, max_cols=DATAFRAME_DISPLAY_MAX_COLS)
    print(html)
