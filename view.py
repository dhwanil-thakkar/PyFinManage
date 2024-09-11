from portfolioManager import Portfolio, Stock




portfolio_a = Portfolio("WelathSimplePortfolio")

microsoft_stock = Stock("MSFT")
apple_stock = Stock("AAPL")

portfolio_a.add_stock_to_portfolio(stock = microsoft_stock, purchase_quantity=100, buying_price=50)
portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=50)

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=100)

portfolio_a.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=200)

print("\n\n PORTFOLIO A \n\n")
portfolio_a.get_positions()




portfolio_b = Portfolio("2nd Portfolio")


portfolio_b.add_stock_to_portfolio(stock = microsoft_stock, purchase_quantity=100, buying_price=50)
portfolio_b.add_stock_to_portfolio(stock = apple_stock, purchase_quantity=100, buying_price=50)


print("\n\n PORTFOLIO b \n\n")
portfolio_b.get_positions()
print("\n\n")

