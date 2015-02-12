complete <- function(directory, id = 1:332) {
  nobs <- vector(mode = "numeric", length = length(id))
  n <- 1

  for (id_ in id) {
    filename <- paste(directory, sprintf("%03d.csv", id_), sep = "/")
    data <- read.csv(filename, colClasses = c("NULL", NA, NA, "NULL"))
    nobs[n] = nrow(data[!is.na(data$sulfate) & !is.na(data$nitrate), ])
    n <- n + 1
  }

  data.frame(cbind(id, nobs))
}
