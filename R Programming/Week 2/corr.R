corr <- function(directory, threshold = 0) {
  comp <- subset(complete(directory, 1:332), nobs > threshold)
  cr <- vector(mode = "numeric", length = nrow(comp))
  n <- 1

  for (id in comp[, 1]) {
    filename <- paste(directory, sprintf("%03d.csv", id), sep = "/")
    data <- read.csv(filename, colClasses = c("NULL", NA, NA, "NULL"))
    data <- subset(data, !is.na(sulfate) & !is.na(nitrate))
    cr[n] <- cor(data[, 1], data[, 2])
    n <- n + 1
  }

  cr
}
