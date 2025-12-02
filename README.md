# Dan Gribbin Web Site
## Redesign of existing web site

### Background

Not long ago, Dan Gribbin appeared at our church to give a talk and perform some of his songs. During the talk, he mentioned that he had a web site with more information about him and his songs.

Figure 1. Original songs.html web page

I recently completed a Python course in which I learned how to create a dynamic web site from data files and how to "scrape" information from a web site's underlying HTML. 

After viewing Dan Gribbin's web site, I saw that the underlying HTML was based on the old concept of using tables with styles embedded in the tags. So, I decided to apply what I had learned about using Python to "scrape" the data from Dan's web pages, create data files, and use Python to generate new web pages. 

### Scraping the Data

Figure 2. Source songs.html

In order to create data files from the contents of the web pages, I wrote Python code to "scrape" the web pages. Fortunately, the data I was looking for was always placed inside table components with a repeated format. I was able to extract the data and place it in a CSV (Comma Separated Value) text file and sort it. 

Other data, such as song lyrics, event information, or images required the creation of separate text and image files.

### Creating Web Pages

By using Python and Bootstrap layout templates, I was able to create a base HTML template which contained only the common header, navigation links, and footer.

In place of the original HTML which used tables to layout the web page, I created a **layout.html** template which used a semantic layout for each page  with a **\<header\>**, **\<main\>** with a **\<section class="content"\>**, and **\<footer\>** HTML tags which made the underlying content much more understandable.

For example, knowing that the **songs.csv** data file contained the song number, the song title with an information link, a play link, and a buy link for each song, the **songs.html** web page was laid out using a table with four (4) columns, and each row contained the individual song information. Play links and buy links were only included if present in the **songs.csv** data file.

### Generating Web Pages

The Python **main.py** program was written with functions (def's) to determine which web page to display and pass data to the page to display.  

For example, the **def songs():** function opened the **songs_sorted.csv** data file, and passed the data to the **songs.html** web page for display. 

### Results

The resultant web site consists of fourteen (14) web pages: about, album (single album with songs list), albums (list of albumns), contact, event (single event information), events (list of events), gallery, index (home page), layout, links, news, photos, song (information about individual song), and songs (list of songs). 

Because the web site used Bootstrap for content layout and styles, only three CSS (Cascading Style Sheets) were written: **dg_gradient_palettes.css** (colors from original site), **dg_styles.css** (web site styles), and **dg_contact_form_postcard.css** (fonts and formats to define the contact page).

Figure 3. Redesigned **songs.html** web page.

### Comparison Statistics

The original "Old" HTML files contained 3,393 lines; mostly made up of HTML head data and repeating lines of individual items, such as albums, events, and songs. These files were written using tables with embedded width and height attributes to layout side bars and contents. This table-layout style was popular during the early days of web design, and made it difficult to determine the meaning of the various table rows and columns.

The redesigned "New" HTML files contained 1,114 lines, including a **layout.html** file that became the template for all the other web pages; it included header and footer information. The new HTML files contained **\<main\>**, **\<header\>**, **\<section\>**, **\<article\>** and **\<footer\>** "semantic" tags which clearly identified the content.  In addition, Bootstrap was used to format the content. The resultant web site, including the Python code, was about a quarter the size of the original site.

Table 1. Web Site Metrics
Web Site Page | Old HTML Lines | New HTML Lines | New py Lines | Total New Lines
--------- | -------- | -------- | ------ | -----
albums.html | 161 | 63 | 6 | 69
album.html | 265 | 133 | 14 | 147
bio.html | 130 | 39 | 3 | 42
contact.html | 159 | 56 | 1 | 57
events.html | 132 | 47 | 6 | 53
event.html | 195 | 125 | 11 | 136
index.html | 146 | 51 | 1 | 52
links.html | 149 | 45 | 6 | 51
layout.html | 0 | 142 | 0 | 142
news.html | 1762 | 34 | 3 | 37
photos.html | 292 | 79 | 6 | 85
songs.html | 462 | 52 | 6 | 58
song.html | 258 | 158 | 14 | 172
**totals** | **3,393** | **1,114** | **77** | **1.101**

### Data Files

Data needed to populate the web pages was "scraped" from the old HTML pages through the use of Python procedures. These procedures were used only once to extract the required data and place it in CSV or Text files.

Table 2. Get Data Procedures Lines of Code
Lines | Python File Name
----- | ----------------
  141 | get_album_data.py
   34 | get_albums_data.py
  107 | get_event_data.py
   58 | get_events_data.py
   44 | get_links_data.py
   88 | get_news_data.py
  105 | get_photo_data.py
  238 | get_song_data.py
   46 | get_songs_data.py
  862 | **total**

Table 3. Data Files
Data Item | CSV Files | Text Files
--------- | --------- | ----------
   Albums |         6 |          4
   Events |         2 |         84
   Songs  |         3 |         48
**Totals** |   **11** |      **136**



## Conclusion

The hardest part of this project was "scraping" the data from the original HTML files. Tables were nested inside tables; only by identifying the specific height or width attributes in the table **\<tr\>** rows, **\<th\>** headings, and **\<td\>** data columns was it finally possible to identify the and extract relevant data. 

Links to audio files for listening and purchasing were sometimes broken, making automation extraction difficult. Each album and song links needed to be validated. Song lyrics were extracted into individual text files, and identified by song number. Events were likewise extracted into individual text files and identified by event number.

## Future Work

Missing from the web site is the ability of the owner to add songs, events, links, and pictures. New **add_song.html**, **add_event.html**, **add_link.html**, and **add_image.html** web pages with input forms would need to be written, with additional Python functions designed to extract the information and append them to existing data files.

Finally, the entire web site with web pages, styles, data files, and Python code would need to be transported to a web server that supports dynamic data.
