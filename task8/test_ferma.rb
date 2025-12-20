require_relative 'ferma.rb'
require 'test/unit'

class TestFerma < Test::Unit::TestCase
  def setup
    @result = FermaTheorem.prove
  end
  
  def test_proof_exists
    assert @result[:proved], "Теорема должна быть доказана"
  end
  
  def test_prover_name
    assert_equal "Andrew Wiles", @result[:prover]
  end
  
  def test_proof_year
    assert_equal 1994, @result[:year]
  end
  
  def test_theorem_name
    assert_equal "Fermat's Last Theorem", @result[:theorem]
  end
  
  def test_has_page_count
    assert @result[:pages] > 0, "Должно быть указано количество страниц"
  end
end

if __FILE__ == $0
  Test::Unit::AutoRunner.run
end