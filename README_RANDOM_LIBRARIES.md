# 🎉 Random Number Libraries for Robot Framework

**Status:** ✅ Fully Installed & Working  
**Version:** 1.0.0  
**Python:** 3.6+  
**Robot Framework:** 5.0+  

---

## 📋 Quick Summary

Hai thư viện Robot Framework chuyên nghiệp để generate số ngẫu nhiên:

| Library | Numbers | File | Status |
|---------|---------|------|--------|
| **RandomEvenLibrary** | 2,4,6,8,10,12,14,16,18,20 | `RandomEvenLibrary.py` | ✅ Installed |
| **RandomOddLibrary** | 1,3,5,7,9,11,13,15,17,19 | `RandomOddLibrary.py` | ✅ Installed |

---

## 🚀 Get Started in 30 Seconds

### Python

```python
from RandomEvenLibrary import RandomEvenLibrary
from RandomOddLibrary import RandomOddLibrary

even = RandomEvenLibrary()
odd = RandomOddLibrary()

print(even.get_random_even_number())  # Random even number
print(odd.get_random_odd_number())    # Random odd number
```

### Robot Framework

```robot
*** Settings ***
Library    RandomEvenLibrary
Library    RandomOddLibrary

*** Test Cases ***
Test Random Numbers
    ${even}=    Get Random Even Number
    ${odd}=     Get Random Odd Number
    Log    Even: ${even}, Odd: ${odd}
```

---

## 📚 Available Keywords

### RandomEvenLibrary
- ✅ `Get Random Even Number` - 1 số chẵn ngẫu nhiên
- ✅ `Get Random Even Numbers` - N số chẵn (default: 5)
- ✅ `Get All Even Numbers` - Tất cả số chẵn [2,4,6,...,20]
- ✅ `Is Even Number Valid` - Validate số chẵn (true/false)
- ✅ `Get Last Generated Number` - Lấy số được gen cuối

### RandomOddLibrary
- ✅ `Get Random Odd Number` - 1 số lẻ ngẫu nhiên  
- ✅ `Get Random Odd Numbers` - N số lẻ (default: 5)
- ✅ `Get All Odd Numbers` - Tất cả số lẻ [1,3,5,...,19]
- ✅ `Is Odd Number Valid` - Validate số lẻ (true/false)
- ✅ `Get Last Generated Number` - Lấy số được gen cuối

---

## 📂 File Locations

```
Source Files:
  /Users/vinhnt0111/Desktop/MCP/RandomEvenLibrary/RandomEvenLibrary.py
  /Users/vinhnt0111/Desktop/MCP/RandomOddLibrary/RandomOddLibrary.py

Installed (Global):
  /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/RandomEvenLibrary.py
  /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/RandomOddLibrary.py

Documentation:
  LIBRARY_SUMMARY.md                 - Complete reference
  LIBRARIES_READY_TO_USE.md          - Quick start guide
  LIBRARIES_INSTALLATION_GUIDE.md    - Detailed setup

Test Demo:
  robot_tests/suites/sample/random_numbers_demo.robot
```

---

## ✅ Verification

Verify libraries are working:

```bash
# Run verification script
bash /Users/vinhnt0111/Desktop/MCP/verify_libraries.sh
```

Expected output:
```
✅ RandomEvenLibrary imported
✅ RandomOddLibrary imported
✅ RandomEvenLibrary: All keywords working
✅ RandomOddLibrary: All keywords working
✅ All checks passed!
```

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| `LIBRARY_SUMMARY.md` | 📚 Complete reference & examples |
| `LIBRARIES_READY_TO_USE.md` | 📖 User guide & quick start |
| `LIBRARIES_INSTALLATION_GUIDE.md` | 🔧 Installation & troubleshooting |
| `RANDOM_NUMBERS_LIBRARY.md` | 📋 Original library info |

---

## 🎯 Use Cases

✅ Test data generation  
✅ Random input testing  
✅ Mobile app automation  
✅ Web testing with random values  
✅ AI test generation  
✅ Performance testing  
✅ Data validation testing  

---

## 💻 Python Examples

### Basic Usage
```python
from RandomEvenLibrary import RandomEvenLibrary

even = RandomEvenLibrary()
number = even.get_random_even_number()
print(f"Random even: {number}")
```

### Batch Generation
```python
from RandomOddLibrary import RandomOddLibrary

odd = RandomOddLibrary()
numbers = odd.get_random_odd_numbers(10)
print(f"Random odds: {numbers}")
```

### Validation
```python
from RandomEvenLibrary import RandomEvenLibrary

even = RandomEvenLibrary()
if even.is_even_number_valid(4):
    print("4 is a valid even number ✅")
```

---

## 🤖 Robot Framework Examples

### Simple Test
```robot
*** Settings ***
Library    RandomEvenLibrary

*** Test Cases ***
Test Even Number
    ${num}=    Get Random Even Number
    Log    Got: ${num}
```

