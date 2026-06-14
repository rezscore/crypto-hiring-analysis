#!/usr/bin/env python3
"""
Generate charts for the crypto-hiring blog post:
"Twin Bear Markets: Why Laid-Off Coders Are Quietly Looking at Crypto"
(docs/marketing/blog/2026-06-04_BLOG_CRYPTO_HIRING.md)

Every number in this file is a verified, cited figure. Sources are noted inline
next to each data literal so they can be audited against the post's methodology
README (docs/marketing/crypto-hiring-analysis/README.md). Do not change a number
here without updating both the post and the README.

Usage:
    python scripts/generate_crypto_blog_charts.py

Output:
    scripts/charts/*.png
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Create output directory (shared with generate_blog_charts.py)
OUTPUT_DIR = Path(__file__).parent / "charts"
OUTPUT_DIR.mkdir(exist_ok=True)

# Set style (matches generate_blog_charts.py)
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titleweight'] = 'bold'

# Brand colors (matches generate_blog_charts.py)
REZSCORE_BLUE = '#2563eb'
REZSCORE_ORANGE = '#f97316'
DANGER_RED = '#dc2626'
SUCCESS_GREEN = '#16a34a'
GRAY = '#6b7280'
LIGHT_GRAY = '#e5e7eb'


def chart_1_labor_bear_market():
    """The tech labor downturn, concentrated at the entry level.

    Sources:
    - layoffs.fyi (as of early June 2026): 152,922 cuts 2024; 165,269 partial 2026.
    - Stanford Digital Economy Lab, "Canaries in the Coal Mine?" (Nov 2025):
      young (22-25) AI-exposed workers ~-16% relative; young software devs ~-20%
      from late-2022 peak (descriptive, not clean AI causation).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # --- Left panel: layoffs by year ---
    years = ['2024', '2026\n(partial,\nthru early Jun)']
    layoffs = [152922, 165269]  # layoffs.fyi
    bars = ax1.bar(years, layoffs, color=[GRAY, DANGER_RED], width=0.55)
    for bar, val in zip(bars, layoffs):
        ax1.text(bar.get_x() + bar.get_width() / 2, val + 3000, f'{val:,}',
                 ha='center', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Tech employees laid off', fontsize=12)
    ax1.set_ylim(0, 195000)
    ax1.set_title('The layoffs never stopped', fontsize=15, fontweight='bold', pad=15)
    ax1.text(0.5, -0.16, 'Source: layoffs.fyi tracker (crowd-aggregated), as of early June 2026',
             ha='center', fontsize=9, color=GRAY, style='italic', transform=ax1.transAxes)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # --- Right panel: who got hit (young vs experienced) ---
    cohorts = ['Young software\ndevs (22-25)', 'Young workers in\nAI-exposed jobs', 'Experienced\nworkers']
    # Stanford "Canaries" Nov 2025: -20% (young devs, descriptive), -16% (relative, AI-exposed),
    # experienced employment stable-to-up (shown as small positive).
    changes = [-20, -16, 4]
    colors = [DANGER_RED if c < 0 else SUCCESS_GREEN for c in changes]
    bars2 = ax2.barh(cohorts, changes, color=colors, height=0.6)
    for bar, val in zip(bars2, changes):
        offset = -1.5 if val < 0 else 0.5
        ha = 'right' if val < 0 else 'left'
        ax2.text(val + offset, bar.get_y() + bar.get_height() / 2,
                 f'{"+" if val > 0 else ""}{val}%', va='center', ha=ha,
                 fontsize=13, fontweight='bold')
    ax2.axvline(x=0, color=GRAY, linewidth=1)
    ax2.set_xlim(-26, 12)
    ax2.set_xlabel('Employment change', fontsize=12)
    ax2.set_title('The bottom rung broke first', fontsize=15, fontweight='bold', pad=15)
    ax2.text(0.5, -0.16,
             'Source: Stanford Digital Economy Lab, "Canaries in the Coal Mine?" (Nov 2025).\n'
             'Young-dev figure is descriptive, not a clean measure of AI causation.',
             ha='center', fontsize=9, color=GRAY, style='italic', transform=ax2.transAxes)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('Bear Market #1: Tech Labor', fontsize=19, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'c1_labor_bear_market.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: c1_labor_bear_market.png")


def chart_2_crypto_drawdown():
    """How far crypto prices are off their highs (June 2-3, 2026).

    Sources:
    - BTC ~$65,853 on Jun 3 2026, ~47% below ATH ~$126,000 (Oct 6 2025).
      news.bitcoin.com / CoinDesk / Fortune.
    - ETH ~$1,922 on Jun 2 2026, ~61% below ATH $4,953.73 (Aug 24 2025).
      Yahoo Finance / TradingView / CoinCodex.
    - Median altcoin -79% from late-2024 peak; altcoin mkt cap (ex BTC/ETH/stables)
      -44% from that peak. Pantera Capital Blockchain Letter (Jan 2026).
    - Crypto Fear & Greed Index = 11 ("Extreme Fear") on Jun 3 2026. alternative.me.
    """
    fig, ax = plt.subplots(figsize=(11, 6.5))

    labels = ['Bitcoin', 'Ethereum', 'Altcoin market cap\n(ex BTC/ETH/stables)', 'Median\ncrypto token']
    drawdowns = [-47, -61, -44, -79]  # % below respective peaks
    colors = [REZSCORE_ORANGE, REZSCORE_BLUE, GRAY, DANGER_RED]

    bars = ax.bar(labels, drawdowns, color=colors, width=0.6)
    for bar, val in zip(bars, drawdowns):
        ax.text(bar.get_x() + bar.get_width() / 2, val - 3, f'{val}%',
                ha='center', va='top', fontsize=15, fontweight='bold', color='white')

    ax.axhline(y=0, color=GRAY, linewidth=1)
    ax.set_ylim(-90, 8)
    ax.set_ylabel('Drawdown from peak', fontsize=12)
    ax.set_title('Bear Market #2: Crypto Prices Are Deep Below Their Highs',
                 fontsize=17, fontweight='bold', pad=20)

    # Fear & Greed callout
    ax.text(0.5, -0.155,
            'BTC/ETH: prices vs all-time highs, June 2-3, 2026 (CoinDesk, Yahoo Finance). '
            'Altcoin figures: Pantera Capital (Jan 2026), peak-to-trough from late-2024 peak.\n'
            'Crypto Fear & Greed Index sat at 11 ("Extreme Fear") on June 3, 2026 — down from 40 a month earlier (alternative.me).',
            ha='center', fontsize=9, color=GRAY, style='italic', transform=ax.transAxes)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'c2_crypto_drawdown.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: c2_crypto_drawdown.png")


def chart_3_crypto_split_screen():
    """The split screen: prices crashed, institutional money hit records.

    Sources:
    - Stablecoin market cap ATH $317B, March 2026. CoinDesk Research.
    - Tokenized U.S. Treasuries ~$14.7B (Jun 4 2026); all-RWA ~$34B early 2026.
      rwa.xyz / a16z.
    - Crypto VC: ~$30B/yr peak (2021-22); $11.5B 2024; ~$20B 2025; ~$4B Q1 2026
      (~$16B annualized). Galaxy Research.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # --- Left: institutional adoption at records ---
    metrics = ['Stablecoin\nmarket cap\n(Mar 2026, ATH)', 'Tokenized RWAs\n(early 2026)', 'Tokenized US\nTreasuries\n(Jun 4 2026)']
    values = [317, 34, 14.7]  # $B
    bars = ax1.bar(metrics, values, color=[SUCCESS_GREEN, REZSCORE_BLUE, REZSCORE_BLUE], width=0.6)
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width() / 2, val + 6, f'${val}B',
                 ha='center', fontsize=13, fontweight='bold')
    ax1.set_ylabel('USD (billions)', fontsize=12)
    ax1.set_ylim(0, 360)
    ax1.set_title('Institutional money: at records', fontsize=15, fontweight='bold', pad=15)
    ax1.text(0.5, -0.18, 'Sources: CoinDesk Research (stablecoins); rwa.xyz, a16z (tokenized assets)',
             ha='center', fontsize=9, color=GRAY, style='italic', transform=ax1.transAxes)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # --- Right: VC funding off peak but still billions ---
    periods = ['2021-22\npeak\n(per year)', '2024', '2025', '2026\n(annualized\nfrom Q1)']
    vc = [30, 11.5, 20, 16]  # $B, Galaxy Research
    colors = [LIGHT_GRAY, REZSCORE_ORANGE, REZSCORE_ORANGE, REZSCORE_ORANGE]
    bars2 = ax2.bar(periods, vc, color=colors, width=0.6)
    for bar, val in zip(bars2, vc):
        ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.6, f'${val}B',
                 ha='center', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Crypto VC invested (USD billions)', fontsize=12)
    ax2.set_ylim(0, 34)
    ax2.set_title('VC funding: off the peak, still billions', fontsize=15, fontweight='bold', pad=15)
    ax2.text(0.5, -0.18, 'Source: Galaxy Research crypto VC reports. 2026 annualized from ~$4B Q1.',
             ha='center', fontsize=9, color=GRAY, style='italic', transform=ax2.transAxes)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('The Twist: The Money Never Left', fontsize=19, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'c3_crypto_split_screen.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: c3_crypto_split_screen.png")


def chart_4_code_vs_coders():
    """More code, flat developer base — facts shown, conclusion left as argument.

    Sources:
    - Crypto devs ~flat: 23,613 monthly active, statistically-insignificant -7% YoY;
      experienced (2+ yr) devs +27% YoY, writing 70% of commits.
      Electric Capital 2024 Developer Report (as of Nov 2024).
    - AI code: Google >25% of new code AI-generated (Pichai, Oct 2024);
      GitHub Copilot 20M all-time users (Jul 2025).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.5))

    # --- Left: "more code" — AI authorship rising ---
    ax1.bar([0], [25], color=REZSCORE_BLUE, width=0.5)
    ax1.text(0, 26, '>25%', ha='center', va='bottom', fontsize=20, fontweight='bold')
    ax1.set_ylim(0, 42)
    ax1.set_xlim(-0.6, 0.6)
    ax1.set_ylabel('Percent of new code', fontsize=12)
    ax1.set_title('"More code": AI authorship is surging', fontsize=14, fontweight='bold', pad=15)
    ax1.text(0.5, 0.5,
             'GitHub Copilot:\n20 million all-time users\n(Jul 2025)',
             ha='center', va='center', fontsize=12, color=GRAY, fontweight='bold',
             transform=ax1.transAxes,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=LIGHT_GRAY, pad=0.6))
    ax1.set_xticks([0])
    ax1.set_xticklabels(['Google: AI-generated\nshare of NEW code'])
    ax1.text(0.5, -0.24,
             'Sources: Sundar Pichai, Alphabet Q3 2024 earnings (Oct 2024)\n'
             '— new code, reviewed by engineers. Copilot users:\n'
             'Microsoft (Jul 2025), cumulative all-time, not active.',
             ha='center', va='top', fontsize=8.5, color=GRAY, style='italic',
             transform=ax1.transAxes)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # --- Right: "fewer coders" — base flat, consolidating around the experienced ---
    cats = ['Monthly active\ncrypto devs (YoY)', 'Experienced devs\n(2+ yrs, YoY)', 'Commits by\nexperienced devs']
    vals = [-7, 27, 70]
    colors = [GRAY, SUCCESS_GREEN, REZSCORE_BLUE]
    bars2 = ax2.bar(cats, vals, color=colors, width=0.6)
    annotations = ['-7% ("flat")', '+27%', '70%']
    for bar, val, label in zip(bars2, vals, annotations):
        va = 'bottom' if val >= 0 else 'top'
        off = 1.5 if val >= 0 else -1.5
        ax2.text(bar.get_x() + bar.get_width() / 2, val + off, label,
                 ha='center', va=va, fontsize=12, fontweight='bold')
    ax2.axhline(y=0, color=GRAY, linewidth=1)
    ax2.set_ylim(-20, 84)
    ax2.set_ylabel('Percent', fontsize=12)
    ax2.set_title('"Fewer coders": base flat, consolidating', fontsize=14, fontweight='bold', pad=15)
    ax2.text(0.5, -0.24,
             'Source: Electric Capital 2024 Developer Report (as of Nov 2024).\n'
             'The -7% is described as a statistically insignificant change — "basically flat."',
             ha='center', va='top', fontsize=8.5, color=GRAY, style='italic',
             transform=ax2.transAxes)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('More Code, Fewer Coders (the facts; the conclusion is the argument)',
                 fontsize=17, fontweight='bold', y=1.00)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(OUTPUT_DIR / 'c4_code_vs_coders.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: c4_code_vs_coders.png")


def main():
    print("Generating charts for the crypto-hiring blog post...")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)

    chart_1_labor_bear_market()
    chart_2_crypto_drawdown()
    chart_3_crypto_split_screen()
    chart_4_code_vs_coders()

    print("-" * 50)
    print(f"Done! Generated 4 charts in {OUTPUT_DIR}")
    print("\nUsage in blog post:")
    print("  ![Tech layoffs and the early-career squeeze](charts/c1_labor_bear_market.png)")
    print("  ![Crypto prices vs all-time highs](charts/c2_crypto_drawdown.png)")
    print("  ![Crypto's split screen: prices down, institutional money up](charts/c3_crypto_split_screen.png)")
    print("  ![More code, flat developer base](charts/c4_code_vs_coders.png)")


if __name__ == "__main__":
    main()
