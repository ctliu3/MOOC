rankall <- function(outcome, num = "best") {
  ## Read outcome data
  data <- read.csv("outcome-of-care-measures.csv")
  data <- data[, c(2, 7, 11, 17, 23)]

  ## Check that state and outcome are valid
  outcomes <- c("heart attack", "heart failure", "pneumonia")
  if (!(outcome %in% outcomes)) {
    stop("invalid outcome")
  }

  ## For each state, find the hospital of the given rank
  ## Return a data frame with the hospital names and the
  ## (abbreviated) state name
  if (outcome == "heart attack") {
    data <- data[, c(1:2, 3)]
  } else if (outcome == "heart failure") {
    data <- data[, c(1:2, 4)]
  } else {
    data <- data[, c(1:2, 5)]
  }

  n <- 1
  states <- as.character(data[, 2])
  states <- states[!duplicated(states)]
  states <- states[order(states)]
  nstate <- length(states)
  hospital <- vector(mode = "character", length = nstate)
  state <- vector(mode = "character", length = nstate)

  for (cur in states) {
    colnames(data)[3] <- "Rate"
    sub <- subset(data, State == cur)
    sub[, 3] <- as.numeric(as.character(sub[, 3]))
    res <- sub[order(sub[, 3], sub[, 1], na.last = NA), ]
    nres <- nrow(res)
    if (num == "best") {
      hospital[n] <- as.character(res[1, 1])
    } else if (num == "worst") {
      hospital[n] <- as.character(res[nres, 1])
    } else if (num <= nres) {
      hospital[n] <- as.character(res[num, 1])
    } else {
      hospital[n] <- NA
    }
    state[n] <- cur
    n <- n + 1
  }
  data.frame(cbind(hospital, state))
}
