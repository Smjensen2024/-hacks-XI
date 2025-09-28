set.seed(123)

# flight times
flight_times = c(9.0, 9.8, 10.0, 10.0, 10.5, 10.5, 10.6,
                 11.0, 11.4, 11.5, 11.8, 11.8, 11.9, 11.9,
                 12.0, 12.5, 12.5, 12.5, 13.0, 13.0, 13.5, 13.5,
                 13.8, 14.9, 15.0, 15.0, 15.1, 15.3, 15.5, 15.6, 
                 16.0, 16.2, 16.5, 16.5, 16.8, 16.9, 17.0, 17.0, 
                 17.1, 17.2, 17.2, 17.3, 17.5, 17.6, 17.8, 17.9,
                 18.4, 18.5, 18.6, 18.8, 18.9, 19.0, 19.1, 19.2, 
                 19.5, 19.5, 19.6, 19.8, 20.0, 20.1, 20.3, 20.5, 
                 21.0, 21.5, 22.3)

shuttle_dept = c(9.15, 13.97, 17.22)
assignments = c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
                2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                3, 3, 3, 3, 3, 3, 3, 3)

# params
travel_m = 55 # avg travek time in mins
travel_sd = 10 # traffic variability
buffer = 90 
trials = 5000 # Monte Carlo simulations

miss_counts = numeric(length(flight_times))

# simulation
for (t in 1:trials) {
  travel_times = rnorm(length(flight_times), mean=travel_m, sd=travel_sd)
  
  for (i in seq_along(flight_times)) {
    leave = shuttle_dept[assignments[i]]
    arrival = leave*60 + travel_times
    flight = flight_times[i]*60
    
    if (arrival > (flight - buffer)) {
      miss_counts[i] = miss_counts[i] + 1
    }
  }
}

# probs
miss_probs = miss_counts / trials
overall_miss = mean(miss_probs) # system wide average missing prob

# results
results = data.frame(
  FlightTime = flight_times, Shuttle = assignments, MissProb = round(miss_probs, 3)
)

print(results) # per passenger prob of missing flight
cat("Overall average missing flight probability:", round(overall_miss, 3), "\n")