import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import sympy as sp
from typing import Tuple, Optional

class WeierstrassTheorem:
    """
    Класс для демонстрации теоремы Вейерштрасса о достижении экстремумов
    """
    
    def __init__(self, f_str: str = "x**3 - 6*x**2 + 9*x + 2", 
                 a: float = 0, b: float = 4):
        """
        Инициализация с функцией и отрезком
        
        Args:
            f_str: строка с функцией f(x)
            a: начало отрезка
            b: конец отрезка
        """
        self.x = sp.symbols('x')
        self.a = a
        self.b = b
        
        try:
            self.f_sym = sp.sympify(f_str)
        except:
            raise ValueError(f"Не удалось распознать функцию: {f_str}")
        
        self.f_np = sp.lambdify(self.x, self.f_sym, 'numpy')
        
        self.f_prime_sym = sp.diff(self.f_sym, self.x)
        self.f_double_prime_sym = sp.diff(self.f_prime_sym, self.x)
        self.f_prime_np = sp.lambdify(self.x, self.f_prime_sym, 'numpy')
        self.f_double_prime_np = sp.lambdify(self.x, self.f_double_prime_sym, 'numpy')
    
    def check_continuity(self, num_points: int = 10000) -> bool:
        """
        Проверка непрерывности функции на отрезке [a, b]
        
        Args:
            num_points: количество точек для проверки
            
        Returns:
            bool: True если функция непрерывна
        """
        x_vals = np.linspace(self.a, self.b, num_points)
        
        try:
            y_vals = self.f_np(x_vals)
            if np.any(np.isnan(y_vals)) or np.any(np.isinf(y_vals)):
                return False
            
            dy = np.abs(np.diff(y_vals))
            if np.max(dy) > 100 * np.mean(dy): 
                return False
                
            return True
        except Exception as e:
            print(f"Ошибка при проверке непрерывности: {e}")
            return False
    
    def find_extremum_points(self) -> Tuple[list, list]:
        """
        Нахождение точек экстремума внутри отрезка
        
        Returns:
            Критические точки и точки перегиба
        """
        critical_points = []
        
        try:
            solutions = sp.solve(self.f_prime_sym, self.x)
            
            for sol in solutions:
                try:
                    if sol.is_real:
                        x_val = float(sol)
                        if self.a < x_val < self.b:  
                            critical_points.append(x_val)
                except:
                    continue
        except:
            pass
        
        if not critical_points:
            x_test = np.linspace(self.a, self.b, 1000)
            f_prime_vals = self.f_prime_np(x_test)
            
            sign_changes = []
            for i in range(len(x_test) - 1):
                if f_prime_vals[i] == 0:
                    critical_points.append(x_test[i])
                elif f_prime_vals[i] * f_prime_vals[i + 1] < 0:
                    left, right = x_test[i], x_test[i + 1]
                    for _ in range(20):  
                        mid = (left + right) / 2
                        if self.f_prime_np(left) * self.f_prime_np(mid) <= 0:
                            right = mid
                        else:
                            left = mid
                    critical_points.append((left + right) / 2)
        
        inflection_points = []
        try:
            inflection_solutions = sp.solve(self.f_double_prime_sym, self.x)
            for sol in inflection_solutions:
                try:
                    if sol.is_real:
                        x_val = float(sol)
                        if self.a < x_val < self.b:
                            inflection_points.append(x_val)
                except:
                    continue
        except:
            pass
        
        return sorted(critical_points), sorted(inflection_points)
    
    def find_extrema_on_interval(self) -> dict:
        """
        Нахождение абсолютных максимума и минимума на отрезке [a, b]
        
        Returns:
            Словарь с информацией об экстремумах
        """
        if not self.check_continuity():
            raise ValueError("Функция не является непрерывной на заданном отрезке")
        
        f_a = self.f_np(self.a)
        f_b = self.f_np(self.b)
        
        critical_points, inflection_points = self.find_extremum_points()
        
        candidates = [self.a, self.b] + critical_points
        candidate_values = [(x, self.f_np(x)) for x in candidates]
        
        min_point = min(candidate_values, key=lambda x: x[1])
        max_point = max(candidate_values, key=lambda x: x[1])
        
        extreme_info = []
        for x in critical_points:
            y = self.f_np(x)
            f_double = self.f_double_prime_np(x)
            
            if f_double > 0:
                extreme_type = "локальный минимум"
            elif f_double < 0:
                extreme_type = "локальный максимум"
            else:
                extreme_type = "точка перегиба или седловая точка"
            
            extreme_info.append({
                'x': x,
                'y': y,
                'type': extreme_type,
                'is_global_min': abs(y - min_point[1]) < 1e-10,
                'is_global_max': abs(y - max_point[1]) < 1e-10
            })
        
        return {
            'interval': [self.a, self.b],
            'function': str(self.f_sym),
            'is_continuous': True,
            'global_min': {'x': min_point[0], 'y': min_point[1]},
            'global_max': {'x': max_point[0], 'y': max_point[1]},
            'endpoints': {'a': (self.a, f_a), 'b': (self.b, f_b)},
            'critical_points': extreme_info,
            'inflection_points': inflection_points,
            'theorem_applies': True
        }
    
    def visualize(self, results: dict):
        """
        Визуализация теоремы Вейерштрасса
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Теорема Вейерштрасса: f(x) = {results["function"]} на [{self.a}, {self.b}]', 
                    fontsize=14, fontweight='bold')
        
        x_vals = np.linspace(self.a - 0.5, self.b + 0.5, 1000)
        y_vals = self.f_np(x_vals)
        
        ax = axes[0, 0]
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
        ax.axvspan(self.a, self.b, alpha=0.2, color='gray', label='Отрезок [a, b]')
        
        ax.scatter(results['global_min']['x'], results['global_min']['y'], 
                  color='green', s=200, zorder=5, 
                  label=f'Глоб. минимум: ({results["global_min"]["x"]:.3f}, {results["global_min"]["y"]:.3f})')
        ax.scatter(results['global_max']['x'], results['global_max']['y'], 
                  color='red', s=200, zorder=5,
                  label=f'Глоб. максимум: ({results["global_max"]["x"]:.3f}, {results["global_max"]["y"]:.3f})')
        
        ax.scatter(self.a, results['endpoints']['a'][1], color='orange', s=100, 
                  label=f'f(a) = {results["endpoints"]["a"][1]:.3f}')
        ax.scatter(self.b, results['endpoints']['b'][1], color='purple', s=100,
                  label=f'f(b) = {results["endpoints"]["b"][1]:.3f}')
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Теорема Вейерштрасса: функция достигает экстремумов')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.2)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.2)
        
        ax = axes[0, 1]
        f_prime_vals = self.f_prime_np(x_vals)
        ax.plot(x_vals, f_prime_vals, 'r-', linewidth=2, label="f'(x)")
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        
        for cp in results['critical_points']:
            ax.scatter(cp['x'], 0, color='orange', s=100, zorder=5)
            ax.annotate(f"x={cp['x']:.3f}", 
                       xy=(cp['x'], 0), 
                       xytext=(0, 20),
                       textcoords='offset points',
                       ha='center',
                       fontsize=9)
        
        ax.set_xlabel('x')
        ax.set_ylabel("f'(x)")
        ax.set_title('Производная функции (f\'(x)=0 в критических точках)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        ax = axes[1, 0]
        x_segment = np.linspace(self.a, self.b, 500)
        y_segment = self.f_np(x_segment)
        
        ax.plot(x_segment, y_segment, 'b-', linewidth=3)
        
        ax.axhline(y=results['global_min']['y'], color='green', linestyle=':', alpha=0.7)
        ax.axhline(y=results['global_max']['y'], color='red', linestyle=':', alpha=0.7)
        
        ax.fill_between(x_segment, y_segment, results['global_min']['y'], 
                       where=(y_segment >= results['global_min']['y']), 
                       alpha=0.3, color='blue')
        
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Функция на отрезке [{self.a}, {self.b}]')
        ax.grid(True, alpha=0.3)
        
        ax = axes[1, 1]
        ax.axis('off')
        
        info_text = (
            f"ТЕОРЕМА ВЕЙЕРШТРАССА\n"
            f"====================\n"
            f"Функция: f(x) = {results['function']}\n"
            f"Отрезок: [{self.a}, {self.b}]\n"
            f"Непрерывность: {'ДА ✓' if results['is_continuous'] else 'НЕТ ✗'}\n\n"
            f"ГЛОБАЛЬНЫЕ ЭКСТРЕМУМЫ:\n"
            f"• Минимум: f({results['global_min']['x']:.4f}) = {results['global_min']['y']:.4f}\n"
            f"• Максимум: f({results['global_max']['x']:.4f}) = {results['global_max']['y']:.4f}\n\n"
            f"ЗНАЧЕНИЯ НА КОНЦАХ:\n"
            f"• f({self.a}) = {results['endpoints']['a'][1]:.4f}\n"
            f"• f({self.b}) = {results['endpoints']['b'][1]:.4f}\n"
        )
        
        if results['critical_points']:
            info_text += f"\nКРИТИЧЕСКИЕ ТОЧКИ:\n"
            for cp in results['critical_points']:
                info_text += f"• x={cp['x']:.4f}: {cp['type']} (y={cp['y']:.4f})\n"
                if cp['is_global_min']:
                    info_text += "  ← ГЛОБАЛЬНЫЙ МИНИМУМ\n"
                if cp['is_global_max']:
                    info_text += "  ← ГЛОБАЛЬНЫЙ МАКСИМУМ\n"
        
        if results['inflection_points']:
            info_text += f"\nТОЧКИ ПЕРЕГИБА:\n"
            for ip in results['inflection_points']:
                info_text += f"• x={ip:.4f}\n"
        
        ax.text(0.1, 0.95, info_text, transform=ax.transAxes, 
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        return fig
    
    def print_detailed_report(self, results: dict):
        """
        Вывод подробного отчета
        """
        print("=" * 70)
        print("ТЕОРЕМА ВЕЙЕРШТРАССА - ДЕТАЛЬНЫЙ ОТЧЕТ")
        print("=" * 70)
        
        print(f"\nФункция: f(x) = {results['function']}")
        print(f"Отрезок исследования: [{results['interval'][0]}, {results['interval'][1]}]")
        print(f"Непрерывна на отрезке: {'ДА' if results['is_continuous'] else 'НЕТ'}")
        
        if not results['theorem_applies']:
            print("\n❌ Теорема Вейерштрасса НЕ ПРИМЕНИМА (функция не непрерывна)")
            return
        
        print("\n" + "=" * 70)
        print("РЕЗУЛЬТАТЫ:")
        print("=" * 70)
        
        print(f"\n1. ГЛОБАЛЬНЫЙ МИНИМУМ на отрезке:")
        print(f"   f({results['global_min']['x']:.6f}) = {results['global_min']['y']:.6f}")
        print(f"   Расположение: {'внутри отрезка' if self.a < results['global_min']['x'] < self.b else 'на конце отрезка'}")
        
        print(f"\n2. ГЛОБАЛЬНЫЙ МАКСИМУМ на отрезке:")
        print(f"   f({results['global_max']['x']:.6f}) = {results['global_max']['y']:.6f}")
        print(f"   Расположение: {'внутри отрезка' if self.a < results['global_max']['x'] < self.b else 'на конце отрезка'}")
        
        print(f"\n3. ЗНАЧЕНИЯ НА КОНЦАХ ОТРЕЗКА:")
        print(f"   f({self.a}) = {results['endpoints']['a'][1]:.6f}")
        print(f"   f({self.b}) = {results['endpoints']['b'][1]:.6f}")
        
        if results['critical_points']:
            print(f"\n4. КРИТИЧЕСКИЕ ТОЧКИ (f'(x)=0):")
            for i, cp in enumerate(results['critical_points'], 1):
                print(f"   {i}. x = {cp['x']:.6f}")
                print(f"      f(x) = {cp['y']:.6f}")
                print(f"      Тип: {cp['type']}")
                if cp['is_global_min']:
                    print(f"      ★ ЯВЛЯЕТСЯ ГЛОБАЛЬНЫМ МИНИМУМОМ")
                if cp['is_global_max']:
                    print(f"      ★ ЯВЛЯЕТСЯ ГЛОБАЛЬНЫМ МАКСИМУМОМ")
        
        print(f"\n" + "=" * 70)
        print("ВЫВОД: Теорема Вейерштрасса подтверждена ✓")
        print(f"       Непрерывная функция достигает своих экстремальных значений")
        print(f"       на замкнутом ограниченном отрезке [{self.a}, {self.b}]")
        print("=" * 70)


def main():
    """Основная функция с примерами"""
    
    print("\n" + "="*70)
    print("ПРИМЕР 1: Кубическая функция")
    print("="*70)
    
    wt1 = WeierstrassTheorem(
        f_str="x**3 - 6*x**2 + 9*x + 2",
        a=0, b=4
    )
    
    results1 = wt1.find_extrema_on_interval()
    wt1.print_detailed_report(results1)
    fig1 = wt1.visualize(results1)
    
    # Пример 2: Тригонометрическая функция
    print("\n\n" + "="*70)
    print("ПРИМЕР 2: Синусоида с косинусом")
    print("="*70)
    
    wt2 = WeierstrassTheorem(
        f_str="sin(x) + 0.5*cos(2*x)",
        a=0, b=2*np.pi
    )
    
    results2 = wt2.find_extrema_on_interval()
    wt2.print_detailed_report(results2)
    fig2 = wt2.visualize(results2)
    
    print("\n\n" + "="*70)
    print("ПРИМЕР 3: Функция с разрывом")
    print("="*70)
    
    def discontinuous_func(x):
        return np.where(x < 2, x**2, x**2 + 10)
    
    print("Для функции с разрывом теорема Вейерштрасса не применима!")
    
    plt.show()
    
    return results1, results2


if __name__ == "__main__":
    results1, results2 = main()
    
    print("\n" + "="*70)
    print("СОБСТВЕННЫЙ ПРИМЕР")
    print("="*70)
    
    user_function = input("Введите свою функцию f(x) (например, 'x**2*sin(x)'): ") or "x**2*sin(x)"
    user_a = float(input(f"Введите начало отрезка a (по умолчанию 0): ") or "0")
    user_b = float(input(f"Введите конец отрезка b (по умолчанию 5): ") or "5")
    
    try:
        user_wt = WeierstrassTheorem(f_str=user_function, a=user_a, b=user_b)
        user_results = user_wt.find_extrema_on_interval()
        user_wt.print_detailed_report(user_results)
        user_fig = user_wt.visualize(user_results)
        plt.show()
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Проверьте правильность ввода функции и границ отрезка")