# 📚 RandomEvenLibrary & RandomOddLibrary – Hướng dẫn Chi Tiết

## 🎯 Giới Thiệu

Hai thư viện Robot Framework chuyên nghiệp:
- **RandomEvenLibrary** - Generate số chẵn từ 1-20
- **RandomOddLibrary** - Generate số lẻ từ 1-20

## 📁 Cấu Trúc Thư Mục

```
/Users/vinhnt0111/Desktop/MCP/
├── RandomEvenLibrary/
│   ├── setup.py                 # Package configuration
│   ├── requirements.txt          # Dependencies
│   ├── README.md                 # Documentation
│   └── RandomEvenLibrary.py      # Main library code
│
└── RandomOddLibrary/
    ├── setup.py                 # Package configuration
    ├── requirements.txt          # Dependencies
    ├── README.md                 # Documentation
    └── RandomOddLibrary.py       # Main library code
```

---

## 🚀 Cài Đặt

### 1. Cài RandomEvenLibrary

```bash
# Vào thư mục
cd /Users/vinhnt0111/Desktop/MCP/RandomEvenLibrary

# Cài dependencies
pip install -r requirements.txt

# Cài library
pip install -e .
```

### 2. Cài RandomOddLibrary

```bash
# Vào thư mục
cd /Users/vinhnt0111/Desktop/MCP/RandomOddLibrary

# Cài dependencies
pip install -r requirements.txt

# Cài library
pip install -e .
```

### 3. Xác Nhận Cài Đặt

```bash
python -c "from RandomEvenLibrary import RandomEvenLibrary; print('✅ RandomEvenLibrary installed')"
python -c "from RandomOddLibrary import RandomOddLibrary; print('✅ RandomOddLibrary installed')"
```

---

## 📖 Cách Sử Dụng

### 1. Trong Robot Framework

#### RandomEvenLibrary

```robot
*** Settings ***
Library    RandomEvenLibrary

*** Test Cases ***
Test Even Numbers
    ${even}=    Get Random Even Number
    Log    Số chẵn: ${even}
    
    ${multiple}=    Get Random Even Numbers    3
    Log List    ${multiple}
    
    ${valid}=    Is Even Number Valid    4
    Should Be True    ${valid}
```

#### RandomOddLibrary

```robot
*** Settings ***
Library    RandomOddLibrary

*** Test Cases ***
Test Odd Numbers
    ${odd}=    Get Random Odd Number
    Log    Số lẻ: ${odd}
    
    ${multiple}=    Get Random Odd Numbers    3
    Log List    ${multiple}
    
    ${valid}=    Is Odd Number Valid    5
    Should Be True    ${valid}
```

### 2. Trong Python

```python
from RandomEvenLibrary import RandomEvenLibrary
from RandomOddLibrary import RandomOddLibrary

# Even Numbers
even_lib = RandomEvenLibrary()
print(even_lib.get_random_even_number())           # e.g., 4
print(even_lib.get_random_even_numbers(3))         # e.g., [2, 8, 14]
print(even_lib.get_all_even_numbers())             # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print(even_lib.is_even_number_valid(6))            # True

# Odd Numbers
odd_lib = RandomOddLibrary()
print(odd_lib.get_random_odd_number())             # e.g., 7
print(odd_lib.get_random_odd_numbers(3))           # e.g., [1, 9, 15]
print(odd_lib.get_all_odd_numbers())               # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
print(odd_lib.is_odd_number_valid(9))              # True
```

---

## 🔑 Danh Sách Keywords

### RandomEvenLibrary

| Keyword | Mô Tả | Tham Số | Return |
|---------|-------|--------|--------|
| `Get Random Even Number` | Lấy 1 số chẵn ngẫu nhiên | - | int (2,4,6,...,20) |
| `Get Random Even Numbers` | Lấy N số chẵn | count=5 | list of int |
| `Get All Even Numbers` | Lấy tất cả số chẵn | - | [2,4,6,8,10,12,14,16,18,20] |
| `Is Even Number Valid` | Kiểm tra số chẵn hợp lệ | number | True/False |
| `Get Last Generated Number` | Lấy số được generate cuối cùng | - | int or None |

### RandomOddLibrary

