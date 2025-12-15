class FermaTheorem
  def self.prove
    puts "=" * 50
    puts "Доказательство Великой теоремы Ферма"
    puts "=" * 50
    puts "Уравнение: a^n + b^n = c^n"
    puts "Утверждение: Нет целочисленных решений при n > 2"
    puts "\nКраткое доказательство:"
    puts "1. Предположим, ∃ целые a, b, c, n>2: a^n + b^n = c^n"
    puts "2. Рассмотрим эллиптическую кривую E: y² = x(x - a^n)(x + b^n)"
    puts "3. Применяем теорему Рибета о модулярности"
    puts "4. Используем гипотезу Таниямы-Шимуры (доказана Уайлсом)"
    puts "5. Получаем противоречие с теоремой Фальтингса"
    puts "6. ∴ Предположение ложно"
    puts "\nПолное доказательство заняло 100+ страниц"
    puts "и 7 лет работы Эндрю Уайлса (1994)"
    puts "=" * 50
    
    return {
      theorem: "Fermat's Last Theorem",
      proved: true,
      year: 1994,
      prover: "Andrew Wiles",
      pages: 100
    }
  end
end

if __FILE__ == $0
  FermaTheorem.prove
end