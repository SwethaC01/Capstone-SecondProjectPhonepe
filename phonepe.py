import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import requests
import json
import plotly_express as px

mydb = mysql.connector.connect(host="localhost",user="root",password="",database='phonepe_db')
print(mydb)
mycursor = mydb.cursor(buffered=True)

st.set_page_config(
    page_title="Phonepe Visualization",
    layout="wide",
    initial_sidebar_state="expanded")

with st.sidebar:
    selected = option_menu(None,
                        ["HOME","EXPLORE","INSIGHTS"],
                        icons=["house-door-fill","tools","card-text"],
                        default_index=0,
                        orientation="vertical",
                        styles={"nav-link":{"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#8B008B"},
                        "icon": {"font-size": "30px"},
                        "container" : {"max-width": "6000px"},
                        "nav-link-selected": {"background-color": "#8B008B"}})
if selected =='HOME':
    st.title(':violet[PHONEPE DATA VISUALIZATION & EXPLORATION:iphone:]')

    st.image("D:\\Swetha Documents\\Python_Code\\CAPSTONE_SEC_PHONEPE\\image_processing20200114-26356-1dzvejl.gif",width=None, 
    caption="PhonePe",use_column_width=True)

    st.write(":iphone: PhonePe is India's leading digital payments platform, offering a wide range of services to millions of users across the country. Founded in 2015, PhonePe has revolutionized the way people transact, making it simple, secure, and convenient to send and receive money, pay bills, recharge mobile phones, and much more, all from the comfort of their smartphones.")

    st.write(":iphone: With over a billion transactions processed every month,PhonePe collects vast amounts of data that provide valuable insights into consumer behavior, spending patterns, and emerging trends in the digital payments ecosystem.Our mission is to empower individuals, businesses, and policymakers with actionable insights derived from data, driving innovation, and fostering financial inclusion across the country.")

    st.subheader(":violet[TECHNOLOGIES USED]")

    st.image("D:\Swetha Documents\Python_Code\CAPSTONE_SEC_PHONEPE\GithubCloning.gif")

    st.write(":iphone: Technologies used in this project include GitHub Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")

    st.write(":iphone: PhonePe Pulse is a project aimed at visualizing and exploring data related to various metrics and statistics available in the PhonePe Pulse GitHub repository.")

    st.write(":iphone: The goal of this project is to extract, process, and visualize the data in a user-friendly manner, providing valuable insights and information.")

    st.write(":iphone: The project falls under the domain of Fintech, focusing on analyzing transaction data and user behavior.")

    st.write(":iphone: To get started, follow the steps outlined in the Problem Statement and Approach sections.")

    st.write(":iphone: Explore the insights and visualizations provided by the dashboard!")

