"""
IPL 2026 NRR Calculator: SRH vs RCB (Match 67, May 22, 2026)

NRR Formula:
  NRR = (Total Runs Scored / Total Overs Faced) - (Total Runs Conceded / Total Overs Bowled)

Key rule: If a team is bowled out, full 20 overs are used in the calculation.

Current standings BEFORE this match (from ESPNcricinfo):
  RCB: For 2442/234.2  Against 2364/252.4  NRR +1.065
  SRH: For 2599/256.1  Against 2475/252.4  NRR +0.350

Overs are in cricket notation: 234.2 means 234 overs and 2 balls = 234 + 2/6 decimal overs
"""


def cricket_overs_to_decimal(overs_str):
    """Convert cricket overs notation (e.g., '234.2') to decimal overs."""
    parts = str(overs_str).split(".")
    whole = int(parts[0])
    balls = int(parts[1]) if len(parts) > 1 else 0
    return whole + balls / 6.0


def decimal_to_cricket_overs(decimal_overs):
    """Convert decimal overs to cricket notation (e.g., 10.833 -> 10.5)."""
    total_balls = int(decimal_overs * 6)
    overs = total_balls // 6
    balls = total_balls % 6
    return f"{overs}.{balls}"


# --- Current tournament data (BEFORE today's match) ---
# From ESPNcricinfo: RCB For 2442/234.2, Against 2364/252.4
RCB_RUNS_SCORED = 2442
RCB_OVERS_FACED = cricket_overs_to_decimal("234.2")  # 234.3333
RCB_RUNS_CONCEDED = 2364
RCB_OVERS_BOWLED = cricket_overs_to_decimal("252.4")  # 252.6667

# From ESPNcricinfo: SRH For 2599/256.1, Against 2475/252.4
SRH_RUNS_SCORED = 2599
SRH_OVERS_FACED = cricket_overs_to_decimal("256.1")  # 256.1667
SRH_RUNS_CONCEDED = 2475
SRH_OVERS_BOWLED = cricket_overs_to_decimal("252.4")  # 252.6667


def verify_current_nrr():
    """Verify our data matches the published NRR values."""
    rcb_nrr = (RCB_RUNS_SCORED / RCB_OVERS_FACED) - (RCB_RUNS_CONCEDED / RCB_OVERS_BOWLED)
    srh_nrr = (SRH_RUNS_SCORED / SRH_OVERS_FACED) - (SRH_RUNS_CONCEDED / SRH_OVERS_BOWLED)
    print(f"  RCB current NRR: {rcb_nrr:+.3f} (published: +1.065)")
    print(f"  SRH current NRR: {srh_nrr:+.3f} (published: +0.350)")
    print()


def scenario_srh_bats_first(b1):
    """
    SRH bats first and scores B1 runs in 20 overs.
    SRH wins, so RCB scores fewer than B1.
    Find max runs RCB can score such that SRH's new NRR > RCB's new NRR.

    After the match:
      SRH Scored: 2599 + B1       SRH Faced: 256.1667 + 20 = 276.1667
      SRH Conceded: 2475 + X      SRH Bowled: 252.6667 + 20 = 272.6667
        (X = RCB's chase score; if RCB bowled out, 20 overs used)

      RCB Scored: 2442 + X        RCB Faced: 234.3333 + 20 = 254.3333
        (if bowled out, 20 overs used for RCB faced)
      RCB Conceded: 2364 + B1     RCB Bowled: 252.6667 + 20 = 272.6667

    Constraint: SRH_NRR_new > RCB_NRR_new
    """
    srh_scored_new = SRH_RUNS_SCORED + b1
    srh_faced_new = SRH_OVERS_FACED + 20.0
    srh_bowled_new = SRH_OVERS_BOWLED + 20.0

    rcb_faced_new = RCB_OVERS_FACED + 20.0  # RCB bats full 20 (or bowled out = 20 used)
    rcb_bowled_new = RCB_OVERS_BOWLED + 20.0
    rcb_conceded_new_base = RCB_RUNS_CONCEDED + b1

    def inequality_holds(rcb_chase_runs):
        srh_conceded_new = SRH_RUNS_CONCEDED + rcb_chase_runs
        rcb_scored_new = RCB_RUNS_SCORED + rcb_chase_runs

        srh_nrr = (srh_scored_new / srh_faced_new) - (srh_conceded_new / srh_bowled_new)
        rcb_nrr = (rcb_scored_new / rcb_faced_new) - (rcb_conceded_new_base / rcb_bowled_new)
        return srh_nrr > rcb_nrr

    max_rcb_runs = -1
    for runs in range(b1 - 1, -1, -1):
        if inequality_holds(runs):
            max_rcb_runs = runs
            break

    if max_rcb_runs == -1:
        print("\nNo valid solution — SRH cannot overtake RCB's NRR with this score.")
        return

    winning_margin = b1 - max_rcb_runs

    srh_conceded_final = SRH_RUNS_CONCEDED + max_rcb_runs
    rcb_scored_final = RCB_RUNS_SCORED + max_rcb_runs
    srh_nrr_final = (srh_scored_new / srh_faced_new) - (srh_conceded_final / srh_bowled_new)
    rcb_nrr_final = (rcb_scored_final / rcb_faced_new) - (rcb_conceded_new_base / rcb_bowled_new)

    print(f"\n{'='*55}")
    print(f"  SRH First Innings Score: {b1}")
    print(f"{'='*55}")
    print(f"  Max RCB can score (chase): {max_rcb_runs}")
    print(f"  Required Winning Margin:   {winning_margin} runs")
    print(f"{'='*55}")
    print(f"  SRH new NRR: {srh_nrr_final:+.3f}")
    print(f"  RCB new NRR: {rcb_nrr_final:+.3f}")
    print(f"{'='*55}")
    print(f"\n  SRH must restrict RCB to at most {max_rcb_runs} runs.")
    print(f"  i.e., SRH must win by at least {winning_margin} runs.")


