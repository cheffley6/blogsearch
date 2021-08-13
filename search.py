from flask import Flask, request
import requests

from blogspot_urls import BLOGSPOT_URLS_BY_CHARACTER_ID, CHARACTER_IDS, CHARACTER_NAMES_BY_ID
from blog_interface import get_titles_and_links
from html_assets import HTML_BLOG_ENTRY_TEMPLATE, HTML_HEADER_TEMPLATE, HTML_OVERALL_TEMPLATE, HTML_SEARCH_RESULTS_TEMPLATE

app = Flask(__name__)


def generate_blogs(search_terms):
    blogs = []
    for character_id in CHARACTER_IDS:
        blogs.append(
            {
                "character_id": character_id,
                "blogs": get_titles_and_links(character_id, search_terms)
            }
        )

    return blogs

def format_blogs(blogs):
    
    formatted_blogs = ""

    for blog in blogs:
        if len(blog['blogs']) == 0:
            continue
        formatted_blogs += HTML_HEADER_TEMPLATE.format(CHARACTER_NAMES_BY_ID[blog['character_id']])
        for post in blog['blogs']:
            formatted_blogs += HTML_BLOG_ENTRY_TEMPLATE.format(post['link'], post['title'])

    return HTML_OVERALL_TEMPLATE.format(formatted_blogs)



@app.route("/blogsearch")
def handle_search_endpoint():
    search_terms = request.args.get('search_terms')
    blogs = generate_blogs(search_terms)

    prepared_elements = format_blogs(blogs)

    return HTML_SEARCH_RESULTS_TEMPLATE.format(search_terms) + prepared_elements
    # return f"<p>Hello, World! You searched the terms: {search_terms}</p>"

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=3251, debug=True)
