from datetime import datetime
import text2emotion as te
import pandas as pd
import spacy
from scipy.stats import linregress

def get_emotions_from_text(text, type, selected_date=datetime.now(), filter=True):
    emotions = te.get_emotion(text)
    base_df = pd.DataFrame(
        {
            'record_dt': selected_date.strftime("%Y-%m-%d"),
            'type': type,
        },
        index=[0]
    )
    emotions = pd.DataFrame(emotions, index=[0])
    emotions[f'main_emotion'] = emotions.idxmax(axis=1)
    emotions = pd.concat([base_df, emotions], axis=1)
    emotions.columns = [x.lower() for x in list(emotions.columns)]
    return emotions
def combine_string_category(df,filter='combined'):
  combine_string = ' '.join(df[f'{filter}_txt'])
  combine_string = combine_string.replace('\n', ' ')
  return combine_string

def get_ner(text):
  # Load the spaCy model
  nlp = spacy.load("en_core_web_sm")

  # Process the text with spaCy
  doc = nlp(text)

  # Initialize a dictionary to collect name counts by entity labels
  name_counts = {}

  # Extract and count names for each entity label
  for ent in doc.ents:
      if ent.label_ not in name_counts:
          name_counts[ent.label_] = {}

      if ent.text in name_counts[ent.label_]:
          name_counts[ent.label_][ent.text] += 1
      else:
          name_counts[ent.label_][ent.text] = 1

  # Convert the nested dictionary to a DataFrame
  df = pd.DataFrame(name_counts)

  # Fill NaN values with 0 (for entities that don't have a name count)
  df = df.fillna(0).astype(int).reset_index()
  df.columns = [x.lower() for x in list(df.columns)]
  df.rename(columns={'index':'text'}, inplace=True)
  return df

def get_max_label_count(df,):
  cols = df.columns.to_list()[1:]
  max_texts = []
  for label in cols:
    max_value = df[label].max()
    max_value_texts = df[df[label] == max_value]['text'].tolist()
    max_texts.append(max_value_texts)
  # Create a new dataframe
  new_data = {
      'column': cols,
      'max_texts': max_texts
  }

  ner_df = pd.DataFrame(new_data)
  ner_df = ner_df.T.reset_index()
  ner_df.columns = ner_df.iloc[0]
  ner_df= ner_df.iloc[1:]
  return ner_df

def get_labels_by_category(df, category, record_dt):
  ner_work_txt = df[f'{category}_txt'].iloc[0]
  ner_df = get_ner(ner_work_txt)
  cols = ['record_dt', 'type'] + ner_df.columns.to_list()[1:]
  category_df = get_max_label_count(ner_df)
  category_df['type'] = category if category != 'combined' else 'day'
  category_df['record_dt'] = record_dt.strftime("%Y-%m-%d")
  category_df = category_df[cols]
  return category_df

def add_remaining_ner_labels(df, value=None):
    """
    PERSON:      People, including fictional.
    NORP:        Nationalities or religious or political groups.
    FAC:         Buildings, airports, highways, bridges, etc.
    ORG:         Companies, agencies, institutions, etc.
    GPE:         Countries, cities, states.
    LOC:         Non-GPE locations, mountain ranges, bodies of water.
    PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
    EVENT:       Named hurricanes, battles, wars, sports events, etc.
    WORK_OF_ART: Titles of books, songs, etc.
    LAW:         Named documents made into laws.
    LANGUAGE:    Any named language.
    DATE:        Absolute or relative dates or periods.
    TIME:        Times smaller than a day.
    PERCENT:     Percentage, including ”%“.
    MONEY:       Monetary values, including unit.
    QUANTITY:    Measurements, as of weight or distance.
    ORDINAL:     “first”, “second”, etc.
    CARDINAL:    Numerals that do not fall under another type.
    """
    ner_labels = ['cardinal', 'date', 'event', 'fac', 'gpe', 'language', 'law', 'loc', 'money',
                  'norp', 'ordinal', 'org', 'percent', 'person', 'product', 'quantity', 'time',
                  'work_of_art', 'loc', 'misc', 'org', 'per']
    cols_list = df.columns.to_list()

    # Convert lists to sets
    set1 = set(ner_labels)
    set2 = set(cols_list)

    # Find missing elements
    missing_elements = set1 - set2

    # Convert the result back to a list
    missing_elements_list = list(missing_elements)

    for col in missing_elements_list:
        df[col] = value
    return df

def get_current_emotion(df, type='day'):
  last_date = df['record_dt'].max()
  main_emotion = df[(df['record_dt']==last_date) & (df['type']=='day')]['main_emotion'].iloc[0]
  mapping = {
      'Happy': 'Happy :grinning:',
      'Sad': 'Sad :cry:',
      'Fear': 'Fear :worried:',
      'Angry': 'Angry :rage:',
      'Surprise': 'Surprise 	:hushed:'
  }
  return mapping[main_emotion]

def get_sentences_from_emotions(df):
  last_date = df['record_dt'].max()
  current_df = df[df['record_dt']==last_date]
  current_df = current_df.groupby('main_emotion')['type'].apply(list).reset_index()
  emotions_sentences = []
  for i in range(0,len(current_df)):
    sentence = current_df.iloc[i,0] + " is the emotion to describe your writing about: " + ', '.join(current_df.iloc[i,1])
    emotions_sentences.append(sentence)
  return emotions_sentences

def get_emotions_trend(df, category):
  df = df[df['type']=='day'][[category]]
  slope, intercept, r_value, p_value, std_err = linregress(range(len(df)), df[category])
  mapping ={
      'happy':'happiness',
      'angry': 'anger',
      'surprise': 'surprise',
      'sad': 'sadness',
      'fear': 'fear',
  }

  high_upward_threshold = 1.5
  low_upward_threshold = 0.1
  low_downward_threshold = -0.1
  high_downward_threshold = -1.5

  if slope > high_upward_threshold:
    return f"The data shows a strong upward trend in related to {mapping[category]}"
  elif slope > low_upward_threshold:
    return f"The analysis reveals a modest increase related to {mapping[category]}."
  elif slope < high_downward_threshold:
    return f"The data shows a strong downward  trend in related to {mapping[category]}."
  elif slope < low_downward_threshold:
    return f"The analysis reveals a modest decrease related to {mapping[category]}."
  else:
    return f"Your emotion related to {mapping[category]} is steady."

def get_most_cited_person(df):
  max_person_count = df['person'].max()
  most_often = list(df[df['person']==max_person_count]['text'].values)
  most_often = ','.join(most_often)
  return most_often