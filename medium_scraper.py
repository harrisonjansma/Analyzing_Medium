import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import pandas as pd
import time



def base_url_builder(tag):
    #BUILDS THE BASE URL TO ITERATE ON FROM GIVEN TAG
    url = "https://medium.com/tag/" + tag +"/archive/"
    return url


def get_start_date(year, month, day):
    #CHECKS IF START DATE IS A VALID DATE, CONVERTS TO DATETIME OBJECT
    try:
        start_date = datetime(year, month, day)
    except:
        raise Exception("Start date is in the wrong format or is invalid.")
    return start_date


def get_end_date(year, month, day):
    #CHECKS IF END DATE IS A VALID DATE, CONVERTS TO DATETIME OBJECT
    try:
        end_date = datetime(year, month, day)
    except:
        raise Exception("End date is in the wrong format or is invalid.")
    return end_date


def open_chrome():
    #OPENS A CHROME DRIVER
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    return driver


def url_masher(base_url, year, month, day):
    #MAKES A NEW URL FRON GIVEN DATE
    #THE FORMAT OF THE URL IS YYYY/MM/DD WE MUST MATCH IT
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    #MASH THE STRINGS TOGETHER TO MAKE A PASSABLE URL
    url = base_url + year + "/" + month + "/" + day
    return url



def find_post_cards(soup):
    #PULLS EACH CARD FROM THE FEED. EACH CARD IS A STORY OR COMMENT
    cards = soup.find_all("div", class_="streamItem streamItem--postPreview js-streamItem")
    return cards



def get_titles_from_cards(cards):
    #PULLS TITLE DATA FROM EACH CARD IN CARDS, RETURNS A LIST OF TITLES
    def title_cleaner(title):
        #REMOVE MEDIUMS ENCODING SYMBOLS AND EMOJIS FROM TITLES
        title = title.replace("\xa0"," ")
        title = title.replace("\u200a","")
        title = title.replace("\ufe0f","")
        title = re.sub(r'[^\x00-\x7F]+','', title)
        return title

    titles=[]
    for card in cards:
        #SEARCH FOR TITLE THERE ARE 3 DIFF CLASSES
        variant1 = card.find("h3", class_="graf graf--h3 graf-after--figure graf--title")
        variant2 = card.find("h3", class_="graf graf--h3 graf-after--figure graf--trailing graf--title")
        variant3 = card.find("h4", class_="graf graf--h4 graf--leading")
        variant4 = card.find("h3", class_="graf graf--h3 graf--leading graf--title")
        variant5 = card.find("p", class_="graf graf--p graf--leading")
        variant6 = card.find("h3", class_="graf graf--h3 graf--startsWithDoubleQuote graf--leading graf--title")
        variant7= card.find("h3", class_="graf graf--h3 graf--startsWithDoubleQuote graf-after--figure graf--trailing graf--title")
        #EACH CARD MUST HAVE ONE OF THE ABOVE TITLE CLASSES FIND IT AND CUT OUT MEDIUM'S
        #STYLING CODES
        variants = [variant1, variant2, variant3, variant4, variant5, variant6, variant7]
        saved = False
        #THE FIRST TITLE ENTRY WE MATCH, WE SAVE
        for variant in variants:
            if ((variant is not None) and (not saved)):
                title = variant.text
                title = title_cleaner(title)
                titles.append(title)
                saved = True
        if not saved:
            titles.append("NaN")
    return titles




