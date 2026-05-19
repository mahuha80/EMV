# 🤖 AI EXECUTION GUIDE - Read Rules & Execute

> AI reads AI_DECISION_FLOW_RULES.md and follows rules to decide which function to call

---

## 🚀 HOW AI SHOULD USE THIS

### Step 1: Read the Rules File
```
Read: AI_DECISION_FLOW_RULES.md
├─ Understand: Rule R1 (Priority based on mcp_value)
├─ Understand: Rule R2 (Test type decision)
├─ Understand: Rule R3 (Batch processing)
├─ Understand: Rule R4 (Error handling)
└─ Understand: Rules R5 (Completion)
```

### Step 2: Execute Flow Based on Rules
```
DO:
1. Call: process_ticket_with_mcp(ticket_id)
2. Check result
3. Read Rule R1 → "If mcp_value >= 16: batch, else: analyze"
4. Execute next function based on rule
5. Repeat until completion
```

---

## 📋 RULES QUICK REFERENCE

### Rule R1: Priority Decision
```
mcp_value <= 5:     Priority = LOW
mcp_value 6-15:     Priority = MID  
mcp_value >= 16:    Priority = HIGH → batch_process_tickets()
```

### Rule R2: Test Type Decision
```
test_type == 'regression':  → Execute regression testing
test_type == 'e2e':         → Execute E2E testing
test_type == 'functional':  → Generate basic tests
```

### Rule R3: Batch Decision
```
priority == 'HIGH':  → batch_process_tickets([similar_tickets])
priority <= 'MID':   → Single ticket processing
```

### Rule R4: Error Handling
```
success == false:    → Log error + Retry OR Fallback
success == true:     → Continue to next function
```

### Rule R5: Completion
```
all_steps_done:      → Generate final report
→ Return complete result with all data
```

---

## 🎯 EXECUTION PSEUDO-CODE FOR AI

```
# AI reads this and executes:

from src.ai_processor import AIProcessor
import json

def ai_execute_with_rules(ticket_id):
    """AI execution following rules from AI_DECISION_FLOW_RULES.md"""
    
    # RULE: Read rules file first
    rules = read_file('AI_DECISION_FLOW_RULES.md')
    
    # STEP 1: Execute first function
    print(f"[STEP 1] AI calling: process_ticket_with_mcp('{ticket_id}')")
    result_1 = AIProcessor.process_ticket_with_mcp(ticket_id)
    
    # RULE R1: Check success first (Rule R4)
    if not result_1.get('success'):
        print("Error! Following Rule R4 error handling...")
        return handle_error(result_1)
    
    mcp_value = result_1['mcp_value']
    print(f"MCP Value: {mcp_value}")
    
    # RULE R1: Classify priority
    if mcp_value >= 16:
        priority = "HIGH"
        print("[DECISION] Rule R1: mcp_value >= 16 → Priority = HIGH")
        print("[DECISION] Rule R3: Priority HIGH → batch_process_tickets()")
        
        # STEP 2: Execute batch
        print(f"[STEP 2] AI calling: batch_process_tickets()")
        result_2 = AIProcessor.batch_process_tickets([ticket_id])
    else:
        priority = "LOW/MID"
        print(f"[DECISION] Rule R1: mcp_value <= 15 → Priority = {priority}")
        print("[DECISION] Rule R2: Check test_type...")
        
        # STEP 2: Execute analysis
        print(f"[STEP 2] AI calling: analyze_and_generate_tests('{ticket_id}')")
        result_2 = AIProcessor.analyze_and_generate_tests(ticket_id)
    
    if not result_2.get('success'):
        print("Error in Step 2! Following Rule R4...")
        return handle_error(result_2)
    
    # RULE R2: Check test type
    test_type = result_2.get('analysis', {}).get('test_type', 'functional')
    
    if test_type == 'regression':
        print(f"[DECISION] Rule R2: test_type == 'regression'")
        print("[STEP 3] AI would execute: Regression testing")
    elif test_type == 'e2e':
        print(f"[DECISION] Rule R2: test_type == 'e2e'")
        print("[STEP 3] AI would execute: E2E testing")
    else:
        print(f"[DECISION] Rule R2: test_type == '{test_type}'")
        print("[STEP 3] AI would execute: Basic testing")
    
    # RULE R5: Completion
    print("\n[COMPLETION] Rule R5: All steps done")
    print("[COMPLETION] Generating final report...")
    
    return {
        'ticket_id': ticket_id,
        'status': 'success',
        'steps': [result_1, result_2],
        'decisions': [
            f"Rule R1: Priority = {priority}",
            f"Rule R2: Test type = {test_type}",
            f"Rule R3: Batch {'enabled' if priority == 'HIGH' else 'disabled'}"
        ]
    }
```

