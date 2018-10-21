# Analyzing_Medium

## What is Medium?

<a href="https://medium.com/">Medium</a> is a blogging platform where writers and readers share their ideas. With a strong following in the tech community, it is a place where people can come to learn from professionals and industry experts. I began writing on Medium very recently, inspired to write about data-science and machine learning. For more information, check out my writing <a href="https://medium.com/@harrisonjansma">here.</a>


<a href="https://medium.com/@harrisonjansma">
<img align="center" src="img/mediumhome.JPG" height=200></a>

# This Project
In this project I collected data on one million Medium stories from 36 of the most popular writing subjects. I used this data to answer the following questions.
1. What do I need to know about Medium as a writer and as a reader? (<a href="https://github.com/harrisonjansma/Analyzing_Medium/blob/master/Medium_EDA.ipynb">source</a>)
2. Who are the top Data-Science writers on Medium? (<a href="https://github.com/harrisonjansma/Analyzing_Medium/blob/master/Medium_Author_Leaderboard.ipynb">source</a>)
3. How can Medium writer's measure the performance of their stories? How can they compare their performance to that of similar writers? (<a href="https://github.com/harrisonjansma/Analyzing_Medium/blob/master/Medium_EDA.ipynb">source</a>)

This repository is a collection of everything I found while analyzing the data collected from Medium. I hope you think it as interesting as I do.


# How I Scraped Medium


If you want to collect your own data, I have made another repository that contains the python files I used to collect my data. You can find what you need in the <a href="https://github.com/harrisonjansma/Medium_Scraper">Medium_Scrape</a> repository.


The scraper pulls data from Medium's archive pages. Each archive page is associated to a story-tag and is a <b>collection of Medium timeline cards organized by date.</b>
<br>

<h3 align="center"> Image of the "<a href="https://medium.com/tag/data-science/archive">data-science</a>" Archive</h3>

<img src="img/archive2.png" align="center" width=500>


## Structure of the Scraped Data
- Title -title of article on timeline card
- Subtitle  -subtitle of article on timeline card
- Image (yes/no)-whether the article has a preview image on its timeline card
- Author -writer of the story
- Publication - the name of the publication the article may have been posted in
- Year - Month - Day-date the article was published
- Tag - text
- Reading Time- Time to read the article
- Claps-Number of claps the article received
- Comment (yes/no)-whether the entry is a comment on another article
- Story Url-link to story
- Author URL-link to Author's Medium homepage




<br>
 <h3 align="center">Example of Data Scraped from a Timeline Card</h3>
<img align="center" src="img/card.png" width=500>
