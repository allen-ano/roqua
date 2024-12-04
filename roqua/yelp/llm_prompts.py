"""
prompts
"""

ENRICH_REVIEW_PROMPT = """
please extract the entities from the following review and assign the topics for the review.
Also, please give your reason why you assign the topic within 20 words.

We show you with two examples below.
########
Example 1:
--- review ---
The food is very good, the prices fair and the atmosphere can't be beat!  The staff is friendly and efficient.  My personal fave is the Florentine Benedict.  This is a go to spot for us every time we are in Vegas! Tip: Use Open Table to reserve your table before walking over!
--- outputs ---
Entities: Food, Prices, Atmosphere, Staff, Florentine Benedict, Vegas, Open Table
Topics: Food Quality, Pricing, Ambiance, Service, Dish
Analysis: Each entity clearly aligns with specific aspects of the dining experience mentioned in the review.
########
Example 2:
--- review ---
Wow! Just wow! What a great place to spend a night enjoying a great steak dinner. I must admit I didn't pay the bill so I can't comment on that buy my filet was cooked to perfection and the frites were on point ;) Would definitely come back!
--- outputs ---
Entities: Vegas, Restaurant, Food, Service
Topics: Dining Experience, Food Quality
Analysis: The review emphasizes positive aspects of the meal and dining atmosphere, indicating a strong focus on the dining and food quality experience.
########
please analyze the following review.
--- review ---
{}
--- outputs ---
Entities:
Topics:
Analysis:
"""

GET_NE_TOPIC_PROMPT ="""
Please extract the entities from the following sentence and assign topics for the sentence. 
If you cannot find entities, please give a label of None. 
If this sentence does not involve a certain topic, please give a label of None.

We show you with two examples below.
########
Example 1:
--- sentence ---
The food is very good, the prices fair and the atmosphere can't be beat!  The staff is friendly and efficient. 
--- outputs ---
Entities: Food, Prices, Atmosphere, Staff
Topics: Food Quality, Pricing, Ambiance, Service
########
Example 2:
--- sentence ---
Wow! Just wow! What a great place to spend a night enjoying a great steak dinner. 
--- outputs ---
Entities: steak, dinner
Topics: Dining Experience
########
please analyze the following sentence.
--- sentence ---
{}
--- outputs ---
Entities:
Topics:
"""

EXP1_PROMPT = """
You are provided a question and a set of reviews. Please attempt to find the answer from the reviews. Your answer should be one of three options: 'yes', 'no', and '?'.
If you can find a positive answer from the reviews, please give a reply 'yes'.
If you can find a negative answer from the reviews, please give a reply 'no'.
If you fail to find the answer, please give a reply '?'.

You are given three examples:
########
Example 1:
Question: can you mount a sound bar using the external `` stick '' arms vertically hanging below the lcd monitor ( 27 inch ) ?
Reviews:
0. it holds a 27 '' lcd monitor ( about 20-25lbs ) . 
1. if you extend both arms in the same direction , the tv ( 30 inch ) tilts . 
2. i purchased a 27 & # 34 ; monitor for my wife and this mount really frees up the desktop real estate .
3. this was needed to mount a 32 '' lcd that weighs 27 lbs in my bedroom. 
4. once that 's done , using the bracket mounted on the tv , you hang the tv on the wall mount and secure it with a single bolt . 
5. lcd tv to the mount . 
6. my mistake was , based on the diagrams , i assumed that the length of both the swinging arms of the mount ( the single and the double arms ) were of the same length . 
7. i will say that the joints in the arms are quite stiff - it can take a little muscle to move the tv . 
8. just remember the spacers go under the arms if you have to use them and you will be ok .
9. some complain that the back plate was too big for the tv they used but it 's fits perfect on the lg 32 lk450 32-inch 1080p 60hz lcd hdtv i am using it on. works perfectly for the area of the room i am using it in which allows me to rearrange the room without the need to move the tv.

Answer: 'yes'
########
Example 2:
Question:  does the tablet have sim card capability ?
Reviews: 
0. i also bought a 32gb memory card for it. 
1. the size of the tablet makes it an ideal alternative to cranking up my desktop , or unpacking my notebook , during the limited time i have before leaving for work . 
2. the video viewer works great with avi files and the audio player does a fair job with earbuds attached.i did n't purchase this tablet to play games , or read books . 
3. craig electronics cmp741d 7-inch tablet it lasted a couple of weeks , but then i dropped it by accident and the screen shattered , it worked great until then , but i did not have it long enough , so now i need to get another one still checking out diff brands. 
4. the craig android does a very good job retrieving messages from five separate accounts , including web access to a secure work account . 
5. this tablet is just the right size and price for my 14 year old daughter .
6. i purchased the craig tablet primarily to receive e-mail over my home wi-fi connection .
7. i do n't expect it to compare to a high price tablet . 
8. this tablet works fine but there are much nicer ones for the same money like the velocity or pandigital . 
9. the internet speed is adequate and the screen display is very functional .

Answer: '?'
########
Example 3:
Question: does this case have a handle ?
Reviews': 
0. granted the tablet does have about a half inch overall space around inside the case . 
1. i wish it would do so when i have my case cover on as well but it will only handle just the tab without the case - will not seal properly with any case on the tab . 
2. product does a great job at keeping devices from getting crushed .
3. i have a bear motion cover for the mini and it fits snug in this pelican 1055 case .
4. it was obviously made to hold 7 and perhaps 8 inch tablets , which it does .
5. i have a gell skin protector on the tablet .
6. seals well , although i have not submerged it and do n't plan to i have full confidence in it .
7. maybe pelican should have included a couple press in pads .

Answer: 'no'
########
Please answer the following question based on the following reviews.
Question: {}
Reviews: 
{}

Answer:
"""

