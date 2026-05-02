"""
Lista simplificada de cryptos disponíveis no Yahoo Finance
Baseada em pesquisa e conhecimento do mercado
"""

import pandas as pd

# Lista completa de cryptos disponíveis no Yahoo Finance
# Esta lista foi compilada com base em pesquisa e testes anteriores

all_cryptos = [
    # Major Cryptocurrencies
    ("BTC-USD", "Bitcoin"),
    ("ETH-USD", "Ethereum"),
    ("BNB-USD", "BNB"),
    ("XRP-USD", "XRP"),
    ("ADA-USD", "Cardano"),
    ("SOL-USD", "Solana"),
    ("DOGE-USD", "Dogecoin"),
    ("DOT-USD", "Polkadot"),
    ("MATIC-USD", "Polygon"),
    ("SHIB-USD", "Shiba Inu"),
    ("AVAX-USD", "Avalanche"),
    ("LINK-USD", "Chainlink"),
    ("UNI-USD", "Uniswap"),
    ("LTC-USD", "Litecoin"),
    ("ATOM-USD", "Cosmos"),
    ("XLM-USD", "Stellar"),
    ("ETC-USD", "Ethereum Classic"),
    ("FIL-USD", "Filecoin"),
    ("TRX-USD", "TRON"),
    ("VET-USD", "VeChain"),
    
    # DeFi Tokens
    ("AAVE-USD", "Aave"),
    ("MKR-USD", "Maker"),
    ("COMP-USD", "Compound"),
    ("SNX-USD", "Synthetix"),
    ("SUSHI-USD", "SushiSwap"),
    ("CRV-USD", "Curve DAO"),
    ("YFI-USD", "yearn.finance"),
    ("BAL-USD", "Balancer"),
    ("1INCH-USD", "1inch"),
    ("LDO-USD", "Lido DAO"),
    ("UNI-USD", "Uniswap"),
    ("CAKE-USD", "PancakeSwap"),
    ("ALCX-USD", "Alchemix"),
    ("PERP-USD", "Perpetual Protocol"),
    ("RUNE-USD", "THORChain"),
    ("THOR-USD", "THORChain"),
    
    # Layer 1 & Layer 2 Solutions
    ("FTM-USD", "Fantom"),
    ("NEAR-USD", "Near Protocol"),
    ("AR-USD", "Arweave"),
    ("OP-USD", "Optimism"),
    ("ARB-USD", "Arbitrum"),
    ("LRC-USD", "Loopring"),
    ("IMX-USD", "Immutable X"),
    ("MANTA-USD", "Manta Network"),
    ("QNT-USD", "Quant"),
    ("ROSE-USD", "Oasis Network"),
    ("SCRT-USD", "Secret"),
    ("CQT-USD", "Covalent"),
    ("INJ-USD", "Injective Protocol"),
    ("TIA-USD", "Celestia"),
    ("SEI-USD", "Sei"),
    ("JUP-USD", "Jupiter"),
    ("ALGO-USD", "Algorand"),
    ("EGLD-USD", "Elrond"),
    ("HBAR-USD", "Hedera"),
    ("FLOW-USD", "Flow"),
    ("MINA-USD", "Mina Protocol"),
    ("CELO-USD", "Celo"),
    ("ONE-USD", "Harmony"),
    ("ICP-USD", "Internet Computer"),
    
    # Gaming & Metaverse
    ("MANA-USD", "Decentraland"),
    ("SAND-USD", "The Sandbox"),
    ("GALA-USD", "Gala"),
    ("AXS-USD", "Axie Infinity"),
    ("ENJ-USD", "Enjin Coin"),
    ("RNDR-USD", "Render Token"),
    ("APE-USD", "ApeCoin"),
    ("CHZ-USD", "Chiliz"),
    ("ALICE-USD", "My Neighbor Alice"),
    ("TLM-USD", "Alien Worlds"),
    ("PYR-USD", "Vulcan Forged"),
    ("RARI-USD", "Rarible"),
    ("SUPER-USD", "SuperVerse"),
    ("WHAL-USD", "WHALE"),
    ("MOVR-USD", "Moonriver"),
    
    # Privacy Coins
    ("ZEC-USD", "Zcash"),
    ("DASH-USD", "Dash"),
    ("XMR-USD", "Monero"),
    ("SCRT-USD", "Secret"),
    ("XVG-USD", "Verge"),
    ("ZEN-USD", "Horizen"),
    ("FIRO-USD", "Firo"),
    ("ARRR-USD", "Pirate Chain"),
    
    # Payment & Utility Tokens
    ("BCH-USD", "Bitcoin Cash"),
    ("HOT-USD", "Holo"),
    ("CRO-USD", "Cronos"),
    ("XDC-USD", "XDC Network"),
    ("NANO-USD", "Nano"),
    ("DGB-USD", "DigiByte"),
    ("RVN-USD", "Ravencoin"),
    ("ZIL-USD", "Zilliqa"),
    ("BAT-USD", "Basic Attention Token"),
    ("ENJ-USD", "Enjin Coin"),
    ("MANA-USD", "Decentraland"),
    ("SAND-USD", "The Sandbox"),
    ("LRC-USD", "Loopring"),
    ("KNC-USD", "Kyber Network"),
    ("BNT-USD", "Bancor"),
    ("REP-USD", "Augur"),
    ("ZRX-USD", "0x"),
    ("DNT-USD", "District0x"),
    ("LPT-USD", "Livepeer"),
    ("MCO-USD", "Monaco"),
    ("CVC-USD", "Civic"),
    
    # Exchange Tokens
    ("BNB-USD", "BNB"),
    ("FTT-USD", "FTX Token"),
    ("CRO-USD", "Cronos"),
    ("KCS-USD", "KuCoin Token"),
    ("HT-USD", "Huobi Token"),
    ("OKB-USD", "OKB"),
    ("LEO-USD", "LEO Token"),
    ("GT-USD", "GateToken"),
    ("BIDR-USD", "Binance IDR"),
    ("BUSD-USD", "Binance USD"),
    
    # AI & Big Data Tokens
    ("FET-USD", "Fetch.ai"),
    ("AGIX-USD", "SingularityNET"),
    ("OCEAN-USD", "Ocean Protocol"),
    ("TAO-USD", "Bittensor"),
    ("RNDR-USD", "Render Token"),
    ("NMR-USD", "Numeraire"),
    ("GRT-USD", "The Graph"),
    ("ALEPH-USD", "Aleph.im"),
    ("ALI-USD", "Alethea AI"),
    ("ORA-USD", "ORA"),
    
    # Storage & File Sharing
    ("FIL-USD", "Filecoin"),
    ("AR-USD", "Arweave"),
    ("STORJ-USD", "Storj"),
    ("SC-USD", "Siacoin"),
    ("MASS-USD", "MASS"),
    ("SIA-USD", "Siacoin"),
    ("BLZ-USD", "Bluzelle"),
    ("HNT-USD", "Helium"),
    
    # Memecoins
    ("DOGE-USD", "Dogecoin"),
    ("SHIB-USD", "Shiba Inu"),
    ("PEPE-USD", "Pepe"),
    ("FLOKI-USD", "Floki"),
    ("BONK-USD", "Bonk"),
    ("WIF-USD", "Dogwifhat"),
    ("BABYDOGE-USD", "Baby Doge Coin"),
    ("ELON-USD", "Elon"),
    ("KISHU-USD", "Kishu Inu"),
    ("HOKK-USD", "Hokkaidu Inu"),
    ("MONG-USD", "Mong Coin"),
    ("WOJAK-USD", "Wojak"),
    ("TURBO-USD", "Turbo"),
    ("COQ-USD", "Coq Inu"),
    
    # Bitcoin Forks
    ("BCH-USD", "Bitcoin Cash"),
    ("BSV-USD", "Bitcoin SV"),
    ("BTG-USD", "Bitcoin Gold"),
    ("ETC-USD", "Ethereum Classic"),
    ("ETHW-USD", "EthereumPoW"),
    
    # Oracle & Data Feeds
    ("LINK-USD", "Chainlink"),
    ("BAND-USD", "Band Protocol"),
    ("TRB-USD", "Tellor"),
    ("API3-USD", "API3"),
    ("DTX-USD", "DTEX"),
    ("PYTH-USD", "Pyth Network"),
    ("UMA-USD", "UMA"),
    
    # Cross-Chain & Interoperability
    ("QNT-USD", "Quant"),
    ("CQT-USD", "Covalent"),
    ("ROSE-USD", "Oasis Network"),
    ("SCRT-USD", "Secret"),
    ("WAN-USD", "Wanchain"),
    ("AION-USD", "Aion"),
    ("ANY-USD", "AnySwap"),
    ("ZETA-USD", "ZetaChain"),
    ("WOO-USD", "WOO Network"),
    
    # NFT & Digital Collectibles
    ("APE-USD", "ApeCoin"),
    ("BLUR-USD", "Blur"),
    ("LOOKS-USD", "LooksRare"),
    ("X2Y2-USD", "X2Y2"),
    ("RARE-USD", "SuperRare"),
    ("SUDO-USD", "Sudo"),
    ("TLM-USD", "Alien Worlds"),
    ("RARI-USD", "Rarible"),
    
    # Real World Assets (RWA)
    ("MKR-USD", "Maker"),
    ("LDO-USD", "Lido DAO"),
    ("RPL-USD", "Rocket Pool"),
    ("SWISE-USD", "StakeWise"),
    ("FXS-USD", "Frax Share"),
    ("FRAX-USD", "Frax"),
    ("TUSD-USD", "TrueUSD"),
    ("USDP-USD", "Pax Dollar"),
    ("USDD-USD", "USDD"),
    
    # Stablecoins (for reference)
    ("USDT-USD", "Tether"),
    ("USDC-USD", "USD Coin"),
    ("BUSD-USD", "Binance USD"),
    ("DAI-USD", "Dai"),
    ("TUSD-USD", "TrueUSD"),
    ("USDP-USD", "Pax Dollar"),
    ("FRAX-USD", "Frax"),
    ("USDD-USD", "USDD"),
    ("FDUSD-USD", "First Digital USD"),
    ("PYUSD-USD", "PayPal USD"),
    ("GUSD-USD", "Gemini Dollar"),
    ("EURS-USD", "Euro Coin"),
    ("USDS-USD", "USDS"),
    
    # Emerging & New Cryptos
    ("PEPE-USD", "Pepe"),
    ("FLOKI-USD", "Floki"),
    ("BONK-USD", "Bonk"),
    ("WIF-USD", "Dogwifhat"),
    ("JUP-USD", "Jupiter"),
    ("SEI-USD", "Sei"),
    ("TIA-USD", "Celestia"),
    ("INJ-USD", "Injective Protocol"),
    ("MANTA-USD", "Manta Network"),
    ("BLUR-USD", "Blur"),
    ("LOOKS-USD", "LooksRare"),
    ("PYR-USD", "Vulcan Forged"),
    ("RARE-USD", "SuperRare"),
    
    # Bitcoin Ecosystem (Ordinals & BRC-20)
    ("ORDI-USD", "ORDI"),
    ("SATS-USD", "SATS"),
    ("RATS-USD", "RATS"),
    ("ARC-USD", "ARC"),
    ("MUBI-USD", "MUBI"),
    ("PUPS-USD", "PUPS"),
    ("BRC-USD", "BRC"),
    ("PIPE-USD", "PIPE"),
    ("DIPA-USD", "DIPA"),
    ("VMPX-USD", "VMPX"),
    ("OXBT-USD", "OXBT"),
    
    # Solana Ecosystem
    ("JUP-USD", "Jupiter"),
    ("BONK-USD", "Bonk"),
    ("WIF-USD", "Dogwifhat"),
    ("PYTH-USD", "Pyth Network"),
    ("JTO-USD", "Jito"),
    ("DRIFT-USD", "Drift"),
    ("RAY-USD", "Raydium"),
    ("MARIN-USD", "Marinade"),
    ("KAMINO-USD", "Kamino"),
    ("ZETA-USD", "Zeta"),
    
    # Additional Popular Altcoins
    ("VET-USD", "VeChain"),
    ("THETA-USD", "Theta Network"),
    ("HOT-USD", "Holo"),
    ("KSM-USD", "Kusama"),
    ("EOS-USD", "EOS"),
    ("XTZ-USD", "Tezos"),
    ("NEO-USD", "NEO"),
    ("WAVES-USD", "Waves"),
    ("ZIL-USD", "Zilliqa"),
    ("BAT-USD", "Basic Attention Token"),
    ("ENJ-USD", "Enjin Coin"),
    ("MANA-USD", "Decentraland"),
    ("SAND-USD", "The Sandbox"),
    ("LRC-USD", "Loopring"),
    ("KNC-USD", "Kyber Network"),
    ("BNT-USD", "Bancor"),
    ("REP-USD", "Augur"),
    ("ZRX-USD", "0x"),
    
    # More Comprehensive List
    ("ANKR-USD", "Ankr"),
    ("ANT-USD", "Aragon"),
    ("ARDR-USD", "Ardor"),
    ("ARK-USD", "Ark"),
    ("ARKM-USD", "Arkham"),
    ("ARPA-USD", "ARPA"),
    ("AST-USD", "AirSwap"),
    ("ASTR-USD", "Astar"),
    ("ATA-USD", "Automata"),
    ("ATH-USD", "Aethir"),
    ("ATLAS-USD", "Star Atlas"),
    ("AUCTION-USD", "Auction"),
    ("AUDIO-USD", "Audius"),
    ("AUTO-USD", "Auto"),
    ("AVA-USD", "Travala.com"),
    ("AXL-USD", "Axelar"),
    ("BADGER-USD", "Badger DAO"),
    ("BAKE-USD", "BakeryToken"),
    ("BAL-USD", "Balancer"),
    ("BAND-USD", "Band Protocol"),
    ("BANK-USD", "Bankless DAO"),
    ("BCH-USD", "Bitcoin Cash"),
    ("BDI-USD", "BidiPass"),
    ("BENQI-USD", "Benqi"),
    ("BICO-USD", "Biconomy"),
    ("BIFI-USD", "Beefy Finance"),
    ("BLUR-USD", "Blur"),
    ("BLZ-USD", "Bluzelle"),
    ("BNT-USD", "Bancor"),
    ("BNX-USD", "BinaryX"),
    ("BOND-USD", "BarnBridge"),
    ("BOTA-USD", "Bottos"),
    ("BREED-USD", "Breed"),
    ("BRG-USD", "Bridge Oracle"),
    ("BRZ-USD", "Brazilian Digital Token"),
    ("BSW-USD", "Biswap"),
    ("BTRST-USD", "Braintrust"),
    ("BTT-USD", "BitTorrent"),
    ("BURGER-USD", "BurgerCities"),
    ("C98-USD", "Coin98"),
    ("CAN-USD", "CanYaCoin"),
    ("CAP-USD", "Cap"),
    ("CASH-USD", "Cashaa"),
    ("CATE-USD", "CateCoin"),
    ("CAW-USD", "A Hunters Dream"),
    ("CCXX-USD", "Counos X"),
    ("CELO-USD", "Celo"),
    ("CELR-USD", "Celer Network"),
    ("CERE-USD", "Cere Network"),
    ("CFT-USD", "CoinFi"),
    ("CGPT-USD", "ChainGPT"),
    ("CHAIN-USD", "Chain"),
    ("CHAT-USD", "ChatCoin"),
    ("CHZ-USD", "Chiliz"),
    ("CIV-USD", "Civic"),
    ("CKB-USD", "Nervos Network"),
    ("CLV-USD", "Clover Finance"),
    ("CND-USD", "Cindicator"),
    ("COCOS-USD", "COCOS BCX"),
    ("CODE-USD", "CodeChain"),
    ("COIN-USD", "Coin"),
    ("COMBO-USD", "COMBO"),
    ("COMP-USD", "Compound"),
    ("CQT-USD", "Covalent"),
    ("CRO-USD", "Cronos"),
    ("CRPT-USD", "Crypterium"),
    ("CRV-USD", "Curve DAO Token"),
    ("CTK-USD", "Certik"),
    ("CTSI-USD", "Cartesi"),
    ("CTXC-USD", "Cortex"),
    ("CVC-USD", "Civic"),
    ("CVP-USD", "PowerPool"),
    ("CVX-USD", "Convex Finance"),
    ("CXO-USD", "CargoX"),
    ("DAR-USD", "Mines of Dalarnia"),
    ("DASH-USD", "Dash"),
    ("DATA-USD", "Streamr"),
    ("DAI-USD", "Dai"),
    ("DEGEN-USD", "DEGEN"),
    ("DEGO-USD", "DEGO"),
    ("DEUS-USD", "DEUS"),
    ("DF-USD", "dForce"),
    ("DGB-USD", "DigiByte"),
    ("DIA-USD", "DIA"),
    ("DODO-USD", "DODO"),
    ("DOGE-USD", "Dogecoin"),
    ("DOMI-USD", "Dominium"),
    ("DON-USD", "Donu"),
    ("DOT-USD", "Polkadot"),
    ("DREP-USD", "DREP"),
    ("DUSK-USD", "Dusk"),
    ("DXD-USD", "DuckDaoDime"),
    ("DXE-USD", "DXE"),
    ("DYDX-USD", "dYdX"),
    ("DYP-USD", "DYP"),
    ("EASY-USD", "Easy"),
    ("ECHO-USD", "Echo"),
    ("EDU-USD", "EDU"),
    ("EFI-USD", "Efinity"),
    ("EGLD-USD", "Elrond"),
    ("EIGEN-USD", "EigenLayer"),
    ("ELF-USD", "aelf"),
    ("ELON-USD", "Elon"),
    ("ELSD-USD", "Elysium"),
    ("EMBERS-USD", "Embers"),
    ("ENJ-USD", "Enjin Coin"),
    ("ENS-USD", "Ethereum Name Service"),
    ("EON-USD", "EON"),
    ("EOS-USD", "EOS"),
    ("EPIK-USD", "Epik Prime"),
    ("EPS-USD", "Ellipsis"),
    ("ERG-USD", "Ergo"),
    ("ERN-USD", "Ethernity Chain"),
    ("ESD-USD", "Empty Set Dollar"),
    ("ESP-USD", "Espers"),
    ("ETC-USD", "Ethereum Classic"),
    ("ETH-USD", "Ethereum"),
    ("ETHF-USD", "EthereumFair"),
    ("ETHW-USD", "EthereumPoW"),
    ("EVU-USD", "EduVation"),
    ("EWT-USD", "Energy Web Token"),
    ("EXRD-USD", "EthereumX"),
    ("FARM-USD", "Harvest Finance"),
    ("FET-USD", "Fetch.ai"),
    ("FIDA-USD", "Bonfida"),
    ("FIL-USD", "Filecoin"),
    ("FINS-USD", "Fins"),
    ("FIRO-USD", "Firo"),
    ("FLM-USD", "Flamingo"),
    ("FLOKI-USD", "Floki"),
    ("FLOW-USD", "Flow"),
    ("FLR-USD", "Flare"),
    ("FLUX-USD", "Flux"),
    ("FORTH-USD", "Ampleforth Governance Token"),
    ("FOUR-USD", "Fourth Revolution"),
    ("FOX-USD", "Shapeshift FOX Token"),
    ("FRAX-USD", "Frax"),
    ("FRENS-USD", "Frens"),
    ("FRM-USD", "Ferrum Network"),
    ("FTM-USD", "Fantom"),
    ("FTT-USD", "FTX Token"),
    ("FXS-USD", "Frax Share"),
    ("GALA-USD", "Gala"),
    ("GAL-USD", "Project Galaxy"),
    ("GAS-USD", "Gas"),
    ("GFT-USD", "Gifto"),
    ("GNO-USD", "Gnosis"),
    ("GNS-USD", "Gains Network"),
    ("GMT-USD", "STEPN"),
    ("GNO-USD", "Gnosis"),
    ("GODS-USD", "Gods Unchained"),
    ("GRT-USD", "The Graph"),
    ("GTC-USD", "Gitcoin"),
    ("GTAI-USD", "GT Protocol"),
    ("GT-USD", "GateToken"),
    ("GTO-USD", "Gifto"),
    ("GTX-USD", "GTX"),
    ("GYEN-USD", "GYEN"),
    ("HARD-USD", "Hard Protocol"),
    ("HBAR-USD", "Hedera"),
    ("HEGIC-USD", "Hegic"),
    ("HELMET-USD", "Helmet"),
    ("HERO-USD", "Hero"),
    ("HFT-USD", "Hashflow"),
    ("HGET-USD", "HGET"),
    ("HIVE-USD", "Hive"),
    ("HNT-USD", "Helium"),
    ("HOPR-USD", "HOPR"),
    ("HOT-USD", "Holo"),
    ("HOTCROSS-USD", "Hot Cross"),
    ("HPS-USD", "HOPERS"),
    ("HT-USD", "Huobi Token"),
    ("HTR-USD", "Hathor"),
    ("ICE-USD", "ICE"),
    ("ICP-USD", "Internet Computer"),
    ("ICX-USD", "ICON"),
    ("ID-USD", "SPACE ID"),
    ("IDEX-USD", "IDEX"),
    ("ILV-USD", "Illuvium"),
    ("IMX-USD", "Immutable X"),
    ("INJ-USD", "Injective Protocol"),
    ("INSUR-USD", "InsurAce"),
    ("IOST-USD", "IOST"),
    ("IOTX-USD", "IoTeX"),
    ("IQ-USD", "Everipedia"),
    ("IRIS-USD", "IRISnet"),
    ("ISP-USD", "Ispolink"),
    ("JASMY-USD", "JasmyCoin"),
    ("JST-USD", "Just"),
    ("JTO-USD", "Jito"),
    ("JUV-USD", "Juventus Fan Token"),
    ("KAI-USD", "KardiaChain"),
    ("KAR-USD", "KardiaChain"),
    ("KAVA-USD", "Kava"),
    ("KDA-USD", "Kadena"),
    ("KCS-USD", "KuCoin Token"),
    ("KEY-USD", "SelfKey"),
    ("KILT-USD", "KILT Protocol"),
    ("KISHU-USD", "Kishu Inu"),
    ("KLAY-USD", "Klaytn"),
    ("KMD-USD", "Komodo"),
    ("KNC-USD", "Kyber Network"),
    ("KSM-USD", "Kusama"),
    ("KUB-USD", "Kubcoin"),
    ("LADYS-USD", "LADYS"),
    ("LAI-USD", "LAI"),
    ("LAMB-USD", "Lambda"),
    ("LBA-USD", "Libra Credit"),
    ("LDO-USD", "Lido DAO"),
    ("LEO-USD", "LEO Token"),
    ("LGCY-USD", "LGCY Network"),
    ("LINA-USD", "Linear"),
    ("LINK-USD", "Chainlink"),
    ("LIT-USD", "Litentry"),
    ("LOKA-USD", "League of Kingdoms Arena"),
    ("LOOKS-USD", "LooksRare"),
    ("LOOM-USD", "Loom Network"),
    ("LPT-USD", "Livepeer"),
    ("LQTY-USD", "Liquity"),
    ("LRC-USD", "Loopring"),
    ("LTO-USD", "LTO Network"),
    ("LUNA-USD", "Terra"),
    ("LUNA2-USD", "Terra 2.0"),
    ("MAGIC-USD", "MAGIC"),
    ("MANA-USD", "Decentraland"),
    ("MASK-USD", "Mask Network"),
    ("MATH-USD", "MATH"),
    ("MATIC-USD", "Polygon"),
    ("MAV-USD", "Maverick Protocol"),
    ("MCB-USD", "MCDEX"),
    ("MBOX-USD", "Mobox"),
    ("MDT-USD", "Measurable Data Token"),
    ("MEDA-USD", "MediBloc"),
    ("MELD-USD", "MELD"),
    ("METIS-USD", "MetisDAO"),
    ("MFT-USD", "Mainframe"),
    ("MINA-USD", "Mina Protocol"),
    ("MIR-USD", "Mirror Protocol"),
    ("MITH-USD", "Mithril"),
    ("MKR-USD", "Maker"),
    ("MLN-USD", "Enzyme"),
    ("MOB-USD", "MobileCoin"),
    ("MOVR-USD", "Moonriver"),
    ("MTA-USD", "mStable"),
    ("MTL-USD", "Metal"),
    ("MTLX-USD", "Metallurgy"),
    ("MULTI-USD", "Multichain"),
    ("MUSE-USD", "Muse"),
    ("MV-USD", "Maverick"),
    ("MXC-USD", "MXC"),
    ("MYC-USD", "MYCE"),
    ("MYST-USD", "Mysterium"),
    ("NAKA-USD", "Nakamigos"),
    ("NANO-USD", "Nano"),
    ("NAS-USD", "Nebulas"),
    ("NAV-USD", "NavCoin"),
    ("NBS-USD", "New BitShares"),
    ("NCT-USD", "Nature Carbon Ton"),
    ("NEAR-USD", "Near Protocol"),
    ("NEBL-USD", "Neblio"),
    ("NEO-USD", "NEO"),
    ("NEXO-USD", "Nexo"),
    ("NFT-USD", "NFT"),
    ("NKN-USD", "NKN"),
    ("NMR-USD", "Numeraire"),
    ("NULS-USD", "NULS"),
    ("NXM-USD", "Nexus Mutual"),
    ("OAX-USD", "OpenAsset Exchange"),
    ("OCEAN-USD", "Ocean Protocol"),
    ("OCTO-USD", "OctoSpace"),
    ("OG-USD", "OG Fan Token"),
    ("OJO-USD", "OJO"),
    ("OKB-USD", "OKB"),
    ("OMG-USD", "OMG"),
    ("OMNI-USD", "Omni"),
    ("ONE-USD", "Harmony"),
    ("OOKI-USD", "Ooki"),
    ("OP-USD", "Optimism"),
    ("ORAI-USD", "Oraichain"),
    ("ORBS-USD", "Orbs"),
    ("ORN-USD", "Orao"),
    ("OSMO-USD", "Osmosis"),
    ("OXT-USD", "Orchid"),
    ("OXY-USD", "Oxygen"),
    ("PAID-USD", "PAID Network"),
    ("PAN-USD", "Panvala pan"),
    ("PARA-USD", "ParaSwap"),
    ("PASS-USD", "Pass"),
    ("PAXG-USD", "PAX Gold"),
    ("PEPE-USD", "Pepe"),
    ("PERP-USD", "Perpetual Protocol"),
    ("PHA-USD", "Phala Network"),
    ("PHB-USD", "Phoenix Global"),
    ("PHX-USD", "Red Pulse Phoenix"),
    ("PI-USD", "PCHAIN"),
    ("PIVX-USD", "PIVX"),
    ("PIXEL-USD", "Pixel"),
    ("PKR-USD", "Poker"),
    ("PLA-USD", "PlayDapp"),
    ("PLU-USD", "Pluton"),
    ("PLY-USD", "PlayDapp"),
    ("PNG-USD", "Pangolin"),
    ("POLIS-USD", "Polispay"),
    ("POLY-USD", "Polymath"),
    ("POLS-USD", "Polkastarter"),
    ("POND-USD", "Marlin"),
    ("PORTAL-USD", "Portal"),
    ("POWR-USD", "Power Ledger"),
    ("PRQ-USD", "PARSIQ"),
    ("PSG-USD", "Paris Saint-Germain Fan Token"),
    ("PSTAKE-USD", "pSTAKE"),
    ("PTU-USD", "Pata"),
    ("PUNDIX-USD", "Pundi X"),
    ("PYR-USD", "Vulcan Forged"),
    ("PYTH-USD", "Pyth Network"),
    ("QI-USD", "Benqi"),
    ("QNT-USD", "Quant"),
    ("QSP-USD", "Quantstamp"),
    ("QTUM-USD", "Qtum"),
    ("RARE-USD", "SuperRare"),
    ("RARI-USD", "Rarible"),
    ("RAY-USD", "Raydium"),
    ("RCN-USD", "Ripio Credit Network"),
    ("RDN-USD", "Raiden Network"),
    ("RDNT-USD", "Radiant Capital"),
    ("REEF-USD", "Reef"),
    ("REI-USD", "REI Network"),
    ("RENDER-USD", "Render"),
    ("REN-USD", "Ren"),
    ("REP-USD", "Augur"),
    ("REQ-USD", "Request"),
    ("RGT-USD", "Rari Governance Token"),
    ("RIF-USD", "RSK Infrastructure Framework"),
    ("RLC-USD", "iExec RLC"),
    ("RNGR-USD", "Ranger"),
    ("ROCK-USD", "Rock"),
    ("ROSE-USD", "Oasis Network"),
    ("RPL-USD", "Rocket Pool"),
    ("RSR-USD", "Reserve Rights"),
    ("RSS3-USD", "RSS3"),
    ("RUNE-USD", "THORChain"),
    ("RVN-USD", "Ravencoin"),
    ("SALT-USD", "Salt"),
    ("SAND-USD", "The Sandbox"),
    ("SANTOS-USD", "Santos FC Fan Token"),
    ("SASHIMI-USD", "Sashimi"),
    ("SC-USD", "Siacoin"),
    ("SCRT-USD", "Secret"),
    ("SDN-USD", "Shiden"),
    ("SEI-USD", "Sei"),
    ("SFP-USD", "SafePal"),
    ("SHIB-USD", "Shiba Inu"),
    ("SHIP-USD", "ShipChain"),
    ("SHOPX-USD", "SHOPX"),
    ("SIPHER-USD", "Sipher"),
    ("SKL-USD", "SKALE"),
    ("SKY-USD", "Sky"),
    ("SLP-USD", "Smooth Love Potion"),
    ("SNT-USD", "Status"),
    ("SNX-USD", "Synthetix"),
    ("SOL-USD", "Solana"),
    ("SOV-USD", "Sovryn"),
    ("SPACE-USD", "Space"),
    ("SPARTA-USD", "Spartan Protocol"),
    ("SPD-USD", "SpaceID"),
    ("SPELL-USD", "Spell Token"),
    ("SPIN-USD", "Spin"),
    ("SPO-USD", "Spore"),
    ("SRM-USD", "Serum"),
    ("SSV-USD", "SSV Network"),
    ("STAR-USD", "Star"),
    ("STARS-USD", "Stargaze"),
    ("STG-USD", "Stargate Finance"),
    ("STMX-USD", "StormX"),
    ("STND-USD", "Standard"),
    ("STORJ-USD", "Storj"),
    ("STPT-USD", "STP"),
    ("STRAX-USD", "Stratis"),
    ("STRM-USD", "Stream"),
    ("STX-USD", "Blockstack"),
    ("SUI-USD", "Sui"),
    ("SUPER-USD", "SuperVerse"),
    ("SUSHI-USD", "SushiSwap"),
    ("SUTER-USD", "Suterusu"),
    ("SWFTC-USD", "SwftCoin"),
    ("SWISE-USD", "StakeWise"),
    ("SWPR-USD", "Swapr"),
    ("SYN-USD", "Synapse"),
    ("SYS-USD", "Syscoin"),
    ("TAO-USD", "Bittensor"),
    ("TAROT-USD", "Tarot"),
    ("TARA-USD", "Taraxa"),
    ("TCT-USD", "TokenClub"),
    ("TEER-USD", "Everscale"),
    ("TEL-USD", "Telcoin"),
    ("TLOS-USD", "Telos"),
    ("TLM-USD", "Alien Worlds"),
    ("TMO-USD", "TMO"),
    ("TMTG-USD", "TMTG"),
    ("TOMO-USD", "Tomochain"),
    ("TON-USD", "Toncoin"),
    ("TOOL-USD", "ToolChain"),
    ("TOP-USD", "Topchain"),
    ("TRAC-USD", "OriginTrail"),
    ("TRB-USD", "Tellor"),
    ("TROY-USD", "TROY"),
    ("TRU-USD", "TrueFi"),
    ("TRX-USD", "TRON"),
    ("TUSD-USD", "TrueUSD"),
    ("TVK-USD", "Terra Virtua Kolect"),
    ("TWT-USD", "Trust Wallet Token"),
    ("TXA-USD", "TXA"),
    ("UFT-USD", "UniLend"),
    ("UMA-USD", "UMA"),
    ("UNFI-USD", "Unifi Protocol"),
    ("UNI-USD", "Uniswap"),
    ("USDD-USD", "USDD"),
    ("USDP-USD", "Pax Dollar"),
    ("USDS-USD", "USDS"),
    ("USDT-USD", "Tether"),
    ("UTK-USD", "Utrust"),
    ("UTOR-USD", "Utopia"),
    ("VAI-USD", "Vai"),
    ("VANRY-USD", "Vanar"),
    ("VEMP-USD", "vEmpire DDAO"),
    ("VEN-USD", "VeChain"),
    ("VEGA-USD", "Vega Protocol"),
    ("VELO-USD", "Velo"),
    ("VET-USD", "VeChain"),
    ("VIB-USD", "Viberate"),
    ("VIDT-USD", "VIDT Datalink"),
    ("VITE-USD", "Vite"),
    ("VRA-USD", "Verasity"),
    ("VRX-USD", "Verox"),
    ("VTHO-USD", "VeChainThor"),
    ("WABI-USD", "Wabi"),
    ("WAN-USD", "Wanchain"),
    ("WAVES-USD", "Waves"),
    ("WAX-USD", "WAX"),
    ("WBT-USD", "WhiteBIT Token"),
    ("WCFG-USD", "Wrapped Celo Gold"),
    ("WEMIX-USD", "WEMIX"),
    ("WHALE-USD", "WHALE"),
    ("WILD-USD", "Wilder World"),
    ("WOO-USD", "WOO Network"),
    ("WPR-USD", "WePower"),
    ("WRX-USD", "WazirX"),
    ("WSTETH-USD", "Wrapped stETH"),
    ("XAUT-USD", "Tether Gold"),
    ("XAVA-USD", "Avax"),
    ("XCH-USD", "Chia"),
    ("XCN-USD", "Chain"),
    ("XDC-USD", "XDC Network"),
    ("XEC-USD", "eCash"),
    ("XEM-USD", "NEM"),
    ("XETH-USD", "XETH"),
    ("XLM-USD", "Stellar"),
    ("XMON-USD", "XMON"),
    ("XNO-USD", "Nano"),
    ("XOR-USD", "Sora"),
    ("XRP-USD", "XRP"),
    ("XRT-USD", "XRT"),
    ("XTZ-USD", "Tezos"),
    ("XVG-USD", "Verge"),
    ("XVS-USD", "Venus"),
    ("YFII-USD", "DFI.Money"),
    ("YFI-USD", "yearn.finance"),
    ("YGG-USD", "Yield Guild Games"),
    ("YFV-USD", "YFValue"),
    ("ZBC-USD", "Zebec"),
    ("ZEC-USD", "Zcash"),
    ("ZEN-USD", "Horizen"),
    ("ZETA-USD", "ZetaChain"),
    ("ZIL-USD", "Zilliqa"),
    ("ZK-USD", "ZK"),
    ("ZKL-USD", "ZKsync"),
    ("ZRX-USD", "0x"),
    ("ZEE-USD", "ZEE"),
    ("ZKS-USD", "ZKS"),
    ("ZMT-USD", "ZMT"),
]

