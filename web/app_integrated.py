"""
Muing Web - separator.py 통합 버전
"""
import streamlit as st
from pathlib import Path
import sys
import time

# 프로젝트 경로 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Muing separator import
from core.separator import MuingSeparator

st.set_page_config(
    page_title="Muing - AI Music Analysis",
    page_icon="🎵",
    layout="wide"
)

# 초기화
@st.cache_resource
def get_separator():
    """Separator 인스턴스 캐싱"""
    return MuingSeparator()

# 헤더
st.title("🎵 Muing (뮤잉)")
st.markdown("AI 기반 음악 분석 플랫폼 - **음원 분리 성공!**")

# 파일 업로더
uploaded_file = st.file_uploader(
    "음악 파일 선택",
    type=['mp3', 'wav', 'm4a'],
    help="3분 이내 권장"
)

if uploaded_file:
    # 파일 정보
    col1, col2 = st.columns(2)
    with col1:
        st.audio(uploaded_file)
    with col2:
        st.metric("파일명", uploaded_file.name)
        st.metric("크기", f"{uploaded_file.size/1024:.1f} KB")
    
    # 임시 저장
    temp_path = PROJECT_ROOT / "temp" / uploaded_file.name
    temp_path.parent.mkdir(exist_ok=True)
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 분리 버튼
    if st.button("🎸 음원 분리 시작", type="primary"):
        with st.spinner("AI가 음악을 분석 중... (30초~1분)"):
            # MuingSeparator 사용
            separator = get_separator()
            result = separator.separate_file(temp_path)
            
            if result['success']:
                st.success("✅ 분리 완료!")
                st.balloons()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🎤 보컬")
                    if result['vocals'].exists():
                        st.audio(str(result['vocals']))
                        
                with col2:
                    st.markdown("### 🎸 반주")
                    if result['accompaniment'].exists():
                        st.audio(str(result['accompaniment']))
            else:
                st.error(f"분리 실패: {result['error']}")
else:
    st.info("👆 음악 파일을 업로드하세요")
    
    # 테스트 파일 사용
    if st.button("🧪 테스트 파일로 시도"):
        test_file = PROJECT_ROOT / "data" / "tiny_test.mp3"
        if test_file.exists():
            with st.spinner("테스트 중..."):
                separator = get_separator()
                result = separator.separate_file(test_file)
                
                if result['success']:
                    st.success("테스트 성공!")
                    st.info(f"결과: {result['path']}")
