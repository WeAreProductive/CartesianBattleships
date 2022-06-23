
target "dapp" {
}

target "server" {
  tags = ["cartesi/dapp:battleships-devel-server"]
}

target "console" {
  tags = ["cartesi/dapp:battleships-devel-console"]
}

target "machine" {
  tags = ["cartesi/dapp:battleships-devel-machine"]
}
