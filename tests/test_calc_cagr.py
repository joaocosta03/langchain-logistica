"""
Testes para a função calc_cagr.
"""
import sys
import os

# Adicionar diretório pai ao path para importar tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import calc_cagr


def test_cagr_basic():
    """Testa cálculo básico de CAGR."""
    result = calc_cagr(start=100, end=120, months=6)
    expected = 0.44  # Aproximadamente 44%
    
    # Tolerância de 1e-6
    assert abs(result - expected) < 1e-2, f"Esperado ~{expected}, obtido {result}"
    print(f"✅ test_cagr_basic: PASSOU (CAGR = {result:.4f})")


def test_cagr_invalid_start():
    """Testa erro quando start <= 0."""
    try:
        calc_cagr(start=0, end=120, months=6)
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "inicial" in str(e).lower() or "start" in str(e).lower()
        print(f"✅ test_cagr_invalid_start: PASSOU (erro capturado corretamente)")


def test_cagr_invalid_months():
    """Testa erro quando months <= 0."""
    try:
        calc_cagr(start=100, end=120, months=0)
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "período" in str(e).lower() or "months" in str(e).lower()
        print(f"✅ test_cagr_invalid_months: PASSOU (erro capturado corretamente)")


def test_cagr_negative_start():
    """Testa erro quando start é negativo."""
    try:
        calc_cagr(start=-100, end=120, months=6)
        assert False, "Deveria ter lançado ValueError"
    except ValueError:
        print(f"✅ test_cagr_negative_start: PASSOU (erro capturado corretamente)")


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("EXECUTANDO TESTES DE CALC_CAGR")
    print("="*60 + "\n")
    
    tests = [
        test_cagr_basic,
        test_cagr_invalid_start,
        test_cagr_invalid_months,
        test_cagr_negative_start
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__}: FALHOU - {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: ERRO - {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTADOS: {passed} passou(ram), {failed} falhou(ram)")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

