# Natural Language Processing Project
# Text processing & data retrieval system

The Reuters-21578 dataset is a collection of documents with news articles. The original corpus has 10,369 documents and a vocabulary of 29,930 words.

The goal of this project is to experiment with text processing with NLTK, and Python.

The project is divided into 4 parts:

Part 1 - Developed a pipeline to read data, extract it, tokenize it, lowercase it, apply the Porter Stemmer algorithm to it (to reduce the words to their root, eg. jumping -> jump), and remove stop words. In each step of the pipeline, the results are exported to a .txt file for clarity. Every step of the pipeline is also a separate function, given that modularity allows for better debugging.

Part 2 - Implemented a naive indexer (stores words and their locations), and a single-term query processing system (handles search for individual words).

Part 3 - Refined the indexing procedure. Implemented ranking of returns.

(MISPLACED) Part 4 - Experimented with web crawling (using Spidy), scraping, and indexing a set of web documents from my university's official website. Also experimented with the AFINN sentiment analysis script.
