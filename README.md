# cloudchains_pks_extractor
Script to extract addresses and associated private keys from xlite/cloudchains cryptocurrency wallet:\
https://xlitewallet.com/ \
need python3+ installed, and pip

usage:
<pre>
clone repo with:
  git clone https://github.com/tryiou/cloudchains_pks_extractor.git
or download/extract repo from web, then
  cd cloudchains_pks_extractor
edit cloudchains_pks_extractor.py file:
  only_funded_address = False          #(False print all the address list, True print only address with funds)
run the script with:
  python cloudchains_pks_extractor.py  #(python3 on ubuntu)
script will print on terminal owned address list for every enabled coins and associated PKs
</pre>
