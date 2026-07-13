from typing import Any, Dict


class CryptoWallet:
    """Cryptocurrency wallet tracking."""

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
        "TRX": [
            {"name": "Tronscan", "url": "https://tronscan.org/#/address/"},
        ],
        "XMR": [
            {"name": "XMRchain", "url": "https://xmrchain.org/address/"},
        ],
    }

    @staticmethod
    async def lookup(wallet_address: str, blockchain: str = "BTC") -> Dict[str, Any]:
        chain = blockchain.upper()
        explorers = CryptoWallet.EXPLORERS.get(chain, [])
        return {
            "wallet": wallet_address,
            "blockchain": chain,
            "explorers": [{"name": e["name"], "url": f"{e['url']}{wallet_address}"} for e in explorers],
            "what_is_public": [
                "Balance",
                "Transactions",
                "Transaction timestamps",
                "Connected wallet addresses",
                "Transferred amounts",
            ],
            "connection_mapping": [
                "Direct transfers between wallets",
                "Common counterparties",
                "Exchange deposit detection",
                "Cluster analysis by spending patterns",
            ],
        }


class ExchangeTracker:
    """Track wallet flows to/from exchanges."""

    @staticmethod
    async def track(wallet_address: str) -> Dict[str, Any]:
        return {
            "wallet": wallet_address,
            "concept": "Transfers to known exchange wallets may map to KYC identities.",
            "how_it_works": [
                "Fetch wallet transaction history.",
                "Detect transfers to known exchange addresses.",
                "Correlate destination labels with exchange operators.",
            ],
            "known_exchanges": [
                "Coinbase",
                "Binance",
                "Kraken",
                "Bitfinex",
                "Gemini",
                "KuCoin",
                "Bybit",
                "OKX",
            ],
            "known_addresses": "https://github.com/spothound/crypto-exchange-addresses",
        }
