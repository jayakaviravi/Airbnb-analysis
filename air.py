import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from streamlit_option_menu import option_menu
pd.set_option('display.max_columns', None)
from PIL import Image
import base64


#setting page configuration

img=Image.open("C:\\Users\\JAYAKAVI\\Downloads\\airbnbimg.png")
st.set_page_config(page_title="Airbnb", 
                    page_icon=img, 
                    layout="wide",
                    initial_sidebar_state="auto") 

# page header transparent color
page_background_color = """
<style>

[data-testid="stHeader"] 
{
background: rgba(0,0,0,0);
}

</style>
"""
st.markdown(page_background_color, unsafe_allow_html=True)

# title and position
st.markdown(f'<h1 style="text-align: center; color: red">Airbnb Analysis</h1>',
            unsafe_allow_html=True)
st.divider()

def dataframe():
    df=pd.read_csv("C:/Users/JAYAKAVI/New folder/file.csv")
    df.drop('Unnamed: 0',axis=1,inplace=True)
    return df

df1=dataframe()

# CREATING OPTION MENU
selected = option_menu(None,  ["Home", "Data Exploration", "Overview"],
                       icons=["house", "bar-chart","Magnifying Glass"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "-3px",
                                            "--hover-color": "#545454"},
                               "icon": {"font-size": "20px"},
                               "container": {"max-width": "3000px"},
                               "nav-link-selected": {"background-color": "violet"}})

if selected=='Home':

    col1,col2=st.columns([2,5],gap='medium')   

    with col1:
        
        file_ = open("C:/Users/JAYAKAVI/Downloads/airbnb.gif",  "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}"  width="310" alt="cat gif">',
            unsafe_allow_html=True,
        )

    st.subheader(':orange[Airbnb]')
    st.markdown('####   Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences.The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.')
   
    
    with col2:
        
        st.subheader(':orange[Technologies]')
        st.markdown('####   Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau. ')
        st.markdown('#### :orange[Domain:] Travel Industry, Property management and Tourism.')

