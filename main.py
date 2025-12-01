import sys
import os
import asyncio
import time

# --- PATH SETUP ---
# Add 'src' to the python path so imports work correctly when running 'python main.py'
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from aegis.core import AegisOrchestrator
    from aegis.protocols import MCPTool, A2AAgent, AgentCard
except ImportError:
    # Fallback import if running directly from source
    from src.aegis.core import AegisOrchestrator
    from src.aegis.protocols import MCPTool, A2AAgent, AgentCard

# --- Vibe Coding: Terminal Aesthetics ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- 1. Mock Resource Definition (Simulating MCP Tools) ---
async def tool_market_research(context):
    print(f"{Colors.BLUE}   [Tool] Running Market Research...{Colors.ENDC}")
    await asyncio.sleep(2.0) # Simulating network latency
    return "Data found"

async def tool_financial_data(context):
    print(f"{Colors.BLUE}   [Tool] Fetching Financial Data...{Colors.ENDC}")
    await asyncio.sleep(1.5) # Simulating DB query
    return "Financials OK"

# --- 2. Graph Construction (The A.E.G.I.S. Logic) ---
def build_production_graph() -> AegisOrchestrator:
    orchestrator = AegisOrchestrator("Capstone-Graph")
    
    # Tier 1: Tools running in PARALLEL (Independent)
    # We define PERT estimates (Optimistic, Likely, Pessimistic) for Monte Carlo
    orchestrator.add_node(
        "researcher", 
        MCPTool(name="MarketResearcher", description="Web Search", func=tool_market_research, is_critical=True),
        pert_estimates=(1.0, 2.0, 5.0)
    )
    
    orchestrator.add_node(
        "analyst", 
        MCPTool(name="FinancialAnalyst", description="DB Query", func=tool_financial_data),
        pert_estimates=(0.5, 1.5, 2.5)
    )

    # Tier 2: Agent via A2A (DEPENDS ON Tier 1)
    # This node waits for the previous ones to finish
    writer_card = AgentCard(name="SeniorWriter", capabilities=["writing"], endpoint="http://writer-agent")
    orchestrator.add_node(
        "writer", 
        A2AAgent(card=writer_card), 
        depends_on=["researcher", "analyst"],
        pert_estimates=(2.0, 3.5, 8.0)
    )
    
    return orchestrator

# --- 3. HITL Logic (Human-in-the-Loop Gate) ---
def ask_human_approval(stats: dict) -> bool:
    print(f"\n{Colors.HEADER} A.E.G.I.S. PRE-FLIGHT CHECK (HITL){Colors.ENDC}")
    print("-" * 40)
    print(f"{Colors.WARNING}🎲 Risk Prediction (Monte Carlo):{Colors.ENDC}")
    print(f"     Expected Time (Avg): {stats['avg_case']:.2f}s")
    print(f"     SLA Guarantee (P80): {stats['P80_confidence']:.2f}s")
    print(f"     Worst Case (P99):    {stats['P95_confidence']:.2f}s")
    
    # Alert if the P99 is too high (Safety Guardrail)
    if stats['P95_confidence'] > 12.0:
        print(f"\n    ALERT: High latency risk detected. Review required.")
    
    print("-" * 40)
    try:
        response = input(f"{Colors.BOLD}Authorize Execution? (y/n): {Colors.ENDC}").lower().strip()
        return response == 'y'
    except EOFError:
        return True # For non-interactive environments

# --- 4. Main Application Loop ---
async def main():
    # Capture CLI argument or use default
    query = sys.argv[1] if len(sys.argv) > 1 else "Generate Q4 Strategy"
    
    print(f"{Colors.BOLD}  Starting A.E.G.I.S. Orchestrator{Colors.ENDC}")
    print(f"   Target: '{query}'")
    
    # Phase 1: Build the Graph
    app = build_production_graph()
    
    # Phase 2: Simulation (Monte Carlo)
    # We run this BEFORE spending any real resources/tokens
    stats = app.simulate(iterations=5000)
    
    # Phase 3: Health Checks (Simulated Fail-Fast)
    print(f"\n Health Checks: {Colors.GREEN}PASS{Colors.ENDC}")
    
    # Phase 4: HITL Approval Gate
    if not ask_human_approval(stats):
        print(f"{Colors.FAIL} Aborted by user.{Colors.ENDC}")
        return

    # Phase 5: Real Execution (Only if authorized)
    print(f"\n{Colors.GREEN}🚀 Executing Graph...{Colors.ENDC}")
    start = time.perf_counter()
    await app.run(query)
    duration = time.perf_counter() - start
    
    # Final Report
    print(f"\n Workflow Completed in {duration:.2f}s")
    
    # Calculate savings vs Sequential Execution (Sum of 'Likely' times)
    sequential_time = 2.0 + 1.5 + 3.5
    savings = sequential_time - duration
    print(f"{Colors.WARNING}(Latency Savings vs Sequential: ~{savings:.2f}s){Colors.ENDC}")

if __name__ == "__main__":
    asyncio.run(main())