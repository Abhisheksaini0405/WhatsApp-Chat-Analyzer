from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

#Make a object for this library
extract = URLExtract()
def fetch_stats(selected_user,df):
    #It means group level analysis or total meassages in the group
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        num_messages = df.shape[0]
    # 1. fetch number of messages
    num_messages = df.shape[0]
    # 2. fetch total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #3. fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    #4. fetch number of link shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_messages,len(links)
#Function for showing the most busy users
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'percent','user':'name'})
    return x,df
def create_wordcloud(selected_user,df):
    #Remove unwanted words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Firstly we will separate the non group notifications from group notifications.
    temp = df[df['user'] != 'group_notification']
    # we will separate <media omitted> message from data frame.
    temp = temp[temp['message'] != '<Media omitted>\n']
    #This function remove all the hinglish stop words.
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

#Function for most using common words
def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Firstly we will separate the non group notifications from group notifications.
    temp = df[df['user'] != 'group_notification']
    # we will separate <media omitted> message from data frame.
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    # For removing the word message and deleted.
    wordss = []
    for i in range(len(words)):
        if words[i] != 'message' and words[i] != 'deleted' and words[i] != 'bsdk' and words[i] != 'gand' and words[i] != '#':
            wordss.append(words[i])
    words = wordss
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

#Monthly timeline function
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

#Daily timeline function
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
#Activity  map
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
 # Make a heatmap for finding which time users most active or  least active.
def activity_heat_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heat_map = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heat_map