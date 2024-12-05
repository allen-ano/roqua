# ***ROQuA***: an opinion question-answering framework on e-commerce reviews
This website provides the datasets and source codes in our work of 

***An RAG-based Opinion Question-Answering Framework on E-commerce Reviews***

We build a [demonstration plateform](http://roqua.cpolar.top/). Owing to GPU rental expenses, QA functionality will be accessible from December 15, 2024, to January 15, 2025.

<hr>

1. The folder of 'qa-data' contains three question-answering dataset used in our work.
2. The reviews of jd, douyin and yelp can be found in [Google Drive](https://drive.google.com/drive/folders/18zInItjabNENuz6Q71lvND7nExDGj7zu?usp=sharing) . They are SQLite databases. Download these db files and put douyin_reviews.db and yelp_qa_reviews.db under douyin/data and yelp/data, respectively.
3. dp_* indicates the data processing files.
4. fn_* indicates the modules in ROQuA.
5. First, set parameters in parmeters.py under douyin and yelp folder, respectively.
6. Second, run dp.py to process data before runing ROQuA.
7. test.ipynb in folder of 'roqua' provides an interface for using ROQuA. 
