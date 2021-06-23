from dataclasses import dataclass
import QuantLib as ql

class Bond:
    def __init__(self):
        self.code: str = '111111.IB'
        self.buy_date: str = '2020-01-01'  # YYYY-MM-DD
        self.buy_clean_price: float = 100
        self.sell_date: str = '2021-03-15'  # YYYY-MM-DD
        self.sell_clean_price: float = 102

        self.issue_date: str = '2019-01-01'
        self.maturity_date: str = '2039-01-01'
        self.coupon_rate: float = 0.05
        self.tenor: int = 6
        self.accrual_method = ql.ActualActual()
        self.settlement: int = 0

        self.bond_ql = self.create_bond_ql()

    def create_bond_ql(self) -> ql.FixedRateBond:
        issue_date = ql.Date(self.issue_date, '%Y-%m-%d')
        maturity = ql.Date(self.maturity_date, '%Y-%m-%d')
        tenor = ql.Period(self.tenor, ql.Months)
        daycount_convention = self.accrual_method

        Bond_ql = ql.FixedRateBond(self.settlement,
                                   ql.China(),
                                   100,
                                   issue_date,
                                   maturity,
                                   tenor,
                                   [self.coupon_rate],
                                   daycount_convention)

        return Bond_ql


def bond_yield(bond: Bond) -> float:
    ql.Settings.instance().evaluationDate = ql.Date(bond.buy_date, '%Y-%m-%d')

    Bond_ql = bond.bond_ql

    return Bond_ql.bondYield(bond.buy_clean_price,
                             Bond_ql.dayCounter(),
                             ql.Compounded,
                             Bond_ql.frequency())


def hpy(bond: Bond, annualized: bool = False) -> float:
    # (sell_dirty + coupon_received) / buy_dirty

    Bond_ql = bond.bond_ql
    buy_date = ql.Date(bond.buy_date, '%Y-%m-%d')
    sell_date = ql.Date(bond.sell_date, '%Y-%m-%d')

    ql.Settings.instance().evaluationDate = buy_date
    buy_dirty = bond.buy_clean_price + Bond_ql.accruedAmount()

    ql.Settings.instance().evaluationDate = sell_date
    sell_dirty = bond.sell_clean_price + Bond_ql.accruedAmount()

    coupon_between = [c.amount() for c in Bond_ql.cashflows()
                      if buy_date < c.date() <= sell_date]
    coupon_received = sum(coupon_between)

    hpy = (sell_dirty + coupon_received) / buy_dirty - 1
    if not annualized:
        return hpy

    # Annualize hpy
    f = bond.bond_ql.dayCounter().yearFraction
    buy_date = ql.Date(bond.buy_date, '%Y-%m-%d')
    sell_date = ql.Date(bond.sell_date, '%Y-%m-%d')

    year_faction = f(buy_date, sell_date)
    hpy_annualized = (1 + hpy) ** (1/year_faction) - 1
    return hpy_annualized


def hpy_repo(bond: Bond, annualized: bool = False) -> float:
    # (sell_dirty + coupon_received) / buy_dirty

    Bond_ql = bond.bond_ql
    buy_date = ql.Date(bond.buy_date, '%Y-%m-%d')
    sell_date = ql.Date(bond.sell_date, '%Y-%m-%d')

    ql.Settings.instance().evaluationDate = buy_date
    buy_dirty = bond.buy_clean_price + Bond_ql.accruedAmount()

    ql.Settings.instance().evaluationDate = sell_date
    sell_dirty = bond.sell_clean_price + Bond_ql.accruedAmount()

    coupon_between = [c.amount() for c in Bond_ql.cashflows()
                      if buy_date < c.date() <= sell_date]
    coupon_received = sum(coupon_between)

    repo_hpy = (sell_dirty - buy_dirty + coupon_received) / buy_dirty
    if not annualized:
        return repo_hpy

    f = bond.bond_ql.dayCounter().yearFraction
    buy_date = ql.Date(bond.buy_date, '%Y-%m-%d')
    sell_date = ql.Date(bond.sell_date, '%Y-%m-%d')

    year_faction = f(buy_date, sell_date)
    hpy_annualized = (1 + repo_hpy) ** (1/year_faction) - 1
    return repo_hpy_annualized


def get_coupon_received(bond: Bond):
    Bond_ql = bond.bond_ql
    buy_date = ql.Date(bond.buy_date, '%Y-%m-%d')
    sell_date = ql.Date(bond.sell_date, '%Y-%m-%d')

    coupon_between = [c.amount() for c in Bond_ql.cashflows()
                      if buy_date < c.date() <= sell_date]
    coupon_received = sum(coupon_between)
    return coupon_received

if __name__ == '__main__':
    b = Bond()
    print(bond_yield(b))
    print(hpy(b))
    print(hpy_repo(b))
    print(get_coupon_received(b))
