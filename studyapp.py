import re
import random
import time
import threading

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = self._validate_password(password)
        self.cards: list[dict] = []
        self.notes: list[str] = []

    def _validate_password(self, password: str) -> str:
        if len(password) < 5:
            raise ValueError("Пароль должен быть не менее 5 символов")
        if not re.fullmatch(r'[a-zA-Z0-9]+', password):
            raise ValueError("Пароль: только латинские буквы и цифры")
        return password

class Registration:
    def __init__(self):
        self.users: list[User] = []

    def _is_username_taken(self, username: str) -> bool:
        return any(u.username == username for u in self.users)

    def register(self, username: str, password: str) -> User:
        if self._is_username_taken(username):
            raise ValueError(f"Имя '{username}' уже занято")
        user = User(username, password)
        self.users.append(user)
        return user

    def login(self, username: str, password: str) -> User:
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        raise ValueError("Неверное имя пользователя или пароль")

class FlashCards:
    def __init__(self, user: User):
        self.user = user

    def add_card(self):
        question = input("Вопрос: ").strip()
        answer = input("Ответ: ").strip()
        if not question or not answer:
            print("Вопрос и ответ не могут быть пустыми.")
            return
        self.user.cards.append({"question": question, "answer": answer})
        print("✓ Карточка добавлена!")

    def random_card(self):
        if not self.user.cards:
            print("У вас нет карточек. Сначала добавьте их.")
            return
        card = random.choice(self.user.cards)
        print(f"\nВопрос: {card['question']}")
        input("Нажмите Enter, чтобы увидеть ответ...")
        print(f"Ответ: {card['answer']}")

    def show_menu(self):
        while True:
            print("\n─── Карточки ───")
            print("1. Добавить карточку")
            print("2. Случайная карточка")
            print("0. Назад")
            choice = input("Выбор: ").strip()
            if choice == "1":
                self.add_card()
            elif choice == "2":
                self.random_card()
            elif choice == "0":
                break
            else:
                print("Неверный выбор.")

class Quiz:
    TIME_LIMIT = 30

    def __init__(self, user: User):
        self.user = user
        self._timed_out = False

    def _start_timer(self):
        self._timed_out = False

        def _timeout():
            self._timed_out = True
            print("\n⏰ Время вышло! Переходим к следующему вопросу.")

        timer = threading.Timer(self.TIME_LIMIT, _timeout)
        timer.daemon = True
        timer.start()
        return timer

    def run(self):
        if not self.user.cards:
            print("Нет карточек для викторины. Сначала добавьте карточки.")
            return

        cards = self.user.cards.copy()
        random.shuffle(cards)
        score = 0

        print(f"\n─── Викторина ({len(cards)} вопросов, {self.TIME_LIMIT} сек на ответ) ───")

        for i, card in enumerate(cards, 1):
            print(f"\nВопрос {i}/{len(cards)}: {card['question']}")
            print(f"(У вас {self.TIME_LIMIT} секунд)")

            start = time.time()
            timer = self._start_timer()

            answer = input("Ваш ответ: ").strip()
            timer.cancel()

            if self._timed_out:
                print(f"Правильный ответ: {card['answer']}")
                continue

            elapsed = time.time() - start
            if answer.lower() == card['answer'].lower():
                print(f"✓ Правильно! ({elapsed:.1f} сек)")
                score += 1
            else:
                print(f"✗ Неверно. Правильный ответ: {card['answer']}")

        print(f"\n─── Результат: {score}/{len(cards)} ───")

    def show_menu(self):
        while True:
            print("\n─── Викторина ───")
            print("1. Начать викторину")
            print("0. Назад")
            choice = input("Выбор: ").strip()
            if choice == "1":
                self.run()
            elif choice == "0":
                break
            else:
                print("Неверный выбор.")

class Notes:
    def __init__(self, user: User):
        self.user = user

    def add_note(self):
        text = input("Текст заметки: ").strip()
        if not text:
            print("Заметка не может быть пустой.")
            return
        self.user.notes.append(text)
        print("✓ Заметка сохранена!")

    def show_notes(self):
        if not self.user.notes:
            print("Заметок нет.")
            return
        print("\n─── Ваши заметки ───")
        for i, note in enumerate(self.user.notes, 1):
            print(f"{i}. {note}")

    def delete_note(self):
        self.show_notes()
        if not self.user.notes:
            return
        try:
            idx = int(input("Номер заметки для удаления: ")) - 1
            if 0 <= idx < len(self.user.notes):
                removed = self.user.notes.pop(idx)
                print(f"✓ Удалено: '{removed}'")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Введите число.")

    def edit_note(self):
        self.show_notes()
        if not self.user.notes:
            return
        try:
            idx = int(input("Номер заметки для редактирования: ")) - 1
            if 0 <= idx < len(self.user.notes):
                new_text = input("Новый текст: ").strip()
                if new_text:
                    self.user.notes[idx] = new_text
                    print("✓ Заметка обновлена!")
                else:
                    print("Текст не может быть пустым.")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Введите число.")

    def show_menu(self):
        while True:
            print("\n─── Заметки ───")
            print("1. Добавить заметку")
            print("2. Просмотреть заметки")
            print("3. Редактировать заметку")
            print("4. Удалить заметку")
            print("0. Назад")
            choice = input("Выбор: ").strip()
            if choice == "1":
                self.add_note()
            elif choice == "2":
                self.show_notes()
            elif choice == "3":
                self.edit_note()
            elif choice == "4":
                self.delete_note()
            elif choice == "0":
                break
            else:
                print("Неверный выбор.")

class App:
    def __init__(self):
        self.registration = Registration()
        self.current_user: User | None = None

    def _auth_menu(self):
        while True:
            print("\n═══════════════════════")
            print("    STUDY APP")
            print("═══════════════════════")
            print("1. Регистрация")
            print("2. Вход")
            print("0. Выход")
            choice = input("Выбор: ").strip()

            if choice == "1":
                self._register()
            elif choice == "2":
                self._login()
                if self.current_user:
                    self._main_menu()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор.")

    def _register(self):
        print("\n─── Регистрация ───")
        username = input("Имя пользователя: ").strip()
        password = input("Пароль: ").strip()
        try:
            user = self.registration.register(username, password)
            print(f"✓ Пользователь '{user.username}' зарегистрирован!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _login(self):
        print("\n─── Вход ───")
        username = input("Имя пользователя: ").strip()
        password = input("Пароль: ").strip()
        try:
            self.current_user = self.registration.login(username, password)
            print(f"✓ Добро пожаловать, {self.current_user.username}!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _main_menu(self):
        while True:
            print(f"\n─── Меню ({self.current_user.username}) ───")
            print("1. Карточки")
            print("2. Викторина")
            print("3. Заметки")
            print("0. Выйти из аккаунта")
            choice = input("Выбор: ").strip()

            if choice == "1":
                FlashCards(self.current_user).show_menu()
            elif choice == "2":
                Quiz(self.current_user).show_menu()
            elif choice == "3":
                Notes(self.current_user).show_menu()
            elif choice == "0":
                print(f"Вы вышли из аккаунта '{self.current_user.username}'.")
                self.current_user = None
                break
            else:
                print("Неверный выбор.")

    def run(self):
        self._auth_menu()

if __name__ == "__main__":
    App().run()
