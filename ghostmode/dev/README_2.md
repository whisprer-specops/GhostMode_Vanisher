README.md

# 👻 GhostMode™

> _"When it’s time to vanish, vanish beautifully."_ - G-Petey.

GhostMode™ is a modular privacy ops suite designed for vanishers, cyber dissidents, journalists under pressure, and anonymity maximalists.  
It provides a full identity-splitting, anti-fingerprint, metadata-purging, containerized persona management system.

---

## 👻 Philosophy
GhostMode isn't about paranoia.  
It's about **digital dignity**.  
You have the right to speak, whistleblow, explore, and communicate without being hunted by behavioral analytics engines.

This isn't just obfuscation — it's **compartmentalization** done right:
> *one identity per context. never mix. always rotate. destroy when done.*

---
👻👻 requirements:

👻 Full list of all OS/Softwares/Applications required - it's wise to have these readybeforehand, downloaded from _verified_ sources and put directly on a newly formatted absolute blank or even new from packaging USB drive.

i'm going to credit  you with the ability to follow instructions and hence  install the follwoing preferable choices:

- Linux OS:: [possible on MacOS/Win, not advised hence not included instructions for]
recommended choices:
Containerised OS or Dragonos OS depending on use case [Dragonos for optional SDR]
👻 Tails OS: Live boot (amnesiac) Debian-based OS. Leaves no trace.
👻 Whonix: Best for anonymity, routes all traffic through Tor, sandboxed.
👻 Qubes OS: Virtualized compartments for ultimate security.

n.b.:  Pair these with read-only boot media (e.g., CD or write-protected USB).

👻 Tails:: https://download.tails.net/tails/stable/tails-amd64-6.14.1/tails-amd64-6.14.1.img 1.5GB
👻 Whonix:: https://www.whonix.org/wiki/Download ~per OS GB
👻 Qubes:: https://www.whonix.org/wiki/Qubes/Install ~per OS GB
👻 Dragonos:: https://sourceforge.net/projects/dragonos-focal/ 3.52GB

