#!/bin/bash
sudo du -sb "$1" | awk '{print $1}'