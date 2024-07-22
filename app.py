import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzstter")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    #for changing the format of file
    data = bytes_data.decode("utf-8")
    #st.text(data)
    #Preprocess the data
    df = preprocessor.preprocess(data)
    #st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    #Remove group notification from user_list
    user_list.remove('group_notification')
    #Sort all the user_list
    user_list.sort()
    #Insert the overall at 0 position
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis",user_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(num_media_messages)
        with col4:
            st.header("Total link Shared")
            st.title(num_links)
        #Monthly timeline

        timeline = helper.monthly_timeline(selected_user,df)
        st.title("Monthly Timeline")
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color = 'orange')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        #Daily time line
        daily_timeline = helper.daily_timeline(selected_user, df)
        st.title("Daily Timeline")
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        #Activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #finding the busiest user in the group(Group level)
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color = 'green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common Words
        most_common_df = helper.most_common_words(selected_user,df)
        st.title("Most 20 Used Words")
        #Convert this into graph
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)

        #Emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            #Showing the emoji graph of top 5
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(),autopct = "%0.2f")
            st.pyplot(fig)
        #Make a heatmap of user time active.
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heat_map(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)