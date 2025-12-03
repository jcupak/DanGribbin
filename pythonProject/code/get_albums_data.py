from bs4 import BeautifulSoup
import requests
import re

# Extract Album image, name, info, and optional buy link
# Write all album information to albums.csv file for later processing

response = requests.get("https://www.dangribbin.com/albums")
dg_albums_web_page = response.text
albums_html = BeautifulSoup(dg_albums_web_page, "html.parser")

pattern = re.compile(r"[\d]*[_][\d]*\.jpg$")

with open("albums.csv", mode="w") as albums_file:
    rows = albums_html.find_all("tr", height=True)
    for row in rows:
        row_height = row["height"]
        if row_height == "80":
            columns = row.find_all("td")
            for column in columns:
                column_width = column["width"]
                if column_width == "80":
                    album_info = column.a["href"]      # Extract link to album info web page
                    album_number = int("".join([ c for c in album_info if str.isdigit(c) ]))
                    album_image_link = column.a.img["src"]  # Extract link to album image
                    album_image_name = re.search(pattern, album_image_link).group()
                elif column_width == "190":
                    album_title = column.span.text
                    buy_link = ""  # Buy links broken on CDBaby
                    albums_file.write(f"{album_number},{album_title},{album_image_name},{buy_link}\n")
                # endif
            # end for column
        # endif
    # end for row
