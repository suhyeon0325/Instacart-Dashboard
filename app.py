# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import plotly.figure_factory as ff


data = pd.read_csv("data/data.csv")

def main():
    st.title("Instacart Dashboard")
    
    # 인기 카테고리
    department_orders = data.groupby('department')['product_id'].count().reset_index()
    fig1 = go.Figure(go.Treemap(
    labels = department_orders['department'],
    parents = [''] * department_orders.shape[0],
    values = department_orders['product_id'],
    textinfo = "label+value"
    ))
    fig1.update_layout(
    title_text='인기 카테고리')
    st.plotly_chart(fig1)


    
    # 요일별 주문수 bar차트
    dow = data['order_dow'].value_counts().sort_values(ascending=False)
    dow_days = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일']  

    fig2 = go.Figure(data=[go.Bar(x=dow_days, y=data['order_dow'].value_counts().sort_index())])
    fig2.update_layout(title='요일별 주문수', xaxis_title='요일', yaxis_title='주문수')
    st.plotly_chart(fig2, use_container_width=True)

    # 시간대별 주문수 line chart
    hourly_orders = data.groupby('order_hour_of_day')['order_id'].count().reset_index()
    fig3 = go.Figure(go.Scatter(x=hourly_orders['order_hour_of_day'], y=hourly_orders['order_id'], mode='lines+markers'))
    fig3.update_layout(
        title_text='시간대별 주문수',
        title_x=0.5,
        xaxis_title='Hour of Day',
        yaxis_title='Number of Orders',
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 전체 데이터 표
    st.write("전체데이터")
    st.dataframe(data)

    # 사이드바
    # 인기제품 top10
    with st.sidebar:
        st.write("Best 10")
        top_products = data['product_name'].value_counts().sort_values(ascending=False).head(10)
        st.dataframe(top_products)

    # 재주문 많은 제품 top 10
    with st.sidebar:
        st.write("재주문 100% 제품")
        total_orders_per_product = data.groupby('product_name')['order_id'].count()
        reorder_per_product = data[data['reordered'] == 1].groupby('product_name')['order_id'].count()
        reorder_ratio = ((reorder_per_product / total_orders_per_product) * 100).sort_values(ascending=False)
        reorder_100 = reorder_ratio[reorder_ratio == 100]
        st.dataframe(reorder_100)
        





if __name__ == "__main__":
    main()

