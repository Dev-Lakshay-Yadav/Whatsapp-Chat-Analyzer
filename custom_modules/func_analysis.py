import emoji
import collections as c
import pandas as pd

import plotly.express as px
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS


# returns the name of participants in chat.
def authors_name(data):
    authors = data.Author.unique().tolist()
    return [name for name in authors if name != None]


# used to calculate emojis in text and return in a list.
def extract_emojis(s):
    return [c for c in s if c in emoji.EMOJI_DATA]


# takes input as data and return number of messages and total emojis used in chat.
def stats(data):
    total_messages = data.shape[0]
    media_messages = data[data['Message'] == '<Media omitted>'].shape[0]
    emojis = sum(data['emoji'].str.len())
    return "Total Messages 💬: {} \n Total Media 🎬: {} \n Total Emoji's 😂: {}".format(total_messages, media_messages, emojis)


# returns the list of emoji's with it's frequency.
def popular_emoji(data):
    total_emojis_list = list([a for b in data.emoji for a in b])
    emoji_dict = dict(c.Counter(total_emojis_list))
    emoji_list = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    return emoji_list


# used to make pie chart of popular emoji's.
def visualize_emoji(data):
    emoji_df = pd.DataFrame(popular_emoji(data), columns=['emoji', 'count'])
    fig = px.pie(emoji_df, values='count', names='emoji', color_discrete_map="identity", title='Emoji Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


# used to generate word cloud using dataframe.
def word_cloud(df):
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']
    words = ' '.join(df['Message'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    fig = plt.figure()
    ax = fig.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig
    

# used to generate horizontal bar graph between date and number of messages dataframe.
def active_date(data):
    fig, ax = plt.subplots()
    ax = data['Date'].value_counts().head(10).plot.barh()
    ax.set_title('Top 10 active date')
    ax.set_xlabel('Number of Messages')
    ax.set_ylabel('Date')
    plt.tight_layout()
    return fig
    

# generate horizontal bar graph between time and number of messages.
def active_time(data):
    fig, ax = plt.subplots()
    ax = data['Time'].value_counts().head(10).plot.barh()
    ax.set_title('Top 10 active time')
    ax.set_xlabel('Number of messages')
    ax.set_ylabel('Time')
    plt.tight_layout()
    return fig


# generate a line polar plot.
def day_wise_count(data):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_df = pd.DataFrame(data["Message"])
    day_df['day_of_date'] = data['Date'].dt.weekday
    day_df['day_of_date'] = day_df["day_of_date"].apply(lambda d: days[d])
    day_df["messagecount"] = 1
    day = day_df.groupby("day_of_date").sum()
    day.reset_index(inplace=True)
    fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )),
    showlegend=False
    )
    return fig


# enerates the line plot of number of messages on monthly basis.
def num_messages(data):
    data.loc[:, 'MessageCount'] = 1
    date_df = data.groupby("Date").sum()
    date_df.reset_index(inplace=True)
    fig = px.line(date_df, x="Date", y="MessageCount")
    fig.update_xaxes(nticks=20)
    return fig

   
# generates a bar plot of members involve in a chat corressponding to the number of messages. 
def chatter(data):
    auth = data.groupby("Author").sum(numeric_only=True)
    auth.reset_index(inplace=True)
    fig = px.bar(auth, y="Author", x="MessageCount", color='Author', orientation="h",
             color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
             title='Number of messages corresponding to author'
            )
    return fig