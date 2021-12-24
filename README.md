# Masjid Bin Baz

Official Website for Masjid Abdul Aziz Bin Baz (UK).

Website is written in HTML5 and CSS3. Server is written in Python via the Flask framework.



## Installation

To run the website on a server:

> cd ./Masjid-Bin-Baz-Site
>
> pipenv install 
>
> pipenv run python3 main.py



## Content Management

### Timetables

The Prayer timetable can be updated by logging into the Admin Portal and uploading a PDF file. The web server will automatically generate the WebP image preview and a unique download URL.

While old timetables will **not** be visible on the site, old download URLs will continue to be served.



### Articles

Articles should be written in GitHub Markdown syntax and uploaded as a `.md` file.  Articles are automatically formatted and served.  In the case that an article needs to be edited, please contact the developer.



#### Sample Markdown Article:

```markdown
title: ARTICLE TITLE

subtitle: ARTICLE SUBTITLE

author: AUTHORS NAME

date: 01/01/2021

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Id aliquet risus feugiat in ante metus dictum. Rhoncus aenean vel elit scelerisque mauris pellentesque.  
  
Diam in arcu cursus euismod quis viverra nibh cras. Arcu dui vivamus arcu felis bibendum ut tristique. Venenatis lectus magna fringilla urna porttitor rhoncus dolor. In aliquam sem fringilla ut morbi. Aliquam malesuada bibendum arcu vitae elementum curabitur. Laoreet sit amet cursus sit amet dictum sit amet justo. Nam aliquam sem et tortor consequat. Nunc sed velit dignissim sodales ut eu sem. Tristique senectus et netus et malesuada fames ac turpis egestas.
  
Sit amet commodo nulla facilisi nullam vehicula ipsum a arcu. Pellentesque habitant morbi tristique senectus. Tincidunt eget nullam non nisi est sit amet facilisis. Semper feugiat nibh sed pulvinar proin gravida hendrerit lectus. Eget aliquet nibh praesent tristique magna sit. Quam quisque id diam vel.

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



## To Do List



