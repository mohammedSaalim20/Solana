import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import time
from mev_analyzer.models import MEVTransaction

API_URL = f"https://mainnet.helius-rpc.com/?api-key={settings.HELIUS_API_KEY}"

# Command to fetch recent Solana transactions and analyze for MEV opportunities
class Command(BaseCommand):
    help = 'Fetch recent Solana transactions and analyze for MEV'

    def handle(self, *args, **kwargs):

        while True:
            self.fetch_transactions()
            time.sleep(60)
                # Example: Get last 100 transactions for a known DEX (Jupiter's Program ID)
    def fetch_transactions(self):
        print("📡 Fetching recent transactions...")
        jupiter_program_id = "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB"
        # Define the payload to get recent transactions for Jupiter DEX
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                jupiter_program_id,
                {"limit": 5}  # You can increase this to 100+
            ]
        }
    # Make the API request to get recent signatures
        response = requests.post(API_URL, json=payload)
        sigs = response.json().get("result", [])

        for tx in sigs:
            signature = tx["signature"]

            # Get transaction details
            txn_payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTransaction",
                "params": [
                    signature,
                    {
                        "encoding": "jsonParsed",
                        "maxSupportedTransactionVersion": 0
                    }
                ]
            }
            # Make the API request to get transaction details
            txn_response = requests.post(API_URL, json=txn_payload)
            txn_result = txn_response.json().get("result")

            if not txn_result:
                continue

            try:
                # Extract relevant data from the transaction
                wallet = txn_result["transaction"]["message"]["accountKeys"][0]["pubkey"]
                meta = txn_result["meta"]
                instructions = txn_result["transaction"]["message"]["instructions"]
                inner = meta.get("innerInstructions", [])
                pre_balances = meta.get("preTokenBalances", [])
                post_balances = meta.get("postTokenBalances", [])

                # Collect unique platforms used
                platforms = set()
                path = []

                #Detect used DEX programs
                known_dex_programs = {
                    "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB": "Jupiter",
                    "RVKd61ztZW9GdT3vX9X3C5SRzfa3UuExKwn7CQoQTMn": "Raydium",
                    "9xQeWvG816bUx9EPDFg2PQSx1W8FQ9UnSr5uQYzjRtd": "Serum",
                    "8tfDNiaEyrV6Q1U4DEXrEigs9DoDtkugzFbybENEbCDz": "Meteora"
                }

                for ix in instructions:
                    program_id = ix.get("programId")
                    if program_id in known_dex_programs:
                        platforms.add(known_dex_programs[program_id])

                # Decode Token Path from token balances
                if pre_balances and post_balances:
                    for pre, post in zip(pre_balances, post_balances):
                        if pre["owner"] == wallet and post["owner"] == wallet:
                            pre_amt = int(pre["uiTokenAmount"]["amount"])
                            post_amt = int(post["uiTokenAmount"]["amount"])
                            token = pre["mint"]
                            if pre_amt != post_amt:
                                path.append(token)

                # Just show mint addresses for now; can decode to symbols later
                token_path_str = " → ".join(path) if path else "Unknown"

                #Estimate Profit (very basic - difference in 1st token amount)
                profit = 0.0
                if pre_balances and post_balances:
                    try:
                        pre_amt = int(pre_balances[0]["uiTokenAmount"]["amount"]) / (
                                    10 ** pre_balances[0]["uiTokenAmount"]["decimals"])
                        post_amt = int(post_balances[0]["uiTokenAmount"]["amount"]) / (
                                    10 ** post_balances[0]["uiTokenAmount"]["decimals"])
                        profit = round(post_amt - pre_amt, 6)
                    except Exception:
                        pass

                # Basic MEV tagging
                is_mev = profit > 0.1  # arbitrary threshold
                pattern = "Likely MEV: profitable token delta"

                # Save to DB
                if not MEVTransaction.objects.filter(tx_hash=signature).exists():
                    MEVTransaction.objects.create(
                        tx_hash=signature,
                        wallet=wallet,
                        path=token_path_str,
                        platforms=", ".join(platforms),
                        profit=profit,
                        is_mev=is_mev,
                        pattern=pattern,
                        timestamp=timezone.now()
                    )
                    print(f"Saved tx {signature}")
                else:
                    print(f"Already exists: {signature}")


            except Exception as e:
                print(f"Error parsing tx {signature}: {e}")
