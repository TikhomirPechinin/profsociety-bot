import os
import json
import requests
from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SHOW_TEST_BUTTON = os.getenv('SHOW_TEST_BUTTON', 'False').lower() == 'true'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/profsociety'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-for-admin'

db = SQLAlchemy(app)

# ========== МОДЕЛИ БД ==========
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vk_id = db.Column(db.BigInteger, nullable=True)
    full_name = db.Column(db.String(200), nullable=False)
    group_name = db.Column(db.String(100))
    joined_at = db.Column(db.Date, default=datetime.now)
    is_member = db.Column(db.Boolean, default=True)

class ScholarshipSetting(db.Model):
    __tablename__ = 'scholarship_settings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Numeric(10,2), nullable=False)

class SocialScholarship(db.Model):
    __tablename__ = 'social_scholarship'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(200))
    amount = db.Column(db.Numeric(10,2))
    description = db.Column(db.Text)

class AdditionalScholarship(db.Model):
    __tablename__ = 'additional_scholarship'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    amount = db.Column(db.Numeric(10,2))
    is_fixed = db.Column(db.Boolean, default=True)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    description = db.Column(db.Text)

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    vk_id = db.Column(db.BigInteger, primary_key=True)
    current_scenario = db.Column(db.String(100))
    context_data = db.Column(db.Text)
    last_activity = db.Column(db.DateTime, default=datetime.now)

# ========== АДМИН-ПАНЕЛЬ (РУССКАЯ) ==========
class CustomModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class MemberView(CustomModelView):
    column_list = ['full_name', 'group_name', 'joined_at', 'is_member', 'vk_id']
    column_labels = {
        'full_name': 'ФИО',
        'group_name': 'Группа',
        'joined_at': 'Дата вступления',
        'is_member': 'Член профсоюза',
        'vk_id': 'VK ID (необязательно)'
    }
    form_columns = ['full_name', 'group_name', 'joined_at', 'is_member', 'vk_id']

class ScholarshipSettingView(CustomModelView):
    column_list = ['name', 'value']
    column_labels = {
        'name': 'Название',
        'value': 'Сумма (руб)'
    }
    form_columns = ['name', 'value']
    can_create = True
    can_edit = True
    can_delete = True

class SocialScholarshipView(CustomModelView):
    column_list = ['category', 'amount', 'description']
    column_labels = {
        'category': 'Категория',
        'amount': 'Сумма (руб)',
        'description': 'Описание'
    }
    can_create = True
    can_edit = True
    can_delete = True

class AdditionalScholarshipView(CustomModelView):
    column_list = ['name', 'amount', 'is_fixed']
    column_labels = {
        'name': 'Название',
        'amount': 'Сумма (руб)',
        'is_fixed': 'Фиксированная'
    }
    can_create = True
    can_edit = True
    can_delete = True

class EventView(CustomModelView):
    column_list = ['event_date', 'title', 'location', 'description']
    column_labels = {
        'event_date': 'Дата',
        'title': 'Название',
        'location': 'Место',
        'description': 'Описание'
    }
    can_create = True
    can_edit = True
    can_delete = True

# Русские переводы для кнопок
app.jinja_env.globals['gettext'] = lambda x: {
    'List': 'Список',
    'Create': 'Создать',
    'With selected': 'С выбранными',
    'Edit': 'Редактировать',
    'Save': 'Сохранить',
    'Delete': 'Удалить',
    'Search': 'Поиск',
    'Filter': 'Фильтр',
    'Reset Filters': 'Сбросить фильтры',
    'Are you sure you want to delete this item?': 'Вы уверены, что хотите удалить эту запись?',
    'Yes': 'Да',
    'No': 'Нет',
    'Back': 'Назад',
    'Save and Add Another': 'Сохранить и добавить ещё',
    'Save and Continue Editing': 'Сохранить и продолжить',
    'Cancel': 'Отмена'
}.get(x, x)

