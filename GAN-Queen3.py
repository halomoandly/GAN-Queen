import random

# Parameter Genetic Algorithm
N = 8  # Jumlah Ratu
POPULATION_SIZE = 200  # Ukuran Populasi
MUTATION_RATE = 0.1  # Tingkat Mutasi
MAX_GENERATIONS = 2000  # Jumlah Maksimal Generasi
ELITISM_RATE = 0.1  # Persentase elitisme (10% terbaik dipertahankan)

# Fungsi untuk menghitung fitness (jumlah pasangan ratu yang tidak saling menyerang)
def fitness(chromosome):
    non_attacking_pairs = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if chromosome[i] != chromosome[j] and abs(chromosome[i] - chromosome[j]) != abs(i - j):
                non_attacking_pairs += 1
    # Maksimal pasangan yang tidak saling menyerang untuk N-Queen adalah N*(N-1)/2
    max_pairs = N * (N - 1) / 2
    return non_attacking_pairs / max_pairs

# Fungsi untuk membuat individu acak
def create_individual():
    return [random.randint(0, N - 1) for _ in range(N)]

# Fungsi untuk melakukan uniform crossover dua individu (parent)
def crossover(parent1, parent2):
    child1, child2 = [], []
    for i in range(N):
        if random.random() > 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    return child1, child2

# Fungsi untuk swap mutation
def mutate(individual):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(N), 2)
        individual[i], individual[j] = individual[j], individual[i]

# Fungsi untuk memilih individu menggunakan turnamen selection
def select(population, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

# Fungsi utama Algoritma Genetika untuk menyelesaikan N-Queen
def genetic_algorithm():
    # Inisialisasi populasi
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    generation = 0
    solution_found = False

    while generation < MAX_GENERATIONS and not solution_found:
        # Sort population by fitness
        population = sorted(population, key=fitness, reverse=True)

        # Check if the best individual is a solution
        if fitness(population[0]) == 1:
            solution_found = True
            break

        # Keep the best individuals (elitism)
        new_population = population[:int(ELITISM_RATE * POPULATION_SIZE)]  # Simpan 10% terbaik

        # Reproduksi (Crossover dan Mutasi) hingga ukuran populasi penuh
        while len(new_population) < POPULATION_SIZE:
            parent1 = select(population)
            parent2 = select(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        population = new_population
        generation += 1

    # Output solusi
    if solution_found:
        print(f"Solusi ditemukan dalam generasi ke-{generation}:")
        print(population[0])
    else:
        print("Solusi tidak ditemukan dalam batas generasi maksimum.")

# Menjalankan Algoritma Genetika untuk N-Queen
genetic_algorithm()
