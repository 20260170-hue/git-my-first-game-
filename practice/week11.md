# Week 11 실습

## 오늘 한 것
- Thonny에 PyInstaller 설치
중간 프로젝트 파일을 이용하여 빌드
절대 경로와 상대 경로, 상대 경로가 개발 중 잘 되는 이유와 빌드 후 깨지는 이유를 확인
- sys._MEIPASS 에 대한 내용 확인
- resource_path() 함수 추가, 추가 후 게임 코드에 resource_path() 가 적용이 될 수 있도록 코드 수정, 수정한 코드를 Thonny에서 F5로 먼저 실행하여 정상 동작하는지 확인
- --add-data 옵션으로 에셋 포함
 에셋 포함 + 이름 지정 pyinstaller --onefile --add-data "image;image" --add-data "sound;sound" --name snakegame snakegame.py 빌드를 하여 .exe 실행
- .exe 실행 후 정상 실행되는지 확인
오류를 확인하기 위해 --windowed를 제거하고 빌드하여 실행했을 때 터미널 창이 함께 뜰 수 있도록 함

## resource_path() 를 써야 하는 이유
resource_path() 함수를 추가하지 않으면 .exe 파일이 실행이 된다고 해도 경로에 문제가 생겨 이미지와 사운드가 없어지기 때문에 resource_path()를 써야 한다.

## 빌드 명령어
pyinstaller --version:터미널에서 실행하여 버전 번호 출력을 통해 제대로 설치가 되었는지 확인
pyinstaller game.py:첫 빌드를 통해 game.exe 실행 파일 생성
  pyinstaller --onefile --windowed --add-data "assets;assets" --name=MyGame game.py
--add-data를 이용하여 .exe 파일을 실행하였을 때 이미지와 사운드 등이 제대로 다 들어있을 수 있도록 함

## AI 활용 내역
이미지 에셋이 많을 때 resource_path() 함수를 어떻게 코드에 적용해야 되는지에 대해서 확인함
pyinstaller 빌드 명령어를 작성할 때 에셋 포함 + 이름 지정에 어떻게 작성해야 되는지, 오류는 없는지 등을 ai를 이용하여 확인함

