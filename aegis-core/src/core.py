import asyncio
import networkx as nx
import random
import statistics
from typing import Dict, List, Any
from .protocols import MCPTool, A2AAgent

class AegisOrchestrator:
    def __init__(self, name: str):
        self.name = name
        self.graph = nx.DiGraph()
        self.tasks = {}
        # Latency history for P99 calculation (Rolling Window)
        self._latency_history = {} 

    def add_node(self, id: str, worker: Any, depends_on: List[str] = [], 
                 pert_estimates: tuple = (1, 2, 3)): 
        """
        Registers a node in the DAG.
        pert_estimates: (Optimistic, Likely, Pessimistic) in seconds.
        """
        self.tasks[id] = worker
        self.graph.add_node(id, pert=pert_estimates)
        self._latency_history[id] = [] # Initialize history
        
        for dep in depends_on:
            self.graph.add_edge(dep, id)

    def simulate(self, iterations: int = 10000) -> Dict[str, float]:
        """
        Executes Monte Carlo Simulation to predict SLA (P80).
        """
        print(f" Running Monte Carlo Simulation ({iterations} iterations)...")
        simulated_durations = []

        for _ in range(iterations):
            temp_graph = self.graph.copy()
            for node in temp_graph.nodes:
                O, M, P = temp_graph.nodes[node]['pert']
                # Triangular Distribution (Standard in PM/SRE)
                duration = random.triangular(O, P, M)
                temp_graph.nodes[node]['duration'] = duration

            path_duration = nx.dag_longest_path_length(
                temp_graph, 
                weight=lambda u, v, d: temp_graph.nodes[u]['duration']
            )
            # Adjustment to include the last node
            last_node = list(nx.topological_sort(temp_graph))[-1]
            total_duration = path_duration + temp_graph.nodes[last_node]['duration']
            simulated_durations.append(total_duration)

        return {
            "best_case": min(simulated_durations),
            "worst_case": max(simulated_durations),
            "avg_case": statistics.mean(simulated_durations),
            "P50_confidence": statistics.median(simulated_durations),
            "P80_confidence": statistics.quantiles(simulated_durations, n=100)[79],
            "P95_confidence": statistics.quantiles(simulated_durations, n=100)[94]
        }

    def _calculate_dynamic_timeout(self, node_id: str) -> float:
        """
        Implements 'Adaptive Capacity Control' logic.
        If history exists, uses P99 + Jitter. Otherwise, uses PERT Pessimistic (P) value.
        """
        history = self._latency_history.get(node_id, [])
        
        if len(history) > 10:
            # If we have real data, calculate real P99
            p99 = statistics.quantiles(history, n=100)[98]
            return p99 * 1.2 # +20% safety margin (Jitter)
        else:
            # Cold Start: Use human-defined Pessimistic (P) estimate
            return self.graph.nodes[node_id]['pert'][2]

    async def _run_node(self, node_id: str, context: Dict):
        """
        Executes a node with Adaptive Timeouts (SRE Pattern).
        """
        worker = self.tasks[node_id]
        timeout = self._calculate_dynamic_timeout(node_id)
        
        print(f"     [Adaptive Timeout] {node_id} limit set to {timeout:.2f}s")

        try:
            # Security wrapper with asyncio.wait_for
            result = await asyncio.wait_for(self._execute_worker(worker, context), timeout=timeout)
            
            # Record metric for future P99 calculations (Mock)
            # In real production, this would be stored in a TimeSeries DB
            self._latency_history[node_id].append(timeout * 0.8) 
            
            return result
            
        except asyncio.TimeoutError:
            print(f"    [FAIL-FAST] {node_id} exceeded timeout ({timeout:.2f}s). Killing process.")
            return None # Or raise custom exception

    async def _execute_worker(self, worker, context):
        """Helper for MCP/A2A polymorphism"""
        if isinstance(worker, MCPTool):
            return await worker.execute(context=context)
        elif isinstance(worker, A2AAgent):
            return await worker.ask(context.get("query", ""))
        return None

    async def run(self, query: str):
        """
        Orchestration Engine: Parallel Execution via Topological Sort.
        """
        context = {"query": query}
        results = {}
        
        for generation in nx.topological_generations(self.graph):
            print(f"\n⚡ [CPM] Executing parallel generation: {generation}")
            
            coroutines = [self._run_node(node, context) for node in generation]
            gen_results = await asyncio.gather(*coroutines)
            
            for node, res in zip(generation, gen_results):
                if res is None:
                    print(f"    Warning: Node {node} failed or timed out.")
                results[node] = res

        return results