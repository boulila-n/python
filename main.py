from bs4 import BeautifulSoup
import requests
import urllib.request
import pandas as pd


def downloadImg(srcUrl, imgname):
    urllib.request.urlretrieve(srcUrl, './venv/images/'+ imgname[0:16]+'.jpg')

def getBookInformations(url, path):
  try:
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        td = soup.findAll("td")
        print(" universal_ product_code (upc): ", td[0].text, "\n",
        "price_including_tax: ", td[2].text, "\n",
        "price_excluding_tax: ", td[3].text, "\n",
        "number_available: ", td[5].text)
        title = soup.find("h1")
        print(" Title: ", title.text)

        p = soup.find_all('p')
        print(" product_description: ", p[3].text)

        a = soup.findAll("a")
        print(" Category: ", a[3].text)

        rating = soup.select_one('.star-rating')
        print(" review_rating: ", rating.attrs.get('class')[1])

        img = soup.find("img")
        img1=img.attrs.get('src')
        srcUrl = 'http://books.toscrape.com/'+ img1[5:len(img1)]
        downloadImg(srcUrl, title.text)
        print(" image_url: ", srcUrl)

        print(" product_page_url: ", url)
        print("#############","\n")

        infos = pd.DataFrame([[title.text, rating.attrs.get('class')[1], td[2].text, td[3].text, td[5].text, p[3].text, a[3].text, srcUrl, url]],
                             columns=['title', 'review_rating', 'price_including_tax','price_excluding_tax','number_available','product_description','Category','image_url','product_page_url'])

        infos.to_csv(path, mode='a', header= False, index=False)



  except Exception as e:
      print(e)

def getCategoryPage(url1, path):
    response = requests.get(url1)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        row = soup.find('ol', {'class':'row'})

        for link in row.findAll('h3'):
            url2 = link.find('a').get('href')
            l = len(url2)
            getBookInformations('http://books.toscrape.com/catalogue/'+url2[9:l], path)

        next = soup.find('li', {'class': 'next'})
        if next:
            next_url = url1.replace('index.html', next.find('a').get('href'))
            getCategoryPage(next_url, path)


## methode main
url3 = 'http://books.toscrape.com/index.html'
response = requests.get(url3)
if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    row = soup.find('aside', {'sidebar col-sm-4 col-md-3'})
    links = row.findAll('a')
    for i in range(1, len(links)):
        urlc = links[i].get('href')
        cg_name = urlc[25:len(urlc)].replace('/index.html', '')

        path = cg_name+".csv"
        f = open(path, "x")
        infos = pd.DataFrame([],
                             columns=['title', 'review_rating', 'price_including_tax', 'price_excluding_tax',
                                      'number_available', 'product_description', 'Category', 'image_url',
                                      'product_page_url'])

        infos.to_csv(path, mode='a', header=True, index=False)
        f.close()
        getCategoryPage('http://books.toscrape.com/' +urlc, path)





