library(rvest)
library(dplyr)
library(lubridate)

url = "https://flyrichmond.com/airline-information/"
page = read_html(url)

# looking at all the tables to find the right one
tables = page %>% html_elements("table")
length(tables)

# the third is departures
departures = tables[[3]] %>% html_table()
head(departures)

# departure times from am/pm format to floating point
departure_times = departures %>%
  mutate(
    Time_24 = hour(parse_date_time(Time, orders = "I:M p")) +
              minute(parse_date_time(Time, orders = "I:M p")) / 60
  )
