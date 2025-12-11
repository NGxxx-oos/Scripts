import dns.resolver
import sys
import socket
from typing import List, Dict, Tuple

def check_mx_records(domain: str) -> Tuple[bool, str]:
    
    try:
        
        try:
            socket.gethostbyname(domain)
        except socket.gaierror:
            return False, "домен отсутствует"
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if len(mx_records) > 0:
                return True, "домен валиден"
            else:
                return False, "MX-записи отсутствуют или некорректны"
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False, "MX-записи отсутствуют или некорректны"
        except dns.resolver.NoNameservers:
            return False, "ошибка серверов имен"
            
    except Exception as e:
        return False, f"ошибка проверки: {str(e)}"

def process_emails(email_list: List[str]) -> List[Dict[str, str]]:
    results = []
    
    for email in email_list:
        email = email.strip()
        if not email:
            continue
            
        if '@' not in email:
            results.append({
                'email': email,
                'status': 'некорректный email',
                'domain': 'N/A'
            })
            continue
            
        domain = email.split('@')[-1]
        is_valid, message = check_mx_records(domain)
        
        results.append({
            'email': email,
            'domain': domain,
            'status': message,
            'valid': is_valid
        })
    
    return results

def main():
    """Основная функция"""
    print("=== Проверка MX-записей email-доменов ===\n")
    
    
    sample_emails = [
        "test@gmail.com",
        "user@example.com",
        "invalid@nonexistentdomain12345.ru",
        "another@yahoo.com"
    ]
    
    print("Пример использования со встроенным списком:")
    print("-" * 50)
    
    results = process_emails(sample_emails)
    
    for result in results:
        print(f"{result['email']}: {result['status']}")
    
    print("\n" + "=" * 50)
    
    
    if len(sys.argv) > 1:
        print("Проверка email-адресов из аргументов командной строки:")
        print("-" * 50)
        
        input_emails = sys.argv[1:]
        results = process_emails(input_emails)
        
        for result in results:
            print(f"{result['email']}: {result['status']}")
    
    
    print("\nДля проверки email-адресов из файла создайте файл emails.txt")
    print("и запустите скрипт: python domain_checker.py --file emails.txt")

if __name__ == "__main__":
    main()
