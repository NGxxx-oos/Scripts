import requests
import argparse
import os
import sys
from typing import Optional


class TelegramBotSender:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Инициализация бота

        Args:
            bot_token: Токен бота от @BotFather
            chat_id: ID приватного чата
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text: str) -> bool:
        """
        Отправляет сообщение в чат

        Returns:
            bool: Успешность отправки
        """
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"}

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            if response.json().get("ok"):
                print(f"✅ Сообщение успешно отправлено в чат {self.chat_id}")
                return True
            else:
                print(f"❌ Ошибка отправки: {response.json()}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            return False

    def send_from_file(self, file_path: str) -> bool:
        """
        Читает текст из файла и отправляет его

        Returns:
            bool: Успешность отправки
        """
        try:
            if not os.path.exists(file_path):
                print(f"❌ Файл не найден: {file_path}")
                return False

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().strip()

            if not text:
                print("❌ Файл пуст")
                return False

            print(f"📄 Чтение файла: {file_path}")
            print(f"📝 Длина текста: {len(text)} символов")

            
            max_length = 4000
            if len(text) > max_length:
                print(f"⚠️ Текст длинный, разбиваю на части...")
                parts = [
                    text[i : i + max_length] for i in range(0, len(text), max_length)
                ]

                success = True
                for i, part in enumerate(parts, 1):
                    print(f"📤 Отправка части {i}/{len(parts)}...")
                    if not self.send_message(f"Часть {i}/{len(parts)}:\n\n{part}"):
                        success = False

                return success
            else:
                return self.send_message(text)

        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
            return False


def setup_instructions():
    """Выводит инструкцию по настройке"""
    print("=" * 60)
    print("ИНСТРУКЦИЯ ПО НАСТРОЙКЕ TELEGRAM БОТА")
    print("=" * 60)
    print("\n1. Создайте бота через @BotFather в Telegram")
    print("   - Напишите /newbot")
    print("   - Выберите имя бота")
    print("   - Получите токен (выглядит как: 1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ)")
    print("\n2. Добавьте бота в приватный чат")
    print("   - Создайте группу в Telegram")
    print("   - Добавьте бота в группу как администратора")
    print("\n3. Получите chat_id:")
    print("   - Отправьте любое сообщение в чат")
    print(
        "   - Перейдите по ссылке: https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates"
    )
    print("   - Найдите 'chat': {'id': -1001234567890}")
    print("\n4. Используйте скрипт:")
    print(
        "   python telegram_sender.py --token <ТОКЕН> --chat <CHAT_ID> --file message.txt"
    )
    print("=" * 60)


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description="Отправка текста из файла в Telegram чат"
    )
    parser.add_argument("--token", help="Токен Telegram бота")
    parser.add_argument("--chat", help="ID чата")
    parser.add_argument("--file", required=True, help="Путь к файлу с текстом")
    parser.add_argument(
        "--setup", action="store_true", help="Показать инструкцию по настройке"
    )

    args = parser.parse_args()

    if args.setup:
        setup_instructions()
        return

    if not args.token or not args.chat:
        print("❌ Требуются --token и --chat аргументы")
        print("\nИспользуйте --setup для инструкции по настройке")
        sys.exit(1)

    if not args.file:
        print("❌ Требуется --file аргумент")
        sys.exit(1)

    
    sender = TelegramBotSender(args.token, args.chat)

    
    success = sender.send_from_file(args.file)

    if success:
        print("\n✅ Отправка завершена успешно!")
        sys.exit(0)
    else:
        print("\n❌ Ошибка отправки")
        sys.exit(1)


if __name__ == "__main__":
    main()
