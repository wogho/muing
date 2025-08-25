import subprocess
import sys
from pathlib import Path

print("🔍 Muing 환경 진단")
print("=" * 50)

# Python 버전
print(f"Python: {sys.version}")

# Demucs 확인
try:
    import demucs
    print(f"✅ Demucs 설치됨: {demucs.__version__}")
except:
    print("❌ Demucs 없음")

# CLI 확인
result = subprocess.run("which demucs", shell=True, capture_output=True, text=True)
if result.stdout:
    print(f"✅ Demucs CLI: {result.stdout.strip()}")
else:
    print("❌ Demucs CLI 없음")

# 디렉토리 확인
print(f"\n📁 현재 위치: {Path.cwd()}")
print(f"📁 data/ 존재: {Path('data').exists()}")
print(f"📁 outputs/ 존재: {Path('outputs').exists()}")

# 테스트 파일
if Path("data/test.mp3").exists():
    print(f"✅ 테스트 파일: {Path('data/test.mp3').stat().st_size / 1024:.1f} KB")
else:
    print("❌ 테스트 파일 없음")

print("=" * 50)
