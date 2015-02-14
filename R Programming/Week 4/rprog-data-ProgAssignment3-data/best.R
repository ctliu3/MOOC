best <- function(state, outcome) {
  ## Read outcome data
  data <- read.csv("outcome-of-care-measures.csv")
  data <- data[, c(2, 7, 11, 17, 23)]

  ## Check that state and outcome are valid
  states <- data[, 2]
  if (!(state %in% states)) {
    stop("invalid state")
  }
  
  outcomes <- c("heart attack", "heart failure", "pneumonia")
  if (!(outcome %in% outcomes)) {
    stop("invalid outcome")
  }

  ## Return hospital name in that state with lowest 30-day death
  ## rate
  if (outcome == "heart attack") {
    data <- data[, c(1:2, 3)]
  } else if (outcome == "heart failure") {
    data <- data[, c(1:2, 4)]
  } else {
    data <- data[, c(1:2, 5)]
  }

  colnames(data)[3] <- "specified"
  data <- subset(data, State == state)
  data[, 3] <- as.numeric(as.character(data[, 3]))
  minval <- min(data[, 3], na.rm = T)
  data <- subset(data, specified == minval)
  data <- as.vector(data[, 1])
  sort(data)[1]
}
