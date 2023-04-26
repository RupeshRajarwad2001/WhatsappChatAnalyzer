import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import emoji
from wordcloud import WordCloud
st.sidebar.title("Whatsapp chat analysis")
upload_file=st.sidebar.file_uploader('Choose file')
if upload_file is not None:
    bytes_data=upload_file.getvalue()


    data=bytes_data.decode("utf-8")
    #df=preprocessor.preprocessor(data)
    #print(type(data))
    #print(data)

    #path = open(r'name.txt', 'w', encoding="utf-8")
    #path.seek(0)

    with open('name.txt', 'w', encoding="utf-8") as f:
        f.write(data)
    #path.truncate()
    #print(path)
    #print(type(data))
    #path.write(data)
    #print(data)
    df = preprocessor.preprocessor()
    #st.dataframe(df)

    #fetch unique user
    user_list=df['user'].unique().tolist()


    if 'group notification' in user_list:

        user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shares")
            st.title(num_media_messages)
        with col4:
            st.header("links shares")
            st.title(num_links)


        #timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'], timeline['Message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['Only_date'], daily_timeline['Message'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy moth")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation='vertical')

            st.pyplot(fig)




        #finding the busiest user in the group

        if selected_user=='Overall':
            st.title("Most Busy Users")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #wordcloud
        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #most comman words
        most_commom_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_commom_df[0],most_commom_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common words")
        st.pyplot(fig)


        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)











