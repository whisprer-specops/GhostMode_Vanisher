# Unlock Infrastructure

7. Cold Signing Pipeline

Offline wallet setup via GUI or script:
```bash
monero-wallet-cli --generate-new-wallet ghostwallet --offline
```

Export:
```bash
monero-wallet-cli --wallet-file ghostwallet --export-transfers all ghost.txn
gpg -r recipient --encrypt ghost.txn
```

Transfer via USB, then decrypt on hot machine:
```bash
gpg -d ghost.txn.gpg > ghost.txn
monero-wallet-cli --wallet-file hotwallet --broadcast-tx ghost.txn
```