import os
import django
import sys
from datetime import datetime
from solana.rpc.api import Client
from solders.pubkey import Pubkey as PublicKey
from solders.signature import Signature

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solana_mev.settings")
django.setup()

from mev_analyzer.models import MEVTransaction

# Connect to Solana public RPC
client = Client("https://api.mainnet-beta.solana.com", config={"max_supported_transaction_version": 0})

def decode_and_store_transactions():
    print("Fetching transactions...")
    slot = client.get_slot().value
    signatures = client.get_signatures_for_address(PublicKey.from_string("11111111111111111111111111111111"), limit=5)

    for tx_meta in signatures.value:
        tx_signature = str(tx_meta.signature)
        print(f"Processing: {tx_signature}")

        tx_detail = client._provider.make_request(
            "getTransaction",
            [tx_signature, {"encoding": "json", "maxSupportedTransactionVersion": 0}]
        )

        if not tx_detail.get('result'):
            continue

        # Simulate MEV detection logic (dummy)
        is_mev = "jupiter" in str(tx_detail).lower()
        profit = round(0.5 + 2.5 * is_mev, 3)
        platforms = "Jupiter" if is_mev else "Unknown"
        path = "TokenA → TokenB → TokenC" if is_mev else "N/A"
        pattern = "Arbitrage Loop" if is_mev else "None"
        timestamp = datetime.now()

        tx_hash = tx_signature
        try:
            wallet = tx_detail['result']['transaction']['message']['accountKeys'][0]
        except (KeyError, IndexError, TypeError):
            print(f"Malformed transaction data for {tx_hash}")
            continue

        try:
            MEVTransaction.objects.update_or_create(
                tx_hash=tx_hash,
                defaults={
                    'wallet': wallet,
                    'path': path,
                    'platforms': platforms,
                    'profit': profit,
                    'is_mev': is_mev,
                    'pattern': pattern,
                    'timestamp': timestamp,
                }
            )
            print(f"Stored: {tx_hash} - MEV: {is_mev}")
        except Exception as e:
            print(f"Error saving {tx_hash}: {e}")

if __name__ == "__main__":
    decode_and_store_transactions()



























# # mev_analyzer/scripts/mev_decoder.py
#
# import os
# import django
# import sys
# import requests
# from datetime import datetime
# from solana.rpc.api import Client
# from solders.pubkey import Pubkey as PublicKey
# from solders.signature import Signature
#
#
#
# # Setup Django
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solana_mev.settings")
# django.setup()
#
# from mev_analyzer.models import MEVTransaction
#
# # Connect to Solana public RPC
# client = Client("https://api.mainnet-beta.solana.com", config={"max_supported_transaction_version": 0})
#
#
#
# def decode_and_store_transactions():
#     # Get latest confirmed transactions from a known address (can use any active one)
#     print("Fetching transactions...")
#     slot = client.get_slot().value
#     signatures = client.get_signatures_for_address(PublicKey.from_string("11111111111111111111111111111111"), limit=5)
#
#
#     for tx_meta in signatures.value:
#         tx_signature = str(tx_meta.signature)
#         print(f"Processing: {tx_signature}")
#
#         tx_detail = client._provider.make_request(
#             "getTransaction",
#             [tx_signature, {"encoding": "json", "maxSupportedTransactionVersion": 0}]
#         )
#
#         if not tx_detail['result']:
#             continue
#
#         # Simulate MEV detection logic (dummy)
#         # In real-world, parse instructions, tokens, profit, etc.
#         is_mev = "jupiter" in str(tx_detail).lower()  # crude keyword check
#         profit = round(0.5 + 2.5 * is_mev, 3)
#         platforms = "Jupiter" if is_mev else "Unknown"
#         path = "TokenA → TokenB → TokenC" if is_mev else "N/A"
#         pattern = "Arbitrage Loop" if is_mev else "None"
#         timestamp = datetime.now()
#
#         tx_hash = tx_signature
#         wallet = tx_detail['result']['transaction']['message']['accountKeys'][0]
#
#         # Store to DB
#         try:
#             MEVTransaction.objects.update_or_create(
#                 tx_hash=tx_hash,
#                 defaults={
#                     'wallet': wallet,
#                     'path': path,
#                     'platforms': platforms,
#                     'profit': profit,
#                     'is_mev': is_mev,
#                     'pattern': pattern,
#                     'timestamp': timestamp,
#                 }
#             )
#             print(f"Stored: {tx_hash} - MEV: {is_mev}")
#         except Exception as e:
#             print(f"Error saving {tx_hash}: {e}")
#
#
# if __name__ == "__main__":
#     decode_and_store_transactions()
