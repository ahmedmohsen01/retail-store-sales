
import pandas as pd
from pandas.core import groupby
import plotly.express as px
import streamlit as st
from datetime import datetime


st.set_page_config(layout='wide')
df = pd.read_csv(r'C:\Users\ahmed\Documents\cleaned_data.csv')
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

## Title of the page
st.markdown(
    """
    <h1 style="text-align: center; white: black;">Retail Store Sales</h1>
    """,
    unsafe_allow_html=True
)


time_range = st.selectbox(
    "Select Time Range:",
    options=["Current Month", "Current Year", "Last Year", "All Time", "Custom Range"],
    index=3  
)


if time_range == "Custom Range":
    start_date = st.date_input("From", min_value=datetime(2000, 1, 1), max_value=datetime.now())
    end_date = st.date_input("To", min_value=start_date, max_value=datetime.now())
    df = df[(df['Transaction Date'] >= pd.to_datetime(start_date)) & (df['Transaction Date'] <= pd.to_datetime(end_date))]
else:
    current_date = datetime.now()
    if time_range == "Current Month":
        df = df[(df['Transaction Date'].dt.month == current_date.month) & (df['Transaction Date'].dt.year == current_date.year)]
    elif time_range == "Current Year":
        df = df[df['Transaction Date'].dt.year == current_date.year]
    elif time_range == "Last Year":
        df = df[df['Transaction Date'].dt.year == current_date.year - 1]

## Total sales orders
row_count = df['Transaction ID'].count()
if row_count < 1000 :
    formatted_count = f'{row_count}'
elif row_count > 1000 and row_count <1000000 :
    formatted_count = f"{row_count / 1000:.1f}k "
elif row_count > 1000000  :
    formatted_count = f"{row_count / 1000000:.1f}M"

## Total revenue
total_revenue = sum(df['Final Sale'])
if total_revenue < 1000:
    formatted_revenue = f"{total_revenue} EGP"
elif 1000 <= total_revenue < 1000000:
    formatted_revenue = f"{total_revenue / 1000:.1f}k EGP"
elif total_revenue >= 1000000:
    formatted_revenue = f"{total_revenue / 1000000:.1f}M EGP"

## total sold items
total_sold_items = sum(df['Quantity'])

if total_sold_items < 1000 :
    formatted_sold_items = f'{total_sold_items} Item'
elif total_sold_items >=  1000 and total_sold_items < 1000000 : 
    formatted_sold_items = f"{total_sold_items / 1000:.1f}k Item"
elif total_sold_items > 1000000 : 
    formatted_sold_items = f"{total_sold_items / 1000000:.1f}M Item"

## Average Order Value
average_order_value = (sum(df['Final Sale']) / row_count)
if average_order_value < 1000 :
    formatted_avg_value = f"{round(average_order_value,2)} EGP"
elif average_order_value >=  1000 and average_order_value < 1000000 : 
    formatted_avg_value = f"{round(average_order_value,2) / 1000:.1f}k EGP"
elif average_order_value > 1000000 : 
    formatted_avg_value = f"{round(average_order_value,2) / 1000000:.1f}M EGP"

##Group By Category


main_col1, main_col2 = st.columns(2)

with main_col1:
    sub_col1, sub_col2 = st.columns(2)
    
    with sub_col1:
        st.subheader('Total Sales Orders')
        st.markdown(
            f"""
            <h1 style="font-size:48px; color:green;">{formatted_count}</h1>
             """,
            unsafe_allow_html=True
        )

        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')



        st.subheader('Total Sold Items')
        st.markdown(
            f"""
            <h1 style="font-size:48px; color:green;">{formatted_sold_items}</h1>
             """,
            unsafe_allow_html=True
        )

    with sub_col2:
        st.subheader('Total Revenue')
        st.markdown(
            f"""
            <h1 style="font-size:48px; color:green;">{formatted_revenue}</h1>
             """,
            unsafe_allow_html=True
        )

        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        
        st.subheader('Average Order Value')
        st.markdown(
            f"""
            <h1 style="font-size:48px; color:green;">{formatted_avg_value}</h1>
             """,
            unsafe_allow_html=True
        )

with main_col2:
    sub_col4 = st.columns(1)[0]  
    with sub_col4:
        st.subheader('Distribution Of Sold Categories')
        st.plotly_chart(px.pie(data_frame=df, names='Category' ,color_discrete_sequence=px.colors.sequential.Viridis , hole = 0.5))

sub_col3 = st.columns(1)[0] 
with sub_col3:
        st.subheader('Products Performance')
        st.plotly_chart(px.histogram(data_frame=df , x= df['Item']))

main_col3, main_col4 = st.columns(2)

