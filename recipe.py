import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import webbrowser

# Конфигурация
RECIPES_FILE = "recipes_generator.json"
CATEGORIES = ["Завтрак", "Обед", "Ужин", "Десерт", "Выпечка", "Салаты"]
COLORS = {
    "background": "#FFF5F5",   # Очень светлый розовый
    "primary": "#F03E3E",      # Томатно-красный
    "secondary": "#FF8787",    # Светло-красный
    "accent": "#C92A2A",       # Вишневый
    "text": "#2B2D42",         # Темно-синий (текст)
    "light": "#FFECEC",        # Светло-розовый
    "highlight": "#37B24D"     # Свежий зеленый
}

# Шрифты
FONTS = {
    "title": ("Impact", 24, "bold"),
    "category": ("Arial Rounded MT Bold", 12),
    "button": ("Arial Rounded MT Bold", 11),
    "recipe": ("Georgia", 12),
    "ingredients": ("Verdana", 11)
}

class RecipeManager:
    def __init__(self):
        self.recipes = {category: [] for category in CATEGORIES}
        self.load_recipes()
        
    def load_recipes(self):
        """Загружает рецепты из файла или создает стандартные"""
        default_recipes = {
            "Завтрак": [
                {"name": "Омлет с сыром и ветчиной", "ingredients": "Яйца (4 шт), молоко (50 мл), сыр (100 г), ветчина (100 г), соль, перец", "time": "15 мин", "method": "Взбейте яйца с молоком, посолите. Обжарьте на сковороде, добавьте нарезанную ветчину и сыр. Накройте крышкой на 2 минуты."},
                {"name": "Французские тосты", "ingredients": "Хлеб (6 ломтиков), яйца (3 шт), молоко (150 мл), корица (1 ч.л.), сахар (2 ст.л.), масло сливочное", "time": "20 мин", "method": "Смешайте яйца, молоко, корицу и сахар. Обмакните хлеб и обжарьте на масле до золотистой корочки."},
                {"name": "Гранола с йогуртом", "ingredients": "Овсяные хлопья (200 г), мед (50 мл), орехи (100 г), сухофрукты (100 г), йогурт натуральный (300 г)", "time": "25 мин", "method": "Смешайте хлопья с медом и орехами, запеките 15 минут при 180°C. Добавьте сухофрукты. Подавайте с йогуртом."},
                {"name": "Авокадо-тост с яйцом", "ingredients": "Хлеб (2 ломтика), авокадо (1 шт), яйца (2 шт), лимонный сок, соль, перец, кунжут", "time": "10 мин", "method": "Разомните авокадо с лимонным соком. Обжарьте яйца. Намажьте тосты авокадо, сверху яйца, посыпьте кунжутом."},
                {"name": "Смузи из манго", "ingredients": "Манго (2 шт), банан (1 шт), йогурт (200 мл), мед (1 ст.л.), лед (100 г)", "time": "5 мин", "method": "Все ингредиенты взбейте в блендере до однородности."},
                {"name": "Сырники с изюмом", "ingredients": "Творог (500 г), яйца (2 шт), мука (100 г), сахар (50 г), изюм (50 г), ваниль", "time": "30 мин", "method": "Смешайте все ингредиенты. Сформируйте сырники, обжарьте на среднем огне по 3-4 минуты с каждой стороны."}
            ],
            "Обед": [
                {"name": "Борщ украинский", "ingredients": "Свекла (2 шт), капуста (300 г), говядина (400 г), картофель (3 шт), морковь (1 шт), лук (1 шт), томатная паста (2 ст.л.), сметана", "time": "120 мин", "method": "Сварите бульон из мяса. Обжарьте овощи, добавьте в бульон. Варите до готовности. Подавайте со сметаной."},
                {"name": "Плов узбекский", "ingredients": "Рис (500 г), баранина (600 г), морковь (3 шт), лук (2 шт), чеснок (1 головка), зира, барбарис, масло растительное", "time": "150 мин", "method": "Обжарьте мясо с овощами. Добавьте рис и воду. Тушите на медленном огне 40 минут."},
                {"name": "Лазанья классическая", "ingredients": "Листы лазаньи (250 г), фарш (500 г), соус бешамель (300 мл), сыр (200 г), томатный соус (200 мл)", "time": "60 мин", "method": "Обжарьте фарш. Слоями выложите листы лазаньи, фарш, соусы и сыр. Запекайте 30 минут при 180°C."},
                {"name": "Греческий салат", "ingredients": "Помидоры (3 шт), огурцы (2 шт), перец (1 шт), красный лук (1/2 шт), маслины (100 г), сыр фета (150 г), оливковое масло, орегано", "time": "15 мин", "method": "Нарежьте овощи кубиками. Добавьте маслины и фету. Заправьте маслом с орегано."},
                {"name": "Тыквенный суп-пюре", "ingredients": "Тыква (600 г), морковь (1 шт), лук (1 шт), имбирь (1 см), сливки (200 мл), бульон (1 л)", "time": "40 мин", "method": "Обжарьте овощи, добавьте тыкву и бульон. Варите до мягкости. Пюрируйте, добавьте сливки."},
                {"name": "Куриные котлеты с пюре", "ingredients": "Куриный фарш (500 г), лук (1 шт), яйцо (1 шт), хлеб (100 г), молоко (50 мл), картофель (6 шт), масло сливочное", "time": "45 мин", "method": "Приготовьте фарш для котлет. Сформируйте котлеты, обжарьте. Картофель отварите, сделайте пюре с маслом."}
            ],
            "Ужин": [
                {"name": "Лосось под сырной корочкой", "ingredients": "Лосось (2 стейка), сыр (100 г), майонез (2 ст.л.), лимон (1/2 шт), укроп, соль, перец", "time": "25 мин", "method": "Смешайте сыр с майонезом. Посолите рыбу, полейте лимоном. Намажьте сырной смесью. Запекайте 15 минут при 200°C."},
                {"name": "Картофель по-деревенски", "ingredients": "Картофель (8 шт), паприка (1 ст.л.), чеснок (3 зубчика), масло растительное, соль", "time": "40 мин", "method": "Нарежьте картофель дольками. Смешайте с маслом и специями. Запекайте 30 минут при 200°C."},
                {"name": "Фаршированные перцы", "ingredients": "Перцы (6 шт), фарш (500 г), рис (100 г), лук (1 шт), морковь (1 шт), томатный соус (200 мл)", "time": "60 мин", "method": "Приготовьте начинку из фарша, риса и овощей. Нафаршируйте перцы, залейте соусом. Тушите 40 минут."},
                {"name": "Грибная паста", "ingredients": "Паста (300 г), шампиньоны (300 г), сливки (200 мл), чеснок (2 зубчика), пармезан (50 г)", "time": "30 мин", "method": "Обжарьте грибы с чесноком. Добавьте сливки и сыр. Смешайте с отваренной пастой."},
                {"name": "Овощное рагу", "ingredients": "Кабачок (1 шт), баклажан (1 шт), перец (2 шт), помидоры (3 шт), лук (1 шт), чеснок (2 зубчика), зелень", "time": "35 мин", "method": "Обжарьте лук, добавьте овощи. Тушите под крышкой 20 минут. Добавьте чеснок и зелень."},
                {"name": "Куриные крылышки BBQ", "ingredients": "Куриные крылья (1 кг), соус BBQ (200 мл), мед (2 ст.л.), соевый соус (50 мл), чеснок (3 зубчика)", "time": "50 мин", "method": "Замаринуйте крылья в смеси ингредиентов. Запекайте 40 минут при 190°C, периодически поливая соусом."}
            ],
            "Десерт": [
                {"name": "Шоколадный фондан", "ingredients": "Шоколад (200 г), масло (150 г), яйца (4 шт), сахар (150 г), мука (60 г)", "time": "25 мин", "method": "Растопите шоколад с маслом. Взбейте яйца с сахаром. Смешайте все, разлейте по формочкам. Выпекайте 10-12 минут при 200°C."},
                {"name": "Чизкейк Нью-Йорк", "ingredients": "Печенье (250 г), масло (100 г), творожный сыр (600 г), сахар (200 г), яйца (3 шт), ваниль", "time": "90 мин", "method": "Измельчите печенье с маслом - это основа. Взбейте сыр с сахаром и яйцами. Выпекайте 60 минут при 160°C."},
                {"name": "Яблочный пирог", "ingredients": "Мука (300 г), яйца (2 шт), сахар (150 г), масло (100 г), яблоки (4 шт), корица", "time": "60 мин", "method": "Замесите тесто. Нарежьте яблоки. Выложите в форму слоями. Выпекайте 40 минут при 180°C."},
                {"name": "Тирамису", "ingredients": "Печенье савоярди (200 г), кофе (200 мл), маскарпоне (500 г), яйца (4 шт), сахар (100 г), какао", "time": "40 мин", "method": "Взбейте желтки с сахаром, добавьте маскарпоне и белки. Слои печенья, пропитанного кофе, и крема. Посыпьте какао."},
                {"name": "Медовик", "ingredients": "Мед (100 г), сахар (200 г), яйца (3 шт), мука (500 г), сметана (800 г)", "time": "120 мин", "method": "Приготовьте медовые коржи. Смажьте сметанным кремом. Дайте пропитаться 6 часов."},
                {"name": "Клубничный мусс", "ingredients": "Клубника (500 г), сливки (300 мл), сахар (100 г), желатин (20 г)", "time": "30 мин", "method": "Пюрируйте клубнику. Взбейте сливки с сахаром. Добавьте желатин. Смешайте и охладите 4 часа."}
            ],
            "Выпечка": [
                {"name": "Банановый хлеб", "ingredients": "Бананы (3 шт), мука (300 г), сахар (150 г), яйца (2 шт), масло (100 г), сода (1 ч.л.), грецкие орехи (100 г)", "time": "60 мин", "method": "Разомните бананы. Смешайте все ингредиенты. Выпекайте 50 минут при 180°C."},
                {"name": "Пирожки с капустой", "ingredients": "Мука (500 г), дрожжи (10 г), молоко (250 мл), капуста (1 кг), яйца (2 шт), лук (1 шт)", "time": "90 мин", "method": "Приготовьте тесто. Обжарьте капусту с луком. Сформируйте пирожки. Выпекайте 25 минут при 190°C."},
                {"name": "Печенье овсяное", "ingredients": "Овсяные хлопья (200 г), мука (100 г), масло (150 г), сахар (100 г), мед (50 г), корица", "time": "30 мин", "method": "Смешайте все ингредиенты. Сформируйте печенье. Выпекайте 15 минут при 180°C."},
                {"name": "Булочки с корицей", "ingredients": "Мука (500 г), молоко (250 мл), дрожжи (10 г), сахар (100 г), корица (2 ст.л.), масло (100 г)", "time": "120 мин", "method": "Замесите тесто. Раскатайте, посыпьте корицей с сахаром. Сверните рулетом, нарежьте. Выпекайте 25 минут при 190°C."},
                {"name": "Шарлотка", "ingredients": "Яблоки (5 шт), яйца (4 шт), сахар (200 г), мука (200 г), корица", "time": "50 мин", "method": "Взбейте яйца с сахаром. Добавьте муку. Выложите яблоки в форму, залейте тестом. Выпекайте 35 минут при 180°C."},
                {"name": "Круассаны", "ingredients": "Готовое слоеное тесто (500 г), шоколад (200 г), яйцо (1 шт)", "time": "30 мин", "method": "Раскатайте тесто, нарежьте треугольниками. Положите шоколад, сверните. Смажьте яйцом. Выпекайте 20 минут при 200°C."}
            ],
            "Салаты": [
                {"name": "Цезарь с курицей", "ingredients": "Куриное филе (300 г), салат романо (1 кочан), сухарики (100 г), пармезан (50 г), соус Цезарь (100 мл)", "time": "25 мин", "method": "Обжарьте курицу. Смешайте с салатом, сухариками и соусом. Посыпьте пармезаном."},
                {"name": "Греческий", "ingredients": "Помидоры (3 шт), огурцы (2 шт), перец (1 шт), красный лук (1/2 шт), маслины (100 г), сыр фета (150 г), оливковое масло", "time": "15 мин", "method": "Нарежьте овощи. Добавьте маслины и фету. Заправьте маслом."},
                {"name": "Оливье", "ingredients": "Картофель (4 шт), морковь (2 шт), яйца (4 шт), колбаса (300 г), огурцы соленые (3 шт), горошек (1 банка), майонез", "time": "40 мин", "method": "Отварите овощи и яйца. Нарежьте кубиками. Смешайте с горошком и майонезом."},
                {"name": "Крабовый", "ingredients": "Крабовые палочки (200 г), рис (200 г), кукуруза (1 банка), яйца (4 шт), огурец (2 шт), майонез", "time": "30 мин", "method": "Отварите рис и яйца. Нарежьте все ингредиенты. Смешайте с майонезом."},
                {"name": "Свекольный", "ingredients": "Свекла (3 шт), чеснок (3 зубчика), грецкие орехи (100 г), чернослив (100 г), майонез", "time": "50 мин", "method": "Запеките свеклу. Натрите, смешайте с измельченными орехами, черносливом и чесноком. Заправьте майонезом."},
                {"name": "Капрезе", "ingredients": "Помидоры (3 шт), моцарелла (200 г), базилик, оливковое масло, бальзамический уксус", "time": "10 мин", "method": "Нарежьте помидоры и моцареллу кружочками. Выложите слоями с листьями базилика. Полейте маслом и уксусом."}
            ]
        }
        
        if not os.path.exists(RECIPES_FILE):
            with open(RECIPES_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_recipes, f, ensure_ascii=False, indent=2)
            self.recipes = default_recipes
        else:
            with open(RECIPES_FILE, 'r', encoding='utf-8') as f:
                self.recipes.update(json.load(f))
    
    def save_recipes(self):
        """Сохраняет рецепты в файл"""
        with open(RECIPES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)
    
    def get_random_recipe(self, category=None):
        """Возвращает случайный рецепт из указанной или любой категории"""
        if category and category in self.recipes:
            recipes = self.recipes[category]
        else:
            recipes = [recipe for cat in self.recipes.values() for recipe in cat]
        
        if not recipes:
            return None
        return random.choice(recipes)
    
    def add_recipe(self, category, recipe_data):
        """Добавляет новый рецепт"""
        if category not in self.recipes:
            self.recipes[category] = []
        self.recipes[category].append(recipe_data)
        self.save_recipes()

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.manager = RecipeManager()
        self.current_recipe = None
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("🍳 Генератор рецептов 🍳")
        self.root.geometry("900x600")  # Уменьшил высоту окна
        self.root.configure(bg=COLORS["background"])
        
        # Стили
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=COLORS["background"])
        style.configure('TLabel', background=COLORS["background"], 
                       foreground=COLORS["text"], font=FONTS["recipe"])
        style.configure('TButton', font=FONTS["button"], padding=10, 
                      background=COLORS["primary"], foreground='white')
        style.map('TButton', 
                 background=[('active', COLORS["secondary"]), 
                           ('pressed', COLORS["accent"])])
        
        # Главный контейнер
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame, 
                              text="ГЕНЕРАТОР РЕЦЕПТОВ", 
                              font=FONTS["title"],
                              fg=COLORS["accent"], bg=COLORS["background"])
        title_label.pack(pady=10)
        
        # Кнопки категорий
        categories_frame = ttk.Frame(main_frame, style='TFrame')
        categories_frame.pack(fill='x', pady=10)
        
        category_icons = {
            "Завтрак": "🍳", 
            "Обед": "🍲", 
            "Ужин": "🍽️", 
            "Десерт": "🍰",
            "Выпечка": "🥐",
            "Салаты": "🥗"
        }
        
        for i, category in enumerate(CATEGORIES):
            btn = tk.Button(categories_frame, 
                          text=f"{category_icons.get(category, '')} {category}",
                          font=FONTS["category"],
                          bg=COLORS["primary"], fg="white",
                          bd=0, padx=10, pady=5,
                          command=lambda c=category: self.show_recipe(c))
            btn.grid(row=0, column=i, padx=5, sticky='ew')
        
        # Кнопка случайного рецепта
        random_btn = tk.Button(categories_frame, 
                             text="🎲 Случайный рецепт",
                             font=FONTS["button"],
                             bg=COLORS["accent"], fg="white",
                             bd=0, pady=8,
                             command=lambda: self.show_recipe())
        random_btn.grid(row=1, column=0, columnspan=len(CATEGORIES), 
                       pady=10, sticky='ew')
        
        # Поле рецепта (уменьшенное)
        recipe_frame = tk.Frame(main_frame, bg=COLORS["light"], 
                              bd=2, relief=tk.GROOVE)
        recipe_frame.pack(fill='both', expand=True, pady=10)
        
        # Верхняя декоративная полоса
        decor_frame = tk.Frame(recipe_frame, bg=COLORS["accent"], height=3)
        decor_frame.pack(fill='x')
        
        self.recipe_text = tk.Text(recipe_frame, wrap='word', 
                                 font=FONTS["recipe"],
                                 bg=COLORS["light"], fg=COLORS["text"],
                                 padx=15, pady=15, height=10,  # Уменьшил высоту
                                 relief=tk.FLAT)
        self.recipe_text.pack(fill='both', expand=True)
        
        # Нижняя декоративная полоса
        tk.Frame(recipe_frame, bg=COLORS["accent"], height=3).pack(fill='x')
        
        # Панель инструментов
        tools_frame = tk.Frame(main_frame, bg=COLORS["background"])
        tools_frame.pack(fill='x', pady=10)
        
        # Стилизованные кнопки
        button_style = {
            "font": FONTS["button"],
            "bg": COLORS["primary"],
            "fg": "white",
            "activebackground": COLORS["accent"],
            "activeforeground": "white",
            "bd": 0,
            "padx": 15,
            "pady": 8
        }
        
        add_btn = tk.Button(tools_frame, text="➕ Добавить рецепт",
                           command=self.show_add_recipe_dialog,
                           **button_style)
        add_btn.pack(side='left', padx=5)
        
        email_btn = tk.Button(tools_frame, text="📧 Отправить рецепт",
                             command=self.show_email_dialog,
                             **button_style)
        email_btn.pack(side='left', padx=5)
        
        # Стартовое сообщение
        self.recipe_text.insert('end', "Выберите категорию или нажмите 'Случайный рецепт'")
        self.recipe_text.config(state='disabled')
    
    def show_recipe(self, category=None):
        """Показывает случайный рецепт"""
        self.current_recipe = self.manager.get_random_recipe(category)
        
        self.recipe_text.config(state='normal')
        self.recipe_text.delete('1.0', 'end')
        
        if not self.current_recipe:
            self.recipe_text.insert('end', f"В категории '{category}' пока нет рецептов")
        else:
            # Красивое оформление рецепта
            self.recipe_text.tag_configure("title", font=("Georgia", 14, "bold"), 
                                         foreground=COLORS["accent"])
            self.recipe_text.tag_configure("time", font=("Arial", 11, "italic"))
            self.recipe_text.tag_configure("header", font=("Arial", 12, "bold"))
            self.recipe_text.tag_configure("ingredients", font=FONTS["ingredients"])
            
            self.recipe_text.insert('end', self.current_recipe['name'] + "\n\n", "title")
            self.recipe_text.insert('end', f"⏱️ {self.current_recipe['time']}\n\n", "time")
            
            self.recipe_text.insert('end', "🍴 Ингредиенты:\n", "header")
            self.recipe_text.insert('end', self.current_recipe['ingredients'] + "\n\n", "ingredients")
            
            self.recipe_text.insert('end', "👩‍🍳 Способ приготовления:\n", "header")
            self.recipe_text.insert('end', self.current_recipe['method'] + "\n\n")
            
            self.recipe_text.insert('end', "🍽️ Приятного аппетита! ✨", "title")
        
        self.recipe_text.config(state='disabled')
    
    def show_add_recipe_dialog(self):
        """Диалог добавления нового рецепта"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить новый рецепт")
        dialog.geometry("600x650")
        dialog.configure(bg=COLORS["background"])
        dialog.resizable(False, False)
        
        # Главный контейнер с прокруткой
        main_container = tk.Frame(dialog, bg=COLORS["background"])
        main_container.pack(fill='both', expand=True)
        
        # Декоративный заголовок
        header_frame = tk.Frame(main_container, bg=COLORS["accent"])
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="ДОБАВИТЬ РЕЦЕПТ", 
                font=("Impact", 14),
                fg="white", bg=COLORS["accent"], pady=10).pack()
        
        # Фрейм для содержимого с прокруткой
        canvas = tk.Canvas(main_container, bg=COLORS["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["background"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Стилизованные элементы формы
        label_style = {"font": ("Georgia", 11), "bg": COLORS["background"], 
                      "fg": COLORS["text"], "anchor": "w"}
        entry_style = {"font": ("Arial", 10), "bg": "white", "bd": 1, 
                      "relief": tk.SOLID, "highlightthickness": 0}
        
        # Категория
        tk.Label(scrollable_frame, text="Категория:", **label_style).pack(fill='x', pady=(10, 5))
        category_var = tk.StringVar(value=CATEGORIES[0])
        category_menu = ttk.Combobox(scrollable_frame, textvariable=category_var,
                                   values=CATEGORIES, state='readonly',
                                   font=("Arial", 10))
        category_menu.pack(fill='x', pady=5)
        
        # Название
        tk.Label(scrollable_frame, text="Название блюда:", **label_style).pack(fill='x', pady=(10, 5))
        name_entry = tk.Entry(scrollable_frame, **entry_style)
        name_entry.pack(fill='x', pady=5)
        
        # Ингредиенты
        tk.Label(scrollable_frame, text="Ингредиенты:", **label_style).pack(fill='x', pady=(10, 5))
        ingredients_text = tk.Text(scrollable_frame, height=5, wrap='word',
                                 font=("Verdana", 10),
                                 bg="white", bd=1, relief=tk.SOLID)
        ingredients_text.pack(fill='x', pady=5)
        
        # Время
        tk.Label(scrollable_frame, text="Время приготовления:", **label_style).pack(fill='x', pady=(10, 5))
        time_entry = tk.Entry(scrollable_frame, **entry_style)
        time_entry.pack(fill='x', pady=5)
        
        # Способ приготовления
        tk.Label(scrollable_frame, text="Способ приготовления:", **label_style).pack(fill='x', pady=(10, 5))
        method_text = tk.Text(scrollable_frame, height=10, wrap='word',
                            font=("Georgia", 10),
                            bg="white", bd=1, relief=tk.SOLID)
        method_text.pack(fill='x', pady=5)
        
        # Фрейм для кнопок (вне scrollable_frame)
        btn_frame = tk.Frame(main_container, bg=COLORS["background"])
        btn_frame.pack(fill='x', pady=10)
        
        def save_recipe():
            recipe_data = {
                "name": name_entry.get(),
                "ingredients": ingredients_text.get("1.0", "end-1c"),
                "time": time_entry.get(),
                "method": method_text.get("1.0", "end-1c")
            }
            if not all(recipe_data.values()):
                messagebox.showwarning("Внимание", "Заполните все поля!")
                return
                
            self.manager.add_recipe(category_var.get(), recipe_data)
            messagebox.showinfo("Успех", "Рецепт успешно добавлен!")
            dialog.destroy()
        
        tk.Button(btn_frame, text="Сохранить", 
                 command=save_recipe,
                 bg=COLORS["primary"], fg="white",
                 font=FONTS["button"],
                 padx=20, pady=5, bd=0).pack(side='right', padx=10)
        
        tk.Button(btn_frame, text="Отмена", 
                 command=dialog.destroy,
                 bg=COLORS["secondary"], fg="white",
                 font=FONTS["button"],
                 padx=20, pady=5, bd=0).pack(side='right', padx=10)
    
    def show_email_dialog(self):
        """Диалог отправки рецепта по email"""
        if not self.current_recipe:
            messagebox.showwarning("Ошибка", "Сначала выберите рецепт!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Отправить рецепт")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS["background"])
        dialog.resizable(False, False)
        
        # Декоративный заголовок
        header_frame = tk.Frame(dialog, bg=COLORS["accent"])
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="ОТПРАВИТЬ РЕЦЕПТ", 
                font=("Impact", 14),
                fg="white", bg=COLORS["accent"], pady=8).pack()
        
        # Основной фрейм
        main_frame = tk.Frame(dialog, bg=COLORS["background"])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Стилизованные элементы формы
        label_style = {"font": ("Georgia", 11), "bg": COLORS["background"], 
                      "fg": COLORS["text"], "anchor": "w"}
        entry_style = {"font": ("Arial", 10), "bg": "white", "bd": 1, 
                      "relief": tk.SOLID, "highlightthickness": 0}
        
        # Поля формы
        tk.Label(main_frame, text="Ваш email:", **label_style).pack(fill='x', pady=(5, 0))
        sender_entry = tk.Entry(main_frame, **entry_style)
        sender_entry.pack(fill='x', pady=5)
        
        tk.Label(main_frame, text="Email получателя:", **label_style).pack(fill='x', pady=(10, 0))
        receiver_entry = tk.Entry(main_frame, **entry_style)
        receiver_entry.pack(fill='x', pady=5)
        
        tk.Label(main_frame, text="Тема письма:", **label_style).pack(fill='x', pady=(10, 0))
        subject_entry = tk.Entry(main_frame, **entry_style)
        subject_entry.insert(0, f"Рецепт: {self.current_recipe['name']}")
        subject_entry.pack(fill='x', pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(main_frame, bg=COLORS["background"])
        btn_frame.pack(fill='x', pady=20)
        
        def send_email():
            sender = sender_entry.get()
            receiver = receiver_entry.get()
            subject = subject_entry.get()
            
            if not sender or not receiver:
                messagebox.showwarning("Ошибка", "Заполните все поля!")
                return
            
            try:
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = subject
                
                body = (
                    f"Привет! Вот рецепт, которым я хочу поделиться:\n\n"
                    f"✨ {self.current_recipe['name']} ✨\n\n"
                    f"⏱️ Время приготовления: {self.current_recipe['time']}\n\n"
                    f"🍴 Ингредиенты:\n{self.current_recipe['ingredients']}\n\n"
                    f"👩‍🍳 Способ приготовления:\n{self.current_recipe['method']}\n\n"
                    f"Приятного аппетита!"
                )
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Настройки SMTP (пример для Gmail)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, "your_password")  # Замените на реальный пароль
                server.send_message(msg)
                server.quit()
                
                messagebox.showinfo("Успех", "Рецепт успешно отправлен!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось отправить письмо: {str(e)}")
        
        tk.Button(btn_frame, text="Отправить", 
                 command=send_email,
                 bg=COLORS["primary"], fg="white",
                 font=FONTS["button"],
                 padx=20, pady=5, bd=0).pack(side='right', padx=10)
        
        tk.Button(btn_frame, text="Отмена", 
                 command=dialog.destroy,
                 bg=COLORS["secondary"], fg="white",
                 font=FONTS["button"],
                 padx=20, pady=5, bd=0).pack(side='right', padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()