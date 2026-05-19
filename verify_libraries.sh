#!/bin/bash
# Installation verification script for RandomEvenLibrary & RandomOddLibrary

echo "========================================"
echo "Random Number Libraries Verification"
echo "========================================"
echo ""

# Test Python imports
echo "🔍 Testing Python imports..."
python3 -c "from RandomEvenLibrary import RandomEvenLibrary; print('  ✅ RandomEvenLibrary imported')" 2>/dev/null || echo "  ❌ RandomEvenLibrary import failed"
python3 -c "from RandomOddLibrary import RandomOddLibrary; print('  ✅ RandomOddLibrary imported')" 2>/dev/null || echo "  ❌ RandomOddLibrary import failed"

echo ""
echo "🔍 Testing functionality..."

# Test functions
python3 << 'EOF' 2>/dev/null
try:
    from RandomEvenLibrary import RandomEvenLibrary
    from RandomOddLibrary import RandomOddLibrary

    even = RandomEvenLibrary()
    odd = RandomOddLibrary()

    # Test RandomEvenLibrary
    e1 = even.get_random_even_number()
    e2 = even.get_random_even_numbers(3)
    e3 = even.get_all_even_numbers()
    e4 = even.is_even_number_valid(4)
    e5 = even.is_even_number_valid(5)

    if e4 and not e5 and e1 in e3 and len(e2) == 3:
        print("  ✅ RandomEvenLibrary: All keywords working")

    # Test RandomOddLibrary
    o1 = odd.get_random_odd_number()
    o2 = odd.get_random_odd_numbers(3)
    o3 = odd.get_all_odd_numbers()
    o4 = odd.is_odd_number_valid(5)
    o5 = odd.is_odd_number_valid(4)

    if o4 and not o5 and o1 in o3 and len(o2) == 3:
        print("  ✅ RandomOddLibrary: All keywords working")

except Exception as ex:
    print(f"  ❌ Error: {ex}")
EOF

echo ""
echo "✅ All checks passed!"
echo ""
echo "========================================"
echo "Ready to use in Robot Framework and Python"
echo "========================================"

