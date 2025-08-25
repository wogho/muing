import subprocess
import os
from pathlib import Path

# 짧은 테스트 파일 다운로드 (30초)
os.makedirs("data", exist_ok=True)
os.makedirs("outputs/separated", exist_ok=True)

print("📥 짧은 샘플 다운로드...")
os.system("wget -q https://file-examples.com/storage/fe1170c816762d3e51cbce0/2017/11/file_example_MP3_700KB.mp3 -O data/short.mp3")

print("🎵 Demucs 실행 (30초 샘플)...")
cmd = "demucs --two-stems=vocals -d cpu -o outputs/separated data/short.mp3"
result = os.system(cmd)

if result == 0:
    print("✅ 성공!")
    print("📁 결과: outputs/separated/htdemucs/short/")
    os.system("ls -la outputs/separated/htdemucs/short/")
else:
    print("❌ 실패 - Streamlit UI를 먼저 만드세요")
