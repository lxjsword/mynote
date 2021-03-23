#!/bin/bash

ps -ef | grep inotifywait | grep sh | awk '{print $2}' | xargs kill -9