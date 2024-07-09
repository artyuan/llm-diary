import plotly.graph_objects as go
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import plotly.express as px
from src.nlp import add_remaining_ner_labels

def plot_filtered_df(df, category):
    """
    Plots a filtered DataFrame by emotion categories over time.

    Args:
        df (pd.DataFrame): The DataFrame containing emotion data.
        category (str): The category of data to be filtered and plotted.

    Returns:
        None
    """
    df = df[df['type'] == category]

    # Define hover text for each trace
    hover_text = (
          "Date: " + df['date'].astype(str) + "<br>" +
          "Person: " + df['person'].astype(str) + "<br>" +
          "Time: " + df['time'].astype(str) + "<br>" +
          "Money: " + df['money'].astype(str) + "<br>" +
          "Org: " + df['org'].astype(str) + "<br>" +
          "Product: " + df['product'].astype(str)
    )

    # Create traces
    trace_happy = go.Scatter(x=df['record_dt'], y=df['happy'], mode='lines+markers', name='Happy',
                           hovertext=hover_text)
    trace_angry = go.Scatter(x=df['record_dt'], y=df['angry'], mode='lines+markers', name='Angry',
                           hovertext=hover_text)
    trace_surprise = go.Scatter(x=df['record_dt'], y=df['surprise'], mode='lines+markers', name='Surprise',
                              hovertext=hover_text)
    trace_sad = go.Scatter(x=df['record_dt'], y=df['sad'], mode='lines+markers', name='Sad',
                         hovertext=hover_text)
    trace_fear = go.Scatter(x=df['record_dt'], y=df['fear'], mode='lines+markers', name='Fear',
                          hovertext=hover_text)

    # Create the figure
    fig = go.Figure()

    # Add traces to the figure
    fig.add_trace(trace_happy)
    fig.add_trace(trace_angry)
    fig.add_trace(trace_surprise)
    fig.add_trace(trace_sad)
    fig.add_trace(trace_fear)

    # Customize layout
    fig.update_layout(
      xaxis_title='Date',
      yaxis_title='Emotion Intensity',
    )
    st.plotly_chart(fig, use_container_width=True, key= f'plot_{category}')

def plot_ner(df, ner_label, color='blue'):
    """
    Plots a bar chart of the most frequent named entities for a specified label.

    Args:
        df (pd.DataFrame): The DataFrame containing named entity recognition (NER) data.
        ner_label (str): The NER label to plot (e.g., 'person', 'org').
        color (str, optional): The color of the bars. Defaults to 'blue'.

    Returns:
        None
    """
    df = df[df[ner_label] > 0]
    fig = px.bar(df, x='text', y=ner_label, title='The most frequent', color_discrete_sequence=[color])
    fig.update_layout(
    xaxis_title='Count',
    yaxis_title=ner_label
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_word_cloud(text):
    """
    Plots a word cloud based on the given text.

    Args:
        text (str): The text to be used for generating the word cloud.

    Returns:
        None
    """
    # Define stopwords
    stopwords = set(STOPWORDS)
    stopwords.update(["and", "or", "the", "of", "to",
                    "January","February","March"])
    # Create a word cloud object with customization
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=200, stopwords=stopwords, contour_width=3, contour_color='steelblue').generate(text)

    # Create a matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Display the word cloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # Pass the figure to st.pyplot
    st.pyplot(fig)


def streamlit_plot_frequency(ner_combined, color='blue'):
    """
    Plots the frequency of named entities using Streamlit tabs for different NER labels.

    Args:
        ner_combined (pd.DataFrame): The DataFrame containing combined NER data.
        color (str, optional): The color of the bars. Defaults to 'blue'.

    Returns:
        None
    """
    # Name entity recognition
    ner_combined = add_remaining_ner_labels(ner_combined, value=0)

    ner_tab1, ner_tab2, ner_tab3, ner_tab4 = st.tabs(["Person", "Org", "Date", "Time"])

    with ner_tab1:
        plot_ner(ner_combined, ner_label='person', color=color)

    with ner_tab2:
        plot_ner(ner_combined, ner_label='org', color=color)

    with ner_tab3:
        plot_ner(ner_combined, ner_label='date', color=color)

    with ner_tab4:
        plot_ner(ner_combined, ner_label='time', color=color)