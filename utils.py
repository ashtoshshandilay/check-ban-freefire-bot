import aiohttp
import asyncio
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
BASE_TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

async def check_ban(uid: str) -> Optional[dict]:
    api_url = f"http://raw.thug4ff.xyz/check_ban/{uid}/great"

    for attempt in range(1, MAX_RETRIES + 1):
        timeout = aiohttp.ClientTimeout(total=BASE_TIMEOUT + (attempt * 5))

        try:
            print(f"[Attempt {attempt}/{MAX_RETRIES}] Checking UID {uid}...")

            async with aiohttp.ClientSession(timeout=timeout, headers=HEADERS) as session:
                async with session.get(api_url) as response:
                    response.raise_for_status()

                    try:
                        response_data = await response.json(content_type=None)
                    except Exception:
                        raw_text = await response.text()
                        print(f"[Attempt {attempt}] Raw response: {raw_text[:300]}")
                        response_data = None

                    if not response_data:
                        print(f"[Attempt {attempt}] Empty or invalid response.")
                    elif response_data.get("status") == 200:
                        data = response_data.get("data")
                        if data:
                            print(f"[Success] UID {uid} fetched on attempt {attempt}.")
                            return {
                                "is_banned": data.get("is_banned", 0),
                                "nickname": data.get("nickname", "NA"),
                                "period": data.get("period", 0),
                                "region": data.get("region", "N/A")
                            }
                        else:
                            print(f"[Attempt {attempt}] Status 200 but no data.")
                    else:
                        print(f"[Attempt {attempt}] API status: {response_data.get('status')}")

        except aiohttp.ClientResponseError as e:
            print(f"[Attempt {attempt}] HTTP error: {e.status} - {e.message}")
        except aiohttp.ClientConnectionError as e:
            print(f"[Attempt {attempt}] Connection error: {e}")
        except asyncio.TimeoutError:
            print(f"[Attempt {attempt}] Timeout for UID {uid}.")
        except Exception as e:
            print(f"[Attempt {attempt}] Error: {type(e).__name__}: {e}")

        if attempt < MAX_RETRIES:
            wait_time = 2 * attempt
            print(f"Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

    print(f"[FAILED] All {MAX_RETRIES} attempts failed for UID {uid}.")
    return None
