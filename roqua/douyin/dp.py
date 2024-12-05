"""
data process in a pipeline
"""
import douyin.dp_EnrichReview as enrich
import douyin.dp_buildindex as index
import douyin.dp_buildVDB as vdb
from douyin.parameters import Parameters as params

rdb = params.rdb
enriched_reviews = params.enriched_reviews
review_vdb = params.review_vdb
topic_vdb = params.topic_vdb
indexdir = params.indexdir

# pipeline
enrich.run(rdb, enriched_reviews)
print("finish enrich...")

index.build_index(indexdir, enriched_reviews)
print("finish build inverted index...")

vdb.run(enriched_reviews, review_vdb, topic_vdb)
print("finish build VDB...")