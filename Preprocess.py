import re
import string

def clean_kannada_text(text):
    """
    Clean Kannada text using comprehensive regex patterns
    """
    #print("Original text:", text)
    #print("-" * 50)
    
    # Step 1: Remove URLs, email addresses and their patterns
    url_email_pattern = r'(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)'
    text = re.sub(url_email_pattern, '', text)
    #print("After removing URLs and emails:", text)
    
    # Step 2: Remove all special characters (including @, ://, . etc)
    special_char_pattern = r'[!@#$%^&*()_+\-=\[\]{};:"|<>/?.,\\]'
    text = re.sub(special_char_pattern, '', text)
    #print("After removing special characters:", text)
    
    # Step 3: Remove English characters
    text = re.sub(r'[a-zA-Z]', '', text)
    #print("After removing English:", text)
    
    # Step 4: Remove numbers (both English and Kannada)
    text = re.sub(r'[0-9]', '', text)
    kannada_digits = ''.join(chr(x) for x in range(0x0CE6, 0x0CF0))
    text = ''.join(char for char in text if char not in kannada_digits)
    #print("After removing numbers:", text)
    
    # Step 5: Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    # print("After cleaning whitespace:", text)
    
    return text

'''
# Test cases
test_cases = [
    """
    Hello ನನ್ನ ಹೆಸರು123 ರವಿ!!! 
    https://example.com
    test@email.com
    ಮತ್ತು    ನಾನು    ಬೆಂಗಳೂರಿನಲ್ಲಿ     ವಾಸಿಸುತ್ತೇನೆ...
    """,
    
    """
    ನಮಸ್ಕಾರ!!! ನಾನು bangalore://test ನಲ್ಲಿ 123 ಜನ ಸ್ನೇಹಿತರನ್ನು ಹೊಂದಿದ್ದೇನೆ... 
    http://test.com user@test.com ಅವರೆಲ್ಲರೂ IT industry ನಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತಾರೆ!!!
    """,
    
    """
    Special test case:
    user.name@domain.com
    https://test.com/path?param=value
    web://random.site
    ನನ್ನ ಹೆಸರು@### ರವಿ!!! 
    """
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTEST CASE {i}")
    print("=" * 50)
    cleaned = clean_kannada_text(test_case)
    print(f"\nFinal cleaned text: {cleaned}")
'''