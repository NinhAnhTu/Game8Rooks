from collections import deque
from heapq import heappush, heappop
import time
import random
import math

def bfs_8_rooks(start_col=None):
    BOARD_SIZE = 8
    q = deque()
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    if start_col is not None:
        initial_state = [start_col] + [None] * (BOARD_SIZE - 1)
        q.append(initial_state)
        steps.append(initial_state[:])
    else:
        initial_state = [None] * BOARD_SIZE
        q.append(initial_state)
        steps.append(initial_state[:])

    result = None
    final_h = 0
    final_g = 0
    final_f = 0

    while q:
        state = q.popleft()
        nodes_expanded += 1

        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            result = state
            final_h = 0
            final_g = BOARD_SIZE
            final_f = 0
            end_time = time.time()
            print(f"BFS completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
            return steps, result, nodes_expanded, final_h, final_g, final_f

        for col in range(BOARD_SIZE):
            if col not in state:
                new_state = state[:]
                new_state[next_row] = col
                q.append(new_state)
                steps.append(new_state[:])

    return steps, None, nodes_expanded, final_h, final_g, final_f

def dfs_8_rooks(start_row=0, start_col=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    result = None
    start_time = time.time()

    def dfs(state):
        nonlocal result, nodes_expanded
        if result is not None:
            return
        
        nodes_expanded += 1
        steps.append(state[:])

        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            result = state[:]
            return

        for col in range(BOARD_SIZE):
            if col not in state:
                new_state = state[:]
                new_state[next_row] = col
                dfs(new_state)
                if result is not None:
                    return

    if start_col is not None:
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        dfs(initial_state)
    else:
        initial_state = [None] * BOARD_SIZE
        dfs(initial_state)

    end_time = time.time()
    
    final_h = 0
    final_g = BOARD_SIZE if result else 0
    final_f = 0

    if result:
        print(f"DFS completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"DFS no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def ucs_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    pq = []
    visited = set()

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        heappush(pq, (0, initial_state))
        steps.append(initial_state[:])
    else:
        initial_state = [None] * BOARD_SIZE
        heappush(pq, (0, initial_state))
        steps.append(initial_state[:])

    result = None
    final_h = 0
    final_g = 0
    final_f = 0

    while pq:
        cost, state = heappop(pq)
        nodes_expanded += 1
        steps.append(state[:])

        if all(x is not None for x in state):
            result = state
            final_h = 0
            final_g = cost
            final_f = cost
            end_time = time.time()
            print(f"UCS completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
            return steps, result, nodes_expanded, final_h, final_g, final_f

        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            continue

        used_cols = {col for col in state if col is not None}

        for col in range(BOARD_SIZE):
            if col not in used_cols:
                new_state = state[:]
                new_state[next_row] = col
                new_cost = cost + 1
                state_key = tuple(new_state)
                if state_key not in visited:
                    visited.add(state_key)
                    heappush(pq, (new_cost, new_state))

    return steps, None, nodes_expanded, final_h, final_g, final_f

def dls_8_rooks(start_pos=None, depth_limit=10):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    result = None
    start_time = time.time()

    def dls_recursive(state, depth):
        nonlocal result, nodes_expanded
        nodes_expanded += 1
        steps.append(state[:])

        if all(x is not None for x in state):
            result = state[:]
            return True

        if depth >= depth_limit:
            return False

        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            return False

        used_cols = {col for col in state if col is not None}

        for col in range(BOARD_SIZE):
            if col not in used_cols:
                new_state = state[:]
                new_state[next_row] = col
                if dls_recursive(new_state, depth + 1):
                    return True
        return False

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        dls_recursive(initial_state, 1)
    else:
        initial_state = [None] * BOARD_SIZE
        dls_recursive(initial_state, 0)

    end_time = time.time()

    final_h = 0
    final_g = BOARD_SIZE if result else 0
    final_f = 0

    if result:
        print(f"DLS completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s (limit={depth_limit})")
    else:
        print(f"DLS reached limit {depth_limit} (cutoff after {nodes_expanded} nodes, {end_time - start_time:.3f}s)")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def ids_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    all_steps = []
    nodes_total = 0
    result = None
    start_time = time.time()

    for depth in range(1, BOARD_SIZE + 3):
        steps, current_result, nodes_expanded, h, g, f = dls_8_rooks(start_pos, depth)
        all_steps.extend(steps)
        nodes_total += nodes_expanded
        if current_result:
            result = current_result
            break

    end_time = time.time()
    
    final_h = 0
    final_g = BOARD_SIZE if result else 0
    final_f = 0

    if result:
        print(f"IDS completed in {nodes_total} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"IDS no solution in {nodes_total} nodes, {end_time - start_time:.3f}s")

    return all_steps, result, nodes_total, final_h, final_g, final_f

def heuristic(state):
    if state is None:
        return 0
        
    conflicts = 0
    used_cols = set()
    for col in state:
        if col is not None:
            if col in used_cols:
                conflicts += 1
            else:
                used_cols.add(col)
    return conflicts

def greedy_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    pq = []
    visited = set()

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        h_val = heuristic(initial_state)
        heappush(pq, (h_val, initial_state))
        steps.append((initial_state[:], h_val, 0, h_val))
    else:
        initial_state = [None] * BOARD_SIZE
        h_val = heuristic(initial_state)
        heappush(pq, (h_val, initial_state))
        steps.append((initial_state[:], h_val, 0, h_val))

    final_h = 0
    final_g = 0
    final_f = 0

    while pq:
        _, state = heappop(pq)
        nodes_expanded += 1

        current_h = heuristic(state)
        current_g = sum(1 for x in state if x is not None)
        current_f = current_h
        
        steps.append((state[:], current_h, current_g, current_f))

        if all(x is not None for x in state) and current_h == 0:
            final_h = current_h
            final_g = current_g
            final_f = current_f
            end_time = time.time()
            print(f"Greedy completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
            return steps, state, nodes_expanded, final_h, final_g, final_f

        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            continue

        used_cols = {col for col in state if col is not None}

        for col in range(BOARD_SIZE):
            if col not in used_cols:
                new_state = state[:]
                new_state[next_row] = col
                state_key = tuple(new_state)
                if state_key not in visited:
                    visited.add(state_key)
                    h_val = heuristic(new_state)
                    heappush(pq, (h_val, new_state))

    return steps, None, nodes_expanded, final_h, final_g, final_f

def astar_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    pq = []
    visited = set()

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        g_val = 1
        h_val = heuristic(initial_state)
        f_val = g_val + h_val
        heappush(pq, (f_val, g_val, initial_state))
        steps.append((initial_state[:], h_val, g_val, f_val))
    else:
        initial_state = [None] * BOARD_SIZE
        g_val = 0
        h_val = heuristic(initial_state)
        f_val = g_val + h_val
        heappush(pq, (f_val, g_val, initial_state))
        steps.append((initial_state[:], h_val, g_val, f_val))

    final_h = 0
    final_g = 0
    final_f = 0

    while pq:
        _, g_val, state = heappop(pq)
        nodes_expanded += 1

        current_h = heuristic(state)
        current_g = g_val
        current_f = current_g + current_h
        
        steps.append((state[:], current_h, current_g, current_f))

        if all(x is not None for x in state) and current_h == 0:
            final_h = current_h
            final_g = current_g
            final_f = current_f
            end_time = time.time()
            print(f"A* completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
            return steps, state, nodes_expanded, final_h, final_g, final_f

        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            continue

        used_cols = {col for col in state if col is not None}

        for col in range(BOARD_SIZE):
            if col not in used_cols:
                new_state = state[:]
                new_state[next_row] = col
                state_key = tuple(new_state)
                if state_key not in visited:
                    visited.add(state_key)
                    new_g_val = g_val + 1
                    h_val = heuristic(new_state)
                    f_val = new_g_val + h_val
                    heappush(pq, (f_val, new_g_val, new_state))

    return steps, None, nodes_expanded, final_h, final_g, final_f

def hill_climbing_8_rooks(start_pos=None, max_iterations=1000, max_restarts=20):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()
    best_solution = None
    best_cost = float("inf")

    for restart in range(max_restarts):
        current_state = random.sample(range(BOARD_SIZE), BOARD_SIZE)
        if start_pos:
            start_row, start_col = start_pos
            current_state[start_row] = start_col

        current_cost = heuristic(current_state)
        nodes_expanded += 1
        steps.append((current_state[:], current_cost, 0, current_cost))

        for iteration in range(max_iterations):
            if current_cost == 0:
                best_solution = current_state[:]
                best_cost = 0
                print(f"Hill Climbing found solution at restart {restart + 1}")
                break

            neighbors = []
            for i in range(BOARD_SIZE):
                for j in range(i + 1, BOARD_SIZE):
                    if start_pos and (i == start_pos[0] or j == start_pos[0]):
                        continue
                    neighbor = current_state[:]
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    cost = heuristic(neighbor)
                    nodes_expanded += 1
                    neighbors.append((cost, neighbor))

            if not neighbors:
                break

            best_neighbor_cost, best_neighbor = min(neighbors, key=lambda x: x[0])

            if best_neighbor_cost < current_cost:
                current_state = best_neighbor
                current_cost = best_neighbor_cost
                steps.append((current_state[:], current_cost, 0, current_cost))
            else:
                break

        if current_cost < best_cost:
            best_solution = current_state[:]
            best_cost = current_cost

        if best_cost == 0:
            break

        print(f"Restart {restart + 1}/{max_restarts} | best_cost = {best_cost} | nodes = {nodes_expanded}")

    end_time = time.time()
    final_h = best_cost
    final_g = 0
    final_f = final_h

    if final_h == 0:
        print(f"Random-Restart Hill Climbing completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s with {restart + 1} restarts")
    else:
        print(f"No optimal solution after {max_restarts} restarts, best_h = {final_h}, nodes = {nodes_expanded}")

    return steps, best_solution, nodes_expanded, final_h, final_g, final_f

def simulated_annealing_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()
    
    max_restarts = 10
    max_iterations_per_restart = 2000
    initial_temperature = 0.8
    cooling_rate = 0.97
    min_temperature = 0.01
    
    best_solution = None
    best_cost = float('inf')
    
    for restart in range(max_restarts):
        current_state = random.sample(range(BOARD_SIZE), BOARD_SIZE)
        
        if start_pos:
            start_row, start_col = start_pos
            current_state[start_row] = start_col
        
        current_cost = heuristic(current_state)
        nodes_expanded += 1
        steps.append((current_state[:], current_cost, 0, current_cost))
        
        temperature = initial_temperature
        iteration_count = 0
        
        while temperature > min_temperature and iteration_count < max_iterations_per_restart and current_cost > 0:
            iteration_count += 1
            nodes_expanded += 1

            i, j = random.sample(range(BOARD_SIZE), 2)
            
            if start_pos and random.random() < 0.7:
                if i == start_pos[0] or j == start_pos[0]:
                    continue
            
            neighbor = current_state[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbor_cost = heuristic(neighbor)

            cost_diff = neighbor_cost - current_cost
            
            if cost_diff < 0:
                current_state = neighbor
                current_cost = neighbor_cost
                steps.append((current_state[:], current_cost, 0, current_cost))
            else:
                acceptance_probability = math.exp(-cost_diff / temperature)
                if random.random() < acceptance_probability:
                    current_state = neighbor
                    current_cost = neighbor_cost
                    steps.append((current_state[:], current_cost, 0, current_cost))

            temperature *= cooling_rate
            
            if current_cost == 0:
                best_solution = current_state[:]
                best_cost = 0
                break

        if current_cost < best_cost:
            best_solution = current_state[:]
            best_cost = current_cost

        print(f"SA Restart {restart + 1}: cost = {current_cost}, nodes = {nodes_expanded}")

        if best_cost == 0:
            break

    end_time = time.time()
    final_h = best_cost
    final_g = 0
    final_f = final_h

    if best_cost == 0:
        print(f"Simulated Annealing completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s, {restart + 1} restarts")
    else:
        print(f"Simulated Annealing best cost = {best_cost} in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, best_solution, nodes_expanded, final_h, final_g, final_f

def genetic_algorithm_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    POPULATION_SIZE = 30
    GENERATIONS = 200
    MUTATION_RATE = 0.2
    ELITISM_COUNT = 2

    def fitness(state):
        conflicts = heuristic(state)
        return 1.0 / (1.0 + conflicts)

    population = []
    for _ in range(POPULATION_SIZE):
        if start_pos:
            start_row, start_col = start_pos
            individual = list(range(BOARD_SIZE))
            random.shuffle(individual)
            if individual[start_row] != start_col:
                for i in range(BOARD_SIZE):
                    if individual[i] == start_col:
                        individual[i], individual[start_row] = individual[start_row], individual[i]
                        break
            individual[start_row] = start_col
        else:
            individual = random.sample(range(BOARD_SIZE), BOARD_SIZE)
        
        population.append(individual)
        if _ == 0:
            h_val = heuristic(individual)
            steps.append((individual[:], h_val, 0, h_val))

    best_individual = None
    best_fitness = -1

    for generation in range(GENERATIONS):
        nodes_expanded += POPULATION_SIZE

        fitness_scores = []
        current_best_individual = None
        current_best_fitness = -1
        
        for individual in population:
            fit = fitness(individual)
            fitness_scores.append(fit)
            if fit > current_best_fitness:
                current_best_fitness = fit
                current_best_individual = individual[:]
        
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = current_best_individual[:]
            h_val = heuristic(best_individual)
            steps.append((best_individual[:], h_val, 0, h_val))

        if heuristic(best_individual) == 0:
            print(f"GA found solution at generation {generation}")
            break

        new_population = []
        
        elite_indices = sorted(range(len(fitness_scores)), 
                              key=lambda i: fitness_scores[i], 
                              reverse=True)[:ELITISM_COUNT]
        for idx in elite_indices:
            new_population.append(population[idx][:])
        
        while len(new_population) < POPULATION_SIZE:
            tournament_size = 3
            tournament1 = random.sample(range(POPULATION_SIZE), tournament_size)
            tournament2 = random.sample(range(POPULATION_SIZE), tournament_size)
            
            parent1 = population[max(tournament1, key=lambda i: fitness_scores[i])]
            parent2 = population[max(tournament2, key=lambda i: fitness_scores[i])]
            
            child = ordered_crossover(parent1, parent2)
            
            if random.random() < MUTATION_RATE:
                i, j = random.sample(range(BOARD_SIZE), 2)
                if not start_pos or (i != start_pos[0] and j != start_pos[0]):
                    child[i], child[j] = child[j], child[i]
            
            new_population.append(child)
        
        population = new_population

        if generation % 10 == 0:
            best_h = heuristic(best_individual)
            print(f"GA Generation {generation}: best_h = {best_h}")

    if best_individual and (not steps or steps[-1][0] != best_individual):
        h_val = heuristic(best_individual)
        steps.append((best_individual[:], h_val, 0, h_val))

    end_time = time.time()
    
    final_h = heuristic(best_individual) if best_individual else BOARD_SIZE
    final_g = 0
    final_f = final_h
    
    if final_h == 0:
        print(f"Genetic Algorithm completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Genetic Algorithm best cost = {final_h} in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, best_individual if final_h == 0 else None, nodes_expanded, final_h, final_g, final_f

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    cut1, cut2 = sorted(random.sample(range(size), 2))
    
    child = [None] * size
    
    for i in range(cut1, cut2 + 1):
        child[i] = parent1[i]
    
    current_pos = (cut2 + 1) % size
    for gene in parent2:
        if gene not in child:
            while child[current_pos] is not None:
                current_pos = (current_pos + 1) % size
            child[current_pos] = gene
    
    return child

def beam_search_8_rooks(start_pos=None, beam_width=5):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        h_val = heuristic(initial_state)
        beam = [(initial_state, h_val)]
        current_g = sum(1 for x in initial_state if x is not None)
        steps.append((initial_state[:], h_val, current_g, h_val))
    else:
        initial_state = [None] * BOARD_SIZE
        h_val = heuristic(initial_state)
        beam = [(initial_state, h_val)]
        current_g = 0
        steps.append((initial_state[:], h_val, current_g, h_val))

    final_h = 0
    final_g = 0
    final_f = 0

    while beam:
        next_beam = []
        
        for state, cost in beam:
            nodes_expanded += 1
            
            if all(x is not None for x in state) and cost == 0:
                final_h = cost
                final_g = sum(1 for x in state if x is not None)
                final_f = final_h
                end_time = time.time()
                print(f"Beam Search completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
                return steps, state, nodes_expanded, final_h, final_g, final_f

            next_row = None
            for i in range(BOARD_SIZE):
                if state[i] is None:
                    next_row = i
                    break

            if next_row is None:
                continue

            used_cols = {col for col in state if col is not None}

            for col in range(BOARD_SIZE):
                if col not in used_cols:
                    new_state = state[:]
                    new_state[next_row] = col
                    new_cost = heuristic(new_state)
                    next_beam.append((new_state, new_cost))
        
        next_beam.sort(key=lambda x: x[1])
        beam = next_beam[:beam_width]

        if beam:
            best_state, best_cost = beam[0]
            current_g = sum(1 for x in best_state if x is not None)
            steps.append((best_state[:], best_cost, current_g, best_cost))

    return steps, None, nodes_expanded, final_h, final_g, final_f

def and_or_search_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    result = None
    
    def and_or_search(state, depth):
        nonlocal result, nodes_expanded
        nodes_expanded += 1
        
        current_h = heuristic(state)
        current_g = sum(1 for x in state if x is not None)
        current_f = current_h
        steps.append((state[:], current_h, current_g, current_f))
        
        if all(x is not None for x in state) and current_h == 0:
            result = state[:]
            return True
            
        if depth >= BOARD_SIZE:
            return False
            
        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            return False

        used_cols = {col for col in state if col is not None}

        for col in range(BOARD_SIZE):
            if col not in used_cols:
                new_state = state[:]
                new_state[next_row] = col
                if and_or_search(new_state, depth + 1):
                    return True
        return False

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        and_or_search(initial_state, 1)
    else:
        initial_state = [None] * BOARD_SIZE
        and_or_search(initial_state, 0)

    end_time = time.time()
    
    final_h = heuristic(result) if result else 0
    final_g = sum(1 for x in result if x is not None) if result else 0
    final_f = final_h
    
    if result:
        print(f"And-Or Search completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"And-Or Search no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def partially_observable_search_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    result = None
    observable_rows = 3
    
    def partial_search(state, depth):
        nonlocal result, nodes_expanded
        nodes_expanded += 1
        
        current_h = heuristic(state)
        current_g = sum(1 for x in state if x is not None)
        current_f = current_h
        
        steps.append((state[:], current_h, current_g, current_f))
        
        if all(x is not None for x in state) and current_h == 0:
            result = state[:]
            return True
            
        if depth >= BOARD_SIZE * 2:
            return False
            
        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            return False

        used_cols = {col for col in state if col is not None}
        available_cols = [col for col in range(BOARD_SIZE) if col not in used_cols]
        
        if next_row < observable_rows:
            for col in available_cols:
                new_state = state[:]
                new_state[next_row] = col
                if partial_search(new_state, depth + 1):
                    return True
        else:
            random.shuffle(available_cols)
            for col in available_cols:
                new_state = state[:]
                new_state[next_row] = col
                if partial_search(new_state, depth + 1):
                    return True

        return False

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        success = partial_search(initial_state, 1)
    else:
        initial_state = [None] * BOARD_SIZE
        success = partial_search(initial_state, 0)

    end_time = time.time()
    
    final_h = heuristic(result) if result else BOARD_SIZE
    final_g = sum(1 for x in result if x is not None) if result else 0
    final_f = final_h
    
    if result:
        print(f"Partially Observable Search completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Partially Observable Search no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def belief_state_search_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        belief_states = [initial_state]
        
        h_val = heuristic(initial_state)
        g_val = 1
        f_val = h_val
        steps.append((initial_state[:], h_val, g_val, f_val))
    else:
        initial_state = [None] * BOARD_SIZE
        belief_states = [initial_state]
        
        h_val = heuristic(initial_state)
        g_val = 0
        f_val = h_val
        steps.append((initial_state[:], h_val, g_val, f_val))

    result = None
    visited = set()
    
    while belief_states and not result:
        new_belief_states = []
        
        for state in belief_states:
            state_key = tuple(state)
            if state_key in visited:
                continue
            visited.add(state_key)
            
            nodes_expanded += 1
            
            if all(x is not None for x in state) and heuristic(state) == 0:
                result = state[:]
                break
                
            next_row = None
            for i in range(BOARD_SIZE):
                if state[i] is None:
                    next_row = i
                    break

            if next_row is None:
                continue

            used_cols = {col for col in state if col is not None}
            available_cols = [col for col in range(BOARD_SIZE) if col not in used_cols]
            available_cols.sort(key=lambda col: abs(col - (BOARD_SIZE // 2)))
            
            for col in available_cols:
                new_state = state[:]
                new_state[next_row] = col
                new_state_key = tuple(new_state)
                
                if new_state_key not in visited:
                    new_belief_states.append(new_state)
                    
                    h_val = heuristic(new_state)
                    g_val = sum(1 for x in new_state if x is not None)
                    f_val = h_val
                    steps.append((new_state[:], h_val, g_val, f_val))
        
        belief_states = new_belief_states

    end_time = time.time()
    
    final_h = heuristic(result) if result else 0
    final_g = sum(1 for x in result if x is not None) if result else 0
    final_f = final_h
    
    if result:
        print(f"Belief State Search completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Belief State Search no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def backtracking_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    result = None
    
    def backtrack(state):
        nonlocal result, nodes_expanded
        nodes_expanded += 1
        
        current_h = heuristic(state)
        current_g = sum(1 for x in state if x is not None)
        current_f = current_h
        steps.append((state[:], current_h, current_g, current_f))
        
        if all(x is not None for x in state) and current_h == 0:
            result = state[:]
            return True
            
        next_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                next_row = i
                break

        if next_row is None:
            return False

        for col in range(BOARD_SIZE):
            if is_valid(state, col):
                new_state = state[:]
                new_state[next_row] = col
                if backtrack(new_state):
                    return True
        return False

    def is_valid(state, new_col):
        return new_col not in [col for col in state if col is not None]

    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        backtrack(initial_state)
    else:
        initial_state = [None] * BOARD_SIZE
        backtrack(initial_state)

    end_time = time.time()
    
    final_h = heuristic(result) if result else 0
    final_g = sum(1 for x in result if x is not None) if result else 0
    final_f = final_h
    
    if result:
        print(f"Backtracking completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Backtracking no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def forward_checking_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    result = None
    
    def forward_check(state, domains):
        nonlocal result, nodes_expanded
        nodes_expanded += 1
        
        current_h = heuristic(state)
        current_g = sum(1 for x in state if x is not None)
        current_f = current_h
        steps.append((state[:], current_h, current_g, current_f))
        
        if all(x is not None for x in state) and current_h == 0:
            result = state[:]
            return True
            
        current_row = None
        for i in range(BOARD_SIZE):
            if state[i] is None:
                current_row = i
                break

        if current_row is None:
            return False

        current_domain = domains[current_row][:]
        
        for col in current_domain:
            if is_valid(state, col):
                new_domains = [d[:] for d in domains]
                new_domains[current_row] = [col]
                
                for i in range(BOARD_SIZE):
                    if state[i] is None and i != current_row:
                        if col in new_domains[i]:
                            new_domains[i].remove(col)
                
                forward_check_valid = True
                for i in range(BOARD_SIZE):
                    if state[i] is None and len(new_domains[i]) == 0:
                        forward_check_valid = False
                        break
                
                if forward_check_valid:
                    new_state = state[:]
                    new_state[current_row] = col
                    if forward_check(new_state, new_domains):
                        return True
        return False

    def is_valid(state, new_col):
        return new_col not in [col for col in state if col is not None]

    domains = [list(range(BOARD_SIZE)) for _ in range(BOARD_SIZE)]
    
    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        domains[start_row] = [start_col]
        for i in range(BOARD_SIZE):
            if i != start_row and start_col in domains[i]:
                domains[i].remove(start_col)
        forward_check(initial_state, domains)
    else:
        initial_state = [None] * BOARD_SIZE
        forward_check(initial_state, domains)

    end_time = time.time()
    
    final_h = heuristic(result) if result else 0
    final_g = sum(1 for x in result if x is not None) if result else 0
    final_f = final_h
    
    if result:
        print(f"Forward Checking completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Forward Checking no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def ac3_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    result = None
    
    def ac3(domains):
        queue = deque()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i != j:
                    queue.append((i, j))
        
        while queue:
            xi, xj = queue.popleft()
            if revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                for xk in range(BOARD_SIZE):
                    if xk != xi and xk != xj:
                        queue.append((xk, xi))
        return True
    
    def revise(domains, xi, xj):
        revised = False
        for x in domains[xi][:]:
            found = False
            for y in domains[xj]:
                if y != x:
                    found = True
                    break
            if not found:
                domains[xi].remove(x)
                revised = True
        return revised
    
    def backtrack_with_ac3(state, domains):
        nonlocal result, nodes_expanded
        nodes_expanded += 1
        
        current_h = heuristic(state)
        current_g = sum(1 for x in state if x is not None)
        current_f = current_h
        steps.append((state[:], current_h, current_g, current_f))
        
        if all(x is not None for x in state) and current_h == 0:
            result = state[:]
            return True
            
        current_row = None
        min_domain_size = BOARD_SIZE + 1
        for i in range(BOARD_SIZE):
            if state[i] is None and len(domains[i]) < min_domain_size:
                min_domain_size = len(domains[i])
                current_row = i

        if current_row is None:
            return False

        current_domain = domains[current_row][:]
        
        for col in current_domain:
            if is_valid(state, col):
                new_domains = [d[:] for d in domains]
                new_domains[current_row] = [col]
                
                for i in range(BOARD_SIZE):
                    if i != current_row and state[i] is None and col in new_domains[i]:
                        new_domains[i].remove(col)
                
                if ac3(new_domains):
                    new_state = state[:]
                    new_state[current_row] = col
                    if backtrack_with_ac3(new_state, new_domains):
                        return True
        return False

    def is_valid(state, new_col):
        return new_col not in [col for col in state if col is not None]

    domains = [list(range(BOARD_SIZE)) for _ in range(BOARD_SIZE)]
    
    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        domains[start_row] = [start_col]
        for i in range(BOARD_SIZE):
            if i != start_row and start_col in domains[i]:
                domains[i].remove(start_col)
    else:
        initial_state = [None] * BOARD_SIZE
    
    if not ac3(domains):
        end_time = time.time()
        print(f"AC-3: Cannot find solution after initial AC-3")
        return steps, None, nodes_expanded, 0, 0, 0
    
    if start_pos:
        result_found = backtrack_with_ac3(initial_state, domains)
    else:
        result_found = backtrack_with_ac3(initial_state, domains)

    end_time = time.time()
    
    final_h = heuristic(result) if result else 0
    final_g = sum(1 for x in result if x is not None) if result else 0
    final_f = final_h
    
    if result:
        print(f"AC-3 completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"AC-3 no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def minimax_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    class MinimaxSolver:
        def __init__(self, n=8):
            self.n = n
            self.steps = steps
            self.nodes_expanded = 0
            
        def is_safe(self, board, row, col):
            for i in range(self.n):
                if board[i] is None:
                    continue
                if board[i] == col:
                    return False
            return True
        
        def evaluate(self, board):
            placed = sum(1 for x in board if x is not None)
            return placed
        
        def minimax_search(self, board, depth, is_maximizing):
            self.nodes_expanded += 1
            
            next_row = None
            for i in range(self.n):
                if board[i] is None:
                    next_row = i
                    break
            
            if next_row is None:
                return self.evaluate(board)
            
            if is_maximizing:
                max_eval = float('-inf')
                
                for col in range(self.n):
                    if self.is_safe(board, next_row, col):
                        new_board = board[:]
                        new_board[next_row] = col
                        
                        current_h = 8 - self.evaluate(new_board)
                        current_g = self.evaluate(new_board)
                        current_f = current_h
                        self.steps.append((new_board[:], current_h, current_g, current_f))
                        
                        eval_score = self.minimax_search(new_board, depth + 1, False)
                        
                        max_eval = max(max_eval, eval_score)
                
                return max_eval
            else:
                min_eval = float('inf')
                
                for col in range(self.n):
                    if self.is_safe(board, next_row, col):
                        new_board = board[:]
                        new_board[next_row] = col
                        
                        current_h = 8 - self.evaluate(new_board)
                        current_g = self.evaluate(new_board)
                        current_f = current_h
                        self.steps.append((new_board[:], current_h, current_g, current_f))
                        
                        eval_score = self.minimax_search(new_board, depth + 1, True)
                        
                        min_eval = min(min_eval, eval_score)
                
                return min_eval
        
        def find_solution(self, board):
            for row in range(self.n):
                if board[row] is not None:
                    continue
                    
                for col in range(self.n):
                    if self.is_safe(board, row, col):
                        board[row] = col
                        self.nodes_expanded += 1
                        
                        current_h = 8 - self.evaluate(board)
                        current_g = self.evaluate(board)
                        current_f = current_h
                        self.steps.append((board[:], current_h, current_g, current_f))
                        
                        if all(x is not None for x in board):
                            return True
                        
                        if self.find_solution(board):
                            return True
                        
                        board[row] = None
            
            return False

    solver = MinimaxSolver(BOARD_SIZE)
    
    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        
        current_h = 8 - solver.evaluate(initial_state)
        current_g = solver.evaluate(initial_state)
        current_f = current_h
        steps.append((initial_state[:], current_h, current_g, current_f))
    else:
        initial_state = [None] * BOARD_SIZE
        current_h = 8
        current_g = 0
        current_f = current_h
        steps.append((initial_state[:], current_h, current_g, current_f))

    best_eval = solver.minimax_search(initial_state, 0, True)
    
    result = None
    if best_eval == BOARD_SIZE:
        solution_board = [None] * BOARD_SIZE
        if start_pos:
            start_row, start_col = start_pos
            solution_board[start_row] = start_col
        
        if solver.find_solution(solution_board):
            result = solution_board

    end_time = time.time()
    
    final_h = 0 if result else 8
    final_g = BOARD_SIZE if result else 0
    final_f = final_h
    
    nodes_expanded = solver.nodes_expanded
    
    if result:
        print(f"Minimax completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Minimax no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f

def alpha_beta_8_rooks(start_pos=None):
    BOARD_SIZE = 8
    steps = []
    nodes_expanded = 0
    start_time = time.time()

    class AlphaBetaSolver:
        def __init__(self, n=8):
            self.n = n
            self.steps = steps
            self.nodes_expanded = 0
            
        def is_safe(self, board, row, col):
            for i in range(self.n):
                if board[i] is None:
                    continue
                if board[i] == col:
                    return False
            return True
        
        def evaluate(self, board):
            placed = sum(1 for x in board if x is not None)
            return placed
        
        def alpha_beta_search(self, board, depth, alpha, beta, is_maximizing):
            self.nodes_expanded += 1
            
            next_row = None
            for i in range(self.n):
                if board[i] is None:
                    next_row = i
                    break
            
            if next_row is None:
                return self.evaluate(board)
            
            if is_maximizing:
                max_eval = float('-inf')
                
                for col in range(self.n):
                    if self.is_safe(board, next_row, col):
                        new_board = board[:]
                        new_board[next_row] = col
                        
                        current_h = 8 - self.evaluate(new_board)
                        current_g = self.evaluate(new_board)
                        current_f = current_h
                        self.steps.append((new_board[:], current_h, current_g, current_f))
                        
                        eval_score = self.alpha_beta_search(new_board, depth + 1, alpha, beta, False)
                        
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        
                        if beta <= alpha:
                            break
                
                return max_eval
            else:
                min_eval = float('inf')
                
                for col in range(self.n):
                    if self.is_safe(board, next_row, col):
                        new_board = board[:]
                        new_board[next_row] = col
                        
                        current_h = 8 - self.evaluate(new_board)
                        current_g = self.evaluate(new_board)
                        current_f = current_h
                        self.steps.append((new_board[:], current_h, current_g, current_f))
                        
                        eval_score = self.alpha_beta_search(new_board, depth + 1, alpha, beta, True)
                        
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        
                        if beta <= alpha:
                            break
                
                return min_eval
        
        def find_solution(self, board):
            for row in range(self.n):
                if board[row] is not None:
                    continue
                    
                for col in range(self.n):
                    if self.is_safe(board, row, col):
                        board[row] = col
                        self.nodes_expanded += 1
                        
                        current_h = 8 - self.evaluate(board)
                        current_g = self.evaluate(board)
                        current_f = current_h
                        self.steps.append((board[:], current_h, current_g, current_f))
                        
                        if all(x is not None for x in board):
                            return True
                        
                        if self.find_solution(board):
                            return True
                        
                        board[row] = None
            
            return False

    solver = AlphaBetaSolver(BOARD_SIZE)
    
    if start_pos:
        start_row, start_col = start_pos
        initial_state = [None] * BOARD_SIZE
        initial_state[start_row] = start_col
        
        current_h = 8 - solver.evaluate(initial_state)
        current_g = solver.evaluate(initial_state)
        current_f = current_h
        steps.append((initial_state[:], current_h, current_g, current_f))
    else:
        initial_state = [None] * BOARD_SIZE
        current_h = 8
        current_g = 0
        current_f = current_h
        steps.append((initial_state[:], current_h, current_g, current_f))

    alpha = float('-inf')
    beta = float('inf')
    best_eval = solver.alpha_beta_search(initial_state, 0, alpha, beta, True)
    
    result = None
    if best_eval == BOARD_SIZE:
        solution_board = [None] * BOARD_SIZE
        if start_pos:
            start_row, start_col = start_pos
            solution_board[start_row] = start_col
        
        if solver.find_solution(solution_board):
            result = solution_board

    end_time = time.time()
    
    final_h = 0 if result else 8
    final_g = BOARD_SIZE if result else 0
    final_f = final_h
    
    nodes_expanded = solver.nodes_expanded
    
    if result:
        print(f"Alpha-Beta Pruning completed in {nodes_expanded} nodes, {end_time - start_time:.3f}s")
    else:
        print(f"Alpha-Beta Pruning no solution in {nodes_expanded} nodes, {end_time - start_time:.3f}s")

    return steps, result, nodes_expanded, final_h, final_g, final_f