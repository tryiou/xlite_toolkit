# xlite_toolkit 

https://xlitewallet.com/ \
https://github.com/blocknetdx/xlite/ \
https://docs.blocknet.org/xlite/setup/

python scripts toolkit 

written with python3



usage:
<pre>
# install git, python if missing, open a terminal,
# clone repo with:
  git clone https://github.com/tryiou/xlite_toolkit
  cd xlite_toolkit
</pre>


# Xlite_privateKeysExtractor.py
Script to extract addresses and associated private keys from Xlite/xlite-daemon wallet:\
Print on terminal

usage:
<pre>
# run the script with:
  python Xlite_privateKeysExtractor.py true
  python Xlite_privateKeysExtractor.py false

# script will print on terminal owned address list for every enabled coins and associated PKs
#   true print only address with funds.
#   false print every address from list.
</pre>

# Xlite_detectAddressCount.py
Script to detect past usage on a mnemonic and set addressCount correctly for Xlite/xlite-daemon:\
Restart Xlite/Xlite-daemon to apply new count.

-This script need user to set his Xlite password into the file 'wallet_password.json'\
-This script need 'xlite-daemon' or 'xlite-daemon.exe' placed in the script directory\
latest binaries can be found on 
https://github.com/blocknetdx/xlite-daemon/releases

usage:
<pre>
# run the script with:
  python Xlite_detectAddressCount.py 25

# argument is a int, number of addresses per batch to test, default at 20 if not provided.
</pre>

# Xlite_changeAddressCount.py
Script to set addressCount for every coins of Xlite/xlite-daemon:\
Restart Xlite/Xlite-daemon to apply new count.

usage:
<pre>
# run the script with:
  python Xlite_changeAddressCount.py 25

# argument is a int, addressCount to set, default at 20 if not provided.
</pre>