| Keyword | Mô Tả | Tham Số | Return |
|---------|-------|--------|--------|
| `Get Random Odd Number` | Lấy 1 số lẻ ngẫu nhiên | - | int (1,3,5,...,19) |
| `Get Random Odd Numbers` | Lấy N số lẻ | count=5 | list of int |
| `Get All Odd Numbers` | Lấy tất cả số lẻ | - | [1,3,5,7,9,11,13,15,17,19] |
| `Is Odd Number Valid` | Kiểm tra số lẻ hợp lệ | number | True/False |
| `Get Last Generated Number` | Lấy số được generate cuối cùng | - | int or None |

---

## 💡 Ví Dụ Thực Tế

### Example 1: Test Input Validation

```robot
*** Settings ***
Library    RandomEvenLibrary
Library    RandomOddLibrary

*** Test Cases ***
Test Valid Even Input
    ${even}=    Get Random Even Number
    Input Text    input_field    ${even}
    Submit Form
    Page Should Show Text    Input accepted

Test Valid Odd Input
    ${odd}=    Get Random Odd Number
    Input Text    input_field    ${odd}
    Submit Form
    Page Should Show Text    Input accepted
```

### Example 2: Test Data Generation

```robot
*** Settings ***
Library    RandomEvenLibrary

*** Test Cases ***
Test Multiple Even Scenarios
    ${test_data}=    Get Random Even Numbers    5
    FOR    ${number}    IN    @{test_data}
        Log    Testing with: ${number}
        ${valid}=    Is Even Number Valid    ${number}
        Should Be True    ${valid}
    END
```

### Example 3: Combined Test

```robot
*** Settings ***
Library    RandomEvenLibrary
Library    RandomOddLibrary

*** Test Cases ***
Test Even and Odd Together
    ${even}=    Get Random Even Number
    ${odd}=     Get Random Odd Number
    
    Log    Even: ${even}
    Log    Odd: ${odd}
    
    ${all_even}=    Get All Even Numbers
    ${all_odd}=     Get All Odd Numbers
    
    Should Contain    ${all_even}    ${even}
    Should Contain    ${all_odd}     ${odd}
```

---

## 🔧 Troubleshooting

### Library không được recognize

```bash
# Xác nhận cài đặt
pip list | grep -i random

# Cài lại
pip install --force-reinstall -e /Users/vinhnt0111/Desktop/MCP/RandomEvenLibrary
pip install --force-reinstall -e /Users/vinhnt0111/Desktop/MCP/RandomOddLibrary
```

### Import error

```bash
# Kiểm tra Python path
python -c "import sys; print(sys.path)"

# Xác nhận file tồn tại
ls -la /Users/vinhnt0111/Desktop/MCP/RandomEvenLibrary/
ls -la /Users/vinhnt0111/Desktop/MCP/RandomOddLibrary/
```

### Robot không tìm thấy library

```bash
# Thử cách khác - dùng path đầy đủ
robot --pythonpath /Users/vinhnt0111/Desktop/MCP/RandomEvenLibrary \
      --variable PYTHONPATH:/Users/vinhnt0111/Desktop/MCP/RandomOddLibrary \
      your_test.robot
```

---

## 📋 Số Chẵn vs Số Lẻ (1-20)

### Số Chẵn (Even)
```
2, 4, 6, 8, 10, 12, 14, 16, 18, 20
```
**Tổng cộng:** 10 số

### Số Lẻ (Odd)
```
1, 3, 5, 7, 9, 11, 13, 15, 17, 19
```
**Tổng cộng:** 10 số

---

## 🎨 Library Info

**RandomEvenLibrary**
- Version: 1.0.0
- Scope: GLOBAL
- Python: 3.6+
- Dependencies: robot-framework>=5.0

**RandomOddLibrary**
- Version: 1.0.0
- Scope: GLOBAL
- Python: 3.6+
- Dependencies: robot-framework>=5.0

---

## ✅ Tính Năng

✅ Hỗ trợ Robot Framework 5.0+
✅ Scope GLOBAL (available everywhere)
✅ Logger integration
✅ Type validation
✅ Comprehensive documentation
✅ Pip installable
✅ Editable install support (-e flag)
✅ Compatible với AI test generation

---

## 📞 Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Robot Framework được cài đúng phiên bản
2. Library được cài trong environment hiện tại
3. Python >= 3.6

---

**Tạo bởi:** GitHub Copilot
**Ngày:** 2026-05-18
**Status:** ✅ Sẵn sàng sử dụng

