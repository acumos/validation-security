import gensim

text = '''
Citigroup earnings boosted by trading results.Citigroup Inc. said its first-quarter profit rose 17% as its trading desk continued to be boosted by companies and investors preparing for rising interest rates.
Quarterly profit at the New York-based bank increased to $4.09 billion from $3.50 billion a year earlier. Per-share earnings were $1.35. After stripping out one-time gains and losses from exits and sales of businesses, the bank earned $1.27 a share.
Analysts, on average, had expected $1.24 a share, according to Thomson Reuters. Revenue was $18.12 billion, up from $17.56 billion a year ago. Analysts had expected $17.76 billion.
Like other banks, Citigroup has benefited from the rate increases by the Federal Reserve. That has been a boon for bond and currency trading desks, as investors seek ways to profit or hedge, and companies try to lock-in cheap financing rates.
The fear that potential trade conflicts sparked by President Donald Trump's tough stance on open borders would disproportionately affect Citigroup, which is deeply involved in cross-border money transfers, hasn't yet been felt by the bank.
Citigroup's shares have jumped 17% since the election, closing the gap with other bank stocks, which had rallied more. The KBW Nasdaq bank index is up 19% since Mr. Trump's victory. In premarket trading Thursday, the stock slipped 0.1% to $58.43.
The bank's first-quarter trading revenue, excluding an accounting adjustment, increased 17% to $4.39 billion from $3.75 billion a year ago. Fixed-income trading showed stronger growth, rising 19%, than equities trading, which improved by 10% from a year ago.
The 17% increase in trading revenue was better than what Chief Financial Officer John Gerspach predicted last month, when he said he expected trading revenue to be up by a percentage in the low-double digits from a year ago. Citi's figure tops rival J.P. Morgan Chase & Co.'s 13% gain in trading.
Investment banking also surged in the first quarter, with revenue rising 39% from a year ago, to $1.21 billion, led by a near-doubling of equity underwriting revenue and a 39% jump in debt underwriting.
Quarterly revenue at the consumer bank added 1% to $7.82 billion. Global consumer banking profit was off by 16%, to $1.00 billion, with the biggest drop in North America, down 25%.
Quarterly expenses slid slightly, to $10.48 billion from $10.52 billion a year earlier.
'''
striptext = text.replace('\n\n', ' ')
striptext = striptext.replace('\n', ' ')


keywords = gensim.summarization.keywords(striptext)
print(keywords)
keywords_list = keywords.split()


dict = ['verizon', 'AT&T']

def keyword_search():
    for i in keywords_list:
        if i in dict:
            return "Fail"
    
        else:
            return "Pass"