
generate.data <- function(N) {

  # create query groups, with an average size of 25 items each
  num.queries <- floor(N/25)
  query <- sample(1:num.queries, N, replace=TRUE)

  # X1 is a variable determined by query group only
  query.level <- runif(num.queries)
  X1 <- query.level[query]

  # X2 varies with each item
  X2 <- runif(N)

  # X3 is uncorrelated with target
  X3 <- runif(N)

  # The target
  Y <- X1 + X2

  # Add some random noise to X2 that is correlated with
  # queries, but uncorrelated with items

  X2 <- X2 + scale(runif(num.queries))[query]

  # Add some random noise to target
  SNR <- 5 # signal-to-noise ratio
  sigma <- sqrt(var(Y)/SNR)
  Y <- Y + runif(N, 0, sigma)

  data.frame(Y, query=query, X1, X2, X3)
}


N=1000
data.train <- generate.data(N)

write.table(data.train, file = "foo.csv", sep = ",")



