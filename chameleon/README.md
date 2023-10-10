# Chameleon Cloud Interface

Setup files for chameleon cloud dev tool access.

## Python virtual env

Load required chameleon cloud tools using the virutal environment described in the Pipfile
```
pipenv shell
```

## chi-auth
After loading the python virtual environment, aithenticate with the chameleon site using `chi-auth`
```
# To authenticate for CHI@TACC
source chi-auth tacc 

# To authenticate for CHI@UC
source chi-auth uc

```