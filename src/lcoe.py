"""

Geothermal direct-heat LCOE model.

Translated from LCOE.xlsx
Authors: Jan-Diederik van Wees, Lars ten Kulve, Derk Straathof, Maarten Pluymaekers 
Date: 10-07-2011
Sources: Cash flow methodology is largely based on dutch economic models and spreadsheets developed by Energie Centrum Nederland (ECN, www.ecn.nl)
Version: 2012.1

Reproduces:
  - subsurface capex (well drilling cost scaling + stimulation + pumps)
  - surface heat-plant capex
  - annual cash flows over the project lifetime (revenue, opex, depreciation,
    debt amortization, tax)
  - debt/equity financed NPV, discounted at the required equity return
  - LCOE solved as the flat €/GJ price that makes the equity investor's NPV
    equal to their equity outlay

"""

import numpy as np

# ---------------------------------------------------------------------
# Financial helpers
# ---------------------------------------------------------------------

def npv(rate, cashflows):
    """Excel NPV convention: first cashflow occurs at the end of the first period"""
    cashflows = np.asarray(cashflows, dtype=float)
    periods = np.arange(1, len(cashflows) + 1)
    return np.sum(cashflows / (1 + rate) ** periods)


def loan_amortization_schedule(rate, nper, principal):
    """
    Returns (interest, principal_payment) arrays, length nper, following
    Excel's IPMT/PPMT sign convention (values are negative = cash outflow).
    Constant total payment (fixed-rate annuity), fv=0, type=0.
    """
    if nper <= 0 or principal <= 0:
        return np.zeros(max(nper, 0)), np.zeros(max(nper, 0))

    if rate == 0:
        pmt = -principal / nper
    else:
        pmt = -principal * rate / (1 - (1 + rate) ** (-nper))

    interest = np.zeros(nper)
    principal_paid = np.zeros(nper)
    balance = principal
    for t in range(nper):
        interest[t] = -balance * rate
        principal_paid[t] = pmt - interest[t]
        balance += principal_paid[t]
    return interest, principal_paid


# ---------------------------------------------------------------------
# Capex building blocks
# ---------------------------------------------------------------------

# def well_cost_mln(depth_m, well_cost_scaling=1.5):
#    """Drilling cost per well, mln euro."""
#    return well_cost_scaling * (0.2 * depth_m ** 2 + 700 * depth_m + 250_000) * 1e-6

def well_cost_mln(depth_m, well_cost_scaling=1.0):
    """
    Drilling cost per well, mln euro.
    Uses the TNO ThermoGIS (2019) Dutch-calibrated formula:
        well capex = 375,000 + 1150*d + 0.3*d^2   (euro, d = depth in m)
    (Vrijlandt et al., "ThermoGIS update", European Geothermal Congress 2019.)
    well_cost_scaling allows scaling up/down for a specific site if needed;
    defaults to 1.0.
    """
    return well_cost_scaling * (375_000 + 1150 * depth_m + 0.3 * depth_m ** 2) * 1e-6

def subsurface_capex_mln(depth_m, n_wells,
                          stim_cost_per_well_mln=0.0,
                          pump_investment_mln=0.3, n_pumps=None):
    """Total subsurface capex, mln euro."""
    if n_pumps is None:
        n_pumps = n_wells
    wc = well_cost_mln(depth_m)
    return (stim_cost_per_well_mln + wc) * n_wells + pump_investment_mln * n_pumps


def heat_surface_capex_mln(heat_mwth, capex_rate_kEuro_per_mwth=150):
    """Surface heat-plant capex, mln euro. Sheet row 43."""
    return capex_rate_kEuro_per_mwth * heat_mwth / 1000

def payback_period(equity_amount, net_revenue_series, discount_rate=None):
    """
    Simple payback: first year cumulative net revenue >= equity invested.
    If discount_rate is given, computes discounted payback instead.
    Returns years (float, interpolated within the crossing year) or None if never recovered.
    """
    cashflows = np.asarray(net_revenue_series, dtype=float)
    if discount_rate is not None:
        periods = np.arange(1, len(cashflows) + 1)
        cashflows = cashflows / (1 + discount_rate) ** periods

    cumulative = np.cumsum(cashflows)
    recovered = cumulative >= equity_amount

    if not recovered.any():
        return None 

    year_index = np.argmax(recovered) 
    prev_cum = cumulative[year_index - 1] if year_index > 0 else 0
    fraction = (equity_amount - prev_cum) / (cumulative[year_index] - prev_cum)
    return year_index + fraction

# ---------------------------------------------------------------------
# Main LCOE model
# ---------------------------------------------------------------------

