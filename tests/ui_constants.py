"""
Константи та селектори для UI тестів бронювання кімнат
"""

class UISelectors:
    """Селектори для елементів UI"""
    
    # Селектори для завантаження кімнат
    ROOMS_LOADING_SELECTORS = [
        '.row.hotel-room-info',
        '.room',
        '[class*="room"]'
    ]
    
    # Селектори для елементів форми бронювання
    FORM_SELECTORS = {
        'firstname': [
            'input[placeholder*="Firstname"]',
            'input[name="firstname"]',
            'input#firstname',
            '.firstname input'
        ],
        'lastname': [
            'input[placeholder*="Lastname"]',
            'input[name="lastname"]',
            'input#lastname',
            '.lastname input'
        ],
        'email': [
            'input[placeholder*="Email"]',
            'input[name="email"]',
            'input#email',
            '.email input',
            'input[type="email"]'
        ],
        'phone': [
            'input[placeholder*="Phone"]',
            'input[name="phone"]',
            'input#phone',
            '.phone input',
            'input[type="tel"]'
        ],
        'checkin': [
            'input[placeholder*="Check-in"]',
            'input[name="checkin"]',
            'input#checkin',
            '.checkin input'
        ],
        'checkout': [
            'input[placeholder*="Check-out"]',
            'input[name="checkout"]',
            'input#checkout',
            '.checkout input'
        ],
        'book_button': [
            'button:has-text("Book")',
            '.btn:has-text("Book")',
            'input[type="submit"][value*="Book"]'
        ]
    }
    
    # Селектори для кнопок бронювання
    BOOKING_BUTTON_SELECTORS = [
        'button:has-text("Book")',
        '.btn:has-text("Book")',
        'input[value*="Book"]'
    ]
    
    # Селектори для кнопок відправки форми
    SUBMIT_BUTTON_SELECTORS = [
        'button[type="submit"]',
        'input[type="submit"]',
        'button:has-text("Submit")',
        'button:has-text("Book")',
        '.btn-primary',
        '.submit-btn'
    ]
    
    # Селектори для календаря
    CALENDAR_DATE_SELECTORS = [
        'button:has-text("{day}")',
        '.day:has-text("{day}")',
        '[data-date*="{date}"]'
    ]
    
    # Селектори для недоступних дат
    UNAVAILABLE_DATE_SELECTORS = [
        'button:has-text("{day}")[disabled]',
        '.disabled:has-text("{day}")',
        '.unavailable:has-text("{day}")'
    ]
    
    # Селектори для індикаторів успіху
    SUCCESS_INDICATORS = [
        'text="Booking Successful"',
        'text="Booking confirmed"',
        'text="Thank you"',
        '.alert-success',
        '.success-message',
        '[class*="success"]'
    ]
    
    # Селектори для індикаторів помилки
    ERROR_INDICATORS = [
        '.alert-danger',
        '.error-message',
        '[class*="error"]',
        'text="must not be empty"',
        'text="must be a well-formed email"',
        'text="must not be null"'
    ]
    
    # Селектори для елементів бронювання на сторінці
    BOOKING_ELEMENTS = [
        'input[placeholder*="name"], input[name*="name"]',
        'input[type="email"], input[placeholder*="email"]',
        'input[type="tel"], input[placeholder*="phone"]',
        'button:has-text("Book"), input[value*="Book"]'
    ]


class UIConstants:
    """Константи для UI тестів"""
    
    # Таймаути
    TIMEOUT_ELEMENTS = 15000
    TIMEOUT_CALENDAR = 3000
    TIMEOUT_RESPONSE = 3000
    TIMEOUT_PAGE_LOAD = 3000
    TIMEOUT_INTERACTION = 2000
    TIMEOUT_FORM_SUBMIT = 2000
    TIMEOUT_CALENDAR_INTERACTION = 1000
    TIMEOUT_MOUSE_MOVE = 1000
    TIMEOUT_ADDITIONAL_WAIT = 5000
    
    # Дати для тестування
    DEFAULT_CHECKIN_DAYS = 7
    DEFAULT_CHECKOUT_DAYS = 2
    TEST_BOOKING_CHECKIN = "2025-08-01"
    TEST_BOOKING_CHECKOUT = "2025-08-03"
    
    # Ключові слова для перевірки успіху
    SUCCESS_KEYWORDS = ['booking', 'confirmed', 'success', 'thank']
    
    # Ключові слова для перевірки помилок
    ERROR_KEYWORDS = ['error', 'invalid', 'required', 'empty']
    
    # Мінімальний розмір контенту сторінки
    MIN_PAGE_CONTENT_LENGTH = 100
    
    # Дані для тестового бронювання через API
    API_TEST_BOOKING_DATA = {
        "firstname": "Test",
        "lastname": "User",
        "email": "test@example.com",
        "phone": "1234567890",
        "bookingdates": {
            "checkin": TEST_BOOKING_CHECKIN,
            "checkout": TEST_BOOKING_CHECKOUT
        }
    }


class UIHelpers:
    """Допоміжні методи для UI тестів"""
    
    @staticmethod
    def format_date_selector(template, day=None, date=None):
        """Форматує селектор дати з підстановкою значень"""
        if day:
            return template.format(day=day)
        if date:
            return template.format(date=date)
        return template
    
    @staticmethod
    def get_calendar_selectors(day):
        """Повертає список селекторів для календаря з конкретним днем"""
        return [
            UIHelpers.format_date_selector(selector, day=day)
            for selector in UISelectors.CALENDAR_DATE_SELECTORS
        ]
    
    @staticmethod
    def get_unavailable_date_selectors(day):
        """Повертає список селекторів для недоступних дат з конкретним днем"""
        return [
            UIHelpers.format_date_selector(selector, day=day)
            for selector in UISelectors.UNAVAILABLE_DATE_SELECTORS
        ]
    
    @staticmethod
    def check_success_indicators(page):
        """Перевіряє наявність індикаторів успіху на сторінці"""
        for indicator in UISelectors.SUCCESS_INDICATORS:
            try:
                if page.locator(indicator).count() > 0:
                    return True
            except:
                continue
        return False
    
    @staticmethod
    def check_error_indicators(page):
        """Перевіряє наявність індикаторів помилки на сторінці"""
        for indicator in UISelectors.ERROR_INDICATORS:
            try:
                if page.locator(indicator).count() > 0:
                    return True
            except:
                continue
        return False
    
    @staticmethod
    def check_content_keywords(page, keywords):
        """Перевіряє наявність ключових слів у контенті сторінки"""
        try:
            page_content = page.content()
            return any(keyword in page_content.lower() for keyword in keywords)
        except:
            return False
    
    @staticmethod
    def count_booking_elements(page):
        """Підраховує кількість елементів бронювання на сторінці"""
        elements_found = 0
        for selector in UISelectors.BOOKING_ELEMENTS:
            try:
                if page.locator(selector).count() > 0:
                    elements_found += 1
            except:
                continue
        return elements_found
    
    @staticmethod
    def try_click_element(page, selectors):
        """Пробує клікнути по елементу з списку селекторів"""
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    element.click()
                    return True
            except:
                continue
        return False
    
    @staticmethod
    def find_element_by_selectors(page, selectors):
        """Знаходить елемент за списком селекторів"""
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    return element
            except:
                continue
        return None