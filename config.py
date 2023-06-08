BLOCKCHAINS = ['bitcoin', 'ethereum', 'xrp',
               'binance-smart-chain', 'tron']

ADDRESSES = {
    "ethereum": "0x437dabbfea2e898783ec0f7402c706bfc5c47c0f",
    "ethereum-classic": "0xb5ca7bfae998b6071a96dcd923de86a6c244e3bb",
    "binance-smart-chain": "0x995bbe0ae362b97cb1b7361258e06822cb9ce9b9",
    "bitcoin": "bc1q8dmrz6eupzdvke98p9p9tyjtw3klx62sqtv73e",
    "tron": "TFt6gK2eNEMhHpdcPQJikRtpFxVcQam26x",
    "bitcoin-cash": "bitcoincash:qz04r7qwuvf3aa62xng80qsg7hxjmgvqj5gd7ue09r",
    "dash": "XsgmMoa4y3oyNDwJxQRPbbRu7JEhQ8hAfB",
    "dogecoin": "D8tCmWBMCXCXrNo2rtB2B97wVKg1Ya6NVn",
    "litecoin": "LKeucMavZ6JL4ZyV6LYsD6mQWauzGiDLs6",
    "zcash": "t1RwLzNX8PDAp4CG4swSX3onF2aVUtXKmUa"
}

# ADDRESSES = {
#     "ethereum": "0x1394a8be5b8fbb43c658679a4fb16abd792adbf4",
#     "binance-smart-chain": "0xab4035952e374671320d0563136dcdfd56e3c91e",
#     "bitcoin": "bc1qnkhnykpqpllu6nfha6y5tuf342kx6mfuyzjpl3",
#     "tron": "TSjG8nVcsys6QBBWfv1mwan7eR9dnXLHUo",
#     "bitcoin-cash": "bitcoincash:qqydfqyujx5ccwzz4n6yat7m0y5wvqm5aca2e9jqqq",
#     "dash": "XifmyVbGuZjtnFNTvRA7qBSnAVV1H5Y9bo",
#     "dogecoin": "DT3LMJP2997xwtbBgtb9sZ6rnuec3y32yV",
#     "litecoin": "Lc4jHTuVohmuy54KcUCfyRkoR35sYMD2WN",
#     "zcash": "t1gwTgnJ29dLNF36BrZ4Le2yJGeA488um5d"
# }

BINANCE_ADDRESSES = {
    "ethereum": "0x3422403275713e2875b59237542b37f1fb7047d4",
    "binance-smart-chain": "0x3422403275713e2875b59237542b37f1fb7047d4",
    "bitcoin": "17BmDJbz4RMGmLAiViGW5oFqD3xPHFV36k",
    "tron": "TGmVf1sUkyu9eFvJPpYi6uMe9fTPuf6zzq",
    "bitcoin-cash": '17BmDJbz4RMGmLAiViGW5oFqD3xPHFV36k',
    "dash": "Xv5ja3BsHn3ce1AcbW8AoxJUb2qJwEtWb5",
    "dogecoin": "D7hT4qeKDYJTYwRUbs47qPVb4EFDn969KT",
    "litecoin": "LXjQt2PhE7siC5UYXhq9snPrXgQtGtFBgz",
    "zcash": "t1enfk7Vftfniwi2x833L61BZcvSTZj2vWY"
}

# BINANCE_ADDRESSES = {
#     "ethereum": "0x5c3060ecaf38519a7c14e77d2c20802a6f5e119f",
#     "binance-smart-chain": "0x5c3060ecaf38519a7c14e77d2c20802a6f5e119f",
#     "bitcoin": "13bFs1qPC7uz5iFJF1cGdYGbKLwT1TEdde",
#     "tron": "TGtKp69xe2W8a8PqXpVsFsWNFR3YQz6ASM",
#     "bitcoin-cash": '13bFs1qPC7uz5iFJF1cGdYGbKLwT1TEdde',
#     "dash": "XsJa4Edfv3vy5Mad8vGmYhLvDN4fNPfm97",
#     "dogecoin": "DPRPQNosU3trqzTJMhUEJYRiJuJx3rh3Pu",
#     "litecoin": "LaMKu4QHLrayJH8RN6BCecuFH8TWwmQrsg",
#     "zcash": "t1YAgEZtCEH6WBFmJRbzjLLGQX1ZPSGD8hU"
# }