admin = Admin(app, name='Профсоюз ХГУ', template_mode='bootstrap4')
admin.add_view(MemberView(Member, db.session, name='Члены профсоюза'))
admin.add_view(ScholarshipSettingView(ScholarshipSetting, db.session, name='Настройки стипендий'))
admin.add_view(EventView(Event, db.session, name='Мероприятия'))
# Временные заглушки для будущих разделов
# admin.add_view(SocialScholarshipView(SocialScholarship, db.session, name='Социальные стипендии'))  # закомментировано
# admin.add_view(AdditionalScholarshipView(AdditionalScholarship, db.session, name='Дополнительные стипендии'))  # закомментировано

# ========== VK И YANDEXGPT ==========
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
CONFIRMATION_STRING = os.getenv('CONFIRMATION_STRING')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')

user_sessions = {}

def send_vk_message(user_id, message, keyboard=None):
    url = 'https://api.vk.com/method/messages.send'
    params = {
        'user_id': user_id,
        'message': message,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.199',
        'random_id': 0
    }
    if keyboard:
        params['keyboard'] = json.dumps(keyboard)
    requests.get(url, params=params)

def get_main_keyboard():
    buttons = [
        [{"action": {"type": "text", "label": "📋 Частые вопросы"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "✅ Проверить членство"}, "color": "positive"}],
        [{"action": {"type": "text", "label": "💰 Калькулятор стипендии"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "❓ Помощь"}, "color": "secondary"}]
    ]
    
    # Тестовая кнопка (включается через .env)
    if SHOW_TEST_BUTTON:
        buttons.append([{"action": {"type": "text", "label": "🧪 ТЕСТ"}, "color": "secondary"}])
    
    return {
        "one_time": False,
        "buttons": buttons
    }

def get_back_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]
        ]
    }

def get_education_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "🎓 Высшее образование (ВО)"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🔧 Среднее проф. (СПО)"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]
        ]
    }

def get_budget_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "🏛 Федеральный бюджет"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🏢 Региональный бюджет"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]
        ]
    }

