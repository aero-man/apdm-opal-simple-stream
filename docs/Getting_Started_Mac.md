# Getting Started
### on Mac OS

### What you need
* 1+ APDM Opal sensors
* 1 APDM access point (7 or more sensors requires 2 APs)
* [APDM Python SDK](http://share.apdm.com/libraries/release/apdm_sdk.zip)
* Python 2.7

### Hardware Setup
1. Place APDM Opal sensors in their dock
2. Connect the APDM dock to a power source
3. Connect the APDM sensor dock and the APDM access point to your computer via USB. A USB hub is recommended when multiple docks and access points are involved.
4. Wait for access point to start up. The screen on the access point will show an APDM logo animation then show a list of configured/unconfigured sensors. The list showing means it is ready to configure (Step 4 under `Software Setup` below)

### Software Setup
1. Place APDM SDK files in the same folder as `main.py` (Files: `_apdm.so` and `apdm.py`)
2. Run `python main.py configure` (`Hardware Setup` must be complete)
3. Remove the Opal sensors from the dock. Wait for them to flash green in unison with each other and the access point.
4. Start streaming to a CSV with `python main.py stream`
5. Quit streaming with `control + C`