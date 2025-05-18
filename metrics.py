import time
from collections import defaultdict
import csv
import os

class PathfindingMetrics:
    def __init__(self):
        self.metrics = defaultdict(list)
        
    def measure_algorithm(self, algorithm_name, algorithm_func, start, goal, *args):
        """
        Mede o desempenho de um algoritmo de pathfinding
        
        Args:
            algorithm_name (str): Nome do algoritmo (A* ou Bellman-Ford)
            algorithm_func (callable): Função do algoritmo
            start (tuple): Posição inicial
            goal (tuple): Posição final
            *args: Argumentos adicionais para o algoritmo
        """
        # Mede tempo de execução
        start_time = time.time()
        path = algorithm_func(start, goal, *args)
        execution_time = time.time() - start_time
        
        # Coleta métricas
        self.metrics[f"{algorithm_name}_time"].append(execution_time)
        self.metrics[f"{algorithm_name}_path_length"].append(len(path) if path else 0)
        
        return path

    def record_score(self, algorithm_name, score):
        """
        Registra a pontuação obtida com um determinado algoritmo
        
        Args:
            algorithm_name (str): Nome do algoritmo (A* ou Bellman-Ford)
            score (float): Pontuação obtida
        """
        self.metrics[f"{algorithm_name}_score"].append(score)

    def save_metrics(self, algorithm_name, filename):
        """
        Salva as métricas de um algoritmo específico em um arquivo CSV (modo append)
        
        Args:
            algorithm_name (str): Nome do algoritmo (A* ou Bellman-Ford)
            filename (str): Nome do arquivo CSV a ser salvo
        """
        # Verifica se o arquivo já existe
        file_exists = os.path.isfile(filename)
        
        # Obtém o último número de execução do arquivo existente
        last_execution = 0
        if file_exists:
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Pula o cabeçalho
                for row in reader:
                    if row:  # Verifica se a linha não está vazia
                        last_execution = max(last_execution, int(row[0]))
        
        # Abre o arquivo em modo append
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Se o arquivo não existir, escreve o cabeçalho
            if not file_exists:
                writer.writerow(['Execution', 'Time', 'Path Length', 'Score'])
            
            # Pega o número de execuções desta sessão
            executions = len(self.metrics[f"{algorithm_name}_time"])
            
            # Para cada execução, escreve uma linha com os dados
            for i in range(executions):
                time_value = self.metrics[f"{algorithm_name}_time"][i]
                path_length = self.metrics[f"{algorithm_name}_path_length"][i]
                score = self.metrics[f"{algorithm_name}_score"][i] if i < len(self.metrics[f"{algorithm_name}_score"]) else 0
                
                # Incrementa o número da execução a partir do último valor
                execution_number = last_execution + i + 1
                writer.writerow([execution_number, f"{time_value:.4f}", path_length, score])
            
        print(f"Métricas do {algorithm_name} adicionadas em {filename}")
            
    def print_summary(self):
        """Imprime um resumo das métricas coletadas"""
        print("\n=== Resumo das Métricas ===")
        
        # A*
        print("\nA*:")
        if self.metrics['A*_time']:
            print(f"Tempo médio: {sum(self.metrics['A*_time']) / len(self.metrics['A*_time']):.4f} segundos")
            print(f"Comprimento médio do caminho: {sum(self.metrics['A*_path_length']) / len(self.metrics['A*_path_length']):.1f} passos")
            print(f"Número de caminhos calculados: {len(self.metrics['A*_time'])}")
            if 'A*_score' in self.metrics and self.metrics['A*_score']:
                print(f"Pontuação média: {sum(self.metrics['A*_score']) / len(self.metrics['A*_score']):.1f} pontos")
            self.save_metrics("A*", "astar_metrics.csv")
        else:
            print("Nenhuma medição realizada")
        
        # Bellman-Ford
        print("\nBellman-Ford:")
        if self.metrics['Bellman-Ford_time']:
            print(f"Tempo médio: {sum(self.metrics['Bellman-Ford_time']) / len(self.metrics['Bellman-Ford_time']):.4f} segundos")
            print(f"Comprimento médio do caminho: {sum(self.metrics['Bellman-Ford_path_length']) / len(self.metrics['Bellman-Ford_path_length']):.1f} passos")
            print(f"Número de caminhos calculados: {len(self.metrics['Bellman-Ford_time'])}")
            if 'Bellman-Ford_score' in self.metrics and self.metrics['Bellman-Ford_score']:
                print(f"Pontuação média: {sum(self.metrics['Bellman-Ford_score']) / len(self.metrics['Bellman-Ford_score']):.1f} pontos")
            self.save_metrics("Bellman-Ford", "bellmanford_metrics.csv")
        else:
            print("Nenhuma medição realizada")

