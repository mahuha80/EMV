# Random Number Libraries

## 📚 Hai thư viện cho AI sử dụng

### Library A: RandomEvenLibrary ✅
**Thư viện số chẵn từ 1 - 20**

Vị trí: `src/testing/random_even_library.py`

**Available Keywords:**

| Keyword | Mô tả | Ví dụ |
|---------|-------|-------|
| `Get Random Even Number` | Lấy 1 số chẵn ngẫu nhiên | `${num}= Get Random Even Number` |
| `Get Random Even Numbers` | Lấy N số chẵn ngẫu nhiên | `${list}= Get Random Even Numbers  3` |
| `Get All Even Numbers` | Lấy tất cả số chẵn | `${all}= Get All Even Numbers` |
| `Is Even Number Valid` | Kiểm tra số chẵn hợp lệ | `${valid}= Is Even Number Valid  4` |

**Ví dụ sử dụng trong Robot:**
```robot
*** Settings ***
Library    src.testing.random_even_library.RandomEvenLibrary

*** Test Cases ***
My Test
    ${even_num}=           Get Random Even Number
    Log    Even number is: ${even_num}
    
    ${multiple_even}=      Get Random Even Numbers    5
    Log List    ${multiple_even}
```

---

### Library B: RandomOddLibrary ⭕
**Thư viện số lẻ từ 1 - 20**

Vị trí: `src/testing/random_odd_library.py`

**Available Keywords:**

| Keyword | Mô tả | Ví dụ |
|---------|-------|-------|
| `Get Random Odd Number` | Lấy 1 số lẻ ngẫu nhiên | `${num}= Get Random Odd Number` |
| `Get Random Odd Numbers` | Lấy N số lẻ ngẫu nhiên | `${list}= Get Random Odd Numbers  3` |
| `Get All Odd Numbers` | Lấy tất cả số lẻ | `${all}= Get All Odd Numbers` |
| `Is Odd Number Valid` | Kiểm tra số lẻ hợp lệ | `${valid}= Is Odd Number Valid  5` |

**Ví dụ sử dụng trong Robot:**
```robot
*** Settings ***
Library    src.testing.random_odd_library.RandomOddLibrary

*** Test Cases ***
My Test
    ${odd_num}=           Get Random Odd Number
    Log    Odd number is: ${odd_num}
    
    ${multiple_odd}=      Get Random Odd Numbers    5
    Log List    ${multiple_odd}
```

---

## 🔧 Cách sử dụng với AI

### 1. Import trong .robot file
```robot
*** Settings ***
Library    src.testing.random_even_library.RandomEvenLibrary
Library    src.testing.random_odd_library.RandomOddLibrary

*** Test Cases ***
Test With Random Numbers
    ${even}=       Get Random Even Number
    ${odd}=        Get Random Odd Number
    ${all_even}=   Get All Even Numbers
    ${all_odd}=    Get All Odd Numbers
    
    Log    Even: ${even}
    Log    Odd: ${odd}
    Log List    ${all_even}
    Log List    ${all_odd}
```

### 2. Gọi từ Python (nếu cần)
```python
from src.testing.random_even_library import RandomEvenLibrary
from src.testing.random_odd_library import RandomOddLibrary

even_lib = RandomEvenLibrary()
odd_lib = RandomOddLibrary()

# Lấy số chẵn
random_even = even_lib.get_random_even_number()
print(f"Random even: {random_even}")

# Lấy số lẻ
random_odd = odd_lib.get_random_odd_number()
print(f"Random odd: {random_odd}")

# Lấy danh sách
evens = even_lib.get_random_even_numbers(5)
odds = odd_lib.get_random_odd_numbers(5)
print(f"Evens: {evens}")
print(f"Odds: {odds}")
```

### 3. Trong AI Robot Generator
Khi AI generate test case, nó có thể sử dụng:
```robot
*** Settings ***
Library    AppiumLibrary
Library    src.testing.random_even_library.RandomEvenLibrary
Library    src.testing.random_odd_library.RandomOddLibrary

*** Test Cases ***
TC_Random_Even_Input
    ${random_even}=    Get Random Even Number
    Input Text    id_input    ${random_even}
    
TC_Random_Odd_Input
    ${random_odd}=    Get Random Odd Number
    Input Text    id_input    ${random_odd}
```

---

## 📦 Số chẵn vs Số lẻ

**Even Numbers (Số chẵn) từ 1-20:**
```
2, 4, 6, 8, 10, 12, 14, 16, 18, 20
```

**Odd Numbers (Số lẻ) từ 1-20:**
```
1, 3, 5, 7, 9, 11, 13, 15, 17, 19
```

---

## 🧪 Test Demo

File test demo: `robot_tests/suites/sample/random_numbers_demo.robot`

**Chạy demo:**
```bash
cd /Users/vinhnt0111/Desktop/MCP
robot robot_tests/suites/sample/random_numbers_demo.robot
```

---

## ✨ Tính năng chính

✅ Generate random even/odd numbers  
✅ Parse từ danh sách cố định  
✅ Validation numbers hợp lệ  
✅ Support Robot Framework Library Protocol  
✅ Có thể gọi từ Python hoặc Robot Framework  
✅ AI có thể sử dụng trong test generation  

---

**Tạo bởi:** GitHub Copilot  
**Ngày:** 2026-05-18

