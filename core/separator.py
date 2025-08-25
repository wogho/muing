"""
Muing Core - 음원 분리 모듈
경로 문제 해결 버전
"""
import os
import subprocess
from pathlib import Path
import logging
import sys

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent  # /workspaces/muing
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MuingSeparator:
    """Muing 음원 분리 엔진"""
    
    def __init__(self, model="htdemucs", device="cpu"):
        self.model = model
        self.device = device
        # 프로젝트 루트 기준으로 경로 설정
        self.output_dir = PROJECT_ROOT / "outputs" / "separated"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 출력 디렉토리: {self.output_dir}")
    
    def separate(self, audio_path, stems=2):
        """음원 분리 실행"""
        # 상대 경로를 절대 경로로 변환
        if not Path(audio_path).is_absolute():
            audio_path = PROJECT_ROOT / audio_path
        
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            logger.error(f"❌ 파일이 없습니다: {audio_path}")
            logger.info(f"💡 현재 디렉토리: {Path.cwd()}")
            logger.info(f"💡 프로젝트 루트: {PROJECT_ROOT}")
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {audio_path}")
        
        logger.info(f"🎵 Muing 음원 분리 시작: {audio_path.name}")
        logger.info(f"📊 파일 크기: {audio_path.stat().st_size / 1024:.1f} KB")
        
        # Demucs 명령어 구성
        cmd = [
            "python", "-m", "demucs.separate",
            "-n", self.model,
            "-d", self.device,
            "-o", str(self.output_dir)
        ]
        
        if stems == 2:
            cmd.append("--two-stems=vocals")
        
        cmd.append(str(audio_path))
        
        # 실행
        try:
            logger.info("🔄 Demucs 실행 중... (1-2분 소요)")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("✅ 분리 완료!")
            result_path = self.output_dir / self.model / audio_path.stem
            logger.info(f"📁 결과 저장 위치: {result_path}")
            return result_path
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ 분리 실패: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("❌ Demucs가 설치되지 않았습니다")
            logger.info("💡 설치 명령: pip install demucs")
            raise

def download_test_file():
    """테스트 파일 다운로드"""
    test_file = PROJECT_ROOT / "data" / "test.mp3"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    if not test_file.exists():
        logger.info("📥 테스트 파일 다운로드 중...")
        import urllib.request
        url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        urllib.request.urlretrieve(url, test_file)
        logger.info(f"✅ 다운로드 완료: {test_file}")
    else:
        logger.info(f"✅ 테스트 파일 존재: {test_file}")
    
    return test_file

# 테스트
if __name__ == "__main__":
    logger.info("🎵 Muing 음원 분리 테스트 시작")
    logger.info(f"📍 현재 위치: {Path.cwd()}")
    logger.info(f"📍 프로젝트 루트: {PROJECT_ROOT}")
    
    # 테스트 파일 준비
    test_file = download_test_file()
    
    # 분리 실행
    try:
        separator = MuingSeparator()
        result = separator.separate(test_file)
        logger.info(f"🎉 테스트 성공! 결과: {result}")
        
        # 결과 파일 확인
        if result.exists():
            files = list(result.glob("*.wav"))
            logger.info(f"📊 생성된 파일: {len(files)}개")
            for f in files:
                logger.info(f"  - {f.name}: {f.stat().st_size / 1024 / 1024:.1f} MB")
    except Exception as e:
        logger.error(f"❌ 테스트 실패: {e}")
        logger.info("💡 다음을 시도해보세요:")
        logger.info("  1. pip install demucs")
        logger.info("  2. cd /workspaces/muing")
        logger.info("  3. python muing/core/separator.py")