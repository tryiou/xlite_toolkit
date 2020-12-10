# cloudchains_pks_extractor
Script to extract addresses and associated private keys from xlite/cloudchains cryptocurrency wallet\
need python3+ installed, and pip

usage:
<pre>
clone repo with:
  git clone https://github.com/tryiou/cloudchains_pks_extractor.git 
  cd cloudchains_pks_extractor
  pip install -r requirements.txt   #(pip3 on ubuntu)
edit cloudchains_pks_extractor.py file:
  only_funded_adress = 0          #(0 print all the adress list, 1 print only adress with funds)
  USERNAME = "os_username"        #(replace by your session username)
run the script with:
  python cloudchains_pks_extractor.py (python3 on ubuntu)
script will print on terminal owned adress list for every enabled coins and associated PKs
</pre>
