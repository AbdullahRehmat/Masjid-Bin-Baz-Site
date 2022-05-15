# Masjid Bin Baz

Official Website for Masjid Abdul Aziz Bin Baz (London, UK).



## Installation

To run the website on a server:

```bash
cd ./Masjid-Bin-Baz-Site

pipenv install 

pipenv run python3 main.py
```



## Content Management

### Timetables

The Prayer timetable can be updated by logging into the Admin Portal and uploading a PDF file. The web server will automatically generate the WebP image preview and a unique download URL.

While old timetables will **not** be visible on the site, old download URLs will continue to be served.



#### Storage Location

```bash
./static/uploads/<timetable>.pdf
```



### Articles

Articles are to be written in GitHub Markdown syntax and uploaded as a `.md` file.  Articles are automatically formatted and served.  In the case that an article needs to be edited, please contact the developer. Server must be restarted for new articles to be displayed (?).



#### Storage Location

```bash
./static/articles/<article>.md
```



#### Sample Article:

```markdown
title: ARTICLE TITLE
subtitle: ARTICLE SUBTITLE
author: AUTHORS NAME
date: 01/01/2021

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Id aliquet risus feugiat in ante metus dictum. Rhoncus aenean vel elit scelerisque mauris pellentesque.  
  
Diam in arcu cursus euismod quis viverra nibh cras. Arcu dui vivamus arcu felis bibendum ut tristique. Venenatis lectus magna fringilla urna porttitor rhoncus dolor. In aliquam sem fringilla ut morbi. Aliquam malesuada bibendum arcu vitae elementum curabitur. Laoreet sit amet cursus sit amet dictum sit amet justo. Nam aliquam sem et tortor consequat. Nunc sed velit dignissim sodales ut eu sem. Tristique senectus et netus et malesuada fames ac turpis egestas.
  
Sit amet commodo nulla facilisi nullam vehicula ipsum a arcu. Pellentesque habitant morbi tristique senectus. Tincidunt eget nullam non nisi est sit amet facilisis. Semper feugiat nibh sed pulvinar proin gravida hendrerit lectus. Eget aliquet nibh praesent tristique magna sit. Quam quisque id diam vel.

```



### Audio

Audio files are hosted on SoundCloud. Playlists are automatically embedded via a Python & Jinja2 script. Server must be restarted for new playlists to be loaded.

#### Storage Location

```bash
./static/audios/audio.json
```



#### File Format

```json
{
    "playlists":{
        "playlist-name": "soundcloud playlist url minus display options",
        "Sahih Al-Bukhāri": "https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1267629787"
    }
}
```



## Tech Stack

### Website

- Python 3.8 Flask Server
- HTML / Jinja2 Syntax
- SQLite Database



### Hosting

- Repository - [GitHub](github.com/abdullahrehmat/masjid-bin-baz-v2)
- Website - [Python Anywhere](pythonanywhere.com)
- CDN - Cloudflare



### Analytics

- Google Analytics Plugin
- Python Anywhere Server Statistics Plugin



## Credits

- Icons sourced from [IconScout]([Icons - Line](https://iconscout.com/unicons/explore/line))
- Banner image sources from [Unsplash](https://unsplash.com/images)



## To Do List

- [ ] Refactor Codebase
- [ ] Simplify CSS Styles
- [ ] Improve image formats
- [ ] Optimise Website For Performance
