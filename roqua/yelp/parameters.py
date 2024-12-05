"""
global parameters
"""

class Parameters:
    encoder = '/root/autodl-tmp/deberta-v3-base'

    # original reviews
    # rdb = "yelp/data/yelp_qa_reviews.db"
    # enriched_reviews = "yelp/data/yelp_enriched_review.json"
    # review_vdb = "yelp/data/yelp_review_milvus.db"
    # topic_vdb = "yelp/data/yelp_topic_milvus.db"
    # indexdir = "yelp/data/yelpindex"

    # splited reviews
    rdb = "yelp/data/yelp_QA_short_reviews.db"
    enriched_reviews = "data/yelp_enriched_short_review.json"
    review_vdb = "yelp/data/yelp_short_review_milvus.db"
    topic_vdb = "yelp/data/yelp_short_topic_milvus.db"
    indexdir = "yelp/data/yelpshortindex"
