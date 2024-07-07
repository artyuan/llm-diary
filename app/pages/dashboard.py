import streamlit as st
from prompts import new_prompt, instruction_str, context, instruction_str_ner
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llamaindex_rag import query_engine
from llama_index.experimental.query_engine import PandasQueryEngine
from plots import *
import pandas as pd
import os
from nlp import *


st.set_page_config(
    page_title="Hello",
    page_icon=":chart_with_upwards_trend:",
)
base_dir = os.path.dirname(__file__)[:-10]
csv_path = os.path.join(base_dir, 'data', 'stats','emotions_df.csv').replace('\\', '/')
emotions_df = pd.read_csv(csv_path)
text_df = pd.read_csv("data/text/text.csv")

min_date = emotions_df['record_dt'].min()
min_date = datetime.strptime(min_date, '%Y-%m-%d').date()
max_date = emotions_df['record_dt'].max()
max_date = datetime.strptime(max_date, '%Y-%m-%d').date()

with st.sidebar:
    begin_dt = st.date_input("Start date", value=min_date, label_visibility="visible")
    begin_dt = begin_dt.strftime("%Y-%m-%d")

    end_dt = st.date_input("End date", value=max_date, label_visibility="visible")
    end_dt = end_dt.strftime("%Y-%m-%d")

# Filtering datasets based on the selected date
emotions_df = emotions_df[(emotions_df['record_dt'] >= begin_dt) & (emotions_df['record_dt'] <= end_dt)]
text_df = text_df[(text_df['record_dt'] >= begin_dt) & (text_df['record_dt'] <= end_dt)]


# Combine the strings according to type
combine_string = combine_string_category(text_df)
combine_highlights_string = combine_string_category(text_df, filter='highlights')
combine_work_string = combine_string_category(text_df, filter='work')
combine_family_string = combine_string_category(text_df, filter='family')
combine_friends_string = combine_string_category(text_df, filter='friends')

# Get NER count for each type
ner_combined = get_ner(combine_string)
ner_highlights_combined = get_ner(combine_highlights_string)
ner_work_combined = get_ner(combine_work_string)
ner_family_combined = get_ner(combine_family_string)
ner_friends_combined = get_ner(combine_friends_string)


# Emotions df
emotions_query_engine = PandasQueryEngine(
    df=emotions_df, verbose=True, instruction_str=instruction_str
)
emotions_query_engine.update_prompts({"pandas_prompt": new_prompt})

# The most common names
text_emotions_query_engine = PandasQueryEngine(
    df=ner_combined, verbose=True, instruction_str=instruction_str_ner
)
text_emotions_query_engine.update_prompts({"pandas_prompt": new_prompt})

## AI Agent
tools = [
    QueryEngineTool(
        query_engine= emotions_query_engine,
        metadata=ToolMetadata(
            name="emotions_score",
            description="this gives information about the score of the emotions (happy, angry, surprise, sad, fear) over time",
        ),
    ),
    QueryEngineTool(
        query_engine=text_emotions_query_engine,
        metadata=ToolMetadata(
            name="most_frequent_name",
            description="this gives information about the most frequent names",
        ),
    ),
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="memories",
            description="this gives detailed information and the date when it happend for the memories recorded",
        ),
    ),
]

llm = OpenAI(model="gpt-3.5-turbo")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

latest_dt = emotions_df['record_dt'].max()

## Introduction
st.write("# Welcome to Dashboard! 👋")

## Summary
overall_emotion = get_current_emotion(emotions_df)
emotions_sentences = get_sentences_from_emotions(emotions_df)
happy_trend = get_emotions_trend(emotions_df, category='happy')
angry_trend = get_emotions_trend(emotions_df, category='angry')
surprise_trend = get_emotions_trend(emotions_df, category='surprise')
sad_trend = get_emotions_trend(emotions_df, category='sad')
fear_trend = get_emotions_trend(emotions_df, category='fear')
names = get_most_cited_person(ner_combined)

# Creating the summary in Markdown
# Creating the summary in Markdown without f-strings
summary = """
<hr style="border: none; height: 2px; background-color: blue;">

<h2 style="color: blue;">Summary of your diary</h2>

### From {}  
Your current dominant emotion is **{}**.  

{}
### Overall
#### Trends
- :grinning: **Happiness**: {}
- :cry: **Sadness**: {}
- :hushed: **Surprise**: {}
- :rage: **Anger**: {}
- :worried:**Fear**: {}

#### Most Cited Person
The person you mentioned the most in your diary is **{}**.

""".format(
    latest_dt,
     overall_emotion,
           '\n\n'.join(emotions_sentences),
           happy_trend, sad_trend,
           surprise_trend,
           angry_trend,
           fear_trend,
           names
    )

# Display the summary in Streamlit
st.markdown(summary, unsafe_allow_html=True)

## Emotions over time
st.markdown('''
 <hr style="border: none; height: 2px; background-color: blue;">  
 
<h2 style="color: blue;">Emotional Trends Over Time</h2>
 
 These plots show the intensity of your emotions extracted from your writing. 
 They're divided into Highlights, Work, Friends, and Family, revealing how your 
 emotions have changed over time in each category.
''',
            unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Highlights", "Work", "Family", "Friends"])

with tab1:
    plot_filtered_df(emotions_df, category='highlights')

with tab2:
    plot_filtered_df(emotions_df, category='work')

with tab3:
    plot_filtered_df(emotions_df, category='family')

with tab4:
    plot_filtered_df(emotions_df, category='friends')


## Name entities count
st.markdown('''
 <hr style="border: none; height: 2px; background-color: blue;">  

<h2 style="color: blue;">Emotional Trends Over Time</h2>
 
 Here you can explore the most frequently used words in your diary, including names, places, 
 and times that you've frequently mentioned. This helps you understand and identify the key 
 aspects of your life that matter most.
''',
            unsafe_allow_html=True)
st.markdown('### :ledger: From all recorded memories')
st.write('Get all the content of the diary from the selected dates')
streamlit_plot_frequency(ner_combined, color='blue')

st.markdown('### :star: From highlights recorded memories')
st.write('Get all content from the highlights section from the selected dates')
streamlit_plot_frequency(ner_highlights_combined, color='yellow')

st.markdown('### :briefcase: From working-related recorded memories')
st.write('Get all content from the work section from the selected dates')
streamlit_plot_frequency(ner_work_combined, color='orange')

st.markdown('### :family: From family-related recorded memories')
st.write('Get all content from the family section from the selected dates')
streamlit_plot_frequency(ner_family_combined, color='red')

st.markdown('### :handshake: From friends-related recorded memories ')
st.write('Get all content from the friends section from the selected dates')
streamlit_plot_frequency(ner_friends_combined, color='green')


# GenAI chat box
with st.sidebar:
    st.write('Chat')
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add custom CSS to make the container scrollable

    # Add a button to clear chat history
    # if st.button("Clear Chat", key='chat'):
    #     st.session_state.messages = []


    with st.container(height=400, border=True):
        # Accept user input
        if prompt := st.chat_input("Chat with your memories"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Use the new agent to get the assistant response
            with st.chat_message("assistant"):
                result = agent.query(prompt)
                st.markdown(result)

            st.session_state.messages.append({"role": "assistant", "content": result})

## Word cloud
st.markdown('''
 <hr style="border: none; height: 2px; background-color: blue;">  

<h2 style="color: blue;">Word Cloud</h2>
''',
            unsafe_allow_html=True)
plot_word_cloud(combine_string)
