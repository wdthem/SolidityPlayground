1. Swap ETH for WETH
2. Deposit WETH into Aave
3. Borrow some asset with the ETH collateral
    1. Sell that borrowed asset (short selling) - EXTRA CHALLENGE
4. Repay everything back


Testing:

Integration test: Rinkeby
Unit tests: Mainnet-fork - mock the entire mainnet

(
    if you have no oracles, you can use mainnet-fork for testing
    Default testing network is Development with Mocking
)