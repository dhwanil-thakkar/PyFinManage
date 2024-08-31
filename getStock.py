import yfinance as yf

msft = yf.Ticker("MSFT")
print(msft)

print(type(msft.info))
infoKeys = msft.info.keys()

# for key in infoKeys:
#     print(f"{key}")

print(msft.info["currentPrice"])
print(msft.info["sector"])
print(msft.info["industry"])
#print(msft.financials)
print(msft.analyst_price_targets)
#print(msft.actions)
print(msft.)