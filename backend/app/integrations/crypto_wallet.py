from typing import Any, Dict


class CryptoWallet:
    """Cryptocurrency wallet tracking"""

    EXPLORERS = {
        "BTC": [
            {"name": "Blockchair", "url": "https://blockchair.com/bitcoin/address/"},
            {"name": "Mempool", "url": "https://mempool.space/address/"},
            {"name": "Blockchain.com", "url": "https://www.blockchain.com/explorer/addresses/btc/"},
        ],
        "ETH": [
            {"name": "Etherscan", "url": "https://etherscan.io/address/"},
            {"name": "Blockchair", "url": "https://blockchair.com/ethereum/address/"},
        ],
        "SOL": [
            {"name": "Solscan", "url": "https://solscan.io/address/"},
            {"name": "Solana Beach", "url": "https://solanabeach.io/address/"},
        ],
        "TRX": [{"name": "Tronscan", "url": "https://tronscan.org/#/address/"}],
        "XMR": [{"name": "XMRchain", "url": "https://xmrchain.net/address/"}],
    }

    @staticmethod
    async def lookup(wallet_address: str, blockchain: str = "BTC") -> Dict[str, Any]:
        explorers = CryptoWallet.EXPLORERS.get(blockchain.upper(), [])

        return {
            "wallet": wallet_address,
            "blockchain": blockchain.upper(),
            "explorers": [{"name": e["name"], "url": f"{e['url']}{wallet_address}"} for e in explorers],
            "what_is_public": [
                "Balance",
                "All transactions",
                "Transaction timestamps",
                "Connected wallet addresses",
                "Amounts transferred",
            ],
            "connection_mapping": [
                "Direct transfers (wallet A ↔ wallet B)",
                "Common counterparty (wallet interacts with both A and B)",
                "Exchange deposits (→ KYC identity)",
                "Cluster analysis (spending patterns)",
            ],
        }
