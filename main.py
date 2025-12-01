import asyncio
import sys
import time
from aegis.core import AegisOrchestrator
from aegis.protocols import MCPTool, A2AAgent, AgentCard

# --- Configuración de "Vibe" (Colores) ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# ... (Las definiciones de herramientas build_graph se mantienen igual) ...
# ... (Copia aquí las funciones tool_market_research, tool_financial_data y build_graph del mensaje anterior) ...

# --- NUEVO: Función HITL (Human-in-the-Loop) ---
def ask_human_approval(stats: dict, graph_topology: list) -> bool:
    """
    Presenta los datos de riesgo al humano y pide autorización.
    """
    print(f"\n{Colors.HEADER} A.E.G.I.S. PRE-FLIGHT CHECK (HITL){Colors.ENDC}")
    print("-" * 40)
    
    # 1. Mostrar Topología (El Plan)
    print(f"{Colors.BLUE} Plan de Ejecución:{Colors.ENDC}")
    print(f"   Nodos: {len(graph_topology)} agentes/herramientas")
    print(f"   Flujo: {graph_topology}")

    # 2. Mostrar Predicción Monte Carlo (El Riesgo)
    print(f"\n{Colors.WARNING} Predicción de Riesgo (Monte Carlo):{Colors.ENDC}")
    print(f"     Tiempo Esperado (P50): {stats['P50_confidence']:.2f}s")
    print(f"     SLA Garantizado (P80): {stats['P80_confidence']:.2f}s")
    
    if stats['worst_case'] > 8.0:
        print(f"     ALERTA: El peor caso ({stats['worst_case']:.2f}s) supera el umbral de seguridad.")
    
    print("-" * 40)
    response = input(f"{Colors.BOLD}¿Autorizar ejecución? (y/n): {Colors.ENDC}").lower().strip()
    return response == 'y'

# --- Entry Point Actualizado ---
async def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "Generar Estrategia Q4"
    
    print(f"{Colors.BOLD}  Iniciando A.E.G.I.S. Orchestrator{Colors.ENDC}")
    
    # 1. Construcción (Planning)
    app = build_graph(query)
    
    # 2. Simulación (Monte Carlo)
    # Hacemos esto ANTES de gastar dinero/recursos reales
    stats = app.simulate(iterations=5000)
    
    # 3. Health Check (Simulado aquí, en real chequearía endpoints)
    # Si falla aquí, ni preguntamos al humano (Fail-Fast)
    print(f"\n Ejecutando Health Checks... {Colors.GREEN}OK{Colors.ENDC}")

    # 4. HITL (Human-in-the-Loop) -> NUEVO PASO CRÍTICO
    # Obtenemos la topología para mostrarla
    topology = list(app.graph.nodes)
    if not ask_human_approval(stats, topology):
        print(f"\n{Colors.FAIL} Ejecución cancelada por el operador.{Colors.ENDC}")
        sys.exit(0)

    # 5. Ejecución Real (Solo si pasó el HITL)
    print(f"\n{Colors.GREEN} Autorización recibida. Ejecutando grafo...{Colors.ENDC}")
    start_time = time.perf_counter()
    results = await app.run(query)
    end_time = time.perf_counter()
    
    print(f"\n Completado en {end_time - start_time:.2f}s")
    # print(results) # Opcional: mostrar resultados crudos

if __name__ == "__main__":
    asyncio.run(main())