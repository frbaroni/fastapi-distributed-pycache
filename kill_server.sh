#!/bin/bash

ps -ax | grep fastapi | awk '{ print $1 }' | xargs kill -9