# BINANCE_INVEST_ADDRESSES = {
#     "ethereum": "0x040a7a61cdc22da003f379fc0bc8b4999c0d0bc3",
#     "binance-smart-chain": "0x040a7a61cdc22da003f379fc0bc8b4999c0d0bc3",
#     "bitcoin": "1C5juPSVCEM4wWYCm5Fmf5v3rqjU98cene",
#     "tron": "TH63xpXnGnUAsQh5LEC3r6zDQ3gBx4Dp8E",
#     "bitcoin-cash": '1C5juPSVCEM4wWYCm5Fmf5v3rqjU98cene',
#     "dash": "XkGkF1pZFTSd2nDJxhp267sJcRjmXJgSH8",
#     "dogecoin": "DD9p2mbrAkPNHwpjBRAidVXsnBLZdTS6Gy",
#     "litecoin": "LaQVsncoFQMtTgxat7yZw3pDv3Q81JpN5X",
#     "zcash": "t1Y8eUmHosFQSrfncg6Hoqv2UeQTSezNxwi"
# }

BINANCE_INVEST_ADDRESSES = {
    "ethereum": "0x015dcc4c986adb777e6f4b2b90a4b56c18dd167f",
    "binance-smart-chain": "0x015dcc4c986adb777e6f4b2b90a4b56c18dd167f",
    "tron": "THwkoJAgi3sLAWB3DQGF9DoofzBcLHXxnC"
}


