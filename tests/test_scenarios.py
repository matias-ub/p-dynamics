"""Tests for scenarios loading from Supabase."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from p_dynamics.lib.scenarios import get_scenarios


async def test_get_scenarios():
    """Test para verificar la carga de escenarios desde Supabase."""
    print("\n[TEST] get_scenarios() con pack 'cotidiano-v1'")
    
    # Cargar escenarios
    scenarios = await get_scenarios("cotidiano-v1")
    
    # Verificaciones básicas
    assert scenarios is not None, "Scenarios no debería ser None"
    assert isinstance(scenarios, list), "Scenarios debería ser una lista"
    assert len(scenarios) > 0, "Debería haber al menos un escenario"
    
    print(f"  ✓ Cargados {len(scenarios)} escenarios")
    
    # Verificar estructura de cada escenario
    for scenario in scenarios:
        # Verificar que tiene todos los campos requeridos
        assert "key" in scenario, f"Escenario debe tener 'key'"
        assert "title" in scenario, f"Escenario debe tener 'title'"
        assert "description" in scenario, f"Escenario debe tener 'description'"
        assert "order_num" in scenario, f"Escenario debe tener 'order_num'"
        assert "options" in scenario, f"Escenario debe tener 'options'"
        
        # Verificar tipos
        assert isinstance(scenario["key"], str), "key debe ser string"
        assert isinstance(scenario["title"], str), "title debe ser string"
        assert isinstance(scenario["description"], str), "description debe ser string"
        assert isinstance(scenario["order_num"], int), "order_num debe ser int"
        assert isinstance(scenario["options"], list), "options debe ser lista"
        
        # Verificar que tiene opciones
        assert len(scenario["options"]) > 0, f"Escenario '{scenario['key']}' debe tener opciones"
        
        # Verificar estructura de opciones
        for option in scenario["options"]:
            assert "key" in option, "Opción debe tener 'key'"
            assert "text" in option, "Opción debe tener 'text'"
            assert "tags" in option, "Opción debe tener 'tags'"
            assert "order_num" in option, "Opción debe tener 'order_num'"
            assert "is_positive" in option, "Opción debe tener 'is_positive'"
            
            # Verificar tipos de opciones
            assert isinstance(option["key"], str), "option.key debe ser string"
            assert isinstance(option["text"], str), "option.text debe ser string"
            assert isinstance(option["tags"], dict), "option.tags debe ser dict"
            assert isinstance(option["order_num"], int), "option.order_num debe ser int"
            assert isinstance(option["is_positive"], bool), "option.is_positive debe ser bool"
    
    print(f"  ✓ Estructura validada correctamente")
    
    # Verificar ordenamiento
    order_nums = [s["order_num"] for s in scenarios]
    assert order_nums == sorted(order_nums), "Escenarios deben estar ordenados por order_num"
    print(f"  ✓ Escenarios ordenados correctamente")


async def test_pack_not_found():
    """Test para verificar manejo de errores cuando el pack no existe."""
    print("\n[TEST] Manejo de errores con pack inexistente")
    
    error_raised = False
    try:
        await get_scenarios("pack-inexistente-12345")
    except ValueError as e:
        error_raised = True
        assert "no encontrado" in str(e).lower(), "Mensaje de error debe indicar que no se encontró"
        print(f"  ✓ ValueError lanzado correctamente: {e}")
    
    assert error_raised, "Debería lanzar ValueError cuando el pack no existe"


async def test_scenarios_have_unique_keys():
    """Test para verificar que los escenarios tienen keys únicos."""
    print("\n[TEST] Escenarios con keys únicos")
    
    scenarios = await get_scenarios("cotidiano-v1")
    keys = [s["key"] for s in scenarios]
    SUITE DE TESTS PARA SCENARIOS")
    print("=" * 70)
    
    tests = [
        ("Cargar escenarios", test_get_scenarios),
        ("Pack inexistente", test_pack_not_found),
        ("Keys únicos de escenarios", test_scenarios_have_unique_keys),
        ("Keys únicos de opciones", test_options_have_unique_keys_per_scenario),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            await test_func()
            passed += 1
            print(f"  ✓ {test_name}: PASSED")
        except AssertionError as e:
            failed += 1
            print(f"  ✗ {test_name}: FAILED - {e}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {test_name}: ERROR - {e}")
            import traceback
            traceback.print_exc()
    
    # Resumen
    print("\n" + "=" * 70)
    total = passed + failed
    print(f" RESUMEN: {passed}/{total} tests pasados")
    if failed > 0:
        print(f"          {failed}/{total} tests fallaron")
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1

async def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n" + "=" * 70)
    print(" EJECUTANDO SUITE DE TESTS PARA SCENARIOS")
    print("=" * 70 + "\n")
    
    results = []
    
    # Test 1: Cargar escenarios exitosamente
    results.append(await test_get_scenarios())
    
    # Test 2: Error handling
    results.append(await test_pack_not_found())
    
    # Resumen
    print("\n" + "=" * 70)
    print(f" RESUMEN: {sum(results)}/{len(results)} tests pasados")
    print("=" * 70 + "\n")
    
    return all(results)


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    if not success:
        raise RuntimeError("One or more tests failed in run_all_tests()")