### Validation Test
```robot
*** Settings ***
Library    RandomEvenLibrary

*** Test Cases ***
Validate Even Numbers
    ${num}=    Get Random Even Number
    ${valid}=    Is Even Number Valid    ${num}
    Should Be True    ${valid}
```

### Loop Test
```robot
*** Settings ***
Library    RandomEvenLibrary

*** Test Cases ***
Process Multiple Numbers
    ${numbers}=    Get Random Even Numbers    5
    FOR    ${n}    IN    @{numbers}
        Log    Processing: ${n}
    END
```

### Integration Test (with Appium)
```robot
*** Settings ***
Library    AppiumLibrary
Library    RandomEvenLibrary

*** Test Cases ***
Test App with Random Input
    ${even}=    Get Random Even Number
    Open Application    http://localhost:4723/wd/hub    ...
    Input Text    id_field    ${even}
    Tap Element    id_submit
    Close Application
```

---

## 🔧 Troubleshooting

### Issue: Import not working
```bash
# Test import
python3 -c "from RandomEvenLibrary import RandomEvenLibrary; print('OK')"

# If failed, check Python path
python3 -c "import sys; print(sys.path)"
```

### Issue: Robot can't find library
```bash
# Use with --pythonpath
robot --pythonpath /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages \
      your_test.robot
```

### Issue: Need to reinstall
```bash
# Copy files to site-packages again
cp RandomEvenLibrary/RandomEvenLibrary.py \
   /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/
   
cp RandomOddLibrary/RandomOddLibrary.py \
   /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/
```

---

## ℹ️ Library Information

**RandomEvenLibrary**
- Version: 1.0.0
- Scope: GLOBAL
- Keywords: 5
- Numbers: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20
- Total: 10 numbers

**RandomOddLibrary**
- Version: 1.0.0
- Scope: GLOBAL
- Keywords: 5
- Numbers: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19
- Total: 10 numbers

---

## 🎓 Advanced Examples

### Example 1: Configuration with Data
```python
from RandomEvenLibrary import RandomEvenLibrary
from RandomOddLibrary import RandomOddLibrary

config = {
    'test_data_even': RandomEvenLibrary().get_random_even_numbers(5),
    'test_data_odd': RandomOddLibrary().get_random_odd_numbers(5),
}

print(config)
```

### Example 2: Robot with Multiple Runs
```robot
*** Settings ***
Library    RandomEvenLibrary
Library    Collections

*** Test Cases ***
Test Multiple Evens
    [Documentation]    Test with 10 different even numbers
    FOR    ${i}    IN RANGE    10
        ${num}=    Get Random Even Number
        Log    Run ${i}: ${num}
        Should Contain    [2,4,6,8,10,12,14,16,18,20]    ${num}
    END
```

### Example 3: AI Test Generation
```python
# AI can generate this automatically:
test_template = """
*** Settings ***
Library    RandomEvenLibrary
Library    RandomOddLibrary

*** Test Cases ***
{test_name}
    {even_var}=    Get Random Even Number
    {odd_var}=     Get Random Odd Number
    Log    Even: {even_var}, Odd: {odd_var}
"""
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Libraries | 2 |
| Total Keywords | 10 |
| Even Numbers Available | 10 |
| Odd Numbers Available | 10 |
| Code Size | ~350 lines |
| Dependencies | 0 (zero external) |
| Python Version | 3.6+ |
| Installation Type | Site-packages (Global) |
| Last Updated | May 18, 2026 |

---

## ✨ Features

✅ **Zero Dependencies** - Uses only Python standard library  
✅ **Global Installation** - Available everywhere  
✅ **Robot Framework Ready** - Full RF support  
✅ **Type Safe** - Input validation  
✅ **Well Documented** - HTML docs included  
✅ **Logger Support** - Integrates with Robot logger  
✅ **Scope GLOBAL** - Available in all contexts  
✅ **Production Ready** - Tested & verified  
✅ **AI Friendly** - Easy for AI generators to use  
✅ **Easy Import** - Simple `Library` statement  

---

## 🎯 Next Steps

1. ✅ **Libraries Installed** - Ready to use
2. 📚 **Read Documentation** - Understand keywords
3. 🧪 **Run Tests** - Try the demo
4. 🚀 **Integrate** - Use in your tests
5. 🤖 **For AI** - Configure in generators

---

## 📞 Support Resources

- `LIBRARY_SUMMARY.md` - Full reference
- `LIBRARIES_READY_TO_USE.md` - User guide
- `verify_libraries.sh` - Verification script
- `robot_tests/suites/sample/random_numbers_demo.robot` - Test examples

---

## 🎉 Ready to Use!

Both libraries are fully installed and ready for:
- ✅ Python scripts
- ✅ Robot Framework tests
- ✅ Appium mobile testing
- ✅ AI test generation
- ✅ Automation pipelines

**Start using immediately with:**
```python
from RandomEvenLibrary import RandomEvenLibrary
```

or

```robot
Library    RandomEvenLibrary
```

---

**Created:** May 18, 2026  
**Status:** ✅ Production Ready  
**Author:** GitHub Copilot  
**License:** MIT

