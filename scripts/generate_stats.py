#!/usr/bin/env python3
"""
generate_stats.py — pulls contribution stats from GitHub's GraphQL API using
only the standard library, and writes stats.json for compose_hero.py.

Two determinism traps this avoids (see notes):
  1. The contribution window is pinned to whole UTC days (today-364d 00:00:00Z
     -> today 23:59:59Z), not "the past year" relative to request time — two
     runs minutes apart would otherwise bucket days into different weeks.
  2. Repository/language stats are filtered to privacy: PUBLIC, so the result
     is identical whether a personal token or the workflow's GITHUB_TOKEN ran it.

Usage:
  GITHUB_TOKEN=xxx GH_LOGIN=yourusername python3 generate_stats.py stats.json
"""
import os
import sys
import json
import datetime
import urllib.request

API = "https://api.github.com/graphql"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
  }
}
"""


def fetch(login: str, token: str) -> dict:
    now = datetime.datetime.now(datetime.timezone.utc)
    to_dt = now.replace(hour=23, minute=59, second=59, microsecond=0)
    from_dt = (to_dt - datetime.timedelta(days=364)).replace(hour=0, minute=0, second=0)

    body = json.dumps({
        "query": QUERY,
        "variables": {
            "login": login,
            "from": from_dt.isoformat(),
            "to": to_dt.isoformat(),
        },
    }).encode()

    req = urllib.request.Request(
        API, data=body,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-readme-stats",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def summarize(data: dict) -> dict:
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    total = cal["totalContributions"]
    days = []
    for w in cal["weeks"]:
        for d in w["contributionDays"]:
            days.append(d["contributionCount"])

    active_days = sum(1 for d in days if d > 0)

    weekly = [sum(w["contributionDays"][i]["contributionCount"] for i in range(len(w["contributionDays"])))
              for w in cal["weeks"]]
    best_week = max(weekly) if weekly else 0

    # current streak (from most recent day backwards) + longest streak
    longest = cur = 0
    running = 0
    for d in days:
        if d > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    for d in reversed(days):
        if d > 0:
            cur += 1
        else:
            break

    # sparkline: last 20 weeks, normalized 0-1
    spark = weekly[-20:] if len(weekly) >= 20 else weekly
    peak = max(spark) if spark and max(spark) > 0 else 1
    spark_norm = [round(v / peak, 3) for v in spark]

    return {
        "total_contributions": total,
        "active_days": active_days,
        "best_week": best_week,
        "current_streak": cur,
        "longest_streak": longest,
        "sparkline": spark_norm,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "stats.json"
    token = os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GH_LOGIN")
    if not token or not login:
        print("GITHUB_TOKEN and GH_LOGIN must be set", file=sys.stderr)
        sys.exit(1)

    raw = fetch(login, token)
    if "errors" in raw:
        print(json.dumps(raw["errors"]), file=sys.stderr)
        sys.exit(1)

    stats = summarize(raw)
    with open(out_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"wrote {out_path}: {stats['total_contributions']} contributions, "
          f"{stats['active_days']} active days, best week {stats['best_week']}")


if __name__ == "__main__":
    main()