def scenario_rcb_bats_first(b2):
    """
    RCB bats first and scores B2 runs in 20 overs.
    SRH chases successfully (scores B2+1).
    Find max overs SRH can take to chase such that SRH's new NRR > RCB's new NRR.

    After the match:
      SRH Scored: 2599 + (B2+1)    SRH Faced: 256.1667 + O_chase
      SRH Conceded: 2475 + B2      SRH Bowled: 252.6667 + 20 = 272.6667

      RCB Scored: 2442 + B2        RCB Faced: 234.3333 + 20 = 254.3333
      RCB Conceded: 2364 + (B2+1)  RCB Bowled: 252.6667 + O_chase

    Constraint: SRH_NRR_new > RCB_NRR_new
    """
    target = b2 + 1
    srh_scored_new = SRH_RUNS_SCORED + target
    srh_conceded_new = SRH_RUNS_CONCEDED + b2
    srh_bowled_new = SRH_OVERS_BOWLED + 20.0

    rcb_scored_new = RCB_RUNS_SCORED + b2
    rcb_faced_new = RCB_OVERS_FACED + 20.0
    rcb_conceded_new = RCB_RUNS_CONCEDED + target

    def inequality_holds(o_chase):
        srh_faced_new = SRH_OVERS_FACED + o_chase
        rcb_bowled_new = RCB_OVERS_BOWLED + o_chase

        srh_nrr = (srh_scored_new / srh_faced_new) - (srh_conceded_new / srh_bowled_new)
        rcb_nrr = (rcb_scored_new / rcb_faced_new) - (rcb_conceded_new / rcb_bowled_new)
        return srh_nrr > rcb_nrr

    if not inequality_holds(1.0 / 6.0):
        print("\nNo valid solution — SRH cannot overtake RCB's NRR even chasing in 1 ball.")
        return

    if inequality_holds(20.0):
        max_o_chase = 20.0
        print(f"\n  SRH can chase in full 20 overs and still overtake RCB's NRR!")
    else:
        lo, hi = 0.0, 20.0
        for _ in range(10000):
            mid = (lo + hi) / 2
            if inequality_holds(mid):
                lo = mid
            else:
                hi = mid
            if hi - lo < 0.00001:
                break
        max_o_chase = lo

    total_balls = int(max_o_chase * 6)
    cricket_overs = decimal_to_cricket_overs(max_o_chase)

    srh_faced_final = SRH_OVERS_FACED + max_o_chase
    rcb_bowled_final = RCB_OVERS_BOWLED + max_o_chase
    srh_nrr_final = (srh_scored_new / srh_faced_final) - (srh_conceded_new / srh_bowled_new)
    rcb_nrr_final = (rcb_scored_new / rcb_faced_new) - (rcb_conceded_new / rcb_bowled_final)

    print(f"\n{'='*55}")
    print(f"  RCB First Innings Score: {b2}")
    print(f"  Target for SRH: {target}")
    print(f"{'='*55}")
    print(f"  Max overs SRH can take (decimal): {max_o_chase:.4f}")
    print(f"  Max overs SRH can take (cricket): {cricket_overs}")
    print(f"  Max balls: {total_balls}")
    print(f"{'='*55}")
    print(f"  SRH new NRR: {srh_nrr_final:+.3f}")
    print(f"  RCB new NRR: {rcb_nrr_final:+.3f}")
    print(f"{'='*55}")
    print(f"\n  SRH must chase {target} within {cricket_overs} overs ({total_balls} balls).")


def main():
    print("\n" + "="*55)
    print("  IPL 2026 NRR Calculator: SRH vs RCB")
    print("  Match 67 — May 22, 2026, Hyderabad")
    print("="*55)
    print("\n  Current NRR verification:")
    verify_current_nrr()

    print("  Who bats FIRST?")
    print("    1. SRH")
    print("    2. RCB")
    choice = input("\n  Enter choice (SRH/RCB): ").strip().upper()

    if choice in ("SRH", "1"):
        b1 = int(input("  Enter SRH First Innings Score: "))
        scenario_srh_bats_first(b1)
    elif choice in ("RCB", "2"):
        b2 = int(input("  Enter RCB First Innings Score: "))
        scenario_rcb_bats_first(b2)
    else:
        print("  Invalid choice. Please enter SRH or RCB.")


if __name__ == "__main__":
    main()
