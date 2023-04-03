from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque
import requests
import sqlite3
import logging
import nltk
import time 
import re

class Crawler:
    def __init__(self):
        self.visited_urls = set()
        self.index = {}
        self.conn = sqlite3.connect('crawler.db')
        self.cursor = self.conn.cursor()
        self.url_queue = deque()

        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))

        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        # Add a console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # Define the log message format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                content TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_occurrences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER,
                word_id INTEGER,
                FOREIGN KEY(page_id) REFERENCES pages(id),
                FOREIGN KEY(word_id) REFERENCES words(id)
            )
        ''')

        self.conn.commit()

    def crawl(self, url):
        self.logger.debug(f"Crawling {url}...")
        # Parse URL
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc

        # Crawl the initial URL
        self._crawl_url(base_url, url)

        # Keep crawling until there are no more links to crawl
        while True:
            # Get the next URL to crawl
            next_url = self._get_next_url()
            if next_url is None:
                break

            # Crawl the URL
            self._crawl_url(base_url, next_url)
            self.logger.debug('Crawling finished for %s', next_url)
        return 'Crawling complete'
    
    def _get_next_url(self):
        # Return the next URL in the queue, if there is one
        if self.url_queue:
            next_url = self.url_queue.popleft()
            return next_url
        # If there are no unvisited URLs, return None
        return None        
    
    def _crawl_url(self, base_url, url):
        # Check if URL has already been visited
        if url in self.visited_urls:
            return
        
        # Fetch the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Add page to database
        self.cursor.execute('INSERT OR IGNORE INTO pages (url, content) VALUES (?, ?)', (url, soup.get_text()))
        page_id = self.cursor.lastrowid
        
        # Add words and word occurrences to database
        words = self._get_words(soup.get_text())
        for word in words:
            word_id = self._get_word_id(word)
            self.cursor.execute('INSERT INTO word_occurrences (page_id, word_id) VALUES (?, ?)', (page_id, word_id))
        
        # Add URLs to queue
        for link in soup.find_all('a'):
            link_url = link.get('href')
            if link_url is not None and not self._is_external_link(base_url, link_url):
                self._add_url_to_queue(base_url, link_url)
        
        # Mark URL as visited
        self.visited_urls.add(url)
        self.conn.commit()


    def _get_word_id(self, word):
        self.cursor.execute('INSERT OR IGNORE INTO words (word) VALUES (?)', (word,))
        self.cursor.execute('SELECT id FROM words WHERE word = ?', (word,))
        return self.cursor.fetchone()[0]

    def _get_words(self, text):
        """Extracts all words from a text string, removing punctuation and digits."""
        words = []
        for word in text.split():
            # Remove punctuation and digits from word
            cleaned_word = re.sub(r'[^\w\s]', '', word)
            cleaned_word = re.sub(r'\d+', '', cleaned_word)
            cleaned_word = cleaned_word.lower()
            # Add cleaned word to list if not empty
            if cleaned_word:
                words.append(cleaned_word)
        return words

    def _is_external_link(self, base_url, link_url):
        """Return True if the link is external, False otherwise."""
        # Parse the base URL and the link URL
        parsed_base_url = urlparse(base_url)
        parsed_link_url = urlparse(link_url)
    
        # Compare the hostname of the base URL and the link URL
        return parsed_base_url.netloc != parsed_link_url.netloc

    def _add_url_to_queue(self, base_url, url):
        # Convert the URL to a canonical form
        url = self._canonicalize_url(base_url, url)
        if url not in self.visited_urls and url not in self.url_queue:
            self.url_queue.append(url)

    def _canonicalize_url(self, base_url, url):
        return urljoin(base_url, url)
                
    def _add_url(self, url):
        if url not in self.visited_urls:
            self.visited_urls.add(url)

    def _get_page_ids(self, word):
        conn = sqlite3.connect('crawler.db')
        cursor = conn.cursor()

        # Get the IDs of pages that contain the word
        query = '''
            SELECT page_id
            FROM word_occurrences wo
            JOIN words w ON wo.word_id = w.id
            WHERE w.word = ?
        '''
        cursor.execute(query, (word,))
        page_ids = [row[0] for row in cursor.fetchall()]

        conn.close()
        return page_ids

    def search(self, query):
        self.logger.debug('Searching for %s', query)
        query_words = query.lower().split(" ")

        # GET the set of pages for each word
        page_sets = []
        for word in query_words:
            page_ids = self._get_page_ids(word)
            page_sets.append(set(page_ids))

        # Intersect all page sets to get URLs that contain all query words
        if page_sets:
            result_set = page_sets[0].intersection(*page_sets[1:])
        else:
            result_set = set()

        # Check if result_set is empty
        if not result_set:
            self.logger.debug('No results found for %s', query)
            return "No results found for query: {}".format(query)

        urls = [self._get_url_by_page_id(page_id) for page_id in result_set]
        corpus = [self._get_content_by_url(url) for url in urls]
        tfidf = TfidfVectorizer(tokenizer=word_tokenize, stop_words='english')
        tfidf_matrix = tfidf.fit_transform(corpus)
        query_vec = tfidf.transform([query])
        cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        document_scores = list(zip(urls, cosine_similarities))
        document_scores = sorted(document_scores, key=lambda x: x[1], reverse=True)
        self.logger.debug('Search finished for %s', query)

        top_result = document_scores[0]
        return top_result[0]



    def wn_search(self, query):
        self.logger.debug('WordNet search for %s', query)
        # Tokenize the query into individual words
        query_words = nltk.word_tokenize(query.lower())
        # Get all synsets for each query word
        synsets = []
        for word in query_words:
            synsets.extend(wordnet.synsets(word))
        if not synsets:
            self.logger.debug('WordNet search no synsets found for %s', query)
            return f"No results found for query: {query}"
        
        # Get all unique query words from the synsets
        query_words = set()
        for synset in synsets:
            for lemma in synset.lemmas():
                word = lemma.name().lower()
                query_words.add(word)

        # Get all page sets for each query word
        page_sets = []
        for word in query_words:
            page_ids = self._get_page_ids(word)
            page_sets.append(set(page_ids))

        # Intersect all page sets to get URLs that contain all query words
        if page_sets:
            result_set = page_sets[0].intersection(*page_sets[1:])
        else:
            result_set = set()

        # Compute document scores using TF-IDF and cosine similarity
        urls = [self._get_url_by_page_id(page_id) for page_id in result_set]

        # Verify if has any URLs
        if not urls:
            self.logger.debug('WordNet search no URLs found for %s', query)
            return f"No results found for query: {query}"
        
        corpus = [self._get_content_by_url(url) for url in urls]
        tfidf = TfidfVectorizer(tokenizer=word_tokenize, stop_words='english')
        tfidf_matrix = tfidf.fit_transform(corpus)
        query_vec = tfidf.transform([query])
        cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        document_scores = list(zip(urls, cosine_similarities))
        document_scores = sorted(document_scores, key=lambda x: x[1], reverse=True)
        self.logger.debug('WordNet search finished for %s', query)

        top_result = document_scores[0]
        return top_result[0]


    def _get_url_by_page_id(self, page_id):
        self.cursor.execute('''
            SELECT url FROM pages WHERE id = ?
        ''', (page_id,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

    def _get_content_by_url(self, url):
        self.cursor.execute('''
            SELECT content FROM pages WHERE url = ?
        ''', (url,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None