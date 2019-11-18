#!/bin/bash
openssl rand -base64 756 > $1
chmod 400 $1