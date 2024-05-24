from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

def get_html():
    try:
        path = 'result.txt'
        with open(path, 'r') as f:
            result = f.read()
            f.close()
        return(result)
    except:
        print('Could not read file...')
        return (None)
    
def parse_html():
    try:
        if get_html() != None:
            result = get_html()
            soup = BeautifulSoup(result, 'html.parser') #type: ignore
            title_list = soup.find_all('span', class_= 'titleline')
            subs = soup.find_all('td', class_='subtext')

            TITLE = []
            URL = []
            POINTS = []
            for items in title_list:
                title = items.find('a').text
                TITLE.append(title.strip())
                url = items.find('a')['href']
                URL.append(url.strip())
            
            for sub in subs:
                try:
                    point = sub.find('span', class_ = 'score').text.strip()
                    point.split(' ')
                    point = point[0]
                    POINTS.append(point)
                except:
                    point = ''
                    POINTS.append(point)
            return(
                TITLE,
                URL,
                POINTS
            )
        else:
            print('None was returned')
            return (None)
    except:
        print('There is something wrong somewhere')
        return(None)

def pandalize():
    try:     
        if parse_html() != None:
            title, url, points = parse_html() #type: ignore
            data = {
                'TITLE': title,
                'URL':url,
                'POINTS':points
            }
            df = pd.DataFrame(data)
            df_points = pd.Series(points)
            df.to_csv('data/df_bsoup.csv')
            #df_points.to_csv('data/df_points.csv')
            return(df)
        else:
            print('Something went wrong while pandalizing data')
            return (None) #type: ignore
    except:
        print('Something went wrong while pandalizing...')
        return None #type:ignore
    
if __name__ == '__main__':
    try:
        service = Service()
        options = Options()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(service = service, options = options)
        driver.get('https://news.ycombinator.com/')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        with open('result.txt', 'w') as f:
            f.write(soup.prettify())
            f.close
    except:
        print('Something went wrong in the main...')
    finally:
        driver.close()

    pandalize()