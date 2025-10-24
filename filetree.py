import os
import datetime

def get_file_emoji(file_name):
    """
    Возвращает эмодзи в зависимости от расширения файла.
    """
    file_types = {
        'dir': '📂',  # Папки
        # Текстовые файлы и документы
        '.txt': '📄', '.doc': '📄', '.docx': '📄', '.pdf': '📄', '.rtf': '📄',
        '.md': '📄', '.log': '📄', '.odt': '📄', '.tex': '📄',
        # Код и скрипты
        '.py': '🐍', '.java': '☕', '.cpp': '💻', '.c': '💻', '.js': '🌐',
        '.html': '🌐', '.css': '🎨', '.php': '🌐', '.rb': '💎',
        '.sh': '🐚', '.go': '🐹', '.ts': '🌐', '.sql': '🗄️',
        # Музыка
        '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.aac': '🎵',
        '.ogg': '🎵', '.m4a': '🎵',
        # Изображения
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
        '.bmp': '🖼️', '.tiff': '🖼️', '.svg': '🖼️', '.webp': '🖼️',
        # Видео
        '.mp4': '🎥', '.mkv': '🎥', '.avi': '🎥', '.mov': '🎥',
        '.wmv': '🎥', '.flv': '🎥', '.webm': '🎥',
        # Архивы
        '.zip': '🗃️', '.rar': '🗃️', '.7z': '🗃️', '.tar': '🗃️',
        '.gz': '🗃️', '.bz2': '🗃️',
        # Исполняемые файлы
        '.exe': '⚙️', '.bin': '⚙️', '.app': '⚙️', '.bat': '⚙️',
        # Электронные таблицы и презентации
        '.xls': '📊', '.xlsx': '📊', '.csv': '📊', '.ods': '📊',
        '.ppt': '📈', '.pptx': '📈',
        # Другие
        '.iso': '💿', '.torrent': '🌊', '.db': '🗄️', '.json': '📋',
        '.xml': '📋', '.yaml': '📋', '.yml': '📋'
    }
    
    if os.path.isdir(file_name):
        return file_types['dir']
    
    extension = os.path.splitext(file_name)[1].lower()
    return file_types.get(extension, '📜')  # 📜 для неизвестных типов

def print_file_tree(path, prefix="", file_output=None, print_to_console=True, sort_key='name'):
    """
    Рекурсивно строит дерево файлов и папок, подсчитывает файлы, сортирует по заданному критерию.
    
    Args:
        path (str): Путь к директории
        prefix (str): Префикс для отступов
        file_output (file): Файл для записи результата
        print_to_console (bool): Выводить ли в консоль
        sort_key (str): Критерий сортировки ('name', 'ctime', 'size')
    
    Returns:
        int: Количество файлов в текущей директории и её поддиректориях
    """
    total_files = 0
    try:
        items = os.listdir(path)
        # Собираем информацию о файлах и папках
        item_info = []
        for item in items:
            item_path = os.path.join(path, item)
            try:
                stats = os.stat(item_path)
                item_info.append({
                    'name': item,
                    'path': item_path,
                    'ctime': stats.st_ctime,
                    'size': stats.st_size if os.path.isfile(item_path) else 0,
                    'is_dir': os.path.isdir(item_path)
                })
            except (PermissionError, FileNotFoundError):
                continue

        # Сортировка
        if sort_key == 'ctime':
            items = [x['name'] for x in sorted(item_info, key=lambda x: x['ctime'], reverse=True)]
        elif sort_key == 'size':
            items = [x['name'] for x in sorted(item_info, key=lambda x: (x['is_dir'], x['size']), reverse=True)]
        else:  # по умолчанию по имени
            items = [x['name'] for x in sorted(item_info, key=lambda x: x['name'].lower())]

    except (PermissionError, FileNotFoundError) as e:
        error_msg = f"{prefix}├── [Ошибка: {e}]"
        if print_to_console:
            print(f"\033[1;31m{error_msg}\033[0m")
        if file_output:
            file_output.write(error_msg + "\n")
        return 0

    dir_file_count = 0  # Счётчик файлов в текущей директории
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        emoji = get_file_emoji(item_path)
        
        # Подсчёт файлов в текущей директории
        if os.path.isfile(item_path):
            dir_file_count += 1
            total_files += 1
        
        # Формируем строку для вывода и записи
        line = f"{prefix}{connector}{emoji} {item}"
        if os.path.isdir(item_path):
            subdir_files = print_file_tree(item_path, prefix + ("    " if is_last else "│   "), file_output, print_to_console, sort_key)
            total_files += subdir_files
            line += f" ({subdir_files} файлов)"

        if print_to_console:
            print(f"\033[1;37m{line}\033[0m")
        if file_output:
            file_output.write(line + "\n")

    return total_files

