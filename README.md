# An NLP Project to Cast Actors in Hypothetical Movies

## Overview

This project utilizes a NLP technique of Topic Modeling and Clustering to match similar people based on their Wikipedia biographies. In this particular case, I compared and matched historical figures and actors. [See Details on Blog.](http://www.chicagoan.io/casting-movies-by-topic-modeling-and-clustering-wikipedia-pages/)
 

## Data

Documents were retrieved, cleaned, and stored on MongoDB.
* `nlp/scraping.py`
    * Parses the Wikipedia pages.
* `wrangling/cast.py`
    * Used for storing/retreiving data on MongoDB
## Modeling
* `nlp/models.py`
    * Function Applications of the following NLP concepts:
        * TF-IDF Vectorizer
        * SVD/LSA Topic Modeler
        * K-Means Clustering

## Notebook
* `notebooks/modelingv3` 
