"""
提示模板
"""

ENRICH_REVIEW_PROMPT = """
请抽取下面评论中的实体。并根据抽取的实体和这条评论，为该评论分配一个讨论的话题。如果没有实体，请分配None。如果没有涉及话题，请分配None。同时给出一个20字以内的分析过程。

请看四个例子：
########
例子1：
--- 评论 ---
好消息  再过三天就 放假啦 坏消息 放假就是要出去玩 的更累[看]  然后回来上六天  哈哈哈哈哈[宕机][宕机][宕机][宕机][宕机][宕机][宕机][宕机]
########
--- 输出 ---
实体：None
话题：假期
分析：评论提及了“放假”、“出去玩”及“回来上六天”，围绕假期活动和工作日程展开。
########
例子2：
--- 评论 ---
因为我到现在也没懂什么是获得感
########
--- 输出 ---
实体：None
话题：心理感受/社会话题 
分析：评论表达了个人对“获得感”的理解困惑，涉及主观心理体验和社会议题。
########
例子3：
--- 评论 ---
就怕羊毛没薅到，假期在高速上度过[抠鼻]########
--- 输出 ---
实体：假期，高速
话题：假日出行 
分析：提及“假期”和“高速”，讨论节假日出行的拥堵情况。
########
例子4：
--- 评论 ---
[比心][比心][比心][比心][比心][比心]
--- 输出 ---
实体：None
话题：None
分析：评论仅包含表情符号，无具体信息提取实体或话题。
########
请分析下面的评论数据
--- 评论 ---
{}
--- 输出 ---
实体：
话题：
分析：
"""

GET_NE_TOPIC_PROMPT ="""
请抽取下面句子中的命名实体（Named Entity）。并抽取该句子在讨论的话题（Topic）。
如果没有命名实体，请分配None。如果没有涉及话题，请分配None。

请看四个例子：
########
例子1：
--- 句子 ---
成都以其独特的魅力在旅游市场中展现出较强的竞争优势
--- 输出 ---
实体：成都，旅游市场
话题：旅游/市场分析
########
例子2：
--- 句子 ---
大家对成都有什么评价？
--- 输出 ---
实体：成都
话题：城市评价/旅游意见 
########
例子3：
--- 句子 ---
就怕羊毛没薅到，假期在高速上度过[抠鼻]########
--- 输出 ---
实体：假期，高速
话题：假日出行 
########
例子4：
--- 句子 ---
[比心][比心][比心][比心][比心][比心]
--- 输出 ---
实体：None
话题：None
########
请分析下面的句子
--- 句子 ---
{}
--- 输出 ---
实体：
话题：
"""
GET_TARGET_TOPIC_PROMPT ="""
请识别下面句子谈论的对象（或目标）。并根据抽取的实体为该句子分配一个讨论的话题。
如果没有识别出谈论的“对象”，请分配None。
如果没有涉及话题，请分配None。

请看四个例子：
########
例子1：
--- 句子 ---
成都以其独特的魅力在旅游市场中展现出较强的竞争优势
--- 输出 ---
对象：成都
话题：旅游/市场分析
########
例子2：
--- 句子 ---
对比成都和长沙的旅游市场，谁更有优势？
--- 输出 ---
对象：成都，长沙
话题：旅游市场对比 
########
例子3：
--- 句子 ---
有什么小众的旅游城市推荐？
--- 输出 ---
对象：城市
话题：旅游地点的推荐 
########
例子4：
--- 句子 ---
[比心][比心][比心][比心][比心][比心]
--- 输出 ---
对象：None
话题：None
########
请分析下面的句子
--- 句子 ---
{}
--- 输出 ---
对象：
话题：
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
请根据用户提交的问题来判断每条评论数据是否和问题相关。
Question标记中首先给出了一个用户提交的问题。Reviews标记中给出了评论集合，每一行是一条评论。Results标记中给出了用”Yes“或”No“表示的相关性。
下面给出一个例子
###
例子：
Question:
成都有什么美食？
Reviews:
0. '来成都吃串串数签签[捂脸][捂脸]' 
1. '去隔壁成都吃  钵钵鸡[微笑]' 
2. '没想到成都还有这么好的地方，必须去看看，吃纯纯的成都火锅'
3. '以后还是来成都吧，成都烤匠好吃，最重要的是不可能有空包[尬笑]' 
4. '雅安石棉吃烧烤，比成都的好吃[赞]'
5. '成都天府红也有吧[微笑][捂脸]'
6. '笑死了想起来我上次去成都煮了8个鸡蛋全给我妹吃了'
Results:
0. Yes
1. Yes
2. Yes
3. Yes
4. No
5. No
6. No
###
任务要求：请根据每条评论是否与用户提交的问题相关，返回一个Yes或No的标记
Question:
{}
Reviews:
{}
Results:
"""

# 防止大模型幻觉的保守型提示模板
OPINION_SUMMARIZE_COT = """
下面给出用户的问题和评论数据。问题放在了Question标记下。评论数据放在了Reviews标记下，其中每行是一条评论。
######
Question: 
{}
Reviews:
{}
######
请按照下面的步骤思考，并产生答案：
1. 分析每条评论数据是否包含了回答问题需要的全部信息？如果没有，请结束作答，返回文本"没有相关信息"。
2. 仅仅根据有效的评论数据内容回答问题，产生答案，不要自我发挥。
3. 判断答案的内容是否超出了给出的评论数据的范围。如果是，请停止作答，返回文本"没有相关信息"。
答案字数限制在{}字以内。
"""

# 大模型有更大总结能力的提示模板
OPINION_SUMMARIZE_PE = """
下面给出用户的问题和评论数据。问题放在了Question标记下。评论数据放在了Reviews标记下，其中每行是一条评论。
######
Question: 
{}
Reviews:
{}
######
请根据评论数据来回答问题，答案字数限制在{}字以内。
"""