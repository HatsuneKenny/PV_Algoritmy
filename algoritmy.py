import itertools
import random
import time
import tracemalloc


def boat_brute_force(weights, capacity):
    best_sum = 0
    best_combination = ()
    n = len(weights)
    for r in range(1, n + 1):
        for subset in itertools.combinations(weights, r):
            s = sum(subset)
            if s <= capacity and s > best_sum:
                best_sum = s
                best_combination = subset
    return best_combination, best_sum


def boat_monte_carlo(weights, capacity, iterations=10000):
    best_sum = 0
    best_combination = ()
    for _ in range(iterations):
        subset = []
        for item in weights:
            if random.choice([True, False]):
                subset.append(item)
        s = sum(subset)
        if s <= capacity and s > best_sum:
            best_sum = s
            best_combination = tuple(subset)
    return best_combination, best_sum


def boat_heuristic(weights, capacity):
    sorted_weights = sorted(weights, reverse=True)
    current_sum = 0
    combination = []
    for item in sorted_weights:
        if current_sum + item <= capacity:
            combination.append(item)
            current_sum += item
    return tuple(sorted(combination)), current_sum


if __name__ == "__main__":
    MIN_N = 4
    MAX_N = 11


    results = {
        "brute_force": [],
        "monte_carlo": [],
        "heuristic": []
    }

    for n in range(MIN_N, MAX_N):
        weights = [random.randint(10, 100) for _ in range(n)]
        capacity = int(sum(weights) * 0.5)

        tracemalloc.start()
        start_time = time.perf_counter()
        boat_brute_force(weights, capacity)
        end_time = time.perf_counter()
        current, bf_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        bf_time = end_time - start_time
        results["brute_force"].append((n, bf_time, bf_peak))

        # Měření pro Monte Carlo
        tracemalloc.start()
        start_time = time.perf_counter()
        boat_monte_carlo(weights, capacity, iterations=10000)
        end_time = time.perf_counter()
        current, mc_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        mc_time = end_time - start_time
        results["monte_carlo"].append((n, mc_time, mc_peak))

        # Měření pro heuristický přístup
        tracemalloc.start()
        start_time = time.perf_counter()
        boat_heuristic(weights, capacity)
        end_time = time.perf_counter()
        current, heur_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        heur_time = end_time - start_time
        results["heuristic"].append((n, heur_time, heur_peak))



    def print_results_block(alg_name, data):
        print(f"{alg_name.upper()}:")
        print("n,čas (s),paměť (B)")
        for row in data:
            n_val, time_val, mem_val = row
            print(f"{n_val},{time_val:.6f},{mem_val}")
        print()


    print_results_block("brute_force", results["brute_force"])
    print_results_block("monte_carlo", results["monte_carlo"])
    print_results_block("heuristic", results["heuristic"])