if selected=='Data Exploration':
    
    with st.sidebar:
        
        select = option_menu(None, ["Price Analysis","Availability AnalysiS","Location Based","Geospatial Visualization","Top Charts"], 
                            default_index=0,
                            orientation="horizontal",
                            styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", 
                                                    "--hover-color": "white"},
                                    "icon": {"font-size": "15px"},
                                    "container" : {"max-width": "3000px"},
                                    "nav-link-selected": {"background-color": "violet"}})
        
    if select=='Price Analysis':
        
        st.subheader(':violet[Price Difference]')
        
        tab1,tab2=st.tabs(['PROPERTY_TYPES','HOST RESPONSE TIME'])
        
        with tab1:
            
            Country= st.selectbox("Country",df1["country"].unique(),index=None,placeholder="Select country")

            df2=df1[df1['country']==Country]
            df2.reset_index(drop= True, inplace= True)

            Room_type= st.selectbox("Room Type",df1["room_type"].unique(),index=None,placeholder="Select Room type")

            df3=df2[df2['room_type']==Room_type]
            df3.reset_index(drop= True, inplace= True)

            df_p= pd.DataFrame(df3.groupby('property_type')[["Price","Review_score","No_of_reviews"]].sum())
            df_p.reset_index(inplace= True)

            fig_p= px.bar(df_p, x='property_type', y= "Price", title= "PRICE FOR PROPERTY_TYPES",color='property_type',hover_data=["No_of_reviews","Review_score"],color_discrete_sequence=px.colors.sequential.Sunsetdark)
            fig_p.update_layout(width=800, height=500,title_font_color='red',title_font=dict(size=18),title_x=0.4)
            st.plotly_chart(fig_p)
    
        with tab2:

            Property_type= st.selectbox("Property_type",df3['property_type'].unique(),index=None,placeholder="Select property type")

            df4=df3[df3['property_type']==Property_type]
            df4.reset_index(drop= True, inplace= True)

            df_H= pd.DataFrame(df4.groupby('host_response_time')[["Price","Bedrooms"]].sum())
            df_H.reset_index(inplace= True)

            fig_H = px.pie(df_H, names='host_response_time',values='Price', hole=0.6,hover_data='Bedrooms',color_discrete_sequence=px.colors.sequential.Tealgrn_r,title="PRICE DIFFERENCE BASED ON HOST RESPONSE TIME",width= 800, height= 400)
            fig_H.update_traces(text=df_H['Price'], textinfo='percent+label',texttemplate='%{percent:.2%}', textposition='outside')
            fig_H.update_layout(title_font_color='red',title_font=dict(size=18),title_x=0.1)
            st.plotly_chart(fig_H)
        
            col1,col2= st.columns([1,1],gap='small')

            with col1:

                Hostresponsetime= st.selectbox("Select the host_response_time",df4["host_response_time"].unique(),index=None,placeholder="Select")

                df5=df4[df4['host_response_time']==Hostresponsetime]
                df5.reset_index(drop= True, inplace= True)

                df_b= pd.DataFrame(df5.groupby("Bed_type")[["Min_nights","max_nights","Price"]].sum())
                df_b.reset_index(inplace= True)

                fig_b= px.bar(df_b, x='Bed_type', y=['Min_nights', 'max_nights'], title='MINIMUM NIGHTS AND MAXIMUM NIGHTS',hover_data="Price",
                                barmode='group',color_discrete_sequence=px.colors.sequential.Magenta)
                fig_b.update_layout( height=500,width=400,title_font_color='red',title_font=dict(size=18),title_x=0.1)
                st.plotly_chart(fig_b)

            with col2:

                df_b1= pd.DataFrame(df5.groupby("Bed_type")[["Bedrooms","Accomodates",'Beds',"Price"]].sum())
                df_b1.reset_index(inplace= True)

                fig_b1= px.bar(df_b1, x='Bed_type', y=["Bedrooms","Accomodates",'Beds'], title='BEDROOMS ,ACCOMMODATES AND BEDS',hover_data="Price",
                        barmode='group',color_discrete_sequence=px.colors.sequential.haline_r)
                fig_b1.update_layout( height=500,width=500,title_font_color='red',title_font=dict(size=18),title_x=0.1)
                st.plotly_chart(fig_b1)    
    
    if select=="Availability AnalysiS":
                
            st.sidebar.header(":violet[Choose your filter:]")
             
            Country_a= st.sidebar.selectbox("Country availability",df1["country"].unique(),index=None,placeholder="Select")
            
            df1_a= df1[df1["country"] == Country_a]
            df1_a.reset_index(drop= True, inplace= True)

            property_typea= st.sidebar.selectbox("Property Type availability",df1_a["property_type"].unique(),index=None,placeholder="Select")
            
            df2_a= df1_a[df1_a["property_type"] == property_typea]
            df2_a.reset_index(drop= True, inplace= True)

            room_typea= st.sidebar.selectbox("Room Type availability", df2_a["room_type"].unique(),index=None,placeholder="Select")
            df3_a= df2_a[df2_a["room_type"] == room_typea]

            df_a= pd.DataFrame(df3_a.groupby("host_response_time")[["availability_30","availability_60","availability_90","availability_365","Price"]].sum())
            df_a.reset_index(inplace= True)
            
            fig_avail = px.bar(df_a, x='host_response_time', y=['availability_30', 'availability_60', 'availability_90', "availability_365"], 
                        title='Availability  based on Host Response time',hover_data="Price",text_auto='.2s',barmode='group')
            fig_avail.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False,marker_color=px.colors.diverging.Portland_r)
            fig_avail.update_layout( height=500,width=1000,title_font_color='red',title_font=dict(size=18),title_x=0.3)
            st.plotly_chart(fig_avail)
            
            col1,col2=st.columns([1,1],gap='small')

            with col1:
                
                df_a_30= px.sunburst(df2_a, path=['room_type','Bed_type','is_location_exact'], values="availability_30",width=500,height=450,title="Availability_30",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r)
                df_a_30.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.3)
                st.plotly_chart(df_a_30)
            
            with col2:
                
                df_a_60 = px.icicle(df2_a, path=['country','room_type', 'Bed_type','is_location_exact'], values='availability_60',
                                    color_discrete_sequence=px.colors.sequential.Tealgrn,width=500,height=400,title="Availability_60")
                df_a_60.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.4)
                st.plotly_chart(df_a_60)

            col1,col2=st.columns([1,1],gap='small')

            with col1:

                df_a_90= px.strip(df2_a, x="room_type", y="availability_90", color="room_type",width=500,height=400,title='Availability_90')
                df_a_90.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.3)
                st.plotly_chart(df_a_90)

            with col2:

                df_a_365= px.bar(df2_a, x="room_type", y="availability_365", color="room_type",pattern_shape="room_type", pattern_shape_sequence=[".", "x", "+"],width=500,height=400,title='Availability_365',
                                    hover_data=["property_type",'Bed_type',"No_of_reviews","Price"])
                df_a_365.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.4)
                st.plotly_chart(df_a_365)
        
    if select=="Location Based":

        def dataframe():
            df=pd.read_csv("C:/Users/JAYAKAVI/New folder/file.csv")
            df.drop('Unnamed: 0',axis=1,inplace=True)
            return df
        
        df_location=dataframe()

        Country_l= st.sidebar.selectbox("Country_l",df_location["country"].unique(),index=None,placeholder="Select")

        df1_l= df_location[df_location["country"] == Country_l]
        df1_l.reset_index(drop= True, inplace= True)

        property_typel= st.sidebar.selectbox("Property_type_l",df1_l["property_type"].unique(),index=None,placeholder="Select")

        df2_l= df1_l[df1_l["property_type"] == property_typel]
        df2_l.reset_index(drop= True, inplace= True)
        
        tab1,tab2,tab3=st.tabs(['Price','Correlation','Charts'])

        with tab1:
            
            d_max_min=df2_l['Price'].max()-df2_l['Price'].min()
            
            def select_the_df(select_val):
                if select_val ==str(df2_l['Price'].min())+' '+str('to')+' '+str(d_max_min*0.30 + df2_l['Price'].min())+' '+str("(30% of the Value)"):

                    df_val_30= df2_l[df2_l["Price"] <= d_max_min*0.30 + df2_l['Price'].min()]
                    df_val_30.reset_index(drop= True, inplace= True)
                    return df_val_30
                
                elif select_val ==str(d_max_min*0.30 + df2_l['Price'].min())+' '+str('to')+' '+str(d_max_min*0.60 + df2_l['Price'].min())+' '+str("(30% to 60% of the Value)"):
                    df_val_60= df2_l[df2_l["Price"] >= d_max_min*0.30 + df2_l['Price'].min()]
                    df_val_60_1= df_val_60[df_val_60["Price"] <= d_max_min*0.60 + df2_l['Price'].min()]
                    df_val_60_1.reset_index(drop= True, inplace= True)
                    return df_val_60_1
                elif select_val==str(d_max_min*0.60 + df2_l['Price'].min())+' '+str('to')+' '+str(df2_l['Price'].max())+' '+str("(60% to 100% of the Value)"):

                    df_val_100= df2_l[df2_l["Price"] >= d_max_min*0.60 + df2_l['Price'].min()]
                    df_val_100.reset_index(drop= True, inplace= True)
                    return df_val_100
                
            value_select= st.radio("Select the Price Range",[str(df2_l['Price'].min())+' '+str('to')+' '+str(d_max_min*0.30 + df2_l['Price'].min())+' '+str("(30% of the Value)"),
                                                        str(d_max_min*0.30 + df2_l['Price'].min())+' '+str('to')+' '+str(d_max_min*0.60 + df2_l['Price'].min())+' '+str("(30% to 60% of the Value)"),
                                                        str(d_max_min*0.60 + df2_l['Price'].min())+' '+str('to')+' '+str(df2_l['Price'].max())+' '+str("(60% to 100% of the Value)")])
            

            df_value_select=select_the_df(value_select)

            st.dataframe(df_value_select.iloc[:, 1::1].style.background_gradient(cmap='summer'))
            
        with tab2:
            #checking correlation
            df_val_sel_corr= df_value_select.drop(columns=['listing_url', 'name', 'property_type', 'room_type', 'Bed_type',
                                                                'Cancellation_policy','Image_url',
                                                                'host_url', 'host_name', 'host_location',
                                                                'host_response_time', 'host_thumbnail_url','host_picture_url','host_neighbourhood',
                                                                'host_responde_rate', 'host_is_superhost',
                                                                'host_has_profile_pic', 'host_identity_verified',
                                                                'host_verifications', 'amenities',
                                                                'street', 'suburb', 'government_area', 'market', 'country',
                                                                'country_code', 'location_type', 
                                                                'is_location_exact']).corr()
            
            st.write(df_val_sel_corr.iloc[:, 1:20:1].style.background_gradient(cmap="Oranges"))
        
        with tab3:
            
            df_val_sel_gr= pd.DataFrame(df_value_select.groupby("Accomodates")[["Cleaning_fees","Bedrooms","Beds"]].sum())
            df_val_sel_gr.reset_index(inplace= True)

            fig_1= px.bar(df_val_sel_gr, x="Accomodates", y= ["Cleaning_fees","Bedrooms","Beds"], title="ACCOMMODATES",
                color_discrete_sequence=px.colors.sequential.Pinkyl_r,orientation='v',barmode='group',width=900,height=500)
            fig_1.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.4)
            st.plotly_chart(fig_1)

            Room_type_l= st.sidebar.selectbox(" Room_Type_location", df_value_select["room_type"].unique(),index=None,placeholder="Select")
            df_val_sel_rt= df_value_select[df_value_select["room_type"] == Room_type_l]

            fig_2= px.bar(df_val_sel_rt, x= ["host_location","host_neighbourhood","street"],y="market", title="MARKET",
                    hover_data= ["name","host_name","market"], barmode='group',orientation='h', color_discrete_sequence=px.colors.sequential.PuBuGn_r,width=1200,height=600)
            fig_2.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.4)
            st.plotly_chart(fig_2)

            fig_3= px.bar(df_val_sel_rt, x="government_area", y= ["host_neighbourhood","Cancellation_policy","host_is_superhost"], title="GOVERNMENT_AREA",
                        hover_data= ["Guest_include","location_type",'government_area'], barmode='group', color_discrete_sequence=px.colors.sequential.Aggrnyl_r,width=1000,height=600)
            fig_3.update_layout(title_font_color='red',title_font=dict(size=22),title_x=0.4)
            st.plotly_chart(fig_3)
    
    if select=='Geospatial Visualization':
        
        fig_4 = px.scatter_mapbox(df1, lat='latitude', lon='longitude',color='Price', size='No_of_reviews',
                         color_continuous_scale="rainbow",hover_name='name',size_max=10,
                        mapbox_style="carto-positron",width=1050,height=600,zoom=1,hover_data=['country']
                        )
        fig_4.update_layout(title='Geospatial Distribution of Listings',title_font_color='red',title_font=dict(size=22),title_x=0.3)

        st.plotly_chart(fig_4)      

    if select=='Top Charts':

        tab1,tab2,tab3=st.tabs(['Host neighbourhood','Host location','Bed type'])

        country_t= st.sidebar.selectbox(" Country_t",df1["country"].unique(),index=None,placeholder="Select")
        df1_t= df1[df1["country"] == country_t]

        Property_type_t= st.sidebar.selectbox("Property_type_t",df1_t["property_type"].unique(),index=None,placeholder="Select")

        df2_t= df1_t[df1_t["property_type"] == Property_type_t]
        df2_t.reset_index(drop= True, inplace= True)

        df2_t_sort= df2_t.sort_values(by="Price")
        df2_t_sort.reset_index(drop= True, inplace= True)

        with tab1:
            
            df_price= pd.DataFrame(df2_t_sort.groupby("host_neighbourhood")["Price"].agg(["sum","mean"]))
            df_price.reset_index(inplace= True)
            df_price.columns= ["host_neighbourhood", "Total_price", "Average_price"]

            fig_price= px.scatter(df_price, y= "Total_price", x= "host_neighbourhood",color='host_neighbourhood',
                                  title= "PRICE BASED ON HOST_NEIGHBOURHOOD", width=1000, height= 500)
            fig_price.update_layout(title_font_color='red',title_font=dict(size=20),title_x=0.2)
            fig_price.update_traces(marker_size=12)
            st.plotly_chart(fig_price)

            fig_price_2= px.scatter(df_price, y= "Average_price", x= "host_neighbourhood",color='Average_price',
                            title= "AVERAGE PRICE BASED ON HOST_NEIGHBOURHOOD",width= 1000, height= 500)
            fig_price_2.update_traces(marker_size=12)
            fig_price_2.update_layout(title_font_color='red',title_font=dict(size=20),title_x=0.2)

            st.plotly_chart(fig_price_2)

        with tab2:
            
            df_price_1= pd.DataFrame(df2_t_sort.groupby("host_location")["Price"].agg(["sum","mean"]))
            df_price_1.reset_index(inplace= True)
            df_price_1.columns= ["host_location", "Total_price", "Average_price"]
        
            fig_price_3= px.bar(df_price_1, y= "Total_price", x= "host_location", orientation='v',color='host_location',
                                width= 1000,height= 600,title= "PRICE BASED ON HOST_LOCATION")
            fig_price_3.update_layout(title_font_color='red',title_font=dict(size=20),title_x=0.2)
            st.plotly_chart(fig_price_3)
            
            fig_price_4= px.bar(df_price_1, x= "Average_price", y= "host_location", orientation='h',
                                width= 1000, height= 500,color_discrete_sequence=px.colors.sequential.Redor_r,
                                title= "AVERAGE PRICE BASED ON HOST_LOCATION")
            fig_price_4.update_layout(title_font_color='red',title_font=dict(size=20),title_x=0.2)
            st.plotly_chart(fig_price_4)

        with tab3:

            df_ob= pd.DataFrame(df1_t.groupby('Bed_type')[["Price",'Bedrooms','Beds','No_of_reviews']].sum())
            df_ob.reset_index(inplace= True)

            fig_ob = px.bar(df_ob, y='Price', x='Bed_type',orientation='v',text_auto='.2s',hover_data=['Bedrooms','Beds','No_of_reviews'],title="Price based on Bedtype",color='Bed_type',color_discrete_sequence=px.colors.sequential.RdBu)
            fig_ob.update_layout(width=750, height=550,title_font_color='red',title_font=dict(size=22),title_x=0.2)
            st.plotly_chart(fig_ob)

            df_or = df1_t.groupby(['room_type', 'Bed_type']).size().unstack().fillna(0).reset_index()
            trace = go.Heatmap(z=df_or.iloc[:, 1:],
                            x=df_or.columns[1:],
                            y=df_or['room_type'],
                            colorscale='sunsetdark_r',
                            colorbar=dict(title='Count'))

            # Add text annotations
            annotations = []
            for i, row in enumerate(df_or.iterrows()):
                for j, value in enumerate(row[1].iloc[1:]):
                    annotations.append(dict(x=df_or.columns[j + 1], y=row[1]['room_type'],
                                            text=str(value), showarrow=False))

            layout = go.Layout(title='Room type based Bed_type',
                            xaxis=dict(title='Bed Type'),
                            yaxis=dict(title='Room Type'),
                            title_x=0.3, title_font_color='red',title_font_size=20)

            fig_or = go.Figure(data=[trace], layout=layout)
            fig_or.update_layout(width=700, height=600)

            # Add annotations to the layout
            fig_or.update_layout(annotations=annotations)
            st.plotly_chart(fig_or)

            df_oc = df1_t.groupby(['room_type', 'Cancellation_policy']).size().unstack().fillna(0).reset_index()
            trace = go.Heatmap(z=df_oc.iloc[:, 1:],
                            x=df_oc.columns[1:],
                            y=df_oc['room_type'],
                            colorscale='tealrose',
                            colorbar=dict(title='Count'))

            # Add text annotations
            annotations = []
            for i, row in enumerate(df_oc.iterrows()):
                for j, value in enumerate(row[1].iloc[1:]):
                    annotations.append(dict(x=df_oc.columns[j + 1], y=row[1]['room_type'],
                                            text=str(value), showarrow=False))

            layout = go.Layout(title='Room type based Cancellation Policy',
                            xaxis=dict(title='Bed Type'),
                            yaxis=dict(title='Room Type'),
                            title_x=0.3, title_font_color='red',title_font_size=20)

            fig_oc = go.Figure(data=[trace], layout=layout)
            fig_oc.update_layout(width=700, height=700)

            # Add annotations to the layout
            fig_oc.update_layout(annotations=annotations)
            st.plotly_chart(fig_oc)

