from blogspot_urls import BLOGSPOT_URLS_BY_CHARACTER_ID
import bs4 as bs
import urllib.request



# returns: 
# [
#   {
#     "title": <title of blog post>
#     "link": <link to that blog post>    
#   }, ...
# ]
def get_titles_and_links(character_id, search_terms):
    print(f"searching {search_terms} for {character_id}")
    
    url = BLOGSPOT_URLS_BY_CHARACTER_ID[character_id]
    response = urllib.request.urlopen(url + f"search?q={search_terms}")
    
    assert response.status == 200

    content = response.read()

    soup = bs.BeautifulSoup(content, "lxml")

    titles = soup.find_all("h3", {"class": "post-title"})
    titles = [title.text.strip() for title in titles]

    links = soup.find_all("a", {"title": "permanent link"})
    links = [link['href'] for link in links]

    return [
        {
            "title": title,
            "link": link
        } for title, link in zip(titles, links)
    ]
