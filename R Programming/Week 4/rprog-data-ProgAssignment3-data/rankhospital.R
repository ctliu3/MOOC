rankhospital <- function(state, outcome, num = "best") {
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

  ## Return hospital name in that state with the given rank
  ## 30-day death rate
  if (outcome == "heart attack") {
    data <- data[, c(1:2, 3)]
  } else if (outcome == "heart failure") {
    data <- data[, c(1:2, 4)]
  } else {
    data <- data[, c(1:2, 5)]
  }

  colnames(data)[3] <- "Rate"
  data <- subset(data, State == state)
  data[, 3] <- as.numeric(as.character(data[, 3]))
  res <- data[order(data[, 3], data[, 1], na.last = NA), ]
  nres <- nrow(res)
  if (num == "best") {
    as.character(res[1, 1])
  } else if (num == "worst") {
    as.character(res[nres, 1])
  } else if (num <= nres) {
    as.character(res[num, 1])
  } else {
    NA
  }
}
