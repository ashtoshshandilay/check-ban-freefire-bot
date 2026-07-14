import asyncio
import sys

from utils import check_ban


async def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python bancheck_cli.py <UID>")
        sys.exit(1)

    uid = sys.argv[1]
    result = await check_ban(uid)

    if result is None:
        print("❌ Could not get information. Please try again later.")
        sys.exit(1)

    is_banned = int(result.get("is_banned", 0))
    period = result.get("period", "N/A")
    period_str = f"more than {period} months" if isinstance(period, int) else "unavailable"

    print()
    print("▌ Banned Account 🛑" if is_banned else "▌ Clean Account ✅")
    print(f"• Nickname : {result.get('nickname', 'NA')}")
    print(f"• Player ID: {uid}")
    print(f"• Region   : {result.get('region', 'N/A')}")
    if is_banned:
        print(f"• Suspension duration: {period_str}")


if __name__ == "__main__":
    asyncio.run(main())
