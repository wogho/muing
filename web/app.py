"""
Muing Web Interface - 실제 작동 버전
"""
import streamlit as st
from pathlib import Path
import subprocess
import time
import os
import base64

st.set_page_config(
    page_title="Muing - AI Music Analysis",
    page_icon="🎵",
    layout="wide"
)

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent

def separate_audio(input_path, output_dir="separated"):
    """실제 Demucs 실행"""
    cmd = f"demucs --two-stems=vocals -d cpu -o {output_dir} {input_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        # 결과 경로 찾기
        stem_name = Path(input_path).stem
        result_path = Path(output_dir) / "htdemucs" / stem_name
        if result_path.exists():
            return result_path
    return None

def get_download_link(file_path, file_label):
    """다운로드 링크 생성"""
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="{Path(file_path).name}">💾 {file_label} 다운로드</a>'
    return href

# 헤더
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🎵 Muing (뮤잉)")
    st.markdown("**AI 기반 음악 분석 플랫폼**")

st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("📊 Day 1 성과")
    st.success("✅ 음원 분리 구현 완료!")
    st.progress(100)
    
    st.markdown("---")
    st.markdown("### 🎯 다음 목표")
    st.markdown("- ⏳ 멜로디 추출 (Day 2)")
    st.markdown("- ⏳ 코드 진행 분석 (Day 3)")
    st.markdown("- ⏳ 리듬 패턴 인식 (Day 4)")
    
    st.markdown("---")
    st.info("**팁**: 3분 이내의 음원을 사용하면 더 빠르게 처리됩니다")

# 메인 컨텐츠
tab1, tab2, tab3 = st.tabs(["🎸 음원 분리", "📝 사용 가이드", "📊 결과 갤러리"])

with tab1:
    st.header("AI 음원 분리")
    
    # 파일 업로더
    uploaded_file = st.file_uploader(
        "음악 파일을 업로드하세요",
        type=['mp3', 'wav', 'm4a', 'ogg'],
        help="최적 성능을 위해 3분 이내, 10MB 이하 권장"
    )
    
    if uploaded_file:
        # 파일 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("파일명", uploaded_file.name[:20] + "...")
        with col2:
            st.metric("크기", f"{uploaded_file.size/1024/1024:.1f} MB")
        with col3:
            st.metric("형식", uploaded_file.type.split('/')[-1].upper())
        
        # 원본 오디오 플레이어
        st.markdown("### 🎧 원본 오디오")
        st.audio(uploaded_file)
        
        # 임시 파일 저장
        temp_dir = PROJECT_ROOT / "temp"
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / uploaded_file.name
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 분리 버튼
        if st.button("🚀 AI 음원 분리 시작", type="primary", use_container_width=True):
            
            # Progress 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_text = st.empty()
            
            # 시작 시간
            start_time = time.time()
            
            # 상태 업데이트
            with st.spinner(""):
                for i in range(30):
                    progress_bar.progress(i/100)
                    status_text.text(f"🔄 AI 모델 로딩 중... {i}%")
                    time_text.text(f"경과 시간: {time.time()-start_time:.1f}초")
                    time.sleep(0.1)
                
                status_text.text("🎵 음원 분석 중...")
                progress_bar.progress(30)
                
                # 실제 분리 실행
                output_dir = PROJECT_ROOT / "separated"
                result_path = separate_audio(temp_path, output_dir)
                
                # 완료
                progress_bar.progress(100)
                elapsed = time.time() - start_time
                status_text.text(f"✅ 분리 완료!")
                time_text.text(f"총 소요 시간: {elapsed:.1f}초")
            
            if result_path and result_path.exists():
                st.success("🎉 음원 분리 성공!")
                st.balloons()
                
                # 결과 표시
                st.markdown("### 🎼 분리된 트랙")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🎤 보컬 트랙")
                    vocal_path = result_path / "vocals.wav"
                    if vocal_path.exists():
                        st.audio(str(vocal_path))
                        st.markdown(get_download_link(vocal_path, "보컬"), unsafe_allow_html=True)
                        st.caption(f"파일 크기: {vocal_path.stat().st_size/1024/1024:.1f} MB")
                
                with col2:
                    st.markdown("#### 🎸 반주 트랙")
                    inst_path = result_path / "no_vocals.wav"
                    if inst_path.exists():
                        st.audio(str(inst_path))
                        st.markdown(get_download_link(inst_path, "반주"), unsafe_allow_html=True)
                        st.caption(f"파일 크기: {inst_path.stat().st_size/1024/1024:.1f} MB")
                
                # 추가 정보
                with st.expander("🔍 기술 정보"):
                    st.markdown(f"""
                    - **사용 모델**: HTDemucs (Hybrid Transformer Demucs)
                    - **처리 모드**: 2-stems (Vocals/Accompaniment)
                    - **처리 시간**: {elapsed:.1f}초
                    - **출력 형식**: WAV 44.1kHz
                    - **결과 경로**: `{result_path}`
                    """)
                
                # 성공 메시지
                st.info("💡 **활용 팁**: 분리된 보컬로 가라오케를 만들거나, 반주로 리믹스를 제작할 수 있습니다!")
                
            else:
                st.error("❌ 분리 실패. 다른 파일로 시도해보세요.")
    
    else:
        # 샘플 파일 제공
        st.info("👆 음악 파일을 업로드하거나 아래 샘플을 다운로드하세요")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("📥 샘플 파일 다운로드"):
                sample_path = PROJECT_ROOT / "data" / "tiny_test.mp3"
                if sample_path.exists():
                    st.markdown(get_download_link(sample_path, "샘플 음악"), unsafe_allow_html=True)

