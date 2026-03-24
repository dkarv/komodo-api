#!/bin/bash

typeshare -V || cargo install typeshare-cli@1.13.3 -F python

node client/core/py/generate_types.mjs
