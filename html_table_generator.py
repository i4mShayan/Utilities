import os
from bs4 import BeautifulSoup

n_cols = 5
max_n = None

IMAGES_FOLDER = './images'
html_code = "<table>"
rows = []

image_files = [f for f in os.listdir(IMAGES_FOLDER) if os.path.isfile(os.path.join(IMAGES_FOLDER, f))]
max_n = len(image_files) if max_n is None or max_n >= len(image_files) else max_n

for i, filename in enumerate(image_files[:max_n]):
    bookname = filename.split('_')[1]
    img_tag = f'<div style="text-align:center">{bookname}</div>'
    img_str = IMAGES_FOLDER + '/' + filename
    img_tag += f'<img src="{img_str}" align="center" alt="{filename}" width="200px">'

    rows.append(f"<td>{img_tag}</td>")

    if (i + 1) % n_cols == 0:
        html_code += f"<tr>{''.join(rows)}</tr>"
        rows = []

if rows:
    html_code += f"<tr>{''.join(rows)}</tr>"

html_code += "</table>"

soup = BeautifulSoup(html_code, 'html.parser')
prettified_html = soup.prettify()

print(prettified_html)
