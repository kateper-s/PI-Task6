import sys
sys.path.insert(0, '.')
from func import WeierstrassTheorem
import numpy as np

def test_basic_functionality():
    """Проверка базовой функциональности"""
    wt = WeierstrassTheorem(f_str="x**2", a=-1, b=1)
    results = wt.find_extrema_on_interval()
    
    assert results['theorem_applies'] == True
    assert abs(results['global_min']['y'] - 0) < 0.001
    assert abs(results['global_max']['y'] - 1) < 0.001
    print("✓ Базовый тест пройден")

def test_continuity_check():
    """Проверка определения непрерывности"""
    wt = WeierstrassTheorem(f_str="x**2", a=-1, b=1)
    assert wt.check_continuity() == True
    print("✓ Проверка непрерывности пройдена")

if __name__ == "__main__":
    test_basic_functionality()
    test_continuity_check()
    print("\n✅ Все тесты выполнены успешно!")