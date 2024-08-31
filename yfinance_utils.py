import yfinance as yf
# tick = "MSFT"
# msft = yf.Ticker("MSFT")
# print(type(msft))

# print(type(msft.info))
# infoKeys = msft.info.keys()

# # with open("fields.txt", 'w') as f:
# #     for key in infoKeys:
# #        f.write("\n "+ key)

# k = "currentPrice"

# print(msft.info["currentPrice"])
# print(yf.Ticker(tick).info[k])

appl = yf.Ticker("MSFT")
print(appl)
#print(appl.info)
print(appl.info["shortName"])
print(appl.info["longName"])

def get_current_price(ticker_symbol: str) -> float:

#    print(f"Geting current price for{ticker_symbol}")
    yfinance_current_price_key = "currentPrice"
    return yf.Ticker(ticker_symbol).info[yfinance_current_price_key]

def get_stock_name(ticker_symbol: str) -> str:
    yfinance_name_key = "longName"
    return yf.Ticker(ticker_symbol).info[yfinance_name_key]