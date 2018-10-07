import os
from medium_scraper import *

#TO RUN THIS FILE YOU NEED SELENIUM, BEAUTIFULSOUP, PANDAS, DATETIME, REGEX, AND OS
#JUST GO TO THE COMMAND LINE AND
#SET WORKING DIRECTORY TO THE DIRECTORY WITH BOTH MEDIUM_SCRAPER.PY AND SCRAPE_MASTER.PY
#THEN ENTER COMMAND "$python scrape_master.py"


#ADD THE TAGS TO SCRAPE HERE
tags = ["python", "ai"]

#Potential TAGs
"""
,"blogging","design", "poetry","javascript","computer-science", "humor", "racism", ""
"""


#already scraped
""" "marketing","life","software-engineering","web-design", "motivation", "love", "data-science", "machine-learning","artificial-intelligence","startup","politics","life-lessons","travel","entrepreneurship", "health","education","technology", "business","self-improvement","tech","programming","web-development","web-design","inspiration","productivity","personal-development","writing","leadership",
 "science", """
#ADD THE DATES TO SCRAPE HERE
yearstart=2017
monthstart=8
yearstop=2018
monthstop=8

#LOOPS THROUGH ALL LISTED-TAGS AND SCRAPES DATA OFF OF MEDIUM/TAG/archive
#SAVES THE FILES TO /TAG_SCRAPES/ IN CSV FORMAT
for tag in tags:
    scrape_tag(tag, yearstart, monthstart, yearstop, monthstop)
    print("Done with tag: ", tag)
print("done")