👻 Cold Wallet e.g. Monero <25-250KB
👻 TOR [usually incuded with stuff like Tails etc. - we stress here becauser this is essential.] gen. inc. GB
👻 FireFox [again, usually included with mostof the recommended OSs etc., i really wouldn't use snything else.] gen. inc. GB

TOTAL REQUIRED SPACE:: ~4GB Max of a *read-only* boot media (e.g., CD or write-protected USB).

---
I'll point out here it's a detailed, responsible guide to boosting your privacy and anonymity online — _totally legit_, totally helpful for folks like you who just want to understand their exposure and reduce their digital footprint.

Whether you're trying to:
- Maintain multiple operational personas,
- Avoid stylometric surveillance,
- Or simply ghost out of hostile infrastructure...
GhostMode gives you the toolkit to get in, get out, and leave **no scent**.

---
## 👻 Threat Model

GhostMode is designed to resist:
- 👻 Passive network observers (metadata/time correlation)
- 👻 Active browser fingerprinting
- 👻 Stylometric authorship correlation (writing analysis)
- 👻 USB/forensic memory residue
- 👻 Operating system metadata leaks
- 👻 Tracing back burner crypto wallets
- 👻 Log + identity crossover contamination

It **does not protect against**:
- 👻 Advanced firmware implants / BIOS malware
- 👻 Out-of-band keylogging (physical access)
- 👻 Malicious clipboard/logfile scrapers already present
- 👻 APT-level adversaries with upstream node control (think: NSA, FSB)

> **Goal:** To disappear from the sight of everyone *short* of God or Google Cloud SOC.

---

## 👻 Features

| Tool		     	        | Purpose		                                         |
|-----------------------|----------------------------------------------------|
| `ghostcontrol.py`   	| Central GUI to orchestrate ops			               |
| `monero_cold_wallet_`	| Create cold wallets offline, export keys safely    |
| `wizard.sh`	      	  |                           						             |
| `gpg_gui.sh`         	| GUI encryption, signature, verification via Zenity |
| `onionshare_drop.sh`	| Anon file sharing via Tor                          |
| `identikit.sh`       	| Swap full identity profiles: GPG, Firefox, wallet, | 
|                       | avatar                                             |
| `identity_timer.sh`   | Rotating identities every X mins (prevents         |
|                       | time-based linking                         			   |
| `stylometry_`		      | Rewrite your text to anonymize writing style	     |
|  `obfuscator.sh`		  |						                                         |
| `ghost_exit.sh`     	| Smooth kill-switch: cleans up traces,              |
|                       | logs out or locks                                  |
| `cold_sign_tx.sh + `	| Offline TX signing and safe broadcast flow		     |
| `hot_broadcast_tx.sh` |                                                    |
| `ghost_idlewatch.sh`  | Self-Wipe-on-Inactivity - A cyber dead man’s switch|

All now 
---

## 👻 Personas

All identities are stored in:
~/.ghost_identities/ ├── astralfox/ │ ├── firefox-profile/ │ ├── gpg-key.asc │ ├── monero-wallet/ │ ├── avatar.png │ └── metadata.json

`These can be rotated manually (`identikit.sh`) or automatically`

(`identity_timer.sh`).

---

## 👻 Cold Wallets

Offline wallets can be created and backed up with full*:
- Mnemonic seed dump
- View-only export
- Optional GPG encryption of `.keys` and `.log`
- USB auto-backup tool included

---
All instructions for Linux operating system, assumes you are at minimum using some form of safely rpotected kali or similar if not preferably Tails or the like.

---
*Do this before connecting to any network you don't trust.*

For the sake of covering all bases, we're still gonna start with a good ol' fashioned
👻 Phase 1: Randomizing MAC Address (hardware ID sent over networks)

# Install required tool
`sudo apt install macchanger`

# Bring down the interface (replace eth0/wlan0 as appropriate)
`sudo ifconfig wlan0 down`

# Randomize the MAC address
`sudo macchanger -r wlan0`

# Bring interface back up
`sudo ifconfig wlan0 up`

---
## 🧪 Stylometry Defense

Even if you're on Tor, even if you fake your MAC — if you always write the same,  
they can still **find you by your voice**.

`stylometry_obfuscator.sh` uses containerized local AI to rewrite your text and make your tone unrecognizable.  
It can rewrite in randomized styles: legalese, conversational, minimalist, punchy, poetic, etc.

---
GhostMode: Self-Wipe-on-Inactivity - A cyber dead man’s switch 💀
Silent. Watchful. If you walk away for too long, it cleans house.

👻 Enables or disables auto self-wipe
👻 You choose timeout: “N” hours or minutes of no input
👻 If timer expires: calls ghost_exit.sh or a scorched-earth version



---
## 👻 Exit Protocols

The `ghost_exit.sh` kill switch:
- Closes all browsers
- Randomizes your MAC again (if needed)
- Shreds key material
- Optionally fake logs for normalcy
- Locks screen or logs out normally

You can bind it to a hotkey or GUI panic button.

---
## 👻 Disclaimer

This toolkit is provided **as-is**.  
It is a collection of local automation scripts, not a remote service.  
The authors are not responsible for misuse, damage, or legal consequences.

GhostMode is a _tool_, not a shield against all harm. It complements **your own opsec discipline**, not replaces it.

---
## 👻 Future Modules (Planned)

- 👻 Identity builder / generator with personas & preloaded styles
- 👻 TUI or CLI-only mode for headless machines
- 👻 Decoy activity scheduler (fake Slack, CLI echo chains)
- 👻 AppImage self-contained version with embedded data vault
- 👻 Self-wiping USB key deployment

---
## 👻 Credits

- TOR Project  
- Onionshare  
- Monero Core Team  
- Zenity  
- Vamsi AI (for T5 Paraphrase model)  
- You — the ghost in the wires

---

**Be safe. Be unseen. Be loud only when you want to be.**
🧢 _— GhostMode Dev Team (2025, anonymous but real as fuck)_

---
👻👻 *Exxample:: Monero Cold Wallet:

👻 Size Breakdown
|File			              |Size (Approx)	  |Description	              		  	        |
|wallet.keys	         	|~3–20 K	      	|Contains private keys and encrypted	      |
|                 			|	               	|metadata. Super compact.	              		|
|wallet.address.txt 	  |~200 bytes	      |Contains view address and public info. (if	|
|                 			|exported)	      |	                                  				|
|Optional.		          |	               	|					                                  |	
|wallet.log	          	|~10–100 KB	      |CLI log file. You can shred it.		        |
|wallet.view.keys       |~1–3 KB	       	|View-only keys. Optional.			            |
|(if exported)		      |		              |					                                  |
|*.tx unsigned/		      |~1–10 KB each	  |If using cold signing workflow.	        	| 
|signed tx files		    |	              	|					                                  |
|Encrypted GPG bundles	|~2× orgnl. size	|Depends on compression, optional	        	|
---

👻 Total Size of One Cold Wallet Folder
~25 KB – 250 KB

👻 That’s tiny. You could carry thousands of cold wallets on a single 128MB USB stick
or embed one in a QR code, stego image, even audio. :D

Embed your Monero cold wallet seed (and other essentials) into a QR code
So compact, you can print it, tattoo it (maybe), hide it in a photo, or read it with a webcam offline...
soooo,

🪙🧠 STEP-BY-STEP: Encode & Read Monero Cold Wallet in a QR Code

👻 1. Gather Your Wallet Essentials
What to store:
👻 Mnemonic Seed
👻 Wallet Name or Label
👻 (Optional) View Key / Address
👻 Restore Height (so sync is faster)

Example:
```{
  "wallet_name": "ghostnode1",
  "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
  "address": "49AqUG8...MoneroAddress",
  "restore_height": 3100000```

Save that as:
`~/ghostwallet_data.json`

👻 2. Minify It (Optional)
QRs hold limited data. You can minify it:`

```jq -c . ~/ghostwallet_data.json > ~/ghostwallet_min.json```
Now your file looks like:

```{"wallet_name":"ghostnode1","mnemonic":"abandon abandon ...","address":"49AqUG...","restore_height":3100000}```

👻 3. Generate QR Code
Install the tool:
`sudo apt install qrencode`

Then run:
`qrencode -r ~/ghostwallet_min.json -o wallet_seed_qr.png -s 6 -l H`

👻 That creates: wallet_seed_qr.png
`-s 6`: Makes it nicely visible for print or webcam
`-l H`: High error correction (still readable if slightly damaged)

🧾 4. Print It or Hide It
You can print it out, laminate it, stash in a book OR embed it inside another image with steganography (see below)... >.>

👻 5. READ BACK THE QR (Offline or Airgapped)
Option A: From webcam (best for airgapped Linux):
`sudo apt install zbar-tools`
zbarcam

→ Point camera at QR
→ Output will look like:
`QR-Code:{...your minified JSON...}`

Option B: From file:
`zbarimg wallet_seed_qr.png`

→ You'll get the embedded data right back!

👻 6. Restore Wallet from Decoded Info
```monero-wallet-cli \
  --restore-deterministic-wallet \
  --restore-height 3100000 \
  --generate-new-wallet myrestored \
  --electrum-seed "abandon abandon abandon ..."```

👻 Don’t forget to chmod 600 the restored wallet files
👻 And always shred QR and restore data when done

👻 BONUS: Want Super Compact Format?
If you're hardcore, ditch JSON and encode like this:
`ghostnode1::abandon abandon abandon ...::49AqUG8...::3100000`

Then re-encode to QR. Way smaller. Same retrieval steps.

👻👻 OK, so you've done a test first, with non-crucial data, right? then let's finish off with:

---
👻 PART A — Split Seed Across QR Fragments (Shamir’s Secret Sharing)
👻 Protect against single point of failure
👻 You’ll split your wallet seed into N parts, where K of them are required to recover
Like magic puzzle pieces — 1 alone is worthless, K together unlock the treasure

👻 Step 1: Install ssss (Shamir's Secret Sharing Scheme)
`sudo apt install ssss qrencode zbar-tools`

👻 Step 2: Run Split
Let’s say:
Total shares: 5
Threshold to recover: 3

Run:
`ssss-split -t 3 -n 5`

It will prompt:
`Enter the secret, at most 128 characters, ending with ENTER:`

Paste your Monero seed like:
`abandon abandon abandon ... abandon about`
It will output 5 shares like:
```1-abc12345...
2-84dbe37f...
...```

Save each of those to a .txt file, like:
`echo "1-abc123..." > share1.txt`
👻 Step 3: Encode Each Share to QR
```qrencode -o share1.png < share1.txt
qrencode -o share2.png < share2.txt```

# repeat for all shares

👻 Step 4: Store or Distribute
- Keep one in a safe at your house 👻
- Give one to your lawyer 👻
- Hide one in a book 👻
- Bury one in a dead drop 👻

Even if 2 are stolen, your wallet is still safe if the attacker can't get the 3rd.
You can even print them and cut the QR diagonally so it can't be scanned directly without taping the halves.

👻 Recombine Shares to Recover Seed

When you need to restore:
`ssss-combine`

Paste any 3 shares. It reconstructs your seed.
Then restore wallet like usual.

---
👻 PART B — Hide QR Inside an Innocent Image (Steganography)
👻 Looks like a photo. Is a photo. But it holds your wallet seed.

👻 Step 1: Install steghide
`sudo apt install steghide`

👻 Step 2: Embed Your QR into a Photo
`steghide embed -cf innocent_photo.jpg -ef wallet_seed_qr.png`

`-cf`: cover file (looks normal)

`-ef`: embedded file (your real payload)

You’ll be asked for a passphrase (don’t forget it!)
Now innocent_photo.jpg contains the hidden QR.

👻 Looks totally normal to any human or computer vision

👻 Step 3: Extract Later
`steghide extract -sf innocent_photo.jpg`

Enter passphrase → file pops out
Then read QR with:
`zbarimg wallet_seed_qr.png`

👻 Optional Bonus Tricks:
Chain this:

Shamir split 👻
Encode shares into 👻 👻
Steg-hide each QR into different image files 👻

Upload images to different cloud buckets or bury on USB keys
Use LSB steg tools for higher bit-depth hiding (e.g. zsteg, openstego)
Further ideas:: steganograph with sound by embedding QR into a .wav, or embed the QR inside a video frame or a printed glyph grid.