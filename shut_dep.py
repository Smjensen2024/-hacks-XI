import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# todays Flight Times
flight_times = [9.0, 9.8, 10.0, 10.0, 10.5, 10.5, 10.6,
                11.0, 11.4, 11.5, 11.8, 11.8, 11.9, 11.9,
                12.0, 12.5, 12.5, 12.5, 13.0, 13.0, 13.5, 13.5,
                13.8, 14.9, 15.0, 15.0, 15.1, 15.3, 15.5, 15.6, 
                16.0, 16.2, 16.5, 16.5, 16.8, 16.9, 17.0, 17.0, 
                17.1, 17.2, 17.2, 17.3, 17.5, 17.6, 17.8, 17.9,
                18.4, 18.5, 18.6, 18.8, 18.9, 19.0, 19.1, 19.2, 
                19.5, 19.5, 19.6, 19.8, 20.0, 20.1, 20.3, 20.5, 
                21.0, 21.5, 22.3]  

# the amount of time needed to drive to RIC and be 90 mins early
lead_time = 150 / 60
shut_need = [t - lead_time for t in flight_times]
shut_need = [(t + 24) %24 for t in shut_need]

# cluster
X = np.array(shut_need).reshape(-1,1)

# different k (number of shuttles)
def optimize_schedule(times, flight_times, k):
    X = np.array(times).reshape(-1, 1)
    k_means = KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)
    centers = sorted((t+24)%24 for t in k_means.cluster_centers_.flatten())
    assign = k_means.labels_

    # passenger wait times in RIC
    wait_times = []
    for f, req, a in zip(flight_times, times, assign):
        assign_leave = centers[a]
        wait = (f - (assign_leave + lead_time)) * 60
        wait_times.append(wait)

    avg_wait = np.mean(wait_times)
    max_wait = np.max(wait_times)
    
    return centers, assign, avg_wait, max_wait

# shuttles between 2 and 5
results = {}
for k in range (2,6):
    centers, assign, avg_wait, max_wait = optimize_schedule(shut_need, flight_times, k)
    results[k] = {
        "centers": centers,
        "avg_wait": avg_wait,
        "max_wait": max_wait
    }

# results
print("Suggested Shuttle Departure Times from Williamsburg: ")
for k, res in results.items():
    print(f"\nIf {k} shuttles:")
    for t in res["centers"]:
        print(f"  - {t:.2f} (approx {int(t)}:{int((t%1)*60):02d})")
    print(f" Avg Wait in RICL {res['avg_wait']:1.1f} min, Max wait: {res["max_wait"]:.1f} min")


# example
centers3, assign3, avg3, max3 = optimize_schedule(shut_need, flight_times, 3)
schedule = pd.DataFrame({
    "Flight Departure": flight_times,
    "Required huttle leave": np.round(shut_need, 2),
    "Assigned Shuttle": assign3
})

print("\nAssignments for 3 shuttles:")
print(schedule)
print(f"Average wait: {avg:.1f} min, Max wait: {max3:.1f} min")

# plot wait time v. number of shuttles
ks = list(results.keys())
avgs = [results[k]["avg_wait"] for k in ks]
maxs = [results[k]["max_wait"] for k in ks]

plt.figure(figsize=(8,5))
plt.plot(ks, avgs, marker="o", label='Average wait time')
plt.plot(ks, maxs, marker="s", label='Max wait time')
plt.xlabel('Number of Shuttles')
plt.ylabel("Wait Time at RIC (mins)")
plt.title('Passenger Wait Time  vs Number of Shuttles')
plt.legend()
plt.grid(True)
plt.show()
