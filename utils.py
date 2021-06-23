import QuantLib as ql
import pandas as pd
from WindPy import *
import numpy as np
import datetime

w.start()
today = datetime.date.today().strftime('%Y-%m-%d')


def get_basic_info(code: str) -> dict:
    # 获取左上部分信息

    info = w.wsd(code, "exch_city,exchange_cn,sec_type", "ED0D", today, "PriceAdj=CP")
    info = np.ravel(info.Data)
    info2 = w.wss(code, "coupon").Data[0][0]
    basic_info = {'location': info[0],
                  'platform': info[1],
                  'quote_convention': '',
                  'category': info[2],
                  'settlement': ''}

    return basic_info


def get_quote(code: str) -> pd.DataFrame:
    quote_df = pd.DataFrame(None, index=['code', 'clean', 'full', 'yield'],
                            columns=['IB', 'SH', 'SZ'])
    code_ib = w.wsd(code, "relationCode", "ED0D", today, "exchangeType=NIB").Data[0][0]
    quote_ib = w.wsq(code_ib, "rt_last_dp,rt_last_cp,rt_last_ytm").Data
    quote_ib.insert(0, [code_ib])
    quote_df['IB'] = pd.Series(np.ravel(quote_ib), index=quote_df.index)

    code_sh = w.wsd(code, "relationCode", "ED0D", today, "exchangeType=SSE").Data[0][0]
    quote_sh = w.wsq(code_sh, "rt_last_dp,rt_last_cp,rt_last_ytm").Data
    quote_sh.insert(0, [code_sh])
    quote_df['SH'] = pd.Series(np.ravel(quote_sh), index=quote_df.index)

    code_sz = w.wsd(code, "relationCode", "ED0D", today, "exchangeType=SZSE").Data[0][0]
    quote_sz = w.wsq(code_sz, "rt_last_dp,rt_last_cp,rt_last_ytm").Data
    quote_sz.insert(0, [code_sz])
    quote_df['SZ'] = pd.Series(np.ravel(quote_sz), index=quote_df.index)

    return quote_df


def get_issue_date(code: str) -> float:
    return w.wss(code, "issue_date").Data[0][0].strftime('%Y-%m-%d')


def get_coupon_rate(code: str) -> float:
    return w.wss(code, "couponrate2").Data[0][0]


def get_maturity_date(code: str) -> str:
    return w.wss(code, "maturitydate").Data[0][0].strftime('%Y-%m-%d')


def get_tenor(code: str) -> int:
    return int(12/w.wss(code, "interestfrequency").Data[0][0])


def get_accrural_method(code: str) -> float:
    return w.wss(code, "coupon").Data[0][0]


def convert_accrural_method(accrural_method: str) -> ql.DayCounter:
    pass