---

## 💡 EXAMPLE EXECUTION FLOWS

### Example 1: Low Value Ticket (KAN-7, value=3)
```
AI reads rules
  ↓
[STEP 1] process_ticket_with_mcp('KAN-7')
  → Returns: {success: true, mcp_value: 3, ...}
  ↓
[DECISION] Rule R1: mcp_value=3 ≤ 15 → Priority = LOW
  ↓
[STEP 2] analyze_and_generate_tests('KAN-7')
  → Returns: {success: true, test_type: 'functional', ...}
  ↓
[DECISION] Rule R2: test_type = 'functional'
  ↓
[STEP 3] Execute basic tests
  ↓
[COMPLETION] Rule R5: Generate report → DONE
```

### Example 2: High Value Ticket (KAN-7, value=18)
```
AI reads rules
  ↓
[STEP 1] process_ticket_with_mcp('KAN-7')
  → Returns: {success: true, mcp_value: 18, ...}
  ↓
[DECISION] Rule R1: mcp_value=18 ≥ 16 → Priority = HIGH
  ↓
[DECISION] Rule R3: Priority HIGH → Execute batch
  ↓
[STEP 2] batch_process_tickets(['KAN-7', 'KAN-8', 'KAN-9'])
  → Returns: {success: true, processed: 3, ...}
  ↓
[COMPLETION] Rule R5: Generate report → DONE
```

### Example 3: Error Handling
```
AI reads rules
  ↓
[STEP 1] process_ticket_with_mcp('INVALID-0')
  → Returns: {success: false, error: '...', ...}
  ↓
[DECISION] Rule R4: success=false → Error handling
  ↓
[ACTION] Log error + Suggest fix
  ↓
[COMPLETION] Return error report → DONE
```

---

## 🎯 CORE CONCEPT

**AI đọc file .md (AI_DECISION_FLOW_RULES.md)**
  ↓
**AI hiểu rules**
  ↓
**AI gọi function từng cái (flow cũ)**
  ↓
**AI check kết quả**
  ↓
**AI đọc rules để quyết định function tiếp theo**
  ↓
**Repeat cho tới completion**

---

## 📝 WHAT AI SHOULD READ BEFORE EXECUTING

1. **File**: `AI_DECISION_FLOW_RULES.md`
2. **Focus on**:
   - Decision Matrix (which function to call based on conditions)
   - Rules R1-R5 (decision logic)
   - Flow diagrams (decision points)
3. **Then execute**: Following those rules

---

## 🚀 INSTRUCTION FOR AI

```
1. Read file: AI_DECISION_FLOW_RULES.md
2. Understand the 5 rules (R1-R5)
3. Execute process_ticket_with_mcp() first
4. Check result against Rule R1
5. Call next function based on rule
6. Continue until Rule R5 completion
7. Return final result with decision trail
```

---

## ✅ SUMMARY

- **What AI does**: Execute functions step by step
- **How AI decides**: Read AI_DECISION_FLOW_RULES.md → Apply rules
- **How AI continues**: Check result → Find matching rule → Call next function
- **When AI stops**: Rule R5 completion condition met

---

**Status**: ✅ Ready for AI execution
**File to read**: `AI_DECISION_FLOW_RULES.md`
**Functions to call**: From `src/ai_processor.py`
**Version**: 1.0.0