SUPPORTED_COINS = {
    "bitcoin": [
        {
            "symbol": "BTC"
        }
    ],
    "tron": [
        {
            "decimals": 6,
            "identifier": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
            "name": "Tether",
            "symbol": "USDT",
            "type": "TRC-20"
        },
        {
            "decimals": 6,
            "identifier": "TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8",
            "name": "USD Coin",
            "symbol": "USDC",
            "type": "TRC-20"
        },
        {
            "decimals": 18,
            "identifier": "TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4",
            "name": "BitTorrent-New",
            "symbol": "BTT",
            "type": "TRC20"
        },
        {
            "decimals": 18,
            "identifier": "TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9",
            "name": "JUST",
            "symbol": "JUST",
            "type": "TRC-20"
        }
    ],
    "ethereum": [
        {
            "decimals": 6,
            "identifier": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "name": "Tether",
            "symbol": "USDT",
            "type": "ERC-20"
        },
        {
            "decimals": 6,
            "identifier": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "name": "USD Coin",
            "symbol": "USDC",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x111111111117dc0aa78b770fa6a738034120c302",
            "name": "1inch Network",
            "symbol": "1INCH",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
            "name": "Aave",
            "symbol": "AAVE",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xff20817765cb7f73d4bde2e66e067e58d11095c2",
            "name": "Amp",
            "symbol": "AMP",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x4d224452801aced8b2f0aebe155379bb5d594381",
            "name": "ApeCoin",
            "symbol": "APE",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xbb0e17ef65f82ab018d8edd776e8dd940327b28b",
            "name": "Axie Infinity",
            "symbol": "AXS",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0xBA11D00c5f74255f56a5E366F4F77f5A186d7f55",
            "name": "Band Protocol",
            "symbol": "BAND",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x0d8775f648430679a709e98d2b0cb6250d2887ef",
            "name": "Basic Attention Token",
            "symbol": "BAT",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x1f573d6fb3f13d689ff844b4ce37794d79a7ff1c",
            "name": "Bancor",
            "symbol": "BNT",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xc00e94cb662c3520282e6f5717214004a7f26888",
            "name": "Compound",
            "symbol": "COMP",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x3506424f91fd33084466f402d5d97f05f8e3b4af",
            "name": "Chiliz",
            "symbol": "CHZ",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x4Fabb145d64652a948d72533023f6E7A623C7C53",
            "name": "Binance USD",
            "symbol": "BUSD",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x6b175474e89094c44da98b954eedeac495271d0f",
            "name": "Dai",
            "symbol": "DAI",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xD533a949740bb3306d119CC777fa900bA034cd52",
            "name": "Curve DAO Token",
            "symbol": "CRV",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c",
            "name": "Enjin Coin",
            "symbol": "ENJ",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x3597bfD533a99c9aa083587B074434E61Eb0A258",
            "name": "Dent",
            "symbol": "DENT",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xc944e90c64b2c07662a292be6244bdf05cda44a7",
            "name": "The Graph",
            "symbol": "GRT",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x50d1c9771902476076ecfc8b2a83ad6b9355a4c9",
            "name": "FTX Token",
            "symbol": "FTT",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x15D4c048F83bd7e37d49eA4C83a07267Ec4203dA",
            "name": "Gala",
            "symbol": "GALA",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0xdeFA4e8a7bcBA345F687a2f1456F5Edd9CE97202",
            "name": "Kyber Network Crystal v2",
            "symbol": "KNC",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x514910771af9ca656af840dff83e8264ecf986ca",
            "name": "Chainlink",
            "symbol": "LINK",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x0f5d2fb29fb7d3cfee444a200298f468908cc942",
            "name": "Decentraland",
            "symbol": "MANA",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
            "name": "Maker",
            "symbol": "MKR",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x45804880De22913dAFE09f4980848ECE6EcbAf78",
            "name": "PAX Gold",
            "symbol": "PAXG",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x4a220e6096b25eadb88358cb44068a3248254675",
            "name": "Quant",
            "symbol": "QNT",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f",
            "name": "Synthetix",
            "symbol": "SNX",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0xb64ef51c888972c908cfacf59b47c1afbc0ab8ac",
            "name": "Storj",
            "symbol": "STORJ",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
            "name": "Wrapped Bitcoin",
            "symbol": "WBTC",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0xd26114cd6ee289accf82350c8d8487fedb8a0c07",
            "name": "OMG Network",
            "symbol": "OMG",
            "type": "ERC-20"
        },
        {
            "decimals": 6,
            "identifier": "0x5245c0249e5eeb2a0838266800471fd32adb1089",
            "name": "Raydium",
            "symbol": "RAY",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x3845badade8e6dff049820680d1f14bd3903a5d0",
            "name": "The Sandbox",
            "symbol": "SAND",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce",
            "name": "Shiba Inu",
            "symbol": "SHIB",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x320623b8E4fF03373931769A31Fc52A4E78B5d70",
            "name": "Reserve Rights",
            "symbol": "RSR",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2",
            "name": "SushiSwap",
            "symbol": "SUSHI",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x0000000000085d4780B73119b644AE5ecd22b376",
            "name": "TrueUSD",
            "symbol": "TUSD",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
            "name": "Uniswap",
            "symbol": "UNI",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xe41d2489571d322189246dafa5ebde1f4699f498",
            "name": "0x",
            "symbol": "ZRX",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e",
            "name": "yearn.finance",
            "symbol": "YFI",
            "type": "ERC-20"
        },
        {
            "decimals": 8,
            "identifier": "0x7a58c0be72be218b41c608b7fe7c5bb630736c71",
            "name": "ConstitutionDAO",
            "symbol": "PEOPLE",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
            "name": "Matic Token",
            "symbol": "Matic Token",
            "type": "ERC-20"
        },
        {
            "decimals": 18,
            "identifier": "0xF94b5C5651c888d928439aB6514B93944eEE6F48",
            "name": "Yield",
            "symbol": "Yield",
            "type": "ERC-20"
        }
    ],
    "binance-smart-chain": [
        {
            "decimals": 18,
            "identifier": "0x55d398326f99059fF775485246999027B3197955",
            "name": "Tether",
            "symbol": "USDT",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "name": "USD Coin",
            "symbol": "USDC",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x111111111117dC0aa78b770fA6A738034120C302",
            "name": "1inch Network",
            "symbol": "1INCH",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x101d82428437127bF1608F699CD651e6Abf9766E",
            "name": "Basic Attention Token",
            "symbol": "BAT",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x352Cb5E19b12FC216548a2677bD0fce83BaE434B",
            "name": "BitTorrent-New",
            "symbol": "BTT",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x52CE071Bd9b1C4B00A0b92D298c512478CaD67e8",
            "name": "Compound",
            "symbol": "COMP",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
            "name": "Dai",
            "symbol": "DAI",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x5f0Da599BB2ccCfcf6Fdfd7D81743B6020864350",
            "name": "Maker",
            "symbol": "MKR",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x7950865a9140cB519342433146Ed5b40c6F210f7",
            "name": "PAX Gold",
            "symbol": "PAXG",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0xb7F8Cd00C5A06c0537E2aBfF0b58033d02e5E094",
            "name": "Pax Dollar",
            "symbol": "USDP",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x88f1A5ae2A3BF98AEAF342D26B30a79438c9142e",
            "name": "yearn.finance",
            "symbol": "YFI",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x4B0F1812e5Df2A09796481Ff14017e6005508003",
            "name": "Trust Wallet Token",
            "symbol": "TWT",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x55d398326f99059fF775485246999027B3197955",
            "name": "Binance-Peg BSC-USD",
            "symbol": "BNB-USDT-Binance-Peg",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
            "name": "Binance-Peg BUSD Token",
            "symbol": "BUSD-Binance-Peg",
            "type": "BEP-20"
        },
        {
            "decimals": 18,
            "identifier": "0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47",
            "name": "Binance-Peg Cardano Token",
            "symbol": "ADA-Binance-Peg",
            "type": "BEP-20"
        }
    ]
}
