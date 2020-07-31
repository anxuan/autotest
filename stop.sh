#!/usr/bin/env bash
ps aux | grep -Ei '(auto_test_server)' | grep -v 'grep' |  awk '{print $2}' | xargs kill
