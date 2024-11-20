import numpy as np
import math
import random

class RouteOptimizationAgent:
    def __init__(self, objective_function, initial_solution, initial_temp=1000, cooling_rate=0.95, min_temp=1):
        """
        Inicializa o agente de otimização de rota com parâmetros fornecidos.

        - objective_function: Função que calcula o custo de uma solução.
        - initial_solution: A solução inicial para otimização (rota inicial).
        - initial_temp: Temperatura inicial para o algoritmo de Têmpera Simulada.
        - cooling_rate: Taxa de resfriamento (como a temperatura diminui a cada iteração).
        - min_temp: Temperatura mínima para parar a busca.
        """
        self.objective_function = objective_function
        self.current_solution = initial_solution  # Solução atual (rota atual)
        self.current_value = objective_function(initial_solution)  # Valor da solução atual (tempo de viagem)
        self.best_solution = initial_solution  # Melhor solução encontrada até o momento
        self.best_value = self.current_value  # Melhor valor encontrado até o momento (tempo de viagem)
        self.temperature = initial_temp  # Temperatura inicial
        self.cooling_rate = cooling_rate  # Taxa de resfriamento
        self.min_temp = min_temp  # Temperatura mínima para parar a execução

    def perturb_solution(self):
        """
        Gera uma nova solução vizinha ao alterar a ordem de cidades na rota atual.
        Esta perturbação é uma troca aleatória de duas cidades na rota.
        """
        new_solution = self.current_solution[:]  # Cria uma cópia da solução atual
        i, j = random.sample(range(len(new_solution)), 2)  # Escolhe dois índices aleatórios
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]  # Troca as cidades
        return new_solution  # Retorna a nova solução perturbada

    def acceptance_probability(self, old_value, new_value):
        """
        Calcula a probabilidade de aceitar a nova solução, baseado na temperatura.

        A probabilidade de aceitar uma solução pior diminui com a temperatura.
        Quanto mais alta a temperatura, maior a chance de aceitar soluções piores.
        """
        if new_value < old_value:  # Se a nova solução é melhor, aceita automaticamente
            return 1.0
        return math.exp((old_value - new_value) / self.temperature)  # Calcula a probabilidade de aceitação

    def cool_down(self):
        """
        Diminui a temperatura de acordo com a taxa de resfriamento.
        Essa temperatura é usada para determinar a aceitação de soluções piores.
        """
        self.temperature *= self.cooling_rate  # Diminui a temperatura com base na taxa de resfriamento

    def run(self):
        """
        Executa uma iteração do algoritmo de Têmpera Simulada.

        A cada iteração, gera uma nova solução perturbada e decide se deve aceitá-la
        com base na probabilidade de aceitação. A temperatura é então resfriada.
        """
        new_solution = self.perturb_solution()  # Gera uma nova solução perturbada
        new_value = self.objective_function(new_solution)  # Calcula o valor (custo) da nova solução
        ap = self.acceptance_probability(self.current_value, new_value)  # Calcula a probabilidade de aceitação

        if random.uniform(0, 1) < ap:  # Se a solução for aceita, atualiza a solução atual
            self.current_solution = new_solution
            self.current_value = new_value

            if new_value < self.best_value:  # Se a nova solução for a melhor encontrada, atualiza a melhor solução
                self.best_solution = new_solution
                self.best_value = new_value

        self.cool_down()  # Resfria a temperatura
        return self.current_solution, self.current_value, self.temperature  # Retorna a solução, o valor e a temperatura

