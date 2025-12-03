from bs4 import BeautifulSoup
import requests
import re

CLEANCC = re.compile(r'[\r\n\t]')  # Control characters to eliminate
CLEANBR = re.compile('<.*?>')      # Any HTML tag to eliminate


def cleancc(raw_html: str) -> str:
    """
    Removes control characters from raw_html

    :param raw_html: String with embedded control characters
    :return: String without control characters

    From: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    """

    return CLEANCC.sub('', raw_html)


def cleanhtml(raw_html: str) -> str:
    """
    Removes HTML tags from raw_html

    :param raw_html: String with HTML tags
    :return: String without HTML tags

    From: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    """

    return CLEANBR.sub('', raw_html)


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


def get_song_data(song_number: int) -> str:
    """
    Extracts individual song data from table-encoded web page

    :param song_number: Number of the song page
    :return: CSV string of non-lyrics data; separated by '|'
    """

    DELIMITER         = "|"
    song_data         = ""  # Create empty song data string

    credit_fields     = {"Lyric Credits:":           "",
                         "Music Credits:":           "",
                         "Producer Credits:":        "",
                         "Publisher Credits:":       "",
                         "Performance Credits:":     "",
                         "Label Credits:":           ""}  # 6 Credit fields

    description_fields = {"Short Song Description:": "",
                          "Long Song Description:":  "",
                          "Story Behind the Song:":  ""}  # 3 Description fields

    metadata_fields    = {"Song Length":             "",
                          "Primary Genre":           "",
                          "Tempo / Feel 1":          "",
                          "Tempo / Feel 2":          "",
                          "Lead Vocal":              "",
                          "Subject Matter 1":        "",
                          "Subject Matter 2":        "",
                          "Mood 1":                  "",
                          "Mood 2":                  "",
                          "Language":                "",
                          "Era":                     ""}  # 11 Metaadata fields


    web_page = f"https://www.dangribbin.com/song/{song_number}"
    print(f"Song page:   {web_page}")           #  What song are we processing?

    song_data += str(song_number) + DELIMITER     # Field 0
    # print(f"Song Number: {song_number}")

    response = requests.get(web_page)              # Connect to Dan's song information page
    contents = response.text                       # Get web page contents
    html = BeautifulSoup(contents, "html.parser")  # Parse HTML

    # Find table with width = 95%
    table = html.find('table', width="95%")

    # Get all table rows
    rows = table.find_all('tr')
    for row in rows:
        height = row.get('height')  # Get height attribute (as text) or None if absent

        # Extract song title, play file id and optional buy file id
        if height == "23":

            # Extract song title from <span> tag
            song_title = row.td.span.string      # <tr><td><span>Song title</span></td>
            song_data += song_title + DELIMITER  # Append Field 1
            # print(f"Song Title:  {song_title}")
            # Find all <a> links
            links = row.find_all('a')

            # Extract Play file id from first (or only) <a> link
            play_link = links[0]["href"]         # Zero-based indexing
            play_file = get_play_file(play_link)
            song_data += play_file + DELIMITER   # Append Field 2
            # print(f"Play File:   {play_file}")


            # If second <a> link present, extract buy file id
            if len(links) == 2:
                buy_link = links[1]["href"]      # Zero-based indexing
                buy_file = get_buy_file(buy_link)
            else:
                buy_file = ""
            # endif buy_file link
            song_data += buy_file + DELIMITER    # Append Field 3
            # print(f"Buy File:    {buy_file}")

        ############################################################################
        # Extract song category label                                              #
        ############################################################################
        elif height == "12":

            #########################################################################
            # Extract category string. Should be "Credits", "Metadata", or "Lyrics" #
            #########################################################################
            category = row.td.string

        ############################################################################
        # Extract up to three song title and description contents                  #
        # Short Song Description, Long Song Description, and Story Behind the Song #
        ############################################################################
        elif height == "45":

            description_title_raw = row.td.contents[0]
            description_title = cleanhtml(cleancc(description_title_raw))
            song_description_raw = row.td.span.string
            song_description = cleanhtml(cleancc(song_description_raw))
            description_fields[description_title] = song_description  # Save

        #########################################################################
        # Table row without height attribute.                                   #
        # Extract Credits, Metadata, and Lyrics.                                #
        #########################################################################
        else:

            if category == "Credits" or category == "Metadata":

                tds = row.find_all('td')
                key   = tds[ 0 ].string  # Extract key from category_label
                value = tds[ 1 ].string  # Extract category value

                # Update corresponding dictionary fields
                if category == "Credits":
                    credit_fields[key] = value  # fill credit category field

                elif category == "Metadata":
                    # Save metadata tempo value depending on label
                    if key.startswith("Tempo"):
                        if metadata_fields["Tempo / Feel 1"] == "":  # Not assigned yet
                            metadata_fields["Tempo / Feel 1"] = value
                        else:                                        # Save to second Tempo field
                            metadata_fields["Tempo / Feel 2"] = value
                        # endif
                    else:
                        metadata_fields[key] = value  # Fill metadata field
                    # endif Metadata Tempo label
                # endif Credits or Metadata

            elif category == "Lyrics":

                # Extract all song lyrics and write to song_lyrics_##.txt file
                song_lyrics = cleanhtml(row.td.span.text) # Remove html tags
                lines = song_lyrics.splitlines()          # Split string at line breaks into a list
                lyrics_filename = f"song_lyrics_{song_number:02}.txt"
                lyrics_file = open(lyrics_filename, mode="w")
                for line in lines:
                    lyrics_file.write(line + '\n ')
                lyrics_file.close()

            # endif song category
        # endif table row height

    # Append all Credit fields
    for value in credit_fields.values():
        song_data += value + DELIMITER

    # for key, value in credit_fields.items():
    #     print(f"Credits:     {key:23} {value}")

    # Append all Description Fields
    for value in description_fields.values():
        song_data += value + DELIMITER

    # for key, value in description_fields.items():
    #     print(f"Description: {key:23} {value}")

    # Append all Metadata fields
    for key in metadata_fields.keys():
        if key == "Era":  # Last metadata field
            song_data += metadata_fields[key]  # Last field; No end DELIMITER
        else:
            song_data += metadata_fields[key] + DELIMITER

    # for key, value in metadata_fields.items():
    #     print(f"Metadata:    {key:23} {value}")

    return song_data


# Loop over selected song pages
# Song info for all songs; song_lyrics_##.txt for song lyrics
# Open song_info.csv file for writing
song_file = open("song_info.csv", mode="w")
for song in range(48):           # Songs 0-47
    song_data = get_song_data(song)
    # print(song_data)
    song_file.write(f"{song_data}\n")       # End of specific song info
song_file.close()

