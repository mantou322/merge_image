@echo off
echo 正在安装依赖...
pip install -r requirements.txt
echo 开始打包程序...
pyinstaller --onefile --name MergeImage merge_image.py
echo 打包完成!
echo 可执行文件位置: dist/MergeImage.exe
pause