def lcoe_heat(
    heat_mwth,                      
    depth_m,                   
    n_wells=2,                      # number of wells (doublet = 2)
    n_pumps=None,                   # defaults to n_wells
    well_cost_scaling=1.0,
    stim_cost_per_well_mln=0.0,     
    pump_investment_mln=0.3,        # mln euro/pump
    pump_replace_interval=5,        # years between pump workovers
    heat_capex_rate_kEuro_per_mwth=150,
    heat_loadhours=6000,            # full-load hours/year
    electricity_price=150,          # euro/MWhe, drives O&M via COP
    COP=27,
    heat_OMvar_override=None,       # euro/MWhth, overrides electricity_price/COP calc
    heat_OMfixed_rate=0.01,         # fraction of total capex, per year
    complementary_heat_price=0.0,   # euro/GJ, for any exogenously-priced heat sold
    lifetime=15,                    # years, economic project life (TNO ThermoGIS default)
    depreciation_time=15,
    term_loan=15,
    loan_rate=0.05,                 # TNO ThermoGIS (2019): 5% interest on loan
    equity_return=0.07,             # TNO ThermoGIS (2019): 7% required return on equity
    equity_share=0.2,               # TNO ThermoGIS (2019): 80% debt ratio -> 20% equity
    tax=0.25,                       # TNO ThermoGIS (2019): 25% tax rate
    inflation=0.02,                  # TNO ThermoGIS (2019): 2% inflation
    n_years=40,                     # simulation horizon (sheet uses 40)
):
    """
    Returns a dict with LCOE (€/GJ and €/MWh_th) plus the intermediate
    capex/cash-flow quantities, for a direct-heat geothermal project.
    """
    if n_pumps is None:
        n_pumps = n_wells

    # --- Capex ---
    capex_sub = subsurface_capex_mln(depth_m, n_wells, well_cost_scaling,
                                      stim_cost_per_well_mln,
                                      pump_investment_mln, n_pumps)
    capex_heat = heat_surface_capex_mln(heat_mwth, heat_capex_rate_kEuro_per_mwth)
    total_capex_mln = capex_sub + capex_heat
    total_capex_eur = total_capex_mln * 1e6

    equity_amount = equity_share * total_capex_eur
    loan_amount = (1 - equity_share) * total_capex_eur

    # --- Variable O&M rate (euro/MWhth), from electricity cost to drive pumps ---
    heat_OMvar = heat_OMvar_override if heat_OMvar_override is not None else electricity_price / COP

    # --- Debt schedule ---
    interest_sched, principal_sched = loan_amortization_schedule(loan_rate, term_loan, loan_amount)

    # --- Year-by-year cash flow, years 1..n_years (year 0 = investment only) ---
    heat_GJ = np.zeros(n_years)
    opex = np.zeros(n_years)
    pump_capex = np.zeros(n_years)
    income = np.zeros(n_years)

    pump_replace_cost_eur = pump_investment_mln * n_pumps * 1e6

    for i in range(n_years):
        year = i + 1
        active = year <= lifetime
        infl = (1 + inflation) ** (year - 1)

        if active:
            heat_GJ[i] = heat_mwth * heat_loadhours * 3.6
            fixed_om = heat_OMfixed_rate * total_capex_eur
            variable_om = heat_mwth * heat_loadhours * heat_OMvar
            opex[i] = -(fixed_om + variable_om) * infl

            if year % pump_replace_interval == 0:
                pump_capex[i] = -pump_replace_cost_eur * infl

            income[i] = complementary_heat_price * heat_GJ[i] * infl

    total_costs = opex + pump_capex
    gross_revenue = income + total_costs

    depreciation = np.array([
        -total_capex_eur / depreciation_time if (i + 1) <= depreciation_time else 0.0
        for i in range(n_years)
    ])

    interest = np.zeros(n_years)
    principal = np.zeros(n_years)
    interest[:len(interest_sched)] = interest_sched
    principal[:len(principal_sched)] = principal_sched
    loan_charges = interest + principal

    taxable_income = gross_revenue + depreciation + interest
    tax_paid = -tax * taxable_income
    net_revenue = gross_revenue + loan_charges + tax_paid
    after_tax_energy_GJ = (1 - tax) * heat_GJ

    discounted_revenue = npv(equity_return, net_revenue)
    discounted_energy_GJ = npv(equity_return, after_tax_energy_GJ)

    lcoe_per_GJ = (equity_amount - discounted_revenue) / discounted_energy_GJ
    lcoe_per_MWh_th = lcoe_per_GJ * 3.6

    return {
        "LCOE_eur_per_GJ": lcoe_per_GJ,
        "LCOE_eur_per_MWhth": lcoe_per_MWh_th,
        "capex_subsurface_mln": capex_sub,
        "capex_heat_plant_mln": capex_heat,
        "total_capex_mln": total_capex_mln,
        "equity_amount_eur": equity_amount,
        "loan_amount_eur": loan_amount,
        "discounted_net_revenue_eur": discounted_revenue,
        "discounted_energy_GJ": discounted_energy_GJ,
        "heat_OMvar_eur_per_MWhth": heat_OMvar,
        "net_revenue_series": net_revenue,
        "equity_amount_eur": equity_amount,
    }


if __name__ == "__main__":
    result = lcoe_heat(heat_mwth=8.26, depth_m=1800, n_wells=2,
                        stim_cost_per_well_mln=0.075)  # e.g. half of the 150k acidizing cost per well

    simple_pb = payback_period(result["equity_amount_eur"], result["net_revenue_series"])
    discounted_pb = payback_period(result["equity_amount_eur"], result["net_revenue_series"], discount_rate=0.15)

    print(f"Simple payback: {simple_pb:.1f} years")
    print(f"Discounted payback: {discounted_pb:.1f} years")

    for k, v in result.items():
        print(f"{k}: {v:,.2f}" if isinstance(v, float) else f"{k}: {v}")