def main():
    # Запрашиваем путь к директории
    print("\033[1;34m=== Построение дерева файлов ===\033[0m")
    path = input("\033[1;32mВведите путь к директории (или нажмите Enter для текущей): \033[0m").strip()
    
    # Если путь не указан, используем текущую директорию
    if not path:
        path = os.getcwd()
    
    # Проверяем, существует ли путь
    if not os.path.exists(path):
        print(f"\033[1;31mОшибка: Путь '{path}' не существует!\033[0m")
        return
    
    # Проверяем, является ли путь директорией
    if not os.path.isdir(path):
        print(f"\033[1;31mОшибка: '{path}' не является директорией!\033[0m")
        return
    
    # Запрашиваем, нужно ли выводить в консоль
    print("\033[1;32mВыводить дерево в консоль?\033[0m")
    print("1 - Да")
    print("2 - Нет")
    console_choice = input("\033[1;32mВыберите (1 или 2, по умолчанию 1): \033[0m").strip()
    print_to_console = console_choice != '2'

    # Запрашиваем критерий сортировки
    print("\033[1;32mКак сортировать файлы и папки?\033[0m")
    print("1 - По имени (алфавитный порядок)")
    print("2 - По времени создания (от новых к старым)")
    print("3 - По размеру (от большего к меньшему)")
    sort_choice = input("\033[1;32mВыберите (1, 2 или 3, по умолчанию 1): \033[0m").strip()
    sort_key = 'name'
    if sort_choice == '2':
        sort_key = 'ctime'
    elif sort_choice == '3':
        sort_key = 'size'

    # Запрашиваем, куда сохранить файл
    print("\033[1;32mКуда сохранить файл?\033[0m")
    print(f"1 - В целевую директорию ({path})")
    print("2 - В другую директорию")
    save_choice = input("\033[1;32mВыберите (1 или 2, по умолчанию 1): \033[0m").strip()
    
    if save_choice == '2':
        save_path = input("\033[1;32mВведите путь для сохранения файла: \033[0m").strip()
        if not save_path:
            print(f"\033[1;31mОшибка: Путь не указан, будет использована целевая директория ({path}).\033[0m")
            save_path = path
        elif not os.path.exists(save_path) or not os.path.isdir(save_path):
            print(f"\033[1;31mОшибка: Путь '{save_path}' не существует или не является директорией!\033[0m")
            return
    else:
        save_path = path

    # Генерируем имя файла
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(save_path, f"file_tree_{timestamp}.txt")
    
    # Выводим заголовок и начинаем построение дерева
    if print_to_console:
        print(f"\n\033[1;36mДерево файлов для: {path}\033[0m")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Дерево файлов для: {path}\n")
            total_files = print_file_tree(path, file_output=f, print_to_console=print_to_console, sort_key=sort_key)
            summary = f"\nОбщее количество файлов: {total_files}"
            if print_to_console:
                print(f"\033[1;36m{summary}\033[0m")
            f.write(summary + "\n")
    except (PermissionError, OSError) as e:
        print(f"\033[1;31mОшибка при записи файла: {e}\033[0m")
        return
    
    print(f"\033[1;32mДерево сохранено в файл: {output_file}\033[0m")
    print("\033[1;34m=== Завершено ===\033[0m")

if __name__ == "__main__":
    main()
