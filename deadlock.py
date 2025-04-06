import numpy as np

def detect_deadlock(processes, resources, allocation, request):
    # Calculate Available Resources
    total_resources = np.sum(allocation, axis=0)  # Sum of allocated resources
    work = np.zeros(resources)  # Available resources

    # Available resources = Total allocated - Total requested
    for j in range(resources):
        work[j] = max(0, np.sum(allocation[:, j]) - np.sum(request[:, j]))  # Ensure no negative values

    finish = [False] * processes  # Track completed processes
    safe_sequence = []

    # Deadlock detection using Banker's Algorithm
    while len(safe_sequence) < processes:
        allocated = False
        for i in range(processes):
            if not finish[i] and all(request[i][j] <= work[j] for j in range(resources)):
                safe_sequence.append(i)
                work += allocation[i]  # Release allocated resources
                finish[i] = True
                allocated = True
                break

        if not allocated:
            return True, "⚠️ Deadlock detected! No safe sequence found."

    return False, f"✅ No deadlock detected. Safe sequence: {safe_sequence}"
