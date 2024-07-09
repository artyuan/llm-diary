import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from src.pdf import CreateDiary
from datetime import datetime
from src.nlp import get_emotions_from_text, get_labels_by_category,add_remaining_ner_labels
import os

load_dotenv()

def save_df(df, folder, filename):
    """
    Saves a DataFrame to a CSV file within a specified folder. If a CSV file with the same name already exists,
    it appends the new DataFrame to the existing one.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        folder (str): The folder where the CSV file will be saved.
        filename (str): The name of the CSV file (without the .csv extension).

    Returns:
        None
    """
    df_path = os.path.join(base_dir, 'data', folder).replace('\\', '/')
    if create_diary.is_folder_empty(df_path):
        df.to_csv(f"data/{folder}/{filename}.csv", index=False)
    else:
        stored_df = pd.read_csv(f"data/{folder}/{filename}.csv")
        stored_df = pd.concat([df, stored_df])
        stored_df.to_csv(f"data/{folder}/{filename}.csv", index=False)

def clear_text():
    """
    Clears the text input fields in the Streamlit session state for diary entries, resetting the fields
    for highlights, work, family, and friends.
    """
    st.session_state["highlights"] = ""
    st.session_state["work"] = ""
    st.session_state["family"] = ""
    st.session_state["friends"] = ""
def transforming_text(question, text):
    """
    Transforms the given text by prepending a formatted date and combining it with a question.

    Args:
        question (str): The question to be prepended to the text.
        text (str): The main text of the diary entry.

    Returns:
        str: The transformed text, starting with the date and question, followed by the main text.
    """
    starting_sentence = f'On {current_month_name} {current_day}, {current_year},'
    diary_text = starting_sentence + '' + text
    diary_text = "\n\n".join([question, diary_text])
    return diary_text

if __name__ == '__main__':
    ## INTRODUCTION
    st.set_page_config(page_title="Daily registry")
    st.title('Welcome to Your Online Diary!')
    st.markdown('''
     Keep track of your daily routine and monitor your emotions over time with our intuitive diary app. 
     Not only can you log your activities and feelings, but you can also engage in conversations with your emotions 
     using advanced AI technology. Discover insights about your emotional journey and maintain a personal record of 
     your experiences.  

    Start your journey towards self-discovery today!

     <hr style="border: none; height: 2px; background-color: blue;">
    ''', unsafe_allow_html=True)

    # Questions
    q1 = "What were the highlights of your day?"
    q2 = "How did your tasks and activities at work unfold today, and how did you feel in the work environment?"
    q3 = "how was the moments you shared with your family today?"
    q4 = "How did your interactions with friends go today?"

    st.header("Begin Your Daily Journey")
    st.write("Let's start documenting your memories and emotions!")
    selected_date = st.date_input("Select date", label_visibility="hidden")


    st.subheader(q1)
    highlights_txt = st.text_area(label="Start writing...",height=200, key='highlights')

    st.subheader(q2)
    work_txt = st.text_area(label="Start writing...", height=200, key='work')

    st.subheader(q3)
    family_txt = st.text_area(label="Start writing...", height=200, key='family')

    st.subheader(q4)
    friends_txt = st.text_area(label="Start writing...", height=200, key='friends')

    current_day = selected_date.day
    current_month_name = selected_date.strftime("%B")
    current_year = selected_date.year


    highlights_txt_qa = transforming_text(q1, highlights_txt)
    work_txt_qa = transforming_text(q2, work_txt)
    family_txt_qa = transforming_text(q3, family_txt)
    friends_txt_qa = transforming_text(q4,friends_txt)

    combined_text = "\n\n".join([highlights_txt, work_txt, family_txt, friends_txt])
    combined_text_qa = "\n\n".join([highlights_txt_qa, work_txt_qa, family_txt_qa, friends_txt_qa])

    highlights_emotions = get_emotions_from_text(highlights_txt,'highlights',selected_date=selected_date, filter=False)
    work_emotions = get_emotions_from_text(work_txt,'work', selected_date=selected_date, filter=False)
    family_emotions = get_emotions_from_text(family_txt,'family', selected_date=selected_date, filter=False)
    friends_emotions = get_emotions_from_text(friends_txt,'friends', selected_date=selected_date, filter=False)
    all_emotions = get_emotions_from_text(combined_text,'day', selected_date=selected_date, filter=False)
    emotions_df = pd.concat(
        [
                 highlights_emotions,
                 work_emotions,
                 family_emotions,
                 friends_emotions,
                 all_emotions
        ],
        axis=0
    ).reset_index(drop=True)

    text_df = pd.DataFrame({
        'record_dt': selected_date.strftime("%Y-%m-%d"),
        'highlights_txt': highlights_txt,
        'work_txt': work_txt,
        'family_txt': family_txt,
        'friends_txt': friends_txt,
        'combined_txt': combined_text,
    },
        index=[0]
    )

    highlights_label = get_labels_by_category(text_df, category='highlights', record_dt=selected_date)
    work_label = get_labels_by_category(text_df, category='work', record_dt=selected_date)
    family_label = get_labels_by_category(text_df, category='family', record_dt=selected_date)
    friends_label = get_labels_by_category(text_df, category='friends', record_dt=selected_date)
    combined_label = get_labels_by_category(text_df, category='combined', record_dt=selected_date)

    label_occurrences = pd.concat([
        highlights_label,
        work_label,
        family_label,
        friends_label,
        combined_label
    ]).reset_index(drop=True)

    emotions_df = emotions_df.merge(label_occurrences, on=['record_dt','type'], how='left')
    emotions_df = add_remaining_ner_labels(emotions_df)


    if st.button("Save", type="primary", key='registry'):
        create_diary = CreateDiary()
        base_dir = os.path.dirname(__file__)[:-4]

        # Saving tabular data
        save_df(emotions_df,'stats', 'emotions_df')
        save_df(text_df,'text', 'text')

        # Saving pdf
        print(combined_text)
        new_page_name = f'diary_from_{current_month_name}_{current_day}_{current_year}.pdf'
        create_diary.create_pdf(new_page_name, combined_text_qa)
        st.write("Your writing has been successfully saved.")
        current_dt = datetime.now()
        formatted_time = current_dt.strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"{formatted_time}")

    if st.button("Clear", type="primary", key='clear_txt', on_click=clear_text):
        st.write('Done!')


