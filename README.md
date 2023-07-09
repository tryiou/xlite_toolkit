# xlite_toolkit 

https://xlitewallet.com/ \
https://github.com/blocknetdx/xlite/ \
https://docs.blocknet.org/xlite/setup/

usage:
<pre>
clone repo with:
  git clone https://github.com/tryiou/xlite_toolkit
  cd xlite_toolkit

</pre>


# xlite-daemon_pks_extractor
Script to extract addresses and associated private keys from xlite/cloudchains cryptocurrency wallet:\

need python3+ installed, and pip

usage:
<pre>
clone repo with:
  git clone https://github.com/tryiou/xlite_toolkit
or download/extract repo from web, then
  pip install requests                 #(pip3 on ubuntu)
edit cloudchains_pks_extractor.py file:
  only_funded_address = False          #(False print all the address list, True print only address with funds)
run the script with:
  python xlite-daemon_pks_extractor  #(python3 on ubuntu)
script will print on terminal owned address list for every enabled coins and associated PKs
</pre>