with main_col3:
    sub_col1, sub_col2 = st.columns(2)
    
    with sub_col1:
        st.subheader('Top 5 Sold Products')
        top_5_items = df['Item'].value_counts().head(5).reset_index()
        top_5_df = pd.DataFrame(top_5_items)
        st.plotly_chart(px.histogram(data_frame=top_5_df, x='Item',y= 'count',color_discrete_sequence=['green']))

    with sub_col2:
        st.subheader('Least 5 Sold Products')
        top_5_items = df['Item'].value_counts().tail(5).reset_index()
        top_5_df = pd.DataFrame(top_5_items)
        st.plotly_chart(px.histogram(data_frame=top_5_df, x='Item',y= 'count',color_discrete_sequence=['red']))
    
with main_col4 :
    st.subheader('Payment Method Distribution')
    st.plotly_chart(px.pie(data_frame=df , names = df['Payment Method'] , hole = 0.5, color_discrete_sequence= px.colors.sequential.Viridis))


## Sales order by month 
df['Month'] = df['Transaction Date'].dt.month_name()
sales_orders_in_month = df.groupby('Month').size().reset_index(name='Number of Orders')

# Sort the DataFrame by calendar month order
sales_orders_in_month['Month'] = pd.Categorical(
    sales_orders_in_month['Month'],
    categories=['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December'],
    ordered=True
)
sales_orders_in_month = sales_orders_in_month.sort_values('Month')
pd.DataFrame(sales_orders_in_month).reset_index()


sub_col4 = st.columns(1)[0] 
with sub_col4:
    fig = px.line(
        sales_orders_in_month, 
        x='Month', 
        y='Number of Orders', 
        markers=True,  
        title='Sales Orders by Month'
    )
    st.plotly_chart(fig)

## Sales order by WeekDay 

df['WeekDay'] = df['Transaction Date'].dt.day_name()
sales_orders_in_day = df.groupby('WeekDay').size().reset_index(name='Number of Orders')
sales_orders_in_day['WeekDay'] = pd.Categorical(
    sales_orders_in_day['WeekDay'],
    categories=['Saturday', 'Sunday', 'Monday', 'Tuesday' , 'Wednnsday' , 'Thursday' , 'Friday' ,],
    ordered=True
)
sales_orders_in_day = sales_orders_in_day.sort_values('WeekDay')
pd.DataFrame(sales_orders_in_day).reset_index()

## Revenue By Category
category_revenue = df.groupby('Category').sum('Final Sale').reset_index()
result = category_revenue.filter(['Category', 'Final Sale'])
pd.DataFrame(result)

## Revenue By Customer
category_revenue = df.groupby('Customer ID').sum('Final Sale').reset_index()
result2 = category_revenue.filter(['Customer ID', 'Final Sale'])
pd.DataFrame(result2)

## Revenue By Location
location_revenue = df.groupby('Location').sum('Final Sale').reset_index()
result3 = location_revenue.filter(['Location', 'Final Sale'])
pd.DataFrame(result3)

main_col5, main_col6 = st.columns(2)
with main_col5 :
    st.plotly_chart(px.line(sales_orders_in_day , x='WeekDay' , y= 'Number of Orders' , markers = True , title = 'Sales Orders By Day'))
    st.plotly_chart(px.histogram(data_frame=df , x= df['Location'] , title = 'Location Distribution Of Sold Orders'))
    st.plotly_chart(px.bar(data_frame=result , x = result['Category'] , y=result['Final Sale'] , title= 'Total Revenue by Category' , color_discrete_sequence= ['green']))
    st.plotly_chart(
    px.histogram(
        data_frame=result,
        x=result3['Final Sale'],
        y=result3['Location'],
        title='Total Revenue by Location',
        color_discrete_sequence=['green'],
        labels={
            'x': 'Final Sale (EGP)',  # Label for the x-axis
            'y': 'Location',         # Label for the y-axis
        }
    )
    )



with main_col6 :
    st.plotly_chart(px.pie(data_frame=df , names= df['Is Weekend'] , title='Orders Sold In Weekend?' , color_discrete_sequence= px.colors.sequential.Viridis))
    st.plotly_chart(px.bar(data_frame=df , x = df['Discount Applied'] , title = 'Orders With Discount Applied'))
    st.plotly_chart(px.line(data_frame= result2 , x='Customer ID' , y= 'Final Sale' , markers = True , title = 'Customers Spent'))
    fig = px.scatter(
    df,
    x='Percentage of Discount',
    y='Final Sale',
    title='Discount Percentage vs. Total Revenue',
    labels={'Percentage of Discount': 'Discount Percentage (%)', 'Final Sale': 'Total Revenue (EGP)'},
    color='Percentage of Discount',  # Optional: Color by discount percentage
    size='Final Sale')
    st.plotly_chart(fig)
    
   


    


    
    



    
