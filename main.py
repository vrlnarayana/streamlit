import streamlit as st
import stapp # import sub-module stapp
from load_css import local_css
import login
import popular_reco
import menu
import user_reg
import user_list
import content_reco
import senti_collection

local_css("style.css") # include style.css

def print_hi(name):
    welcome_head=f"<div>Hi <span class='highlight blue'>{name}</span>, Welcome!</div>"
    st.markdown(welcome_head,unsafe_allow_html=True)

def main():
    st.header('Top Songs Recommender System')
    yourname, yourpass, auth = login.login() #get login field values
    if auth == 'authenticated': # display blocks below if authenticated
        print_hi(yourname)
        st.write ('\n')
        menu_out=menu.menu()
        if menu_out == 'Senti-Collections':
            radio_collect = st.select_slider('Select your mood now ', options=['happy','neutral','sad'])
            n = st.slider('Select how many song recommendations you would need?',min_value= 2, max_value=10)
            if radio_collect and n:
                senti_reco = senti_collection.top_senti_recommendation(radio_collect, n)
                st.write('\n')
                if not senti_reco.empty:
                    st.header(f'Top {n} {radio_collect} titles recommendation for you')
                    st.table(senti_reco)

        elif menu_out == 'User Registration':
            usr_lst=user_list.user_list()
            st.header('Registered users list.')
            st.write('Total no of users: '+str(len(usr_lst.name)))
            st.table(usr_lst)
            st.write('\n')
            if yourname == 'Lachu':
                ret_val = user_reg.register()  # display user registration option when user is authenticated
                ret_msg = f"<div><span class='highlight red'>{ret_val}</span></div>"
                st.markdown(ret_msg, unsafe_allow_html=True)
        elif menu_out == 'User Choices':
            # menu_mesg = stapp.func_welcome(menu_out,1)# call welcome function from the sub-module
            # st.markdown(menu_mesg, unsafe_allow_html=True)
            pop = popular_reco.artist_choice()  # populate list of popular artists
            if pop:
                choice = st.multiselect('choose your favourite artists', options=pop, key=844)
                if len(choice) == 5:
                    ret_val = popular_reco.insert_user_choice(yourname, choice, flag='A')
                    if ret_val == 'success':
                        pop_msg = f"<div>Your favourite(s), <span class='highlight blue'>{choice}</span></div>"
                        st.markdown(pop_msg, unsafe_allow_html=True)

            st.write('\n')

            pop_rel = popular_reco.release_choice()  # populate list of popular artists
            if pop_rel:
                rel_choice = st.multiselect('choose your favourite albums/releases', options=pop_rel, key=845)
                if len(rel_choice) == 5:
                    ret_val = popular_reco.insert_user_choice(yourname, rel_choice, flag='R')
                    if ret_val == 'success':
                        pop_rel_msg = f"<div>Your favourite(s), <span class='highlight blue'>{rel_choice}</span></div>"
                        st.markdown(pop_rel_msg, unsafe_allow_html=True)

            st.write('\n')


        elif menu_out=='Popular Titles':
            # menu_mesg=stapp.func_welcome(menu_out,1)# call welcome function from the sub-module
            # st.markdown(menu_mesg, unsafe_allow_html=True)

            #sub_menu popularity menus
            sub_menu_out=menu.submenu_1()
            if sub_menu_out=='Most Played':
                # sub_menu_mesg = stapp.func_welcome(sub_menu_out,2)  # call welcome function from the sub-module
                # st.markdown(sub_menu_mesg, unsafe_allow_html=True)
                st.write('\n')
                n=st.slider('Select how many song recommendations you would need?',min_value=2, max_value=10)
                title, top_pop_songs_title = stapp.top_pop_songs(n)# call popular songs function top-5
                st.subheader(f"Most played titles, {n} recommendations for you")
                st.spinner()
                with st.spinner(text='In progress'):
                    st.table(top_pop_songs_title)
                    st.success('Done')

                    # content based recommendation of related titles
                search_title = st.radio('Click here for related titles ', options=title, key=555)
                st.header('Related titles based on your selection')
                st.write('\n')
                recommended_songs = content_reco.text_recommendations(search_title)
                recommended_songs = recommended_songs[recommended_songs.score > 0] # filter out 0 score songs
                if recommended_songs.empty:
                    related_msg = f"<div> >>>>>>>>> <span class='highlight lblue'>Sorry, couldn't find related songs.</span> >>>>>>>>> </div>"
                    st.markdown(related_msg, unsafe_allow_html=True)
                else:
                    st.table(recommended_songs)

            elif sub_menu_out == 'Most Rated':
                #sub_menu_mesg = stapp.func_welcome(sub_menu_out,2)
                #st.markdown(sub_menu_mesg, unsafe_allow_html=True)
                st.write('\n')
                region=st.selectbox('Choose your region',options=['IN','US','/N'])
                if region:
                    n=st.slider('Select how many song recommendations you would need?',min_value=2, max_value=10)
                    top_rated_songs_title = stapp.top_rated_songs(n, region)  # call popular songs function top-5
                    st.subheader(f"Most rated titles, {n} recommendations for you")

                    st.spinner()
                    with st.spinner(text='In progress'):
                        st.table(top_rated_songs_title)
                        st.success('Done')
                else:
                    st.write('Choose your region')
            st.write('\n')
        elif menu_out == 'Search songs':

            st.header(menu_out)
            # content based recommendation of related titles
            search_options = st.radio('', options=['Search based on title, artist name, release, and genre', 'Search based on lyrics'], key = 5666)
            search_title = st.text_input(' ', key=999)
            if search_title and search_options == 'Search based on title, artist name, release, and genre':
                st.header('Related titles based on your search')
                st.write('\n')
                recommended_songs = content_reco.text_recommendations(search_title)
                recommended_songs = recommended_songs[recommended_songs.score > 0] # filter out 0 score songs
                if recommended_songs.empty:
                    related_msg = f"<div> >>>>>>>>> <span class='highlight lblue'>Sorry, couldn't find related songs.</span> >>>>>>>>> </div>"
                    st.markdown(related_msg, unsafe_allow_html=True)
                else:
                    st.table(recommended_songs)
            elif search_title and search_options == 'Search based on lyrics':
                st.header('Related titles based on your search')
                st.write('\n')
                recommended_songs = content_reco.lyrics_recommendations(search_title)
                recommended_songs = recommended_songs[recommended_songs.score > 0] # filter out 0 score songs
                if recommended_songs.empty:
                    related_msg = f"<div> >>>>>>>>> <span class='highlight lblue'>Sorry, couldn't find related songs.</span> >>>>>>>>> </div>"
                    st.markdown(related_msg, unsafe_allow_html=True)
                else:
                    st.table(recommended_songs)

    else:
        st.sidebar.markdown(auth,unsafe_allow_html=True)

# call main function here
if __name__ == '__main__':
    main()