def main():
    """Função principal para gerar os arquivos"""
    
    print("🚀 Gerando lista completa de cryptos do Yahoo Finance...")
    print(f"📊 Total de cryptos: {len(all_cryptos)}")
    
    # Criar DataFrame
    df = pd.DataFrame(all_cryptos, columns=['Symbol', 'Name'])
    
    # Ordenar por símbolo
    df = df.sort_values('Symbol')
    
    # Salvar CSV
    csv_filename = 'yfinance_all_cryptos_complete.csv'
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"💾 CSV salvo: {csv_filename}")
    
    # Criar arquivo Python para importação
    py_filename = 'crypto_symbols_complete.py'
    
    # Criar dicionário
    crypto_dict = dict(all_cryptos)
    
    # Separar por categorias principais
    major_cryptos = {symbol: name for symbol, name in all_cryptos 
                    if symbol in ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 
                                 'SOL-USD', 'DOGE-USD', 'DOT-USD', 'MATIC-USD', 'SHIB-USD', 
                                 'AVAX-USD', 'LINK-USD', 'UNI-USD', 'LTC-USD', 'ATOM-USD', 'XLM-USD']}
    
    defi_tokens = {symbol: name for symbol, name in all_cryptos 
                  if symbol in ['AAVE-USD', 'MKR-USD', 'COMP-USD', 'SNX-USD', 'SUSHI-USD', 
                               'CRV-USD', 'YFI-USD', 'BAL-USD', '1INCH-USD', 'LDO-USD']}
    
    gaming_tokens = {symbol: name for symbol, name in all_cryptos 
                    if symbol in ['MANA-USD', 'SAND-USD', 'GALA-USD', 'AXS-USD', 'ENJ-USD', 
                                 'CHZ-USD', 'APE-USD']}
    
    memecoins = {symbol: name for symbol, name in all_cryptos 
                if symbol in ['DOGE-USD', 'SHIB-USD', 'PEPE-USD', 'FLOKI-USD', 'BONK-USD']}
    
    content = f'''"""
Lista COMPLETA de cryptos disponíveis no Yahoo Finance
Total: {len(all_cryptos)} cryptos
Gerado em: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

# Dicionário completo de cryptos
CRYPTO_SYMBOLS = {crypto_dict}

# Lista de todos os símbolos
ALL_CRYPTO_SYMBOLS = {list(crypto_dict.keys())}

# Lista de todos os nomes
ALL_CRYPTO_NAMES = {list(crypto_dict.values())}

# Principais cryptos (Top 20)
MAJOR_CRYPTOS = {major_cryptos}

# Tokens DeFi
DEFI_TOKENS = {defi_tokens}

# Tokens de Gaming
GAMING_TOKENS = {gaming_tokens}

# Memecoins
MEMECOINS = {memecoins}

def get_crypto_name(symbol):
    """Retorna o nome da crypto pelo símbolo"""
    return CRYPTO_SYMBOLS.get(symbol, "Unknown")

def get_all_symbols():
    """Retorna todos os símbolos de crypto"""
    return ALL_CRYPTO_SYMBOLS

def get_all_names():
    """Retorna todos os nomes de crypto"""
    return ALL_CRYPTO_NAMES

def search_crypto(query):
    """Busca crypto por símbolo ou nome"""
    query = query.lower()
    results = []
    
    for symbol, name in CRYPTO_SYMBOLS.items():
        if query in symbol.lower() or query in name.lower():
            results.append((symbol, name))
    
    return results

def get_cryptos_by_category(category):
    """Retorna cryptos por categoria"""
    categories = {{
        'major': MAJOR_CRYPTOS,
        'defi': DEFI_TOKENS,
        'gaming': GAMING_TOKENS,
        'memecoin': MEMECOINS
    }}
    
    return categories.get(category.lower(), {{}})

def get_random_crypto():
    """Retorna uma crypto aleatória"""
    import random
    symbol, name = random.choice(list(CRYPTO_SYMBOLS.items()))
    return symbol, name

def filter_by_symbol_start(prefix):
    """Filtra cryptos por prefixo do símbolo"""
    return {{symbol: name for symbol, name in CRYPTO_SYMBOLS.items() 
            if symbol.startswith(prefix)}}

def filter_by_name_keyword(keyword):
    """Filtra cryptos por palavra-chave no nome"""
    keyword = keyword.lower()
    return {{symbol: name for symbol, name in CRYPTO_SYMBOLS.items() 
            if keyword in name.lower()}}

# Exemplo de uso:
if __name__ == "__main__":
    print("🚀 Lista de cryptos disponíveis:")
    
    # Mostrar algumas cryptos de exemplo
    examples = list(CRYPTO_SYMBOLS.items())[:10]
    for symbol, name in examples:
        print(f"  {{symbol}}: {{name}}")
    
    print(f"\\n📊 Total disponível: {{len(CRYPTO_SYMBOLS)}} cryptos")
    print(f"🥇 Major cryptos: {{len(MAJOR_CRYPTOS)}}")
    print(f"🏦 DeFi tokens: {{len(DEFI_TOKENS)}}")
    print(f"🎮 Gaming tokens: {{len(GAMING_TOKENS)}}")
    print(f"🐸 Memecoins: {{len(MEMECOINS)}}")
    
    # Exemplo de busca
    print("\\n🔍 Exemplo de busca por 'Bitcoin':")
    results = search_crypto('Bitcoin')
    for symbol, name in results[:5]:
        print(f"  {{symbol}}: {{name}}")
'''
    
    with open(py_filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Arquivo Python salvo: {py_filename}")
    
    # Estatísticas
    print("\n" + "=" * 80)
    print("📊 ESTATÍSTICAS:")
    print("=" * 80)
    print(f"✅ Total de cryptos: {len(all_cryptos)}")
    print(f"🥇 Major cryptos: {len(major_cryptos)}")
    print(f"🏦 DeFi tokens: {len(defi_tokens)}")
    print(f"🎮 Gaming tokens: {len(gaming_tokens)}")
    print(f"🐸 Memecoins: {len(memecoins)}")
    
    # Exemplos
    print(f"\n🔍 Exemplos de cryptos disponíveis:")
    for i, (symbol, name) in enumerate(all_cryptos[:15]):
        print(f"  {symbol}: {name}")
    
    print(f"\n📂 Arquivos criados:")
    print(f"  📄 {csv_filename} - Planilha com todas as cryptos")
    print(f"  🐍 {py_filename} - Arquivo Python para importação")
    
    print(f"\n🚀 Como usar no seu sistema:")
    print(f"  from crypto_symbols_complete import CRYPTO_SYMBOLS, get_crypto_name")
    print(f"  ")
    print(f"  # Usar no YahooProvider:")
    print(f"  crypto_provider = YahooProvider(period='10y', interval='1d')")
    print(f"  btc_data = MarketAsset('BTC-USD', provider=crypto_provider)")
    print(f"  eth_data = MarketAsset('ETH-USD', provider=crypto_provider)")
    
    return df, crypto_dict

if __name__ == "__main__":
    df, crypto_dict = main()
