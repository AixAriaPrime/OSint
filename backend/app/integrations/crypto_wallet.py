from typing import Any


class CryptoWallet:
    """Cryptocurrency wallet tracking."""

    EXPLORERS: dict[str, list[dict[str, str]]] = {
        "BTC": [
            {"name": "Blockchair", "url": "https://blockchair.com/bitcoin/address/"},
            {"name": "Mempool", "url": "https://mempool.space/address/"},
            {
                "name": "Blockchain.com",
                "url": "https://www.blockchain.com/explorer/addresses/btc/",
            },
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
        "XMR": [{"name": "XMRchain", "url": "https://xmrchain.org/search?value="}],
    }

    @staticmethod
    async def lookup(wallet_address: str, blockchain: str = "BTC") -> dict[str, Any]:
        chain = blockchain.upper()
        explorers = CryptoWallet.EXPLORERS.get(chain, [])

        return {
            "wallet": wallet_address,
            "blockchain": chain,
            "explorers": [
                {"name": explorer["name"], "url": f"{explorer['url']}{wallet_address}"}
                for explorer in explorers
            ],
            "what_is_public": [
                "Balance",
                "All transactions",
                "Transaction timestamps",
                "Connected wallet addresses",
                "Amounts transferred",
            ],
        }
