# IPL 2026 NRR Calculator — SRH vs RCB (Match 67)

A Python script that calculates exactly how SRH needs to win against RCB to overtake them on Net Run Rate in IPL 2026.

## Context

With both SRH and RCB qualified for the IPL 2026 playoffs, table position depends on NRR. This calculator determines:

- **If SRH bats first:** The minimum winning margin (in runs) needed for SRH's NRR to surpass RCB's.
- **If RCB bats first:** The maximum overs SRH can take to chase the target while still finishing above RCB on NRR.

## Data Source

Tournament stats pulled from [ESPNcricinfo](https://www.espncricinfo.com/series/ipl-2026-1510719/points-table-standings) before Match 67 (May 22, 2026):

| Team | Runs Scored / Overs Faced | Runs Conceded / Overs Bowled | NRR |
|------|--------------------------|------------------------------|-----|
| RCB | 2442 / 234.2 | 2364 / 252.4 | +1.065 |
| SRH | 2599 / 256.1 | 2475 / 252.4 | +0.350 |

## NRR Formula

```
NRR = (Total Runs Scored / Total Overs Faced) − (Total Runs Conceded / Total Overs Bowled)
```

Key rule: if a team is bowled out, the full 20-over quota is used in the calculation regardless of actual overs played.

## Usage

```bash
python3 nrr_calculator.py
```

You'll be prompted to select who bats first and enter the first innings score.

### Example — SRH bats first

```
Who bats FIRST? SRH
Enter SRH First Innings Score: 200

Max RCB can score (chase): 113
Required Winning Margin:   87 runs
SRH new NRR: +0.644
RCB new NRR: +0.642
```

### Example — RCB bats first

```
Who bats FIRST? RCB
Enter RCB First Innings Score: 180

Target for SRH: 181
Max overs SRH can take (cricket): 11.0
Max balls: 66
SRH new NRR: +0.662
RCB new NRR: +0.662
```

## Requirements

- Python 3.6+
- No external dependencies
