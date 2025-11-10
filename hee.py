import streamlit as st
import pandas as pd
import requests # 이미지가 실제로 있는지 확인하기 위해 사용할 수 있습니다.

# 📌 가상의 국가지질공원 데이터 생성 및 업데이트
@st.cache_data
def load_data():
    data = {
        '공원_이름': [
            '제주도 지질공원', 
            '청송 국가지질공원', 
            '무등산권 국가지질공원', 
            '한탄강 국가지질공원',
            '부산 국가지질공원'
        ],
        '위도': [33.3617, 36.4385, 35.1226, 38.0076, 35.1578],
        '경도': [126.5458, 129.2155, 126.9859, 127.1818, 129.0700],
        '특징': [
            '화산 지형과 동굴', 
            '백악기 퇴적암과 응회암', 
            '무등산 주상절리와 광주천', 
            '현무암 협곡과 폭포',
            '퇴적암 지층과 해안 지형'
        ],
        # ⭐ 추가: 가상의 상세 이미지 URL (실제 이미지를 링크로 대체하세요)
        '이미지_URL': [
            'https://upload.wikimedia.org/wikipedia/commons/e/e4/Jeju-island_hallasan.jpg', # 제주 한라산 (예시)
            'https://upload.wikimedia.org/wikipedia/commons/d/df/Cheongsong_Jusangjeolli.jpg', # 청송 주산지 (예시)
            'https://upload.wikimedia.org/wikipedia/commons/2/27/Mudeungsan_national_park_view.jpg', # 무등산 (예시)
            'https://upload.wikimedia.org/wikipedia/commons/2/22/Hantan_River_Jusangjeolli.jpg', # 한탄강 (예시)
            'https://upload.wikimedia.org/wikipedia/commons/e/e7/Taejongdae_Busan_Korea.jpg' # 부산 태종대 (예시)
        ],
        # ⭐ 추가: 가상의 서울 출발 예상 이동 시간 (자가용 기준, 대략적인 추정치)
        # 실제 API를 사용하지 않고 단순 텍스트로 표시합니다.
        '서울_출발_시간': [
            '항공편 이용 (약 1시간)',
            '약 3시간 30분',
            '약 4시간',
            '약 1시간 30분',
            '약 4시간 30분'
        ]
    }
    df = pd.DataFrame(data)
    return df

# 데이터 로드
df = load_data()

## 🌟 앱 레이아웃 설정
st.title("🇰🇷 국가지질공원 탐색기")
st.markdown("---")

## 🗺️ 사이드바: 공원 선택 및 정보 표시
st.sidebar.header("🔎 공원 선택")
selected_park_name = st.sidebar.selectbox(
    '정보를 보고 싶은 지질공원을 선택하세요:',
    df['공원_이름']
)

# 선택된 공원 정보 필터링
selected_park = df[df['공원_이름'] == selected_park_name].iloc[0]

st.sidebar.subheader(f"✨ {selected_park_name} 정보")
st.sidebar.write(f"**주요 특징:** {selected_park['특징']}")
st.sidebar.write(f"**서울 출발 예상 이동 시간:** {selected_park['서울_출발_시간']}") # ⭐ 이동 시간 추가
st.sidebar.write(f"**위도:** {selected_park['위도']:.4f}")
st.sidebar.write(f"**경도:** {selected_park['경도']:.4f}")

## 🖼️ 상세 이미지 표시 (메인 화면)
st.header(f"⛰️ {selected_park_name} 상세 이미지")
image_url = selected_park['이미지_URL']

try:
    # URL로 이미지를 표시합니다.
    st.image(image_url, caption=f"{selected_park_name}의 주요 지질 명소", use_column_width=True)
except:
    st.warning("이미지를 불러오지 못했습니다. URL을 확인하거나 로컬 파일을 사용하세요.")


## 📍 지도 시각화
st.header("선택된 공원의 위치")

map_data = pd.DataFrame({
    'lat': [selected_park['위도']],
    'lon': [selected_park['경도']]
})

st.map(map_data, zoom=9)

## 📊 전체 데이터 테이블 (옵션)
st.markdown("---")
if st.checkbox('전체 지질공원 데이터 보기'):
    st.subheader("전체 국가지질공원 목록")
    st.dataframe(df)

# 앱 실행 방법
st.markdown(
    """
    <br>
    **실행 방법:**
    터미널에서 다음 명령어를 입력하세요:
    `streamlit run app.py`
    """, 
    unsafe_allow_html=True
)
