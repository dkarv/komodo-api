# Komodo Python API

Python client API for [Komodo](https://komo.do).

https://pypi.org/project/komodo-api/

## How it works

The types are generated from the source rust files using typeshare:
```
node client/core/py/generate_types.mjs
```

The API itself is manually created and needs to be adjusted after each release. For this reason, the repository is a fork of the original one. From time to time, I check the changes in the original repository and update the API file with new routes.