if selected == "Overview":

    st.header(":blue[ABOUT THIS PROJECT]")

    st.subheader(":orange[1. Data Collection:]")

    st.markdown(''' #####  Gather data from Airbnb's public API or other available sources.Collect information on listings, hosts, reviews, pricing, and location data.''')
    
    st.subheader(":orange[2. Data Cleaning and Preprocessing:]")

    st.markdown(''' ##### Clean and preprocess the data to handle missing values, outliers, and ensure data quality.Convert data types, handle duplicates, and standardize formats.''')
    
    st.subheader(":orange[3. Exploratory Data Analysis (EDA):]")

    st.markdown(''' ##### Conduct exploratory data analysis to understand the distribution and patterns in the data.Explore relationships between variables and identify potential insights.''')
    
    st.subheader(":orange[4. Visualization:]")

    st.markdown('''##### Create visualizations to represent key metrics and trends.Use charts, graphs, and maps to convey information effectively.Consider using tools like Matplotlib, Seaborn, or Plotly for visualizations.''')
    
    st.subheader(":orange[5. Geospatial Analysis:]")

    st.markdown(''' ##### Utilize geospatial analysis to understand the geographical distribution of listings.Map out popular areas, analyze neighborhood characteristics, and visualize pricing variations.***''')






                








                        














