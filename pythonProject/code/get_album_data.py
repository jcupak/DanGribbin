from bs4 import BeautifulSoup
import requests
import re

album_image_pattern = re.compile(r"[\d]*[_][\d]*.jpg$")
CLEANCC             = re.compile(r'[\r\n\t]')  # Control characters to eliminate
CLEANBR             = re.compile('<.*?>')      # Any HTML tag to eliminate


def cleancc(raw_html: str) -> str:
    """
    Removes control characters from raw_html

    :param raw_html: String with embedded control characters
    :return: String without control characters

    From: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    """

    return CLEANCC.sub('', raw_html)


def get_play_file(play_link: str) -> str:
    """
    Extracts play_file from play_link
    :param play_link: Javascript OpenNew Window link
    :return: play_file string
    """

    play_start = play_link.find("play_file=") + 10
    play_end = play_link.find(")") - 1  # Ignore ') at end
    return play_link[play_start:play_end]


def get_buy_file(buy_link: str) -> str:
    """
    Extracts buy file from buy_link string
    :param buy_link: Link to shopping card buy file
    :return: buy_file string
    """

    buy_start = buy_link.find("ciid=") + 5
    return buy_link[buy_start:]  # To the end of the href


def get_album_data(album_number: int):
    """
    Extracts album image file name, title, description, and tracks from album web page
    :param album_number: Number of album
    :return: nothing

    Album information written to album_#_info.txt.
    Album tracks written to album_#_tracks.csc
    """

    web_page = f"https://www.dangribbin.com/album/{album_number}"  # Which album page to extract
    album_info_filename   = f"album_{album_number}_info.txt"       # Album information file
    album_tracks_filename = f"album_{album_number}_tracks.csv"     # Album tracks file

    print(f"\nExtracting {web_page}")

    response = requests.get(web_page)                              # Connect to Dan's album information page
    contents = response.text                                       # Get web page contents
    html     = BeautifulSoup(contents, "html.parser")              # Parse HTML

    album_info_file = open(album_info_filename, "w")               # Contains image filename, title, and description
    album_tracks_file = open(album_tracks_filename, "w")           # Contains track number, song number, song title,
                                                                   #  play file id, and buy file id

    # The album web page is designed using old tables, <tr> rows, and <td> data tags
    # Main album content contained in central table of width=400
    tables = html.find_all("table", width="400")
    for table in tables:
        table_width = table.get("width")
        rows = table.find_all("tr")
        for row in rows:
            row_height = row.get("height")
            if row_height == None:
                columns = row.find_all("td")  # <td> tags
                for column in columns:
                    column_width = column.get("width")
                    if column_width == "80":
                        album_image_link = column.img["src"]  # Extract album cover image link
                        album_image_file = re.search(album_image_pattern, album_image_link).group()
                        album_info_file.write(f"{album_image_file}\n")
                    elif column_width == "10":
                        pass  # Ignore empty <td> tag
                    elif column_width == None:
                        column_height = column.get("height")
                        if column_height == "45":
                            album_title = column.span.string
                            album_info_file.write(f"{album_title}\n")
                        elif column_height == "20":
                            pass  # Ignore empty <td>
                    elif column_width == "300":
                        album_description = cleancc(column.string)
                        album_info_file.write(f"{album_description}\n")
                    # endif
            elif row_height == "11":
                pass  # Ignore spacer row
            elif row_height == "15":
                pass  # Ignore track column headings
            elif row_height == "12":
                # Extract album track number, track name, play_link, and buy_link
                columns = row.find_all("td")
                for column in columns:
                    column_width = column.get("width")
                    if column_width == "22":
                        track_number = column.string
                        album_tracks_file.write(f"{track_number},")
                    elif column_width == None:
                        song_link = column.a["href"]
                        song_number = int("".join([ c for c in song_link if str.isdigit(c) ]))  # Field 0
                        album_tracks_file.write(str(f"{song_number},"))
                        song_title = column.a.text
                        song_title = song_title.replace(",", " -")
                        album_tracks_file.write(f"{song_title},")
                    elif column_width == "158":
                        len_links = len(column.contents)
                        print(f"Len(Links): {len_links}")
                        play_link = column.contents[1]["href"]
                        play_file = get_play_file(play_link)
                        album_tracks_file.write(f"{play_file},")
                        if len_links > 3:
                            buy_link = column.contents[3]["href"]
                            buy_file = get_buy_file(buy_link)
                        else:
                            buy_file = ""
                        # endif
                        album_tracks_file.write(f"{buy_file}\n")
                    # end if column_width
            # end if row_height
        # end for rows
    # end for tables
    album_info_file.close()
    album_tracks_file.close()
# end get_album_data

# Loop over all album pages 0-3
for album in range(4):
    get_album_data(album)