EXP2_PROMPT = """
You are provided a question and a set of reviews. Please attempt to find the answer from the reviews. 
If a review positively addresses the question, please reply 'yes'."
If a review negatively addresses the question, please reply 'yes'."
If you fail to find the answer or find contradictory answers, please give a reply '?'.
Please explain your thought process.
########
Please answer the following question based on the following reviews.
Question: {}
Reviews: 
{}

Answer:
"""


EXP3_PROMPT = """
You are provided a question and a review. Please make sure if the review provides useful information to answer the question. 
If you think that the review is useful, please reply 'yes'. Otherwise, 'no'.

You are given two examples:
########
Example 1:
Question: can you mount a sound bar using the external `` stick '' arms vertically hanging below the lcd monitor ( 27 inch ) ?
Reviews: i will say that the joints in the arms are quite stiff - it can take a little muscle to move the tv . 
Answer: 'no'

########
Example 2:
Question: will it fit vizio tvs?
Reviews: took a bit of work , but used this to fit an older vizio 32 & # 34 ; monitor to the wall to use as a compute monitor .
Answer: 'yes'

########
Please answer the following question based on the following reviews.
Question: {}
Reviews: {}

Answer:
"""

EXP4_PROMPT = """
You are provided a question and a review. Please attempt to find the answer for the question from the review.
Your answer should be one of three options: 'yes', 'no', and '?'.
If you can find a positive answer from the review, please give a reply 'yes'.
If you can find a negative answer from the review, please give a reply 'no'.
If you fail to find the answer, please give a reply '?'.

########
Please answer the following question based on the following review.
Question: {}
Reviews: {}
Answer:
"""

QUESTION_REVIEW_RELATIVE="""
The user's question is marked under the 'Question' tag, and reviews are listed under the 'Reviews' tag. 
Evaluate if each review is related to the question. Under the 'Results' tag, list 'yes' for relevant reviews and 'no' for irrelevant ones.

You are given an example:
########
Question:
What delicious foods are there in Chengdu?
Reviews:
0. 'Come to Chengdu to eat hotpot.' 
1. 'The barbecue in Ya'an is better than in Chengdu'
2. 'Chengdu has giant pandas.'
3. 'Laughing to think I boiled eight eggs for my sister to eat last time I went to Chengdu'
Results:
0. yes
1. no
2. no
3. no
###
Please start your analysis.
Question:
{}
Reviews:
{}
Results:
"""

SEGMENT_REVIEW="""
Please segment the review under the tag of 'Review' into a list of sentences according to the involved topics.
The results are presented in a form of :
1. Topic: sentence sentence   ...
2. Topic: sentence sentence   ...

we show you an example.
######
Review: 
Excellent!! We had the brie appetizer and filet mignon.  Best steak I have ever had!!  Great location too - ask to sit outside to see the Bellagio fountains.  Very reasonably priced too. Highly recommend!!
Results:
1. Food Quality: Excellent!! We had the brie appetizer and filet mignon. Best steak I have ever had!!
2. Location and Atmosphere: Great location too - ask to sit outside to see the Bellagio fountains.
3. Pricing: Very reasonably priced too.
4. Overall Recommendation: Highly recommend!!
######
please start your task.
Review:
{}
Results:
"""

EXTRACT_NE_PROMPT ="""
Please extract the entities from the following sentence. 
If you cannot find entities, please give a label of None. 

We show you with two examples below.
########
Example 1:
--- sentence ---
The food is very good, the prices fair and the atmosphere can't be beat!  The staff is friendly and efficient.  My personal fave is the Florentine Benedict.  This is a go to spot for us every time we are in Vegas! Tip: Use Open Table to reserve your table before walking over!
--- outputs ---
Entities: Food, Prices, Atmosphere, Staff, Florentine Benedict, Vegas, Open Table
########
Example 2:
--- sentence ---
Wow! Just wow! What a great place to spend a night enjoying a great steak dinner. I must admit I didn't pay the bill so I can't comment on that buy my filet was cooked to perfection and the frites were on point ;) Would definitely come back!
--- outputs ---
Entities: Vegas, Restaurant, Food, Service
########
please analyze the following sentence.
--- sentence ---
{}
--- outputs ---
Entities:
"""

# 防止大模型幻觉的保守型提示模板
OPINION_SUMMARIZE_COT = """
The user's question and review data are provided below. The question is marked under Question tag, and the review data is marked under Reviews tag, with each line representing one review.
######
Question: 
{}
======
Reviews:
{}
######
Please follow these steps to think and generate an answer:
1. Analyze whether each review contains all the necessary information to answer the question. If not, stop answering and return the text "No relevant information."
2. Answer the question based solely on the valid content of the reviews, without adding any personal interpretation.
3. Determine if the answer exceeds the scope of the given review data. If so, stop answering and return the text "No relevant information."
The answer should be limited to {} characters.
"""

OPINION_SUMMARIZE_PE = """
The user's question appears beneath the 'Question' tag. 
Each individual review is listed under the 'Reviews' tag, with each review on a new line.
######
Question: 
{}
======
Reviews:
{}
######
Please answer the user's question based on the reviews. 
Do not generate any extra content beyond the provided information. Answers are limited to {} words.
"""