with tab2:
    st.header("📝 사용 가이드")
    
    st.markdown("""
    ### Muing 사용법
    
    1. **파일 업로드**: MP3, WAV, M4A 등 오디오 파일 업로드
    2. **분리 시작**: 'AI 음원 분리 시작' 버튼 클릭
    3. **대기**: 30초~2분 정도 대기 (파일 크기에 따라 다름)
    4. **결과 확인**: 보컬과 반주가 분리된 결과 확인
    5. **다운로드**: 필요한 트랙 다운로드
    
    ### 최적 사용 조건
    - 파일 크기: 10MB 이하
    - 곡 길이: 3분 이내
    - 음질: 128kbps 이상
    
    ### 활용 예시
    - 🎤 **가라오케 제작**: 보컬 제거된 반주 사용
    - 🎧 **리믹스**: 분리된 트랙으로 새로운 편곡
    - 📚 **음악 학습**: 특정 파트만 분리해서 연습
    - 🎵 **커버 제작**: 원곡 반주에 새로운 보컬 녹음
    """)

with tab3:
    st.header("📊 결과 갤러리")
    
    # separated 디렉토리의 결과들 표시
    separated_dir = PROJECT_ROOT / "separated" / "htdemucs"
    
    if separated_dir.exists():
        results = list(separated_dir.iterdir())
        if results:
            st.success(f"🎵 총 {len(results)}개의 분리 결과")
            
            for result in results[-5:]:  # 최근 5개만
                with st.expander(f"📁 {result.name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        vocal_file = result / "vocals.wav"
                        if vocal_file.exists():
                            st.markdown("**🎤 보컬**")
                            st.audio(str(vocal_file))
                    with col2:
                        inst_file = result / "no_vocals.wav"
                        if inst_file.exists():
                            st.markdown("**🎸 반주**")
                            st.audio(str(inst_file))
        else:
            st.info("아직 분리된 결과가 없습니다")
    else:
        st.info("첫 번째 음원을 분리해보세요!")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🛠️ Muing v0.1.0 | Built with ❤️ using Demucs & Streamlit</p>
        <p><a href='https://github.com/yourusername/muing'>GitHub</a> | 
        Day 1 - Mission Complete! 🎉</p>
    </div>
    """,
    unsafe_allow_html=True
)
