import os
import sys
import re
from PIL import Image

def resource_path(relative_path):
    """获取资源的绝对路径，用于PyInstaller打包后的资源访问"""
    try:
        # PyInstaller创建临时文件夹并将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_working_directory():
    """获取用户当前的工作目录"""
    return os.getcwd()

def natural_sort_key(s):
    """按照人类自然排序方式处理字符串，例如 'img2.jpg' 排在 'img10.jpg' 前面"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def merge_images():
    try:
        # 获取图片源路径
        source_dir = input("请输入图片所在文件夹路径(直接回车将使用当前工作目录): ").strip()
        
        # 如果为空，则使用当前工作目录
        if not source_dir:
            # 使用当前工作目录而不是程序所在目录
            source_dir = get_working_directory()
            print(f"使用当前工作目录: {source_dir}")
        
        # 验证源路径是否有效
        if not os.path.isdir(source_dir):
            print(f"错误: 路径 '{source_dir}' 不是有效的文件夹")
            return
            
        print(f"正在使用路径: {source_dir}")
        
        # 获取输出路径
        output_dir = input("请输入保存结果的文件夹路径(直接回车将使用与源相同的文件夹): ").strip()
        if not output_dir:
            output_dir = source_dir
        elif not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"已创建输出文件夹: {output_dir}")
            except Exception as e:
                print(f"无法创建输出文件夹: {str(e)}")
                output_dir = source_dir
                print(f"将使用源文件夹作为输出: {output_dir}")
                
        # 支持的图片格式
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        
        # 获取所有图片文件
        image_files = []
        for file in os.listdir(source_dir):
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(file_path)
        
        # 如果没有图片文件，退出
        if not image_files:
            print(f"在 '{source_dir}' 中没有找到图片文件。")
            return
        
        # 选择排序方式
        print("\n请选择图片排序方式:")
        print("1. 按文件名字母顺序 (a.jpg, b.jpg, ...)")
        print("2. 按文件名自然顺序 (1.jpg, 2.jpg, 10.jpg, ...)")
        print("3. 按文件修改时间 (最早修改的优先)")
        print("4. 按文件修改时间 (最近修改的优先)")
        print("5. 按文件大小 (从小到大)")
        print("6. 按文件大小 (从大到小)")
        
        sort_choice = input("请输入选择 (1-6，默认为1): ").strip()
        
        # 根据选择排序
        if sort_choice == "2":
            # 自然排序 (img1, img2, img10 而不是 img1, img10, img2)
            image_files.sort(key=lambda x: natural_sort_key(os.path.basename(x)))
            print("按文件名自然顺序排序")
        elif sort_choice == "3":
            # 按修改时间排序 (最早的优先)
            image_files.sort(key=lambda x: os.path.getmtime(x))
            print("按修改时间排序（最早优先）")
        elif sort_choice == "4":
            # 按修改时间排序 (最近的优先)
            image_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            print("按修改时间排序（最近优先）")
        elif sort_choice == "5":
            # 按文件大小排序 (从小到大)
            image_files.sort(key=lambda x: os.path.getsize(x))
            print("按文件大小排序（从小到大）")
        elif sort_choice == "6":
            # 按文件大小排序 (从大到小)
            image_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
            print("按文件大小排序（从大到小）")
        else:
            # 默认按字母顺序
            image_files.sort()
            print("按文件名字母顺序排序")

        # 显示排序后的文件列表
        print("\n排序后的文件列表:")
        for i, file_path in enumerate(image_files, 1):
            file_info = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"{i}. {file_info} ({file_size:.1f} KB)")
        
        # 询问是否调整顺序
        adjust_order = input("\n是否需要手动调整顺序? (y/n，默认为n): ").strip().lower()
        if adjust_order == "y":
            print("\n请输入调整后的文件顺序，例如 '3,1,2,4' 表示将第3个文件放在第1位，依此类推")
            try:
                new_order_input = input("新顺序 (使用逗号分隔，留空则保持原顺序): ").strip()
                if new_order_input:
                    # 转换用户输入为索引列表
                    new_order = [int(x) - 1 for x in new_order_input.split(',')]
                    # 验证输入
                    if max(new_order) >= len(image_files) or min(new_order) < 0:
                        print("输入的序号超出范围，将保持原顺序")
                    else:
                        # 应用新顺序
                        image_files = [image_files[i] for i in new_order]
                        print("已应用新的文件顺序")
                        # 再显示一次调整后的顺序
                        print("\n调整后的文件列表:")
                        for i, file_path in enumerate(image_files, 1):
                            print(f"{i}. {os.path.basename(file_path)}")
            except Exception as e:
                print(f"调整顺序时出错: {str(e)}，将保持原顺序")
        
        print(f"\n准备合并 {len(image_files)} 个图片文件...")
        
        # 打开所有图片
        images = []
        for img_path in image_files:
            try:
                images.append(Image.open(img_path))
                print(f"已加载: {os.path.basename(img_path)}")
            except Exception as e:
                print(f"无法加载图片 {img_path}: {str(e)}")
        
        if not images:
            print("没有可合并的有效图片。")
            return
            
        # 确定合并方向（默认垂直合并）
        merge_direction = input("请选择合并方向(h-水平合并/v-垂直合并，默认为垂直合并): ").lower()
        
        if merge_direction == 'h':
            # 水平合并：宽度之和，高度取最大值
            total_width = sum(img.width for img in images)
            max_height = max(img.height for img in images)
            
            # 创建新图片
            merged_image = Image.new('RGB', (total_width, max_height))
            
            # 粘贴图片
            current_width = 0
            for img in images:
                merged_image.paste(img, (current_width, 0))
                current_width += img.width
        else:
            # 垂直合并：高度之和，宽度取最大值
            max_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)
            
            # 创建新图片
            merged_image = Image.new('RGB', (max_width, total_height))
            
            # 粘贴图片
            current_height = 0
            for img in images:
                merged_image.paste(img, (0, current_height))
                current_height += img.height
        
        # 让用户指定输出文件名
        output_name = input("请输入输出文件名(无需扩展名，直接回车将使用默认名称): ").strip()
        if not output_name:
            # 默认文件名带时间戳
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_name = f"merged_image_{timestamp}"
        
        # 添加扩展名
        output_format = input("请选择输出格式(jpg/png/bmp，默认为jpg): ").lower().strip()
        if output_format not in ["jpg", "png", "bmp"]:
            output_format = "jpg"
            
        output_filename = f"{output_name}.{output_format}"
        output_path = os.path.join(output_dir, output_filename)
        
        # 检查是否存在同名文件，如果存在则先删除
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
                print(f"已删除同名文件: {output_path}")
            except Exception as e:
                print(f"警告: 无法删除同名文件 {output_path}: {str(e)}")
                # 修改文件名避免冲突
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                output_filename = f"{output_name}_{timestamp}.{output_format}"
                output_path = os.path.join(output_dir, output_filename)
                print(f"将使用新文件名: {output_filename}")
        
        # 保存文件
        merged_image.save(output_path)
        print(f"图片已合并，保存为: {output_path}")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        input("按Enter键退出...")

if __name__ == "__main__":
    print("图片合并工具")
    print("-------------")
    merge_images()
    print("处理完成!")
    input("按Enter键退出...")