elif selected =="EXPLORE":
        
    st.markdown("<h1 style='text-align: center; color:WHITE;'>EXPLORE</h1>", unsafe_allow_html=True)

    select = option_menu(None,options=["AGGREGATED", "MAP", "TOP"],default_index=0,orientation="horizontal",styles={"container": {"width": "100%"},"nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},"nav-link-selected": {"background-color": "#00008B"}})

    if select == "AGGREGATED":
        tab1, tab2 = st.tabs(["TRANSACTION","USER"])

                                        #-----------------------------TRANSACTION TAB FOR AGGREGATED---------------------#
        with tab1:
            col1, col2, col3 = st.columns([1,2,3])

            with col1:
                agg_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='agg_yr')
            with col2:
                agg_quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='agg_quarter')
            with col3:
                agg_trans_type = st.selectbox('**Select Transaction type**',('Recharge & bill payments', 'Peer-to-peer payments','Merchant payments', 'Financial Services', 'Others'), key='agg_trans_type')

            mycursor.execute(f"SELECT State,Transaction_amount FROM aggtransaction WHERE Year = '{agg_yr}' AND Quarter = '{agg_quarter}' AND Transaction_type = '{agg_trans_type}';")

            transaction_query = mycursor.fetchall()
            
            agg_transpd= pd.DataFrame(transaction_query,columns=['State', 'Transaction_amount'])

            agg_tran_output= agg_transpd.set_index(pd.Index(range(1, len(agg_transpd) + 1)))

            # GEO VISUALISATION

            agg_transpd.drop(columns=['State'], inplace=True)

            url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()

            df_state_names_tra = pd.DataFrame({'State': state_names_tra})

            df_state_names_tra['Transaction_amount']=agg_transpd

            df_state_names_tra.to_csv('agg_trans.csv', index=False)

            agg_data = pd.read_csv('agg_trans.csv')

            fig_user = px.choropleth(
                agg_data,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Transaction_amount',
                color_continuous_scale='balance',  
                title='Transaction Amount Analysis')
            fig_user.update_geos(fitbounds="locations", visible=False)

            fig_user.update_layout(title_font=dict(size=33), title_font_color='#5F9EA0', height=750, geo=dict(
                scope='asia',
                projection=dict(type='mercator'),
                lonaxis=dict(range=[65.0, 100.0]),
                lataxis=dict(range=[5.0, 40.0])))

            st.plotly_chart(fig_user, use_container_width=True)

                #-----------------------------Transaction Amount Sunburst Chart---------------------#
            agg_tran_output['State'] = agg_tran_output['State'].astype(str)
            agg_tran_output['Transaction_amount'] = agg_tran_output['Transaction_amount'].astype(float)

            fig1 = px.sunburst(agg_tran_output, 
                                path=['State','Transaction_amount'], 
                                values='Transaction_amount',
                                color='Transaction_amount',
                                color_continuous_scale='magma',
                                title='Transaction Amount Chart',
                                height=700)
            
            fig1.update_layout(title_font=dict(size=33), title_font_color='#FFFFFF')

            st.plotly_chart(fig1, use_container_width=True)

                                    #-----------------------------USER TAB FOR AGGREGATED---------------------#
        with tab2:
            col1, col2 = st.columns([1, 2])

            with col1:
                agg_user_yr = st.selectbox('Select Year', ['2018', '2019', '2020', '2021', '2022', '2023'], key='agg_user_yr')

            with col2:
                if agg_user_yr == '2022':
                    in_us_qtr = st.selectbox('Select Quarter', ['1'], key='in_us_qtr')
                else:                       
                    in_us_qtr = st.selectbox('Select Quarter', ['1', '2', '3', '4'], key='in_us_qtr')
        
            mycursor.execute(f"SELECT State, SUM(Counts) AS Total_Count FROM agguser WHERE Year = '{agg_user_yr}' AND Quarter = '{in_us_qtr}' GROUP BY State;")
            query2 = mycursor.fetchall()
            agg_userpd = pd.DataFrame(query2, columns=['State', 'User Count'])
            agg_user_output = agg_userpd.set_index(pd.Index(range(1, len(agg_userpd) + 1)))

            # GEO VISUALIZATION
            agg_userpd.drop(columns=['State'], inplace=True)
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            state_names_user = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_user.sort()
            user_state_names = pd.DataFrame({'State': state_names_user})
            user_state_names['User Count'] = agg_userpd['User Count'] 

            # CHANGES TO CSV FILES 
            user_state_names.to_csv('user.csv', index=False)

            datas_gd = pd.read_csv('user.csv')

            fig_user = px.choropleth(
                datas_gd,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='User Count',
                color_continuous_scale='oxy',
                title='User Count Analysis')
            
            fig_user.update_geos(fitbounds="locations", visible=False)

            fig_user.update_layout(title_font=dict(size=33), title_font_color='#7FFFD4', height=750,geo=dict(scope='asia',
            projection=dict(type='mercator'),lonaxis=dict(range=[65.0, 100.0]),lataxis=dict(range=[5.0, 40.0])))

            st.plotly_chart(fig_user, use_container_width=True)

                                #-----------------------------BAR CHART FOR BRAND CHART---------------------#
            mycursor.execute(f"SELECT Brand, SUM(Counts) AS User_Count FROM agguser WHERE Year = '{agg_user_yr}' AND Quarter = '{in_us_qtr}' GROUP BY Brand;")
            avg_agguser = mycursor.fetchall()
            avg_userpd = pd.DataFrame(avg_agguser, columns=['Brand', 'User Count'])
            avg_output = avg_userpd.set_index(pd.Index(range(1, len(avg_userpd) + 1)))
            avg_output['Brand'] = avg_output['Brand'].astype(str)
            avg_output['User Count'] = avg_output['User Count'].astype(int)
            avg_fig = px.bar(
                avg_output,
                x='Brand',
                y='User Count',
                color='User Count',
                color_continuous_scale='purpor',
                title='User Count Chart',
                height=700)
            
            avg_fig.update_layout(title_font=dict(size=33), title_font_color='#D2691E')
            st.plotly_chart(avg_fig, use_container_width=True)

                                        #-----------------------------MAP---------------------#
    if select == "MAP":
        tab3,tab4= st.tabs(["TRANSACTION","USER"])
                                    #-----------------------------TRANSACTION TAB FOR MAP---------------------#
        with tab3:
                col1, col2, col3 = st.columns(3)
                with col1:
                    map_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='st_tr_st')
                with col2:
                    map_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='st_tr_yr')
                with col3:
                    map_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')
                                    #-----------------------------Transaction Amount BAR chart query---------------------#
                mycursor.execute(f"SELECT Districts, Transaction_count FROM maptransaction WHERE State = '{map_st}' AND Year = '{map_yr}' AND Quarter = '{map_qr}';")
                mapquery = mycursor.fetchall()
                maptrans_df = pd.DataFrame(mapquery,columns=['Districts', 'Transaction_count'])
                map_tran_output = maptrans_df.set_index(pd.Index(range(1, len(maptrans_df) + 1)))

                # Convert data types if necessary
                map_tran_output['Transaction_count'] = map_tran_output['Transaction_count'].astype(int)

                # Create the BAR chart
                map_fig = px.bar(map_tran_output, y='Transaction_count', x='Districts',title='Transaction Count Analysis by Districts')

                # Customize the layout if needed
                map_fig.update_layout(title_font=dict(size=33),title_font_color='#6495ED',font=dict(size=14),height=700,width=800)

                # Display the bar chart
                st.plotly_chart(map_fig, use_container_width=True)  

                                    #-----------------------------Transaction Amount pie chart query---------------------#
                mycursor.execute(f"SELECT Districts, Transaction_amount FROM maptransaction WHERE State = '{map_st}' AND Year = '{map_yr}' AND Quarter = '{map_qr}';")
                maptransamt = mycursor.fetchall()
                maptransamt_df = pd.DataFrame(maptransamt,columns=['Districts', 'Transaction_amount'])
                map_tran_amtoutput = maptransamt_df.set_index(pd.Index(range(1, len(maptransamt_df) + 1)))

                # Convert data types if necessary
                map_tran_amtoutput['Transaction_amount'] = map_tran_amtoutput['Transaction_amount'].astype(float)

                # Create the pie chart
                pie_chart_fig = px.pie(map_tran_amtoutput, values='Transaction_amount',names='Districts',
                title='Transaction Amount Analysis by District',hole = 0.4)

                # Customize the layout if needed
                pie_chart_fig.update_layout(title_font=dict(size=33), title_font_color='#A52A2A',font=dict(size=14),height=700,width=800)            
                # Display the pie chart
                st.plotly_chart(pie_chart_fig, use_container_width=True)

                                        #-----------------------------USER TAB FOR MAP---------------------#
        with tab4:
                col1, col2, col3 = st.columns(3)
                with col1:
                    map_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='map_st')
                with col2:
                    mapuser_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='mapuser_yr')
                with col3:
                    mapuser_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='mapuser_qr')
                
                            #-----------------------------RegisteredUsers Scatter Chart query---------------------#
                mycursor.execute(f"SELECT Districts, RegisteredUsers FROM mapuser WHERE State = '{map_st}' AND Year = '{mapuser_yr}' AND Quarter = '{mapuser_qr}';")
                mapuserquery = mycursor.fetchall()
                mapuser_df = pd.DataFrame(mapuserquery, columns=['Districts','RegisteredUsers'])
                map_useroutput = mapuser_df.set_index(pd.Index(range(1, len(mapuser_df) + 1)))

                # Convert data types if necessary
                map_useroutput['RegisteredUsers'] = map_useroutput['RegisteredUsers'].astype(float)

                # Create the scatter plot
                mapuser_fig = px.scatter(map_useroutput, x='Districts', y='RegisteredUsers',title='RegisteredUsers Analysis by District')

                # Customize the layout if needed
                mapuser_fig.update_layout(title_font=dict(size=33),title_font_color='#8B008B',font=dict(size=14),height=700,width=800)

                # Display the scatter plot
                st.plotly_chart(mapuser_fig, use_container_width=True)

                                #-----------------------------AppOpens line chart query---------------------#
                mycursor.execute(f"SELECT Districts, AppOpens FROM mapuser WHERE State='{map_st}' AND Year = '{mapuser_yr}' AND Quarter = '{mapuser_qr}';")
                mapuserquery = mycursor.fetchall()
                map_users_df = pd.DataFrame(mapuserquery, columns=['Districts', 'AppOpens'])
                map_tran_useroutput = map_users_df.set_index(pd.Index(range(1, len(map_users_df) + 1)))  

                # Convert data types if necessary
                map_tran_useroutput['AppOpens'] = map_tran_useroutput['AppOpens'].astype(float)

                # Create the line chart
                line_mapchart_fig = px.line(map_tran_useroutput, x='Districts', y='AppOpens',title='AppOpens Analysis by District')

                # Customize the layout if needed
                line_mapchart_fig.update_layout(title_font=dict(size=33),title_font_color='#006400',font=dict(size=14),height=700,width=800)            

                # Display the line chart
                st.plotly_chart(line_mapchart_fig, use_container_width=True)

                                                #-----------------------------TOP---------------------#

    if select == "TOP":
            tab5 ,tab6 = st.tabs(["TRANSACTION","USER"])
                                        #-----------------------------TRANSACTION TAB FOR TOP---------------------#
            with tab5:
                col1, col2, col3 = st.columns(3)
                with col1:
                    top_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='top_st')
                with col2:
                    top_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='top_yr')
                with col3:
                    top_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='top_qr')

                            #-----------------------------#Transaction count Analysis pie chart query---------------------#
                mycursor.execute(f"SELECT Pincodes, Transaction_count FROM toptransaction WHERE State = '{top_st}' AND Year = '{top_yr}' AND Quarter = '{top_qr}';")
                topcountquery = mycursor.fetchall()
                toptrans_df = pd.DataFrame(topcountquery, columns=['Pincodes','Transaction_count'])
                toptrans_output = toptrans_df.set_index(pd.Index(range(1, len(toptrans_df) + 1)))

                toptrans_output['Pincodes'] = toptrans_output['Pincodes'].astype(float)
                toptrans_output['Transaction_count'] = toptrans_output['Transaction_count'].astype(int)

                # Create the pie chart
                toptrans_pie_fig = px.pie(toptrans_output, values='Transaction_count', names='Pincodes',color_discrete_sequence=px.colors.sequential.ice,title='Pincodes')

                # Customize the layout and appearance
                toptrans_pie_fig.update_layout(title_font=dict(size=33),title_font_color='#0000FF',font=dict(size=14),height=700,width=800)

                # Display the pie chart
                st.plotly_chart(toptrans_pie_fig, use_container_width=True)

                        #-----------------------------#Transaction Amount Analysis query---------------------#
                mycursor.execute(f"SELECT State, SUM(Transaction_amount) FROM toptransaction WHERE Year = '{top_yr}' AND Quarter = '{top_qr}' GROUP BY State;")
                top_transc_query = mycursor.fetchall()
                df_top_transc_query = pd.DataFrame(top_transc_query, columns=['State', 'Transaction amount'])
                df_top_transc_result = df_top_transc_query.set_index(pd.Index(range(1, len(df_top_transc_query) + 1)))
        
                # GEO VISUALIZATION FOR USER

                df_top_transc_query.drop(columns=['State'], inplace=True)

                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data5 = json.loads(response.content)

                top_state_names_use = [feature['properties']['ST_NM'] for feature in data5['features']]
                top_state_names_use.sort()

                df_state_names_use = pd.DataFrame({'State': top_state_names_use})

                df_state_names_use['Transaction amount'] = df_top_transc_query

                df_state_names_use.to_csv('State_tr_amt.csv', index=False)

                df_use = pd.read_csv('State_tr_amt.csv')

                # Geo plot
                top_fig_use = px.choropleth(df_use,geojson=data5,featureidkey='properties.ST_NM', locations='State', color='Transaction amount',color_continuous_scale='purpor',title='Transaction amount Analysis')

                top_fig_use.update_geos(fitbounds="locations", visible=False)

                top_fig_use.update_layout(title_font=dict(size=33), title_font_color='#A9A9A9', height=750,geo=dict(scope='asia',
                projection=dict(type='mercator'),lonaxis=dict(range=[65.0, 100.0]),lataxis=dict(range=[5.0, 40.0])))

                st.plotly_chart(top_fig_use, use_container_width=True) 

                                #-----------------------------USER TAB FOR TOP---------------------#
            with tab6:
                col1, col2, col3 = st.columns(3)
                with col1:
                    topuser_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='topuser_st')
                with col2:
                    topuser_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='topuser_yr')
                with col3:
                    topuser_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='topuser_qr')

                mycursor.execute(f"SELECT State,Pincodes,RegisteredUsers FROM topuser WHERE State='{topuser_st}' AND Year = '{topuser_yr}' AND Quarter = '{topuser_qr}'GROUP BY Pincodes;")
                top_user_query = mycursor.fetchall()
                df_top_user_query = pd.DataFrame(top_user_query,columns=['State','Pincodes', 'RegisteredUsers'])
                df_top_user_result = df_top_user_query.set_index(pd.Index(range(1, len(df_top_user_query) + 1)))

                topuser_fig = px.sunburst(df_top_user_result, path=['State', 'Pincodes', 'RegisteredUsers'], values='RegisteredUsers',color='RegisteredUsers',color_continuous_scale='gray',title='RegisteredUsers Chart',height=700,labels={'Pincodes': 'Pincode'})

                topuser_fig.update_layout(title_font=dict(size=33), title_font_color='#FFFF00')

                st.plotly_chart(topuser_fig, use_container_width=True)

