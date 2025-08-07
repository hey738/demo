import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(layout="wide", page_title="병원 개원 비용 대시보드")

# 사용자 정의 CSS for metrics border
st.markdown(
    """
    <style>
    /* Metric 위젯에 테두리 추가 */
    .stMetric {
        border: 2px solid #4CAF50;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 사이드바: 입력 변수
st.sidebar.header("입력 변수")
region = st.sidebar.selectbox("개원 지역", ["서울", "부산", "대구", "인천", "기타"])
area = st.sidebar.number_input("병원 평수", min_value=10, value=30, step=1)
nurses = st.sidebar.number_input("간호사 수", min_value=0, value=1, step=1)
assistants = st.sidebar.number_input("간호조무사 수", min_value=0, value=1, step=1)

# 장비 리스트 입력 (동적 추가 가능)
st.sidebar.markdown("---")
st.sidebar.subheader("장비 추가")
equipment = []
num_equip = st.sidebar.number_input("장비 항목 수", min_value=0, value=3, step=1)
for i in range(int(num_equip)):
    with st.sidebar.expander(f"장비 {i+1}"):
        name = st.text_input("장비명", key=f"name_{i}")
        brand = st.text_input("브랜드", key=f"brand_{i}")
        condition = st.selectbox("신품/중고 여부", ["신품", "중고"], key=f"cond_{i}")
        price = st.number_input("금액 (원)", min_value=0, value=0, step=100000, key=f"price_{i}")
        if name:
            equipment.append({"name": name, "brand": brand, "condition": condition, "price": price})

# 비용 계산
interior_cost = area * 3_000_000
employee_cost = nurses * 3_000_000 + assistants * 2_000_000
rent_deposit = area * 500_000
rent_monthly = area * 50_000
equipment_cost_total = sum(item['price'] for item in equipment)
other_cost = 50_000_000  # 기타비용

# 장비 도움말 문자열 생성
if equipment:
    equip_help = "\n".join([f"{item['name']}: {item['price']:,.0f}원" for item in equipment])
else:
    equip_help = "선택된 장비가 없습니다"

initial_cost = interior_cost + equipment_cost_total + rent_deposit + other_cost

# KPI 카드 표시
st.title("병원 개원 비용 한눈에 보기")

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="인테리어 비용", value=f"{interior_cost:,.0f}원", help=f"{area}평수 × 3,000,000원")
col2.metric(label="장비 구매 비용", value=f"{equipment_cost_total:,.0f}원", help=equip_help)
col3.metric(label="임차 보증금", value=f"{rent_deposit:,.0f}원", help=f"{area}평수 × 평균 평당가 50,000원 × 10배수")
col4.metric(label="기타 비용", value=f"{other_cost:,.0f}원", help="가전, 가구, 정수기, 네트워크 등")

st.markdown("---")
col5, col6, col7 = st.columns(3)
col5.metric(label="월 임대료", value=f"{rent_monthly:,.0f}원", help=f"{area}평수 × 평균 평당가 50,000원")
col6.metric(label="인건비 총합", value=f"{employee_cost:,.0f}원", help=f"간호사: {nurses}명×3,000,000원 + 간호조무사: {assistants}명×2,000,000명")
col7.metric(label="기타 비용", value=f"{10_000_000:,.0f}원", help=f"위수탁 비용 + 의약품 및 소모품 비용")

# 초기 비용 구성 차트
initial_df = pd.DataFrame({
    "항목": ["인테리어", "장비", "보증금", "기타"],
    "비용": [interior_cost, equipment_cost_total, rent_deposit, other_cost]
})
fig1 = px.pie(initial_df, names="항목", values="비용", title="초기 개원 비용 구성")
st.plotly_chart(fig1, use_container_width=True)

# 월 운영비 구성 차트
monthly_df = pd.DataFrame({
    "항목": ["임대료", "인건비", "기타 비용"],
    "비용": [rent_monthly, employee_cost, 10_000_000]
})
fig2 = px.pie(monthly_df, names="항목", values="비용", title="월 운영비 구성")
st.plotly_chart(fig2, use_container_width=True)