def get_scholarship_keyboard(step):
    keyboards = {
        1: {"buttons": [[{"action": {"type": "text", "label": "1 курс"}, "color": "primary"},
                         {"action": {"type": "text", "label": "2 курс"}, "color": "primary"},
                         {"action": {"type": "text", "label": "3 курс"}, "color": "primary"},
                         {"action": {"type": "text", "label": "4+ курс"}, "color": "primary"}],
                         [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]]},
        2: {"buttons": [[{"action": {"type": "text", "label": "1 семестр"}, "color": "primary"},
                         {"action": {"type": "text", "label": "2 семестр"}, "color": "primary"}],
                         [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]]},
        3: {"buttons": [[{"action": {"type": "text", "label": "Только пятёрки"}, "color": "positive"},
                         {"action": {"type": "text", "label": "Четыре и пять"}, "color": "primary"},
                         {"action": {"type": "text", "label": "Есть тройки или ниже"}, "color": "secondary"}],
                         [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]]},
        4: {"buttons": [[{"action": {"type": "text", "label": "✅ Да, есть"}, "color": "positive"},
                         {"action": {"type": "text", "label": "❌ Нет, нет оснований"}, "color": "secondary"}],
                         [{"action": {"type": "text", "label": "❓ Что за основания?"}, "color": "primary"},
                          {"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]]},
        5: {"buttons": [[{"action": {"type": "text", "label": "✅ Да, победил"}, "color": "positive"},
                         {"action": {"type": "text", "label": "❌ Нет"}, "color": "secondary"}],
                         [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]]},
        6: {"buttons": [[{"action": {"type": "text", "label": "✅ Да, состою"}, "color": "positive"},
                         {"action": {"type": "text", "label": "❌ Нет, не состою"}, "color": "secondary"}],
                         [{"action": {"type": "text", "label": "🔙 Назад"}, "color": "secondary"}]]}
    }
    return keyboards.get(step, get_back_keyboard())

def get_setting_value(name):
    setting = ScholarshipSetting.query.filter_by(name=name).first()
    return float(setting.value) if setting else 0

def calculate_scholarship(data):
    edu_type = data['edu_type']
    course = data['course']
    semester = data['semester']
    grade_type = data.get('grade_type', '')
    has_social = data.get('has_social', False)
    has_pgas = data.get('has_pgas', False)
    is_member = data.get('is_member', False)
    # ВРЕМЕННО: выводим в консоль для отладки
    print(f"[DEBUG] grade_type = '{grade_type}'")
    gas = 0
    gas_enhancement = 0
    
    # ГАС получают все, у кого оценки 4/5 или 5 (кроме троечников)
    if grade_type in ['Только пятёрки', 'Четыре и пять']:
        gas = get_setting_value(f'{edu_type}_gas')
        if grade_type == 'Только пятёрки':
            gas_enhancement = get_setting_value(f'{edu_type}_gas_enhancement')
    
    social = get_setting_value(f'{edu_type}_social') if has_social else 0
    
    enhanced_social = 0
    if edu_type == 'vo' and has_social and course in [1, 2] and grade_type in ['Только пятёрки', 'Четыре и пять']:
        if (course == 1 and semester == 2) or course == 2:
            enhanced_social = get_setting_value('vo_psocial')
    
    pgas = get_setting_value('vo_pgas') if edu_type == 'vo' and has_pgas and course >= 2 else 0
    
    total = gas + gas_enhancement + social + enhanced_social + pgas
    fee = total * 0.03 if is_member else 0
    final = total - fee
    
    return {
        'gas': gas,
        'gas_enhancement': gas_enhancement,
        'social': social,
        'enhanced_social': enhanced_social,
        'pgas': pgas,
        'total_before': total,
        'fee': fee,
        'final': final,
        'is_member': is_member
    }

def format_scholarship_result(result, data):
    edu_type = data['edu_type']
    edu_text = {
        'vo': 'Высшее образование',
        'spo_fed': 'СПО (федеральный бюджет)',
        'spo_reg': 'СПО (региональный бюджет)'
    }.get(edu_type, 'не определено')
    
    # Определяем текст в зависимости от оценок
    if data.get('grade_type') == 'Четыре и пять':
        grade_text = 'хорошист'
    elif data.get('grade_type') == 'Только пятёрки':
        grade_text = 'отличник'
    elif data.get('grade_type') == 'Есть тройки или ниже':
        grade_text = 'троечник'
    else:
        grade_text = 'не определено'
    
    social_text = "есть" if data.get('has_social') else "нет"
    pgas_text = "победитель" if data.get('has_pgas') else "нет"
    
    message = f"""🧮 РАСЧЁТ СТИПЕНДИИ

Тип образования: {edu_text}
Ваши данные: {data['course']} курс, {data['semester']} семестр, {grade_text}
Социальное основание: {social_text}
ПГАС: {pgas_text}

Выбранные стипендии:
"""
    if result['gas'] > 0:
        message += f"• Государственная академическая: {result['gas']:.0f} ₽\n"
    if result['gas_enhancement'] > 0:
        message += f"• Повышение к ГАС (за отличные оценки): {result['gas_enhancement']:.0f} ₽\n"
    if result['social'] > 0:
        message += f"• Социальная стипендия: {result['social']:.0f} ₽\n"
    if result['enhanced_social'] > 0:
        message += f"• Повышенная социальная стипендия: {result['enhanced_social']:.0f} ₽\n"
    if result['pgas'] > 0:
        message += f"• ПГАС: {result['pgas']:.0f} ₽\n"
    
    message += f"""
ℹ️ Статус профсоюза: {'Вы являетесь членом профсоюза' if result['is_member'] else 'Вы НЕ являетесь членом профсоюза'}

📝 Итог до вычета: {result['total_before']:.0f} ₽
➖ Членский взнос (3%): -{result['fee']:.0f} ₽
✅ Примерная сумма к получению: ~ {result['final']:.0f} ₽

Примечания: 
1) Сбор 3% взимается со всех стипендиальных выплат
2) Итоговая сумма утверждается стипендиальной комиссией"""
    return message

def ask_yandexgpt(question):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {YANDEX_API_KEY}"}
    body = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": "500"},
        "messages": [
            {"role": "system", "text": "Ты — консультант профсоюза студентов ХГУ. Отвечай кратко и по делу."},
            {"role": "user", "text": question}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        if response.status_code == 200:
            return response.json()['result']['alternatives'][0]['message']['text']
        return f"Ошибка: {response.status_code}"
    except Exception as e:
        return f"Ошибка подключения: {str(e)}"

@app.route('/')
def index():
    return "VK Consultant Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('type') == 'confirmation':
        return CONFIRMATION_STRING
    
    if data.get('type') == 'message_new':
        message_obj = data['object']['message']
        user_id = message_obj['from_id']
        user_text = message_obj.get('text', '').strip()
        
        if user_text == '🏠 В главное меню' or user_text == '🔙 Назад':
            if user_id in user_sessions:
                del user_sessions[user_id]
            send_vk_message(user_id, "🏠 Главное меню", get_main_keyboard())
            return 'ok'
        
        if user_text == '🧪 ТЕСТ':
            send_vk_message(user_id, "✅ Тестовая кнопка работает!", get_main_keyboard())
            return 'ok'

        if user_text == '❓ Помощь':
            help_text = """🤖 *Я бот-ассистент профсоюза ХГУ!*

Вот что я умею:
• 📋 Частые вопросы – справочник
• ✅ Проверить членство – статус в профсоюзе
• 💰 Калькулятор стипендии – предварительный расчет

Просто нажми на нужную кнопку."""
            send_vk_message(user_id, help_text, get_main_keyboard())
            return 'ok'
        
        if user_text == '📋 Частые вопросы':
            faq_text = """📚 *Частые вопросы*

Скоро здесь появятся категории:
• 🎁 Бонусы профсоюза
• 📚 Сессия и учеба
• 💸 Материальная помощь

Пока что задай свой вопрос текстом!"""
            send_vk_message(user_id, faq_text, get_back_keyboard())
            return 'ok'
        
        if user_text == '✅ Проверить членство':
            user_sessions[user_id] = {'scenario': 'check_membership', 'step': 'waiting_fio'}
            send_vk_message(user_id, "🔍 Для проверки членства введи, пожалуйста, своё полное ФИО", get_back_keyboard())
            return 'ok'
        
        if user_text == '💰 Калькулятор стипендии':
            user_sessions[user_id] = {'scenario': 'scholarship', 'step': 0, 'data': {}}
            send_vk_message(user_id, "🎓 *Калькулятор стипендии*\n\nПо программам какого образования вы обучаетесь?", get_education_keyboard())
            return 'ok'
        
        if user_id in user_sessions:
            session_data = user_sessions[user_id]
            
            if session_data['scenario'] == 'check_membership':
                if session_data['step'] == 'waiting_fio':
                    send_vk_message(user_id, f"✅ Спасибо! Информация о членстве будет добавлена позже.", get_main_keyboard())
                    del user_sessions[user_id]
            
            elif session_data['scenario'] == 'scholarship':
                step = session_data['step']
                data = session_data['data']
                
                if step == 0:
                    if 'Высшее образование' in user_text:
                        data['edu_type'] = 'vo'
                        session_data['step'] = 2
                        send_vk_message(user_id, "На каком ты курсе?", get_scholarship_keyboard(1))
                    elif 'Среднее проф.' in user_text:
                        data['edu_type'] = 'spo'
                        session_data['step'] = 1
                        send_vk_message(user_id, "Бюджет какой подчиненности?", get_budget_keyboard())
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери тип образования из кнопок.", get_education_keyboard())
                        return 'ok'
                
                elif step == 1:
                    if 'Федеральный' in user_text:
                        data['edu_type'] = 'spo_fed'
                    elif 'Региональный' in user_text:
                        data['edu_type'] = 'spo_reg'
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери бюджет из кнопок.", get_budget_keyboard())
                        return 'ok'
                    session_data['step'] = 2
                    send_vk_message(user_id, "На каком ты курсе?", get_scholarship_keyboard(1))
                
                elif step == 2:
                    if '1 курс' in user_text:
                        data['course'] = 1
                    elif '2 курс' in user_text:
                        data['course'] = 2
                    elif '3 курс' in user_text:
                        data['course'] = 3
                    elif '4' in user_text:
                        data['course'] = 4
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери курс из кнопок.", get_scholarship_keyboard(1))
                        return 'ok'
                    session_data['step'] = 3
                    send_vk_message(user_id, "Какой у тебя семестр?", get_scholarship_keyboard(2))
                
                elif step == 3:
                    if '1 семестр' in user_text:
                        data['semester'] = 1
                    elif '2 семестр' in user_text:
                        data['semester'] = 2
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери семестр из кнопок.", get_scholarship_keyboard(2))
                        return 'ok'
                    
                    if data['course'] == 1 and data['semester'] == 1:
                        session_data['step'] = 5
                        send_vk_message(user_id, "Есть ли у тебя основание для социальной стипендии?", get_scholarship_keyboard(4))
                    else:
                        session_data['step'] = 4
                        send_vk_message(user_id, "Какие у тебя оценки за прошлую сессию?", get_scholarship_keyboard(3))
                
                elif step == 4:
                    if 'Четыре и пять' in user_text:
                        data['grade_type'] = 'Четыре и пять'
                    elif 'пятёрки' in user_text:
                        data['grade_type'] = 'Только пятёрки'
                    elif 'тройки' in user_text:
                        data['grade_type'] = 'Есть тройки или ниже'
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери вариант с оценками.", get_scholarship_keyboard(3))
                        return 'ok'
                    session_data['step'] = 5
                    send_vk_message(user_id, "Есть ли у тебя основание для социальной стипендии?", get_scholarship_keyboard(4))
                             
                elif step == 5:
                    if 'Да, есть' in user_text:
                        data['has_social'] = True
                    elif 'Нет, нет оснований' in user_text:
                        data['has_social'] = False
                    elif 'Что за основания' in user_text:
                        social_list = SocialScholarship.query.all()
                        msg = "📋 Основания для социальной стипендии:\n\n"
                        for s in social_list:
                            msg += f"• {s.category}: {s.amount} ₽\n  {s.description}\n\n"
                        send_vk_message(user_id, msg, get_scholarship_keyboard(4))
                        return 'ok'
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери ответ из кнопок.", get_scholarship_keyboard(4))
                        return 'ok'
                    session_data['step'] = 6
                    
                    if data['edu_type'] == 'vo' and data['course'] >= 2:
                        send_vk_message(user_id, "Участвуешь ли ты в конкурсе на ПГАС?", get_scholarship_keyboard(5))
                    else:
                        session_data['step'] = 7
                        send_vk_message(user_id, "Ты состоишь в профсоюзе?", get_scholarship_keyboard(6))
                
                elif step == 6:
                    if 'Да, победил' in user_text:
                        data['has_pgas'] = True
                    elif 'Нет' in user_text:
                        data['has_pgas'] = False
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери ответ из кнопок.", get_scholarship_keyboard(5))
                        return 'ok'
                    session_data['step'] = 7
                    send_vk_message(user_id, "Ты состоишь в профсоюзе?", get_scholarship_keyboard(6))
                
                elif step == 7:
                    if 'Да, состою' in user_text:
                        data['is_member'] = True
                    elif 'Нет, не состою' in user_text:
                        data['is_member'] = False
                    else:
                        send_vk_message(user_id, "Пожалуйста, выбери ответ из кнопок.", get_scholarship_keyboard(6))
                        return 'ok'
                    
                    result = calculate_scholarship(data)
                    output = format_scholarship_result(result, data)
                    send_vk_message(user_id, output, get_main_keyboard())
                    del user_sessions[user_id]
        
        else:
            answer = ask_yandexgpt(user_text)
            send_vk_message(user_id, answer, get_main_keyboard())
    
    return 'ok'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False)
