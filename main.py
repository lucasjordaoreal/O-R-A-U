from agent import RouteOptimizationAgent
import matplotlib.pyplot as plt
import numpy as np

# Função objetivo: tempo de viagem baseado em distâncias reais
def objective_function(route):
    """
    Função que calcula o custo da rota (tempo de viagem).
    A função leva em consideração distâncias entre as cidades e um fator de tráfego aleatório.

    Parâmetros:
        route (list): A rota (lista de cidades na ordem em que são visitadas).

    Retorna:
        float: O tempo de viagem total (considerando distância e tráfego).
    """
    # Distâncias fictícias entre cidades (em km)
    distances = {
        'A': {'B': 10, 'C': 15, 'D': 20},
        'B': {'A': 10, 'C': 25, 'D': 30},
        'C': {'A': 15, 'B': 25, 'D': 35},
        'D': {'A': 20, 'B': 30, 'C': 35},
    }

    # Calcula a distância total da rota
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[route[i]][route[i+1]]  # Soma as distâncias entre as cidades

    # Fator de tráfego aleatório entre 1 e 2
    traffic_factor = np.random.uniform(1, 2)

    # Retorna o tempo total de viagem, considerando a distância e o tráfego
    return total_distance * traffic_factor

# Rota inicial (exemplo)
initial_solution = ['A', 'B', 'C', 'D']  # Exemplo de uma solução inicial de rota
initial_temp = 1000  # Temperatura inicial para o algoritmo de Têmpera Simulada
cooling_rate = 0.9  # Taxa de resfriamento
min_temp = 0.1  # Temperatura mínima para parar o algoritmo

# Inicializa o agente de otimização com a função objetivo e outros parâmetros
agent = RouteOptimizationAgent(
    objective_function=objective_function,
    initial_solution=initial_solution,
    initial_temp=initial_temp,
    cooling_rate=cooling_rate,
    min_temp=min_temp,
)

# Executa o agente para otimizar a rota
solutions = []  # Lista para armazenar as soluções encontradas
values = []  # Lista para armazenar os valores (tempos de viagem)
temperatures = []  # Lista para armazenar as temperaturas ao longo das iterações

while agent.temperature > agent.min_temp:  # Enquanto a temperatura for maior que o mínimo
    solution, value, temperature = agent.run()  # Executa uma iteração do algoritmo
    solutions.append(solution)  # Armazena a solução encontrada
    values.append(value)  # Armazena o valor (tempo de viagem) da solução
    temperatures.append(temperature)  # Armazena a temperatura atual

# Exibe os resultados finais
print(f"Melhor solução encontrada (tempo de viagem): {agent.best_value:.4f}")
print(f"Melhor rota: {agent.best_solution}")

# Gráficos
plt.figure(figsize=(10, 5))  # Tamanho da figura dos gráficos

# Evolução das soluções (tempo de viagem ao longo das iterações)
plt.subplot(1, 2, 1)  # Subgráfico 1: Evolução do tempo de viagem
plt.plot(values, label="Tempo de Viagem")
plt.xlabel("Iterações")
plt.ylabel("Tempo de Viagem")
plt.title("Evolução do Tempo de Viagem")
plt.legend()

# Temperatura ao longo do tempo
plt.subplot(1, 2, 2)  # Subgráfico 2: Decaimento da temperatura
plt.plot(temperatures, label="Temperatura")
plt.xlabel("Iterações")
plt.ylabel("Temperatura")
plt.title("Decaimento da Temperatura")
plt.legend()

plt.tight_layout()  # Ajusta o layout dos gráficos para que não se sobreponham
plt.show()  # Exibe os gráficos
