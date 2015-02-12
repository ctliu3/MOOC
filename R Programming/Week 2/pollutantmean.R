pollutantmean <- function(directory, pollutant, id = 1:332) {
  sum_ <- 0
  count <- 0

  for (id_ in id) {
    filename <- paste(directory, sprintf("%03d.csv", id_), sep = "/")
    if (pollutant == "sulfate") {
      cols <- c("NULL", NA, "NULL", "NULL")
    } else { # "nitrate"
      cols <- c("NULL", "NULL", NA, "NULL")
    }
    data <- read.csv(filename, colClasses = cols)
    sum_ <- sum_ + sum(data[, 1], na.rm = T)
    count <- count + sum(!is.na(data[, 1]))
  }

  sum_ / count
}
