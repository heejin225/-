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
            'data:image/jpeg;base64,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', # 제주 한라산 (예시)
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

#
