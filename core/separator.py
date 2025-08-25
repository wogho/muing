"""
Muing Core - 음원 분리 모듈
FFmpeg 설치 후 작동 버전
"""
import os
import subprocess
from pathlib import Path
import logging
import sys

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class MuingSeparator:
    """Muing 음원 분리 엔진"""
    
    def __init__(self, model="htdemucs", device="cpu"):
        self.model = model
        self.device = device
        self.output_dir = PROJECT_ROOT / "separated"  # outputs 대신 separated 사용
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 출력 디렉토리: {self.output_dir}")
        
        # FFmpeg 확인
        if not self.check_ffmpeg():
            raise RuntimeError("FFmpeg가 설치되지 않았습니다")
    
    def check_ffmpeg(self):
        """FFmpeg 설치 확인"""
        try:
            result = subprocess.run("ffmpeg -version", shell=True, capture_output=True)
            if result.returncode == 0:
                logger.info("✅ FFmpeg 확인됨")
                return True
        except:
            pass
        
        logger.error("❌ FFmpeg가 없습니다. 설치: sudo apt install ffmpeg")
        return False
    
    def separate(self, audio_path, stems=2):
        """음원 분리 실행 - 단순하고 안정적인 버전"""
        # 경로 처리
        if not Path(audio_path).is_absolute():
            audio_path = PROJECT_ROOT / audio_path
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {audio_path}")
        
        logger.info(f"🎵 Muing 음원 분리 시작: {audio_path.name}")
        logger.info(f"📊 파일 크기: {audio_path.stat().st_size / 1024:.1f} KB")
        
        # Demucs 명령어 (가장 단순한 형태)
        if stems == 2:
            cmd = f"demucs --two-stems=vocals -d cpu -o {self.output_dir} \"{audio_path}\""
        else:
            cmd = f"demucs -d cpu -o {self.output_dir} \"{audio_path}\""
        
        logger.info(f"🔄 실행 명령: {cmd}")
        
        # 실행
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ 분리 완료!")
                
                # 결과 경로 찾기 (Demucs는 htdemucs 폴더에 저장)
                stem_name = audio_path.stem
                result_path = self.output_dir / "htdemucs" / stem_name
                
                if result_path.exists():
                    # 결과 파일 확인
                    files = list(result_path.glob("*.wav"))
                    logger.info(f"📁 결과 위치: {result_path}")
                    logger.info(f"�� 생성된 파일: {len(files)}개")
                    for f in files:
                        logger.info(f"  - {f.name}: {f.stat().st_size / 1024 / 1024:.1f} MB")
                    return result_path
                else:
                    logger.warning(f"⚠️ 예상 경로에 결과 없음: {result_path}")
                    # 다른 가능한 경로 탐색
                    for path in self.output_dir.iterdir():
                        if path.is_dir():
                            possible = path / stem_name
                            if possible.exists():
                                logger.info(f"📁 결과 발견: {possible}")
                                return possible
                    
                    logger.error("❌ 결과 파일을 찾을 수 없습니다")
                    return None
            else:
                logger.error(f"❌ Demucs 실행 실패")
                logger.error(f"에러: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 오류 발생: {e}")
            return None
    
    def separate_file(self, file_path):
        """외부에서 쉽게 사용할 수 있는 간단한 인터페이스"""
        try:
            result = self.separate(file_path)
            if result:
                return {
                    'success': True,
                    'path': result,
                    'vocals': result / "vocals.wav",
                    'accompaniment': result / "no_vocals.wav"
                }
            else:
                return {'success': False, 'error': 'Separation failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

def test_separator():
    """간단한 테스트 함수"""
    logger.info("=" * 50)
    logger.info("🎵 Muing Separator 테스트")
    logger.info("=" * 50)
    
    # 테스트 파일 확인
    test_files = [
        PROJECT_ROOT / "data" / "tiny_test.mp3",
        PROJECT_ROOT / "data" / "test.mp3",
        PROJECT_ROOT / "data" / "short_test.mp3"
    ]
    
    test_file = None
    for f in test_files:
        if f.exists():
            test_file = f
            logger.info(f"✅ 테스트 파일 발견: {test_file}")
            break
    
    if not test_file:
        logger.info("📥 테스트 파일 다운로드 중...")
        test_file = PROJECT_ROOT / "data" / "test.mp3"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        
        import urllib.request
        url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        urllib.request.urlretrieve(url, test_file)
        logger.info(f"✅ 다운로드 완료: {test_file}")
    
    # 분리 실행
    try:
        separator = MuingSeparator()
        result = separator.separate_file(test_file)
        
        if result['success']:
            logger.info("🎉 테스트 성공!")
            logger.info(f"📁 보컬: {result['vocals']}")
            logger.info(f"📁 반주: {result['accompaniment']}")
            return True
        else:
            logger.error(f"❌ 테스트 실패: {result['error']}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 오류: {e}")
        return False

if __name__ == "__main__":
    # 테스트 실행
    success = test_separator()
    
    if success:
        print("\n" + "=" * 50)
        print("✨ Muing Separator 준비 완료!")
        print("이제 web/app.py에서 사용할 수 있습니다")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("💡 문제 해결 방법:")
        print("1. sudo apt install ffmpeg")
        print("2. pip install demucs")
        print("3. 다시 실행: python core/separator.py")
        print("=" * 50)
