import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

# Fake flight times
flight_times = [6.5, 7.0, 8.0, 9.0, 
                11.0, 14.0, 16.0, 18.5, 19.0, 20.0]

# The amount of time needed to drive to RIC and be 90 mins early
lead_time = 150 / 60
shut_need = [t - lead_time for t in flight_times]
shut_need = [t if t > 0 else t + 24 for t in shut_need]

# cluster
X = np.array(shut_need).reshape(-1,1)

# operate 3 shuttles per day
k = 3
k_means = KMeans(n_clusters=k, random_state=0).fit(X)

cluster_cent = sorted(k_means.cluster_centers_.flatten())
assign = k_means.labels_

# results
schedule = pd.DataFrame({
    "Flight Time": flight_times,
    "Required Shuttle Leave": np.round(shut_need, 2),
    "Assigned Shuttle": assign
})

print("Suggested Williamsburg Shuttle Departure Times")
for t in cluster_cent:
    print(f" -{t:.2f} (approx {int(t)}:{int((t%1)*60):02d})")
print("\nAssignments:")
print(schedule)