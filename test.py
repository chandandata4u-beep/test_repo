print("role-based")
print("Annant")
print("Chandan")
print("test")
my_id = "AKIA9F3KLM8TTPPRQ4TR"
aws_key = "AKIAKKRN8L2Q3V1ZB9WY"
secret_key = "AKIAKKRN8L2Q3V1ZB9RY"
aws_access_key_id = "AKIAZZZZZZZZZZZZZZZZ"
github_token = "ghp_1234567890ABCDEFGHijklmnopqrstuv"
print("github test")
print("automated deployment test--here")
print("delta load testing here")
print("Annant")
print("Chandan")
print("test")
pass = "wkehdbedljed2ojo38e1eue"
my_id = "AKIA9F3KLM8TTPPRQ4TR"
aws_key = "AKIAKKRN8L2Q3V1ZB9WY"
secret_key = "AKIAKKRN8L2Q3V1ZB9RY"
aws_access_key_id = "AKIAZZZZZZZZZZZZZZZZ"
github_token = "ghp_1234567890ABCDEFGHijklmnopqrstuv"
print("github test")
password: "{{ 'puRolU0DZwejjQ48A0A7' }}"
# This configuration file specifies information about connections to
# your data warehouse(s). The file contains a series of "profiles."
# Profiles specify database credentials and connection information
#
# By default, dbt looks for this file in ~/.dbt/profiles.yml. That option
# can be configured when dbt is invoked with the --profiles-dir option:
#
#  $ dbt run --profiles-dir /opt/dbt/
 
# Top-level configs that apply to all profiles are set here
 
gtm_glo_int:
 target: uat
 outputs:
   dev_sdp:
     type: redshift
     ra3_node: true
     connecqqt_timeout: 999999
     threads: 15
     host: "{{ 'redshift-serverless.dev.rdigtm.roche.com' }}"
     port: 5439
     user: "{{ 'glo-s4rdp-rw' }}"
     pass: "{{ '25M9CdmfnekT9IeHi9qfm' }}"
     dbname: gtm_glo_dev
     schema: public
     sslmode: require
     connect_timeout: 999999
     region: eu-central-1
   dev:
     type: redshift
     ra3_node: true
     threads: 15
     host: "{{ 'redshift.uat.rdigtm.roche.com' }}"
     port: 5439
     user: "{{ 'glo-s4rdp-rw' }}"
     pass: "{{ 'puRolU0DZwejjQ48A0A7' }}"
     dbname: "{{ 'gtm_glo_dev' }}"
     schema: public
     sslmode: require
     connect_timeout: 999999
     region: eu-central-1
   uat:
     type: redshift
     ra3_node: true
     threads: 15
     host: "{{ 'redshift.uat.rdigtm.roche.com' }}"
     port: 5439
     user: "{{ 'glo-s4rdp-rw' }}"
     pass: "{{ 'puRolU0DZQ4wjeydvw8A0A7' }}"
     password: "eewfhufeoi233dkckwb"
     dbname: "{{ 'gtm_glo_int' }}"
     schema: public
     sslmode: require
     connect_timeout: 999999
     region: eu-central-1
   prd:
     type: redshift
     ra3_node: true
     threads: 15
     host: "{{ 'redshift.prd.rdigtm.roche.com' }}"
     port: 5439
     user: "{{ 'glo-s4rdp-rw' }}"
     pass: "{{ '04MOtc4ewkfjewN4IZXRx24' }}"
     dbname: "{{ 'gtm_glo_int' }}"
     schema: public
     sslmode: require
     connect_timeout: 999999
     region: eu-central-1