def get_subtitles_from_cards(cards):
    #PULLS TITLE DATA FROM EACH CARD IN CARDS, RETURNS A LIST OF TITLES
    def subtitle_cleaner(subtitle):
        #REMOVE MEDIUMS ENCODING SYMBOLS AND EMOJIS FROM TITLES
        subtitle = subtitle.replace("\xa0"," ")
        subtitle = subtitle.replace("\u200a","")
        subtitle = subtitle.replace("\ufe0f","")
        subtitle = re.sub(r'[^\x00-\x7F]+','', subtitle)
        return subtitle

    subtitles=[]
    for card in cards:
        #SEARCH FOR TITLE THERE ARE 3 DIFF CLASSES
        variant1 = card.find("h4", class_="graf graf--h4 graf-after--h3 graf--subtitle")
        variant2 = card.find("h4", class_="graf graf--h4 graf-after--h3 graf--trailing graf--subtitle")
        variant3 = card.find("strong", class_="markup--strong markup--p-strong")
        variant4 = card.find("h4", class_="graf graf--p graf-after--h3 graf--trailing")
        variant5= card.find("p", class_="graf graf--p graf-after--h3 graf--trailing")
        variant6= card.find("blockquote", class_="graf graf--pullquote graf-after--figure graf--trailing")
        variant7 = card.find("p", class_="graf graf--p graf-after--figure")
        variant8 = card.find("blockquote", class_="graf graf--blockquote graf-after--h3 graf--trailing")
        variant9 = card.find("p", class_="graf graf--p graf-after--figure graf--trailing")
        variant10 = card.find("em", class_="markup--em markup--p-em")
        variant11=card.find("p", class_="graf graf--p graf-after--p graf--trailing")
        #EACH CARD MUST HAVE ONE OF THE TITLE CLASSES FIND IT AND CUT OUT MEDIUM'S
        #STYLING CODES
        variants = [variant1, variant2, variant3, variant4, variant5, variant6, variant7, variant8, variant9, variant10, variant11]
        saved = False
        for variant in variants:
            if ((variant is not None) and (not saved)):
                subtitle = variant.text
                subtitle = subtitle_cleaner(subtitle)
                subtitles.append(subtitle)
                saved = True
        if not saved:
            subtitles.append("NaN")
    return subtitles



def get_image_from_cards(cards):
    #RETURNS A 1 IF IMAGE IS PRESENT
    images = []
    for card in cards:
        img = card.find("img",class_="progressiveMedia-image js-progressiveMedia-image")
        if img is not None:
            images.append(1)
        else:
            images.append(0)
    return images



def get_auth_and_pubs_from_cards(cards):
    # PULLS AUTHOR AND PUBLICATION FROM EACH STORY CARD
    authors = []
    pubs = []
    for card in cards:
        # get the author and publication
        author = card.find("a", class_="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken")
        pub = card.find("a", class_="ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal")
        if author is not None:
            text = author.text
            text = re.sub('\s+[^A-Za-z]', '', text)
            text = re.sub(r'[^\x00-\x7F]+',' ', text)
            authors.append(text)
        else:
            raise Exception("Author Not found")
        if pub is not None:
            text2 = pub.text
            text2 = re.sub('\s+[^A-Za-z]', '', text2)
            text2 = re.sub(r'[^\x00-\x7F]+',' ', text2)
            pubs.append(text2)
        else:
            pubs.append("NaN")
    return authors, pubs


def get_dates_and_tags(tag, year,month,day,cards):
    #CREATES A LIST OF TAGS AND DATES
    Year=[]
    Month=[]
    Day = []
    tags=[]
    for card in cards:
        tags.append(tag)
        Year.append(year)
        Month.append(month)
        Day.append(day)
    return Year, Month, Day, tags


def get_readTime_from_cards(cards):
    #PULL READTIME FROM EACH CARD IN CARDS
    readingTimes=[]
    for card in cards:
        time = card.find("span", class_="readingTime")
        if time is not None:
            time = time['title']
            time = time.replace(" min read", "")
            readingTimes.append(time)
        else:
            readingTimes.append("0")
    return readingTimes


def get_applause_from_cards(cards):
    #PULL CLAPS FROM CARDS
    applause=[]
    for card in cards:
        claps=card.find("button", class_="button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents")
        if claps is not None:
            applause.append(claps.text)
        else:
            applause.append("0")
    return applause


def get_comment_from_cards(cards):
    #DETERMINES WHETHER THE TIMELINE CARD IS A COMMENT 1 IF COMMENT
    comments = []
    for card in cards:
        comment = card.find("div", class_="u-fontSize14 u-marginTop10 u-marginBottom20 u-padding14 u-xs-padding12 u-borderRadius3 u-borderCardBackground u-borderLighterHover u-boxShadow1px4pxCardBorder")
        if comment is not None:
            comments.append(1)
        else:
            comments.append(0)
    return comments



def get_urls_from_cards(cards):
    #GETS ARTICLE URLS FROM ALL CARDS
    urls = []
    for card in cards:
        url = card.find("a", class_="")
        if url is not None:
            urls.append(url['href'])
        else:
            raise Exception("couldnt find a url")
    return urls

