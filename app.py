<<<<<<< HEAD
# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px  

data = pd.read_csv("data/data.csv")

def main():
    st.title("Instacart Dashboard")
    st.sidebar.title("Sidebar")

    layout = go.Layout(
        title_font=dict(size=25),
        font=dict(family="Courier New, monospace"),
        colorway=px.colors.qualitative.D3  # Consistent color scheme
    )
    # metric 기능써보기
    total_orders = data['order_id'].nunique()
    average_items_per_order = data.groupby('order_id')['product_id'].count().mean()
    peak_order_hour = data['order_hour_of_day'].value_counts().idxmax()

    # 이전 시간대와 비교할 데이터 (임시)
    total_orders_change = "-1%"
    average_items_change = "0.5%"
    peak_order_hour_change = "1 hour earlier"

    # Streamlit 대시보드
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 주문 수", total_orders, total_orders_change)
    with col2:
        st.metric("주문 당 평균 상품수", f"{average_items_per_order:.2f}", average_items_change)
    with col3:
        st.metric("주문이 많은 시간대", f"{peak_order_hour}:00", peak_order_hour_change)

    st.divider()

    # 인기 카테고리 - Treemap
    st.write("인기 카테고리")
    department_orders = data.groupby('department')['product_id'].count().reset_index()
    fig1 = px.treemap(
        department_orders,
        path=['department'],
        values='product_id',
        color='product_id',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig1, use_container_width=True)

    tab1, tab2 = st.tabs(["요일별", "시간대별"])

    # 요일별 주문수 - Bar Chart
    with tab1:
        with st.expander("**설명 보기**"):
            st.write("""
                아래의 막대 차트는 **각 요일별 주문수**를 보여준다. 이 데이터를 통해 어떤 요일에 주문이 많고 적은지 파악할 수 있다. 이 데이터를 통해, **마케팅 캠페인을 계획**하거나, **인력 및 자원 배치를 최적화**할 수 있다. 
            """)
        dow = data['order_dow'].value_counts().sort_index()
        dow_days = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일']


        fig2 = px.bar(
            x=dow_days,
            y=dow,
            labels={'x': '요일', 'y': '주문수'},
            title='요일별 주문수',
            text=dow
            )

        fig2.update_layout(layout,
        xaxis=dict(title='요일', tickangle=-45),  
        yaxis=dict(title='주문수'),
        )

        annotations = []
        for i, value in enumerate(dow):
            annotations.append(dict(x=dow_days[i], y=value, text=str(value),
                                    font=dict(family='Arial', size=12,
                                    color='rgb(50, 171, 96)'),
                                    showarrow=False))
        fig2.update_layout(annotations=annotations)

        st.plotly_chart(fig2, use_container_width=True)





    # 시간대별 주문수 - Line Chart
    with tab2:
        with st.expander("**설명 보기**"):
            st.write("""
                아래의 선 차트는 하루 중 **각 시간대별 주문수**를 보여준다. 특정 시간대에 주문이 집중되는지 파악하고, 그 시간대에 맞춰 **재고 관리나 배송 준비**를 최적화할 수 있다. 또한, 사용자들이 가장 활발하게 활동하는 시각을 파악하여, 그 시간대에 맞춰 **광고나 프로모션을 집행**하여 마케팅 효과를 극대화할 수 있다.
            """)
        hourly_orders = data.groupby('order_hour_of_day')['order_id'].count().reset_index()
        fig3 = px.line(
            hourly_orders,
            x='order_hour_of_day',
            y='order_id',
            title='시간대별 주문수',
            labels={'order_hour_of_day': 'Hour of Day', 'order_id': 'Number of Orders'}
        )
        fig3.update_layout(layout)
        st.plotly_chart(fig3, use_container_width=True)



    st.divider()

    # 전체 데이터 표
    st.write("전체데이터")
    st.dataframe(data)

    # Sidebar - 인기제품 top10
    side_tab1, side_tab2 = st.sidebar.tabs(["Best", "Reorder"])
    with side_tab1:
        st.write("Best 10")
        top_products = data['product_name'].value_counts().sort_values(ascending=False).head(10)
        st.dataframe(top_products)

    # Sidebar - 재주문 많은 제품 top 10
    with side_tab2:
        st.write("재주문 100% 제품")
        total_orders_per_product = data.groupby('product_name')['order_id'].count()
        reorder_per_product = data[data['reordered'] == 1].groupby('product_name')['order_id'].count()
        reorder_ratio = ((reorder_per_product / total_orders_per_product) * 100).sort_values(ascending=False)
        reorder_100 = reorder_ratio[reorder_ratio == 100]
        st.dataframe(reorder_100)


if __name__ == "__main__":
    main()
=======
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


