from bs4 import BeautifulSoup
import requests
import numpy as np

def get_scrape_google_scholar(author):

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url = f"""https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={author.replace(' ', '+')}&btnG="""
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content)

    table = soup.find_all("table")

    personal_url = table[0].findAll('a')[0]['href']

    full_url = 'https://scholar.google.com/' + personal_url

    response=requests.get(full_url,headers=headers)
    new_soup = BeautifulSoup(response.content)

    citations = []
    titles = {}
    for s in new_soup.find_all('tbody'):
        articles = s.findAll("tr", {"class": "gsc_a_tr"})
        for article in articles:
            title = article.findAll('a')[0].text
            citation = article.findAll('a')[1].text
            
            titles[title] = citation
            if citation != '':
                citations += [eval(citation)]

    citations.sort()

    citations = np.array(citations)

    h_index = np.arange(len(citations))[np.arange(len(citations)) > citations[::-1]][0]
    
    print(h_index)
    return titles
    

if __name__ == "__main__":
  
    name = 'Arjun Savel'
    
    try:
        paper_dict = get_scrape_google_scholar(name)
    except requests.Timeout as err:
        print('Timeout error')
        print(err)
        time.sleep(60)
        paper_dict = get_scrape_google_scholar(name)
        
    with open("../data/google_scholar_scrape.json", "w") as f:
        json.dump(paper_dict, f, sort_keys=True, indent=2, separators=(",", ": "))
