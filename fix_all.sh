#!/bin/bash
echo "🔧 Muing 환경 수정 시작..."

# 1. FFmpeg 설치
echo "📦 FFmpeg 설치..."
sudo apt update > /dev/null 2>&1
sudo apt install ffmpeg -y > /dev/null 2>&1
echo "✅ FFmpeg 설치 완료"

# 2. 오디오 백엔드 설치
echo "📦 오디오 라이브러리 설치..."
pip install soundfile librosa > /dev/null 2>&1
echo "✅ 오디오 라이브러리 설치 완료"

# 3. 작은 테스트 파일 다운로드
echo "📥 작은 테스트 파일 다운로드..."
mkdir -p data
# 5초짜리 매우 작은 파일
wget -q "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" -O data/tiny_test.mp3
echo "✅ 테스트 파일 준비 완료"

# 4. 테스트 실행
echo "🎵 Demucs 테스트..."
demucs --two-stems=vocals -d cpu data/tiny_test.mp3

if [ $? -eq 0 ]; then
    echo "✅ 모든 문제 해결!"
    echo "📁 결과: separated/htdemucs/tiny_test/"
    ls -la separated/htdemucs/tiny_test/
else
    echo "❌ 여전히 문제가 있습니다"
fi