def get_auth_urls_from_cards(cards):
    #PULLS AUTHORS URL ADDRESS FROM EACH CARD
    auth_urls = []
    for card in cards:
        url = card.find("a", class_="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken")
        if url is not None:
            auth_urls.append(url['href'])
        else:
            raise Exception("couldnt find a url")
    return auth_urls

def scrape_tag(tag, yearstart, monthstart, yearstop, monthstop):
    #-------------------------------------------------------------
    #INPUT CHECKS
    #1. MAKE SURE TAG IS VALID (no idea how to do this without exhaustive list... too much work )
    #2.CHECK VALID FILE PATH
    path = os.getcwd()
    path = path + "/TAG_SCRAPES/medium_"+tag+".csv"
    #3. TRY TO OPEN FILE PATH
    try:
        file = open(path, "w")
        file.close()
    except:
        raise Exception("Could not open file.")

    #4. MAKE SURE START DATE <= STOP DATE
    current_date = get_start_date(int(yearstart), int(monthstart), 1)
    end_date = get_start_date(int(yearstop), int(monthstop), 1)
    if current_date > end_date:
        raise Exception("End date exceeds start date.")
    else:
        None

#-----------------------------------------------------------------
    #BEGIN SCRAPE

    #BUILDS THE BASE URL FROM GIVEN TAG TO ITERATE ON
    base_url = base_url_builder(tag)
    #MEDIUM DENIES ANY COMMANDLINE REQUESTS, NEED BROWSER
    chrome_driver = open_chrome()

    #USE FIRSTPAGE TO ADD HEADERS TO CSV, USE COUNTER TO GET COMMANDLINE PREVIEW OF PROGRESS
    firstPage=True
    counter=0

    #START ITERATION OVER DATES
    while(current_date <= end_date):
        #BUILD URL FROM CURRENT_DATE
        url = url_masher(base_url,
                        str(current_date.year),
                        str(current_date.month),
                        str(current_date.day))

        #PARSE WEB RESPONSE

        response = chrome_driver.get(url)


        soup = BeautifulSoup(chrome_driver.page_source, features='lxml')

        #FIND ALL STORY CARDS, EACH IS AN ARTICLE
        cards = find_post_cards(soup)

        #PULL DATA FROM CARDS
        titles = get_titles_from_cards(cards)
        subtitles = get_subtitles_from_cards(cards)
        images = get_image_from_cards(cards)
        authors, pubs = get_auth_and_pubs_from_cards(cards)
        year, month, day, tags = get_dates_and_tags(tag,
                                        current_date.year,
                                        current_date.month,
                                        current_date.day,
                                        cards)
        readingTimes = get_readTime_from_cards(cards)
        applause = get_applause_from_cards(cards)
        urls = get_urls_from_cards(cards)
        auth_urls = get_auth_urls_from_cards(cards)
        comment = get_comment_from_cards(cards)

        #ACCUMULATE DATA INTO A DICTIONARY
        dict = {"Title":titles,"Subtitle":subtitles,"Image":images,"Author":authors, "Publication":pubs, "Year":year, "Month":month, "Day":day, "Tag":tags, "Reading_Time":readingTimes, "Claps":applause,"Comment":comment, "url":urls, "Author_url":auth_urls}

        #CHECK THAT DATA IN EACH CATEGORY IS THE SAME LENGTH
        vals = list(dict.values())
        for col in vals:
            if len(col)==len(cards):
                continue
            else:
                raise Exception("Data length does not match number of stories on page.")

        #CREATE DATAFRAME TO ORGANIZE AND SAVE TO CSV
        df = pd.DataFrame.from_dict(dict)

        #APPEND DATA TO FILE,
        # IF FIRSTPAGE-> ADD A HEADER
        if firstPage:
            with open(path, 'a') as f:
                df.to_csv(f, mode="a", header=True, index = False)
            firstPage=False
        #IF NOT FIRSTPAGE -> NO HEADER
        else:
            with open(path, 'a') as f:
                df.to_csv(f, mode="a", header=False, index=False)

        #ADDS A DAY TO THE CURRENT DATE FOR NEXT URL CALL
        current_date = current_date + timedelta(days=1)

        #PRINTS THE NUMBER OF TOTAL TIMELINE CARDS SAVED TO CSV
        counter = counter + len(cards)
        print(counter, "    ",current_date)
        time.sleep(2)
    chrome_driver.close()
