### obtain a csv of addresses
address_out = read.csv("final_locations.csv")

## use the Census API
library(httr)
url <- "https://geocoding.geo.census.gov/geocoder/geographies/addressbatch"

# the API is very slow...
addresses <- address_out[1:30,]

# write out 30 addresses into a .csv file
f <- tempfile(fileext = ".csv") # creates a temporary file connection somewhere
write.csv(addresses, f, row.names=FALSE, col.names = NULL)

# the API call
req <- POST(url, body=list(addressFile = upload_file(f),
                           benchmark = "Public_AR_Census2010",
                           vintage = "Census2010_Census2010"),
            encode = "multipart")

length(content(req, "text", encoding = "UTF-8"))

# write the output into a .csv file and then read it in
outfile <- tempfile(fileext = ".csv")
writeLines(content(req, "text", encoding = "UTF-8"), outfile)

v <- read.csv(outfile, header=FALSE, as.is=TRUE)
head(v)

