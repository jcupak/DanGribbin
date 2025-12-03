from bs4 import BeautifulSoup
import requests

# Dan's song web page was laid out uwing tables
# This python program searches for the song name,
# the link to the play file, and the link to the optional buy file
# and writes the song data to the songs.csv data file

response = requests.get("https://www.dangribbin.com/songs")  # Connect to Dan's song page
dg_songs_web_page = response.text                            # Get web page contents
soup = BeautifulSoup(dg_songs_web_page, "html.parser")       # Parse HTML

with open("songs.csv", mode="w") as songs_file:

    # Find all table data cells with a width attribute
    cells = soup.find_all("td", width=True)

    for cell in cells:

        width = cell["width"]  # Extract width value

        if width == "250":  # Songs are in table data with width 250

            song_link = cell.a["href"]  # /song/00
            song_number = int("".join([c for c in song_link if str.isdigit(c)]))  # Field 0
            song_title = cell.a.string  # Extract title as field 1

            links = cell.next_sibling.next_element

            # Get PLAY link
            play_href  = links.contents[1].attrs.get('href')  # Extract Play href
            play_start = play_href.find("play_file=") + 10
            play_end   = play_href.find(")") - 1  # Ignore ') at end
            play_link  = play_href[play_start:play_end]  # Field 2

            if len(links) == 5:
                # Get BUY link
                buy_href = links.contents[3].attrs.get('href')  # Extract Buy href
                buy_start = buy_href.find("ciid=") + 5
                buy_link = buy_href[buy_start:]  # Field 3
            else:
                # Missing BUY link
                buy_link = ""  # Create empty buy link
            # endif

            songs_file.write(f"\n{song_number},{song_title},{play_link},{buy_link}")
