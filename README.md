# AQA Inforce Automation Project

## Project Overview

This project provides a set of **UI** та **API** автотестів для перевірки функціоналу бронювання кімнат на сайті [automationintesting.online](https://automationintesting.online).  
Тести охоплюють основні сценарії для користувача та адміністратора: створення, бронювання, редагування та видалення кімнат, а також перевірку валідації форм.

---

## Structure

```
|-- requirements.txt
|-- test-cases.txt
|-- test_data.json
|-- utils.py
|-- tests/
|   |-- test_admin_api.py
|   |-- test_user_ui.py
```

---

## Requirements

- Python 3.8+
- [pytest](https://docs.pytest.org/)
- [requests](https://docs.python-requests.org/)
- [playwright](https://playwright.dev/python/)
- [pytest-playwright](https://github.com/microsoft/playwright-pytest)

### Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

---

## Test Data

Тестові дані зберігаються у файлі [`test_data.json`](./test_data.json).  
Ви можете змінити дані для своїх сценаріїв, наприклад, логін/пароль адміністратора, шаблон кімнати, валідні/невалідні дані для бронювання.

---

## Running Tests

### Запуск усіх тестів

```bash
pytest
```

### Запуск лише UI тестів

```bash
pytest tests/test_user_ui.py
```

### Запуск лише API тестів

```bash
pytest tests/test_admin_api.py
```

> **Примітка:**  
> Для коректної роботи UI-тестів Playwright браузер відкривається автоматично.  
> Для headless-режиму змініть параметр у тестах на `headless=True`.

---

## Test Cases

Опис тест-кейсів знаходиться у файлі [`test-cases.txt`](./test-cases.txt).

---

## Основні можливості

- **UI Automation:**  
  - Перевірка бронювання кімнати з валідними та невалідними даними  
  - Перевірка недоступності вже заброньованих дат  
  - Перевірка наявності основних елементів інтерфейсу

- **API Automation:**  
  - Створення, перевірка, редагування та видалення кімнат  
  - Створення та видалення бронювань  
  - Перевірка існування кімнати та деталей бронювання

---

## Platform

- **OS:** Windows, Linux, MacOS
- **Python:** 3.8+
- **Playwright:** остання стабільна версія

---

## License

MIT License (or specify your license here)

---

## Citing

If you use this project, please cite as:

```
@misc{aqa-inforce-automation,
  title={AQA Inforce Automation Project},
  url={https://automationintesting.online},
  year={2025}
}
```

---

## References

- [automationintesting.online](https://automationintesting.online)
- [Playwright Python](https://playwright.dev/python/)