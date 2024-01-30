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
    # metric 기능 써보기
    total_orders = data['order_id'].nunique() # 총 주문수
    average_items_per_order = data.groupby('order_id')['product_id'].count().mean() # 주문당 상품수
    peak_order_hour = data['order_hour_of_day'].value_counts().idxmax() # 주문 많은 시간
    top_product = data['product_name'].value_counts().idxmax()  # 가장 많이 주문된 제품

    # 임시로 비교할 데이터 만들기
    total_orders_change = "-1%"
    average_items_change = "0.5%"
    peak_order_hour_change = "1 hour earlier"
    top_product_change = "2 more orders" 

    # 열 4개 설정하기
    col1, col2, col3, col4 = st.columns(4) 
    with col1:
        with st.container(height=150, border=True):
            st.metric("총 주문 수", total_orders, total_orders_change)
    with col2:
        with st.container(height=150, border=True):
            st.metric("주문 당 평균 상품수", f"{average_items_per_order:.2f}", average_items_change)
    with col3:
        with st.container(height=150, border=True):
            st.metric("주문이 많은 시간대", f"{peak_order_hour}:00", peak_order_hour_change)
    with col4:
        with st.container(height=150, border=True):
            st.metric("가장 인기 있는 제품", top_product, top_product_change)  # 새로운 메트릭 추가


    st.divider()

    # 인기 카테고리 - Treemap
    with st.container(border=True):
        st.subheader("인기 카테고리")
        department_orders = data.groupby('department')['product_id'].count().reset_index()
        fig1 = px.treemap(
            department_orders,
            path=['department'],
            values='product_id',
            color='product_id',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with st.container(border=True):
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
                    아래의 선 차트는 하루 중 **각 시간대별 주문수**를 보여준다. 어떤 시간대에 주문이 집중되는지 파악하고, 그 시간대에 맞춰 **재고 관리나 배송 준비**를 최적화할 수 있다. 또한, 사용자들이 가장 활발하게 활동하는 시간대에 맞춰 **광고나 프로모션을 집행**하여 마케팅 효과를 극대화할 수 있다.
                """)
            hourly_orders = data.groupby('order_hour_of_day')['order_id'].count().reset_index()
            fig3 = px.line(
                hourly_orders,
                x='시간대',
                y='주문수',
                title='시간대별 주문수',
                labels={'order_hour_of_day': 'Hour of Day', 'order_id': 'Number of Orders'}
            )
            fig3.update_layout(layout)
            st.plotly_chart(fig3, use_container_width=True)



    st.divider()

    with st.container(border=True):
        st.subheader("카테고리별 인기제품")
        department_list = data['department'].unique().tolist()
        selected_departments = st.multiselect(
            '선택한 카테고리의 인기 제품 보기',
            department_list,
            default=department_list[0]  # 기본적으로 첫 번째 department 선택
        )
        if selected_departments:
            # 선택된 department의 데이터 필터링
            filtered_data = data[data['department'].isin(selected_departments)]
            
            # 제품별 주문수 계산
            top_products = filtered_data['product_name'].value_counts().reset_index()
            top_products.columns = ['Product Name', 'Order Count']
            
            # 결과 표시
            st.write(f'선택한 카테고리: {selected_departments}')
            st.write('인기 제품 Top:')
            st.dataframe(top_products)


    st.divider()
    # 전체 데이터 표
    with st.container(border=True):
        st.write("전체데이터")
        st.link_button("Instacart Market Basket Analysis", "https://www.kaggle.com/c/instacart-market-basket-analysis")
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

    with st.sidebar:
        st.info(" 설연휴 배송 기간 연장 안내", icon="ℹ️")


if __name__ == "__main__":
    main()
