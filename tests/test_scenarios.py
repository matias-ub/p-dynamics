"""Tests for scenarios loading from Supabase."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from p_dynamics.lib.scenarios import get_scenarios


async def test_get_scenarios():
    """Test function para verificar la carga de escenarios."""
    print("=" * 60)
    print("Testing get_scenarios() con pack 'cotidiano-v1'")
    print("=" * 60)
    
    try:
        scenarios = await get_scenarios("cotidiano-v1")
        print(f"\n✓ Cargados {len(scenarios)} escenarios exitosamente\n")
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['title']} (key: {scenario['key']})")
            print(f"   Descripción: {scenario['description']}")
            print(f"   Orden: {scenario['order_num']}")
            print(f"   Opciones: {len(scenario['options'])}")
            
            # Mostrar las opciones
            for option in scenario['options']:
                tags_str = ", ".join(f"{k}:{v}" for k, v in option.get('tags', {}).items())
                print(f"      [{option['key']}] {option['text']}")
                if tags_str:
                    print(f"          Tags: {tags_str}")
            print()
        
        print("=" * 60)
        print("Test completado exitosamente")
        print("=" * 60)
        return True
        
    except ValueError as e:
        print(f"\n✗ Error de validación: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_pack_not_found():
    """Test para verificar manejo de errores cuando el pack no existe."""
    print("\n" + "=" * 60)
    print("Testing error handling con pack inexistente")
    print("=" * 60)
    
    try:
        await get_scenarios("pack-inexistente")
        print("✗ Debería haber lanzado ValueError")
        return False
    except ValueError as e:
        print(f"✓ ValueError capturado correctamente: {e}")
        return True
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


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
    sys.exit(0 if success else 1)
