
# part of data scan from webpage and clean

y <- matrix(NA,nrow=27307,ncol=7)
y[1:27307,1] <- 1:27307
baseroute <- 'VisionAppraisal/newdata2017/XXX.html'
these <- 1:27307
for (i in these) {
  cat(i, "\n")
  newfile <- gsub('XXX', i, baseroute)
  x <- try(scan(newfile, what="", sep="\n"),TRUE)
  
  if (class(x)=="try-error") next
  else
  
  line2 <- grep("MainContent_lblLocation",x)
  line3 <- grep("MainContent_ctl01_lblYearBuilt",x)
  temp2 <- trimws(gsub("<[^<>]*>", "", x[line2]))
  temp3 <- as.numeric(gsub("<[^<>]*>", "", x[line3]))
  y[i,2:3] <- c(temp2,temp3)
  
  line4 <- grep("MainContent_lblGenAppraisal",x)
  temp4 <- gsub("<[^<>]*>", "", x[line4[2]])
  temp4 <- as.numeric(gsub(",","",gsub("\\$","",temp4)))
  y[i,4] <- temp4
 
  #wedpage from different date may have different title
  #"Bedrooms", "Bedrms"
  #"Ttl Bathrms", "Total Bthrms", "Total Baths"
  #"Half Bths", "Half Baths"
  line5 <- grep("Bedrooms|Bedrms",x)
  temp5 <- gsub("<[^<>]*>"," ",x[line5]) #replace with blank
  temp5 <- suppressWarnings(as.numeric(unlist(strsplit(temp5," "))))
  
  line6 <- grep("Total Bthrms|Ttl Bathrms|Total Baths",x)
  temp6 <- gsub("<[^<>]*>"," ",x[line6])
  temp6 <- suppressWarnings(as.numeric(unlist(strsplit(temp6," "))))
    
  line7 <- grep("Half Bths|Half Baths",x)
  temp7 <- gsub("<[^<>]*>"," ",x[line7])
  temp7 <- suppressWarnings(as.numeric(unlist(strsplit(temp7," "))))
 
  #if a vector doesn't have non-NA element, set room number to NA
  #if there are at least one non-NA element, sum up all the non-NA numbers
  if (length(temp5[is.na(temp5)==0])==0) {y[i,5] <- NA} else {
    y[i,5] <- sum(temp5[is.na(temp5)==0])}
  if (length(temp6[is.na(temp6)==0])==0) {y[i,6] <- NA} else {
    y[i,6] <- sum(temp6[is.na(temp6)==0])}
  if (length(temp7[is.na(temp7)==0])==0) {y[i,7] <- NA} else {
    y[i,7] <- sum(temp7[is.na(temp7)==0])}
  
}

#for pids have .5 bathrooms, convert 0.5 bathroom to 1 half bath
half <- grep(".5",y[,6],fixed = TRUE)
for (j in half) {
  if (is.na(y[j,7])) {y[j,7]=1} else {y[j,7]=as.numeric(y[j,7])+1}
}
y[half,6] <- as.numeric(y[half,6])-0.5

output <- data.frame(pid=y[,1],location=y[,2], yearbuilt=y[,3],
                     totval=y[,4],bedrooms=y[,5],bathrooms=y[,6],
                     halfbaths=y[,7],stringsAsFactors=FALSE)