#----------------------------------------------------- INSIGHTS TAB---------------------------------------------------------------------------#
elif selected == 'INSIGHTS':

    st.write("<h1 style='color:Red;text-align:center;'>INSIGHTS</h1>", unsafe_allow_html=True)

    options = ["--Select any of the Questions--",
            "1.Does the number of transactions vary based on different PIN codes?",
            "2.How does the Count vary by brand(e.g., Xiaomi, Samsung, Apple)?",
            "3.How did transaction percentages vary among different states in 2022?",
            "4.List the top 5 states in India with the highest transaction amount?",
            "5.What is the highest transaction amount recorded for the years 2018 and 2023?",
            "6.Which districts have the highest Transaction Count?",
            "7.Could you list the ten states with the fewest registered users and their respective PIN codes?",
            "8.What district had the most significant number of AppOpens?",
            "9.Among all the pin codes, which one has the lowest transaction count?",
            "10.What is the highest transaction amount recorded for each transaction type?"]

    select = st.selectbox("Select the option", options)

    if select =="1.Does the number of transactions vary based on different PIN codes?":
        mycursor.execute("SELECT Pincodes, AVG(Transaction_count) AS Avg_Transaction_Count FROM toptransaction GROUP BY Pincodes")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Pincodes', 'Avg_Transaction_Count'])
        fig = px.line(df, x='Pincodes', y='Avg_Transaction_Count', title='Transaction Count Across Different Pincodes')
        fig.update_xaxes(type='category')
        st.plotly_chart(fig, use_container_width=True)

    elif select =="2.How does the Count vary by brand(e.g., Xiaomi, Samsung, Apple)?":
        mycursor.execute("SELECT Brand, SUM(Counts)AS total_count FROM agguser GROUP BY Brand;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Brand', 'total_count'])
        ques2= px.sunburst(df, path=['Brand', 'total_count'], values='total_count', color='total_count',
                            color_continuous_scale='gnbu', title='Brand Count Chart', height=700)
        ques2.update_layout(title_font=dict(size=33), title_font_color='#483D8B')
        st.plotly_chart(ques2, use_container_width=True)

    elif select =="3.How did transaction percentages vary among different states in 2022?":
        mycursor.execute("SELECT State, Year, Percentage FROM agguser WHERE Year = 2022 GROUP BY State ORDER BY State,Percentage DESC;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['State','Year','Percentage'])
        fig = px.scatter(df, x="State", y="Percentage", color="State", title="Percentage by State in 2022",
                        labels={"Percentage":"Percentage","State":"State"},
                        category_orders={"State": sorted(df['State'].unique())})
        fig.update_traces(mode='markers+lines')
        st.plotly_chart(fig)

    elif select =="4.List the top 5 states in India with the highest transaction amount?":
        mycursor.execute("SELECT State, Transaction_Amount AS total_amount FROM maptransaction GROUP BY State ORDER BY total_amount DESC LIMIT 5;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['State', 'total_amount'])
        fig = px.histogram(df, x="State", y="total_amount", title="Top 5 States by Total Transaction Amount",
                        labels={"total_amount": "Total Transaction Amount", "State": "State"},
                        category_orders={"State": sorted(df['State'].unique())})
        st.plotly_chart(fig, use_container_width=True)

    elif select =="5.What is the highest transaction amount recorded for the years 2018 and 2023?":
        mycursor.execute("SELECT Year,Transaction_type,Transaction_amount FROM aggtransaction WHERE Year in ('2018','2019','2020','2021','2022','2023') group by Year,Transaction_type;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Year', 'Transaction_type', 'Transaction_amount'])
        fig = px.scatter(df, x="Transaction_amount", y="Transaction_type", animation_frame="Year", animation_group="Year",
                        color="Transaction_type", hover_name="Transaction_type", log_x=True,
                        range_x=[1, df['Transaction_amount'].max()],
                        labels={"Transaction_amount": "Transaction Amount", "Year": "Year"},
                        title="Transaction Amount over Years by Transaction Type")
        fig.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True)

    elif select =="6.Which districts have the highest Transaction Count?":
        mycursor.execute("SELECT Districts,Transaction_count as Count FROM maptransaction ORDER BY Transaction_count DESC LIMIT 10;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Districts', 'Count'])
        ques6 = px.sunburst(df, path=['Districts', 'Count'], values='Count', color='Count', color_continuous_scale='speed',
                            title='District Transaction Count Chart', height=700)
        ques6.update_layout(title_font=dict(size=33), title_font_color='#20B2AA')
        st.plotly_chart(ques6, use_container_width=True)

    elif select =="7.Could you list the ten states with the fewest registered users and their respective PIN codes?":
        mycursor.execute("SELECT State,Pincodes,SUM(RegisteredUsers)AS Users FROM topuser GROUP BY State,Pincodes ORDER BY Users ASC LIMIT 10;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['State', 'Pincodes', 'RegisteredUsers'])
        fig = px.bar(df, x='State', y='RegisteredUsers', color='Pincodes', title='Least 10 States and Pincodes based on Registered Users')
        st.plotly_chart(fig, use_container_width=True)

    elif select =="8.What district had the most significant number of AppOpens?":
        mycursor.execute("SELECT Districts, AVG(AppOpens)AS AvgAppOpens FROM mapuser GROUP by Districts ORDER BY AvgAppOpens DESC LIMIT 15;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Districts', 'AvgAppOpens'])
        fig = px.line(df, x='Districts', y='AvgAppOpens', title='Average App Opens by District')
        st.plotly_chart(fig, use_container_width=True)

    elif select =="9.Among all the pin codes, which one has the lowest transaction count?":
        mycursor.execute("SELECT Pincodes, MIN(Transaction_count) AS Least_Count FROM toptransaction GROUP BY Pincodes ORDER by Least_Count DESC LIMIT 15;")
        data=mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Pincodes', 'Least_Count'])
        pie_chart = px.pie(df, values='Least_Count', names='Pincodes',title='Least Count Distribution by Pincodes')
        pie_chart.update_layout(title_font=dict(size=33), title_font_color='#F5F5F5')
        st.plotly_chart(pie_chart, use_container_width=True)

    elif select =="10.What is the highest transaction amount recorded for each transaction type?":
        mycursor.execute("SELECT Transaction_type, MAX(Transaction_amount) AS Highest_amount FROM aggtransaction GROUP BY Transaction_type ORDER by Highest_amount DESC;")
        lastqry=mycursor.fetchall()
        df = pd.DataFrame(lastqry, columns=['Transaction_type', 'Highest_amount'])
        st.dataframe(df)
        fig = px.bar(df, x='Transaction_type', y='Highest_amount',title='Highest Transaction Amount by Transaction Type',labels={'Transaction_type': 'Transaction Type','Highest_amount': 'Highest Amount'})
        fig.update_layout(xaxis_title='Transaction Type',yaxis_title='Highest Amount',title_font=dict(size=25), title_font_color='#0000CD')
        st.plotly_chart(fig, use_container_width=True)