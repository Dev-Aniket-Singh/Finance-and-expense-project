from datetime import date,datetime
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from expense import Expense
# Activity 3: Problem decomposition - stock analysis module.
# Activity 6: Object modeling - StockAnalyzer class and its behaviors.
class StockAnalyzer:
    CURRENCY_SYMBOLS={
            "USD": "$", "INR": "₹", "JPY": "¥", "EUR": "€", "GBP": "£",
            "CNY": "¥", "HKD": "HK$", "SGD": "S$", "AUD": "A$", "CAD": "C$",
            "CHF": "CHF ", "KRW": "₩", "TWD": "NT$", "NZD": "NZ$", "AED": "AED ",
            "SAR": "SAR ", "ZAR": "R"
    }
    def get_currency_info(self,info=None):
        try:
            data=info if isinstance(info,dict) else self.stock.info
            self.currency_code=str(data.get("currency") or "USD").upper()
        except Exception:
            self.currency_code="USD"
        self.currency_symbol=self.CURRENCY_SYMBOLS.get(self.currency_code,self.currency_code+" ")
        return self.currency_code, self.currency_symbol
    def money(self,value):
        if value is None or value=="N/A":
            return "N/A"
        try:
            return f"{self.currency_symbol}{float(value):,.2f} {self.currency_code}"
        except (TypeError,ValueError):
            return f"{self.currency_symbol}{value} {self.currency_code}"
    def __init__(self,ticker):
        self.ticker=ticker.strip().upper()
        self.stock=yf.Ticker(self.ticker)
        self.currency_code="USD"
        self.currency_symbol="$"
    # Activity 7: Data interpretation - visualize historical stock prices.
    def plot_chart(self,series,title):
        if series.empty:
            print("\nNo Data Available To Plot Graph.")
            return
        plt.figure(figsize=(10,5))
        plt.plot(series.index,series.values,label="Close Price",color="#1f77b4",linewidth=2,marker="o",markersize=4)
        plt.title(title,fontsize=14,fontweight="bold")
        plt.xlabel("Date",fontsize=11)
        plt.ylabel(f"Price ({self.currency_code} - {self.currency_symbol.strip()})",fontsize=11)
        plt.grid(True,linestyle="--",alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()
    # Activity 7: Data interpretation - calculate and interpret historical risk statistics.
    def risk_analysis(self):
        print("\n"+" STOCK RISK & RETURN ANALYSIS ".center(90,"─"))
        benchmark=input("Enter Benchmark Ticker (default: ^GSPC): ").strip().upper() or "^GSPC"
        risk_free_rate=0.04
        try:
            stock_hist=self.stock.history(period="1y",auto_adjust=True)
            benchmark_hist=yf.Ticker(benchmark).history(period="1y",auto_adjust=True)
            if stock_hist.empty or "Close" not in stock_hist:
                print("\nUnable to Fetch Stock Price History.")
                return
            if benchmark_hist.empty or "Close" not in benchmark_hist:
                print(f"\nUnable to Fetch Benchmark Data for {benchmark}.")
                return
            stock_prices=stock_hist["Close"].dropna()
            benchmark_prices=benchmark_hist["Close"].dropna()
            stock_returns=stock_prices.pct_change().dropna()  # Daily percentage changes.
            benchmark_returns=benchmark_prices.pct_change().dropna()
            if stock_returns.index.tz is not None:
                stock_returns.index=stock_returns.index.tz_localize(None)
            if benchmark_returns.index.tz is not None:
                benchmark_returns.index=benchmark_returns.index.tz_localize(None)
            stock_returns.index=stock_returns.index.normalize()
            benchmark_returns.index=benchmark_returns.index.normalize()
            if len(stock_returns)<30:
                print("\nNot Enough Historical Data for Reliable Analysis.")
                return
            annual_return=((1+stock_returns).prod()**(252/len(stock_returns))-1)*100
            annual_volatility=stock_returns.std()*((252)**0.5)*100  # Assumes 252 trading days per year.
            daily_risk_free=(1+risk_free_rate)**(1/252)-1
            excess_returns=stock_returns-daily_risk_free
            if stock_returns.std()>0:
                sharpe_ratio=(excess_returns.mean()/stock_returns.std())*(252**0.5)
            else:
                sharpe_ratio=None
            wealth=(1+stock_returns).cumprod()
            wealth=pd.concat([pd.Series([1.0]),wealth.reset_index(drop=True)],ignore_index=True)
            drawdown=(wealth/wealth.cummax())-1
            max_drawdown=drawdown.min()*100  # Largest historical percentage decline from a peak.
            combined=pd.concat([stock_returns.rename("Stock"),benchmark_returns.rename("Benchmark")],axis=1).dropna()
            if len(combined)>=30 and combined["Benchmark"].var()>0:
                beta=combined["Stock"].cov(combined["Benchmark"])/combined["Benchmark"].var()
            else:
                beta=None
            period_return=((stock_prices.iloc[-1]/stock_prices.iloc[0])-1)*100
            print("\n"+"─"*90)
            print(f" STOCK: {self.ticker} | BENCHMARK: {benchmark}")
            print(" ANALYSIS PERIOD: Approximately 1 Year")
            print("─"*90)
            print(f" • Period Return          : {period_return:+.2f}%")
            print(f" • Annualized Return      : {annual_return:+.2f}%")
            print(f" • Annualized Volatility  : {annual_volatility:.2f}%")
            print(f" • Maximum Drawdown       : {max_drawdown:.2f}%")
            print(f" • Beta                   : {beta:.2f}" if beta is not None else " • Beta                   : N/A")
            print(f" • Sharpe Ratio           : {sharpe_ratio:.2f}" if sharpe_ratio is not None else " • Sharpe Ratio           : N/A")
            print("─"*90)
            print("\n RISK INTERPRETATION:")
            if annual_volatility<15:
                print(" • Volatility: Relatively Low")
            elif annual_volatility<30:
                print(" • Volatility: Moderate")
            else:
                print(" • Volatility: High")
            if beta is not None:
                if beta>1:
                    print(" • Market Sensitivity: Historically More Sensitive Than Benchmark")
                elif beta<1:
                    print(" • Market Sensitivity: Historically Less Sensitive Than Benchmark")
                else:
                    print(" • Market Sensitivity: Historically Similar To Benchmark")
            if max_drawdown<=-30:
                print(" • Drawdown: Experienced A Large Historical Decline")
            elif max_drawdown<=-15:
                print(" • Drawdown: Experienced A Notable Historical Decline")
            else:
                print(" • Drawdown: Historical Peak-To-Trough Decline Was Smaller")
            if sharpe_ratio is not None:
                if sharpe_ratio>1:
                    print(" • Risk-Adjusted Return: Historically Strong")
                elif sharpe_ratio>0:
                    print(" • Risk-Adjusted Return: Historically Positive")
                else:
                    print(" • Risk-Adjusted Return: Historically Weak")
            print("─"*90)
            print(" NOTE: These are historical measurements, not predictions or investment advice.")
            print(" Sharpe Ratio assumes a 4% annual risk-free rate.")
            print(" Beta uses only dates shared by the stock and benchmark.")
            print("─"*90)
        except Exception as e:
            print(f"\nUnable to Complete Risk Analysis: {e}")
    def run_menu(self):
        while True:
            print("\n"+"─"*90)
            print(f" ACTIVE COMPANY: [{self.ticker}]")
            print("─"*90)
            print("  1. Company Overview & Key Statistics")
            print("  2. Recent Price History & 1-Year Matplotlib Graph")
            print("  3. Annual Income Statement")
            print("  4. Annual Balance Sheet")
            print("  5. Annual Cash Flow Statement")
            print("  6. Analyst Recommendations")
            print("  7. Valuation Measures (P/E, PEG, Price-to-Book)")
            print("  8. Profitability & Margins (Profit Margin, ROE)")
            print("  9. Financial Health & Debt (Total Debt, Current Ratio)")
            print(" 10. Dividend & Yield Details")
            print(" 11. Growth & Earnings Metrics")
            print(" 12. Analyst Price Targets & Consensus")
            print(" 13. Ownership & Short Interest")
            print(" 14. 50-Day & 200-Day Moving Averages")
            print(" 15. Stock Risk & Return Analysis")
            print("─"*90)
            print("  0. Return to Main Menu")
            print("─"*90)
            choice=input("Select an Option (0-15):").strip()
            if choice=="0":
                break
            try:
                info=self.stock.info if choice in {"1","7","8","9","10","11","12","13","14"} else {}
                if info:
                    self.get_currency_info(info)
                if choice=="1":
                    print("\n"+ f" COMPANY OVERVIEW: {info.get('longName',self.ticker)} ".center(90,"─"))
                    print(f" • Sector         : {info.get('sector','N/A')}")
                    print(f" • Industry       : {info.get('industry','N/A')}")
                    print(f" • Current Price  : {self.money(info.get('currentPrice',info.get('regularMarketPrice','N/A')))}")
                    mcap=info.get("marketCap")
                    print(f" • Market Cap     : {self.money(mcap)}" if isinstance(mcap,(int,float)) else " • Market Cap     : N/A")
                    print(f" • 52-Week High   : {self.money(info.get('fiftyTwoWeekHigh','N/A'))}")
                    print(f" • 52-Week Low    : {self.money(info.get('fiftyTwoWeekLow','N/A'))}")
                    print("─"*90)
                if choice=="2":
                    self.get_currency_info()
                    hist=self.stock.history(period="1y")
                    if not hist.empty:
                        print("\n"+f" RECENT PRICE TABLE (Last 10 Days | {self.currency_code}) ".center(90,"─"))
                        print(hist[["Open","High","Low","Close","Volume"]].tail(10).to_string())
                        print("─"*90)
                        self.plot_chart(hist["Close"],title=f"{self.ticker} Share Price Trend (1 Year)")
                    else:
                        print("\nNo historical price data found.")
                if choice=="3":
                    print("\n"+" INCOME STATEMENT ".center(90,"─"))
                    smt=self.stock.financials
                    print(smt.head(10).to_string() if not smt.empty else "No data.")
                if choice=="4":
                    print("\n"+" BALANCE SHEET ".center(90,"─"))
                    bs=self.stock.balance_sheet
                    print(bs.head(10).to_string() if not bs.empty else "No data.")
                if choice=="5":
                    print("\n"+" CASH FLOW STATEMENT ".center(90,"─"))
                    cf=self.stock.cashflow
                    print(cf.head(10).to_string() if not cf.empty else "No data.")
                if choice=="6":
                    print("\n"+" ANALYST RECOMMENDATIONS ".center(90,"─"))
                    recs=self.stock.recommendations
                    print(recs.tail(5).to_string() if recs is not None and not recs.empty else "No recommendations.")
                if choice=="7":
                    print("\n"+" VALUATION MEASURES ".center(90,"─"))
                    print(f" • Trailing P/E   : {info.get('trailingPE','N/A')}")
                    print(f" • Forward P/E    : {info.get('forwardPE','N/A')}")
                    print(f" • PEG Ratio      : {info.get('pegRatio','N/A')}")
                    print(f" • Price to Book  : {info.get('priceToBook','N/A')}")
                if choice=="8":
                    print("\n"+" PROFITABILITY & MARGINS ".center(90,"─"))
                    print(f" • Profit Margin  : {info.get('profitMargins',0)*100 if info.get('profitMargins') else 'N/A'}%")
                    print(f" • Operating Margin: {info.get('operatingMargins',0)*100 if info.get('operatingMargins') else 'N/A'}%")
                    print(f" • Return on Equity: {info.get('returnOnEquity',0)*100 if info.get('returnOnEquity') else 'N/A'}%")
                if choice=="9":
                    print("\n"+" FINANCIAL HEALTH & DEBT ".center(90,"─"))
                    tc=info.get("totalCash")
                    print(f" • Total Cash     : {self.money(tc)}" if isinstance(tc,(int,float)) else " • Total Cash     : N/A")
                    td=info.get("totalDebt")
                    print(f" • Total Debt     : {self.money(td)}" if isinstance(td,(int,float)) else " • Total Debt     : N/A")
                    print(f" • Debt to Equity : {info.get('debtToEquity','N/A')}")
                    print(f" • Current Ratio  : {info.get('currentRatio','N/A')}")
                if choice=="10":
                    print("\n"+" DIVIDEND & YIELD DETAILS ".center(90,"─"))
                    print(f" • Dividend Rate  : {self.money(info.get('dividendRate','N/A'))}")
                    print(f" • Dividend Yield : {info.get('dividendYield',0)*100 if info.get('dividendYield') else 0}%")
                    print(f" • Payout Ratio   : {info.get('payoutRatio',0)*100 if info.get('payoutRatio') else 0}%")
                if choice=="11":
                    print("\n"+" GROWTH & EARNINGS METRICS ".center(90,"─"))
                    print(f" • Earnings Growth: {info.get('earningsGrowth',0)*100 if info.get('earningsGrowth') else 'N/A'}%")
                    print(f" • Revenue Growth : {info.get('revenueGrowth',0)*100 if info.get('revenueGrowth') else 'N/A'}%")
                if choice=="12":
                    print("\n"+" ANALYST TARGETS & CONSENSUS ".center(90,"─"))
                    print(f" • Target Mean Price : {self.money(info.get('targetMeanPrice','N/A'))}")
                    print(f" • Recommendation Key: {str(info.get('recommendationKey','N/A')).upper()}")
                if choice=="13":
                    print("\n"+" OWNERSHIP & SHORT INTEREST ".center(90,"─"))
                    so=info.get("sharesOutstanding")
                    print(f" • Shares Outstanding: {so:,}" if isinstance(so,(int,float)) else " • Shares Outstanding: N/A")
                    print(f" • Held by Insiders  : {info.get('heldPercentInsiders',0)*100 if info.get('heldPercentInsiders') else 'N/A'}%")
                    print(f" • Short % of Float  : {info.get('shortPercentOfFloat',0)*100 if info.get('shortPercentOfFloat') else 'N/A'}%")
                if choice=="14":
                    print("\n"+" MOVING AVERAGES (TREND ANALYSIS) ".center(90,"─"))
                    print(f" • 50-Day Moving Average  : {self.money(info.get('fiftyDayAverage', 'N/A'))}")
                    print(f" • 200-Day Moving Average : {self.money(info.get('twoHundredDayAverage','N/A'))}")
                    print("-"*90)
                if choice=="15":
                    self.risk_analysis()
            except Exception as e:
                print(f"\nError fetching data: {e}")
# Activity 3: Problem decomposition - portfolio tracking module.
# Activity 6: Object modeling - PortfolioTracker class and its attributes.
class PortfolioTracker:
    def __init__(self):
        self.watchlist=[]
        self.realized_trades=[]
        self.transaction_history=[]
    def get_stock_info(self,ticker):
        stk=yf.Ticker(ticker)
        info=stk.info or {}
        cp=info.get("currentPrice") or info.get("regularMarketPrice")
        if cp is None or cp<=0:
            hist=stk.history(period="1d")
            if not hist.empty:
                cp=hist["Close"].iloc[-1]
            else:
                cp=0.0
        return info,float(cp)
    # Activity 7: Data interpretation - display transaction history.
    def transaction_history_report(self):
        if not self.transaction_history:
            print("\nNo Transactions Recorded Yet.")
            return
        print("\n"+" COMPLETE TRANSACTION HISTORY ".center(90,"─"))
        for i,trade in enumerate(self.transaction_history,1):
            sym=trade["currency_symbol"]
            code=trade["currency"]
            print(f"\n{i}. [{trade['ticker']}] — {trade['type']}")
            print(f" • Date       : {trade['date']}")
            print(f" • Shares     : {trade['shares']}")
            print(f" • Price      : {sym}{trade['price']:,.2f} {code}")
            print(f" • Fees       : {sym}{trade['fees']:,.2f} {code}")
            print(f" • Platform   : {trade['platform']}")
            if trade["type"]=="SELL":
                print(f" • Allocated Buy Fees: {sym}{trade['buy_fees']:,.2f} {code}")
                print(f" • Realized P&L      : {sym}{trade['realized_pnl']:+,.2f} {code}")
            print("─"*90)
    def run_menu(self):
        while True:
            print("\n"+"─"*90)
            print(" MODULE 2: STOCK PORTFOLIO & TRADING TRACKER")
            print("─"*90)
            print("  1. Add Stock, Shares, Price & Buying Platform")
            print("  2. View Live Portfolio Valuation & Unrealized P&L")
            print("  3. Sell Shares at Current Market Price")
            print("  4. View Realized Trade History")
            print("  5. Analyze Best & Worst Performers")
            print("  6. View Portfolio Sector Breakdown")
            print("  7. View Complete Transaction History")
            print("  0. Return to Main Menu")
            print("─"*90)
            choice=input("Choose an Option (1-7 or 0):").strip()
            if choice=="0":
                break
            elif choice=="1":
                ticker=(input("Enter Ticker Symbol (e.g.: AAPL, MSFT, TSLA, etc.): ").strip().upper())
                if ticker:
                    try:
                        shares=float(input(f" Enter Number of Shares Owned for {ticker}:"))
                        buy_price=float(input("Enter Average Purchase Price Per Share:"))
                        if shares<=0 or buy_price<=0:
                            print("\nShares and Purchase Price Must Be Greater Than Zero.")
                            continue
                        buy_platform=(input("Enter Buying Platform (e.g.: Zerodha, Groww, Upstox, etc.):").strip() or "Unknown")
                        buy_fees=float(input("Enter Buying Fees/Charges (0 if none):") or 0)
                        if buy_fees<0:
                            print("\nFees Cannot Be Negative.")
                            continue
                        analyzer=StockAnalyzer(ticker)
                        info=analyzer.stock.info
                        currency_code,currency_symbol=analyzer.get_currency_info(info)
                        self.watchlist.append({
                            "ticker": ticker,
                            "shares": shares,
                            "buy_price": buy_price,
                            "buy_platform": buy_platform,
                            "buy_fees": buy_fees,
                            "currency": currency_code,
                            "currency_symbol": currency_symbol
                        })
                        self.transaction_history.append({
                            "type": "BUY",
                            "ticker": ticker,
                            "shares": shares,
                            "price": buy_price,
                            "fees": buy_fees,
                            "platform": buy_platform,
                            "date": date.today().isoformat(),
                            "currency": currency_code,
                            "currency_symbol": currency_symbol
                        })
                        print(f"\nSuccess! Added {ticker} to your Portfolio.")
                    except ValueError:
                        print("\nInvalid Numeric Input Entered.")
                    except Exception as e:
                        print(f"\nCouldn't Fetch Stock Information: {e}")
                else:
                    print("\nInvalid Ticker.")
            elif choice == "2":
                if not self.watchlist:
                    print("\nYour Portfolio Watchlist is currently Empty.")
                else:
                    print("\n"+" LIVE PORTFOLIO PERFORMANCE REPORT ".center(90,"-"))
                    currency_totals={}
                    for i,item in enumerate(self.watchlist,1):
                        t,s,bp=item["ticker"],item["shares"],item["buy_price"]
                        currency_code=item.get("currency","USD")
                        currency_symbol=item.get("currency_symbol",StockAnalyzer.CURRENCY_SYMBOLS.get(currency_code,currency_code+" "))
                        try:
                            info,cp=self.get_stock_info(t)
                            cb=(s*bp)+item.get("buy_fees",0)
                            hv=s*cp
                            pl=hv-cb
                            ret=(pl/cb)*100 if cb>0 else 0
                            currency_totals.setdefault(currency_code,[0.0,0.0])
                            currency_totals[currency_code][0]+=cb
                            currency_totals[currency_code][1]+=hv
                            print(f" {i}. [{t}] — {s} Shares")
                            print(f"    Buying Platform: {item.get('buy_platform','Unknown')}")
                            print(f"    Currency: {currency_code}")
                            print(f"    Buy Avg: {currency_symbol}{bp:,.2f} | Current Price: {currency_symbol}{cp:,.2f}")
                            print(f"    Invested: {currency_symbol}{cb:,.2f} | Market Val: {currency_symbol}{hv:,.2f}")
                            print(f"    Unrealized P&L: {currency_symbol}{pl:+,.2f} ({ret:+.2f}%)")
                            print("─"*90)
                        except Exception as e:
                            print(f" {i}. [{t}] — Couldn't Fetch Live Data: {e}")
                    print(" PORTFOLIO SUMMARY (Kept Separate By Currency):")
                    for code,(inv,val) in currency_totals.items():
                        net=val-inv
                        net_ret=(net/inv)*100 if inv>0 else 0
                        sym=StockAnalyzer.CURRENCY_SYMBOLS.get(code,code+" ")
                        print(f"  • {code}: Cost {sym}{inv:,.2f} | Value {sym}{val:,.2f} | P&L {sym}{net:+,.2f} ({net_ret:+.2f}%)")
                    print("─"*90)
            elif choice=="3":
                if not self.watchlist:
                    print("\nNo Stocks Available in Portfolio to Sell.")
                else:
                    print("\n Select a Stock To Sell Shares From:")
                    for i,item in enumerate(self.watchlist,1):
                        print(f"  {i}. {item['ticker']} ({item['shares']} shares available)")
                    try:
                        sel=int(input(" Enter stock number:").strip())
                        if 1<=sel<=len(self.watchlist):
                            holding=self.watchlist[sel-1]
                            t=holding["ticker"]
                            currency_code=holding.get("currency","USD")
                            currency_symbol=holding.get("currency_symbol",StockAnalyzer.CURRENCY_SYMBOLS.get(currency_code,currency_code+" "))
                            info,cp=self.get_stock_info(t)
                            if cp<=0:
                                print("Couldn't Fetch a Valid Current Market Price.")
                                continue
                            print(f"Current Market Price: {currency_symbol}{cp:,.2f} {currency_code} per share")
                            selling=float(input(f" Enter Number of Shares to Sell (max {holding['shares']}):").strip())
                            if not 0<selling<=holding["shares"]:
                                print("\nInvalid Share Quantity Specified.")
                                continue
                            sell_platform=input("Enter Selling Platform (e.g.: Zerodha, Groww, Upstox, etc.): ").strip() or "Unknown"
                            sell_fees=float(input("Enter Selling Fees/Charges (0 if none):") or 0)
                            if sell_fees<0:
                                print("\nFees Cannot Be Negative.")
                                continue
                            if 0<selling<=holding["shares"]:
                                cost_sold=selling*holding["buy_price"]
                                proceeds=selling*cp
                                buy_fees=holding.get("buy_fees",0)*(selling/holding["shares"])  # Allocates buy fees to the shares sold.
                                real=proceeds-cost_sold-buy_fees-sell_fees
                                real_pct=(real/(cost_sold+buy_fees))*100 if cost_sold+buy_fees>0 else 0
                                self.transaction_history.append({
                                    "type": "SELL",
                                    "ticker": t,
                                    "shares": selling,
                                    "price": cp,
                                    "buy_fees": buy_fees,
                                    "realized_pnl": real,
                                    "fees": sell_fees,
                                    "platform": sell_platform,
                                    "date": date.today().isoformat(),
                                    "currency": currency_code,
                                    "currency_symbol": currency_symbol
                                })
                                holding["buy_fees"]=holding.get("buy_fees",0)-buy_fees
                                self.realized_trades.append({
                                        "ticker": t,
                                        "shares_sold": selling,
                                        "buy_price": holding["buy_price"],
                                        "sell_price": cp,
                                        "buy_platform": holding.get("buy_platform", "Unknown"),
                                        "sell_platform": sell_platform,
                                        "realized_pnl": real,
                                        "currency": currency_code,
                                        "currency_symbol": currency_symbol
                                })
                                holding["shares"]-=selling
                                if holding["shares"]<=0.00000001:
                                    self.watchlist.pop(sel-1)
                                print(f"\nSale Executed Successfully!")
                                print(f"  • Shares Sold    : {selling}")
                                print(f"  • Sell Platform  : {sell_platform}")
                                print(f"  • Execution Price: {currency_symbol}{cp:,.2f} {currency_code}")
                                print(f"  • Total Proceeds : {currency_symbol}{proceeds:,.2f} {currency_code}")
                                print(f"  • Realized P&L   : {currency_symbol}{real:+,.2f} {currency_code} ({real_pct:+.2f}%)")
                            else:
                                print("\nInvalid Share Quantity Specified.")
                        else:
                            print("\nInvalid Selection Number.")
                    except ValueError:
                        print("\nPlease, Enter Valid Numbers.")
                    except Exception as e:
                        print(f"\nCouldn't Complete the Sale: {e}")
            elif choice=="4":
                if not self.realized_trades:
                    print("\nNo Completed Trades Recorded Yet.")
                else:
                    print("\n"+" REALIZED TRADE HISTORY ".center(90,"─"))
                    currency_totals={}
                    for i,trade in enumerate(self.realized_trades,1):
                        sym=trade.get("currency_symbol","$")
                        code=trade.get("currency","USD")
                        real=trade["realized_pnl"]
                        print(f"{i}. [{trade['ticker']}] — Sold {trade['shares_sold']} shares")
                        print(f"Bought: {sym}{trade['buy_price']:,.2f} {code} ({trade.get('buy_platform','Unknown')})")
                        print(f"Sold:   {sym}{trade['sell_price']:,.2f} {code} ({trade.get('sell_platform','Unknown')})")
                        print(f"Realized P&L: {sym}{real:+,.2f} {code}")
                        print("─"*90)
                        currency_totals[code]=currency_totals.get(code,0.0)+real
                    print(" TOTAL REALIZED P&L (SEPARATE BY CURRENCY):")
                    for code,prof in currency_totals.items():
                        sym=StockAnalyzer.CURRENCY_SYMBOLS.get(code,code+" ")
                        print(f" • {code}: {sym}{prof:+,.2f} {code}")
                    print("─"*90)
            elif choice=="5":
                if not self.watchlist:
                    print("\nWatchlist is Empty.")
                else:
                    print("\n"+" PORTFOLIO PERFORMANCE SCANNER ".center(90, "─"))
                    bst,wst,maxi,mini=None,None,-999999,999999
                    for item in self.watchlist:
                        t,bp=item["ticker"],item["buy_price"]
                        try:
                            info,curr=self.get_stock_info(t)
                            cost=item["shares"]*bp+item.get("buy_fees",0)
                            value=item["shares"]*curr
                            if curr>0 and cost>0:
                                ret=((value-cost)/cost)*100
                                if ret>maxi:
                                    maxi,bst=ret,(t,ret)
                                if ret<mini:
                                    mini,wst=ret,(t,ret)
                        except Exception as e:
                            print(f" Couldn't Fetch Data for {t}: {e}")
                    if bst:
                        print(f" Best Performer: [{bst[0]}] with {bst[1]:+.2f}% return")
                    if wst:
                        print(f" Worst Performer: [{wst[0]}] with {wst[1]:+.2f}% return")
                    print("─"*90)
            elif choice=="6":
                if not self.watchlist:
                    print("\nWatchlist is Empty.")
                else:
                    print("\n"+" PORTFOLIO SECTOR ALLOCATION ".center(90,"─"))
                    total={}
                    for item in self.watchlist:
                        try:
                            info,cp=self.get_stock_info(item["ticker"])
                            sec=info.get("sector","Unknown")
                            val=item["shares"]*cp if cp>0 else item["shares"]*item["buy_price"]
                            key=(sec,item.get("currency","USD"))
                            total[key]=total.get(key,0.0)+val
                        except Exception:
                            key=("Unknown",item.get("currency","USD"))
                            total[key]=total.get(key,0.0)+item["shares"]*item["buy_price"]
                    for code in sorted({code for sec,code in total}):
                        sym=StockAnalyzer.CURRENCY_SYMBOLS.get(code,code+" ")
                        print(f"\n {code} SECTOR ALLOCATION:")
                        for (sec,curr),val in sorted(total.items(),key=lambda x:x[1],reverse=True):
                            if curr==code:
                                print(f" • {sec:<25} : {sym}{val:>10,.2f} {code}")
                    print("─"*90)
            elif choice=="7":
                self.transaction_history_report()
            else:
                print("\nInvalid choice, Please Try again.")
# Activity 3: Problem decomposition - separate expense menu and method calls.
# Activity 6: Object modeling - interact with the existing Expense object.
def expense_menu(expenses):
    while True:
        print("\n"+"─"*90)
        print(" MODULE 3: DAILY EXPENSE & THRESHOLD TRACKER")
        print("─"*90)
        print("  1. Add Daily Expense")
        print("  2. View Daily Expense Report")
        print("  3. Edit / Delete Expense")
        print("  4. Search Expenses")
        print("  5. Monthly Expense Dashboard & Threshold Warning")
        print("  6. Category Spending Analytics")
        print("  7. Set Monthly Expense Threshold Limit")
        print("  8. Monthly Savings Rate Calculator")
        print("  9. Recurring Expense Manager")
        print("  0. Return to Main Menu")
        print("─"*90)
        choice=input("Select an option (0-9):").strip()
        if choice=="0":
            break
        elif choice=="1":
            expenses.add()
        elif choice=="2":
            expenses.view()
        elif choice=="3":
            expenses.edit_or_delete()
        elif choice=="4":
            expenses.search()
        elif choice=="5":
            expenses.monthly_summary()
        elif choice=="6":
            expenses.analytics()
        elif choice=="7":
            expenses.threshold()
        elif choice=="8":
            expenses.calculator()
        elif choice=="9":
            expenses.recurring_manager()
        else:
            print("\nInvalid Option, Please Try Again.")
# Activity 2: Flowchart 1 - main menu choices, loop and exit.
# Activity 3: Problem decomposition - coordinate the three modules.
# Activity 6: Object modeling - create objects and call their methods.
def main():
    portfolio=PortfolioTracker()
    expenses=Expense()  # Creates the expense tracker object.
    while True:
        print("\n"+"─"*90)
        print(" PERSONAL FINANCE & INVESTMENT SYSTEM (OOP) ")
        print("─"*90)
        print("  1. Share Price & Fundamental Analyzer")
        print("  2. Stock Portfolio & Trading Tracker")
        print("  3. Daily Expense & Threshold Tracker")
        print("  0. Exit Program")
        print("─"*90)
        choice=input("Select an option (1, 2, 3 or 0):").strip()
        if choice=="1":
            ticker=(input("Enter Stock Ticker Symbol (e.g.: AAPL, MSFT, TSLA, RELIANCE.NS, etc.): ").strip().upper())
            if ticker:
                analyzer=StockAnalyzer(ticker)
                analyzer.run_menu()
        elif choice=="2":
            portfolio.run_menu()
        elif choice=="3":
            expense_menu(expenses)
        elif choice=="0":
            print("\nExiting Application, Goodbye!")
            break
        else:
            print("\nInvalid Option, Please Choose Correct Option!")
if __name__=="__main__":
    main()
