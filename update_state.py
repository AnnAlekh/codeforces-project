import requests
import re
from datetime import datetime

def get_codeforces_stats(handle):
    """Получает статистику из Codeforces API"""
    try:
        # Получаем информацию о пользователе
        user_url = f"https://codeforces.com/api/user.info?handles={handle}"
        user_response = requests.get(user_url, timeout=10)
        user_data = user_response.json()
        
        # Получаем список решенных задач
        submissions_url = f"https://codeforces.com/api/user.status?handle={handle}"
        submissions_response = requests.get(submissions_url, timeout=10)
        submissions_data = submissions_response.json()
        
        if user_data['status'] == 'OK' and submissions_data['status'] == 'OK':
            user_info = user_data['result'][0]
            
            # Подсчитываем уникальные решенные задачи
            solved_problems = set()
            for submission in submissions_data['result']:
                if submission['verdict'] == 'OK':  # Решенная задача
                    problem = submission['problem']
                    problem_id = f"{problem['contestId']}{problem['index']}"
                    solved_problems.add(problem_id)
            
            rating = user_info.get('rating', 'Новичок')
            max_rating = user_info.get('maxRating', 'Новичок')
            solved_count = len(solved_problems)
            
            return rating, max_rating, solved_count
        else:
            return "Новичок", "Новичок", 0
            
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return "Новичок", "Новичок", 0

def update_readme():
    """Обновляет README.md с актуальной статистикой"""
    handle = "dumooroo"
    rating, max_rating, solved_count = get_codeforces_stats(handle)
    
    # Читаем текущий README
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print("Файл README.md не найден!")
        return
    
    # Создаем новые бейджи
    new_badges = f'''[![Codeforces](https://img.shields.io/badge/Codeforces-dumooroo-blue?style=for-the-badge&logo=codeforces)](https://codeforces.com/profile/dumooroo)
[![Рейтинг](https://img.shields.io/badge/Рейтинг-{rating}-green?style=for-the-badge)](https://codeforces.com/profile/dumooroo)
[![Решено задач](https://img.shields.io/badge/Решено_задач-{solved_count}+-brightgreen?style=for-the-badge)](https://codeforces.com/submissions/dumooroo)'''
    
    # Обновляем секцию с бейджами
    badge_pattern = r'\[\!\[Codeforces\].*?\n\[\!\[Рейтинг\].*?\n\[\!\[Решено задач\].*?\]'
    content = re.sub(badge_pattern, new_badges, content, flags=re.DOTALL)
    
    # Обновляем дату последнего обновления
    update_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    content = re.sub(r'Последнее обновление:.*', f'Последнее обновление: {update_time}', content)
    
    # Записываем обновленный контент
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Статистика обновлена! Решено задач: {solved_count}, Рейтинг: {rating}")

if __name__ == "__main__":
    update_readme()