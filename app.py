from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB client setup
client = MongoClient('mongodb://localhost:27017/')
db = client.arxivDB
articles_collection = db.articles

def get_DOI_AND_PROJECT(article_link):
    response = requests.get(article_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        project_element = soup.find('a', class_="link-external link-https")
        project = project_element.get("href") if project_element else 'project not found'
        doi_element = soup.select_one('td.tablecell.doi a')
        doi = doi_element.get("href") if doi_element else 'DOI not found'
                
        references_citations = []
        ref_cite_section = soup.find('div', class_='extra-ref-cite')
        if ref_cite_section:
            refs = ref_cite_section.find_all('a', href=True)
            for ref in refs:
                references_citations.append({
                    'text': ref.text.strip(),
                    'href': ref['href'],
                })

        pdf_link = 'https://arxiv.org'+ soup.find('a', class_="abs-button download-pdf")['href']

        
        return project, doi, references_citations, pdf_link
    return '', '', '', ''

def fetch_article_info(keywords):
    formatted_keywords = '+'.join(keywords.split())
    url = f"https://arxiv.org/search/?query={formatted_keywords}&searchtype=all&abstracts=show&order=-announced_date_first&size=50"
    response = requests.get(url)
    articles_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('li', class_='arxiv-result')

        for article in articles[:10]: # Only process the first 10 results
            data = {}
            title_element = article.find('p', class_='title is-5 mathjax')
            data['title'] = title_element.text.strip() if title_element else "Title not found"

            authors_element = article.find('p', class_='authors')
            data['author_names'] = ', '.join([a.text for a in authors_element.find_all('a')]) if authors_element else "Authors not found"

            abstract_element = article.find('span', class_='abstract-full has-text-grey-dark mathjax')
            data['abstract'] = abstract_element.text.strip().replace("Abstract: ", "") if abstract_element else "Abstract not found"

            keywords_elements = article.find_all('span', class_='search-hit mathjax')
            data['makale_anahtar_kelimeleri'] = [kw.text for kw in keywords_elements] if keywords_elements else []


            submission_info_element = article.find('p', class_='is-size-7')
            data['submission_date'] = submission_info_element.text.split(";")[0].replace("Submitted", "").strip() if submission_info_element else "Submission date not found"

            list_title_element = article.find('p', class_='list-title is-inline-block')
            data['arxiv_id'] = list_title_element.a.text.strip() if list_title_element and list_title_element.a else "arXiv ID not found"
            data['arxiv_link'] = list_title_element.a['href'] if list_title_element and list_title_element.a else "Link not found"

            project_link, doi, reference, pdf_link = get_DOI_AND_PROJECT(data['arxiv_link'])
            data['doi'] = doi
            data['project_link'] = project_link
            data['reference'] = reference

            data['pdf_link']=pdf_link

            articles_collection.insert_one(data)

            articles_data.append(data)

    return articles_data


# Filtreleme fonksiyonu burada tanımlanacak
def filter_articles(author_names=None, submission_date=None):
    query = {}
    if author_names:
        query['author_names'] = {'$regex': author_names, '$options': 'i'}
    if submission_date:
        query['submission_date'] = submission_date

    articles = list(articles_collection.find(query).sort("submission_date", -1).limit(10))
    return articles

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        author_names = request.form.get('author_names')
        submission_date = request.form.get('submission_date')
        
   
        if keywords:
            articles = fetch_article_info(keywords)
        else:
            articles = filter_articles(author_names, submission_date)
        
        # This ensures that a response is returned after POST request processing.
        return render_template('results.html', articles=articles)
    else:
        # Handles the GET request path.
        articles = list(articles_collection.find().sort("title", 1))
        return render_template('index.html', articles=articles)

    return redirect(url_for('index'))


@app.route('/article/<article_id>')
def article_detail(article_id):
    article = articles_collection.find_one({'_id': ObjectId(article_id)})
    if article:
        return render_template('article_detail.html', article=article)
    else:
        return "Makale bulunamadı", 404

if __name__ == '__main__':
    app.run(debug=True)