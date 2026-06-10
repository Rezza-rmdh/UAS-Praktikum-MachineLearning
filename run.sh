#!/usr/bin/bash

function run_server() { 
    uvicorn server.main:app --reload 
}

function run_app() { 
    streamlit run app/app.py
}

declare -r CMD="$1"

case "$CMD" in
    "server")
        run_server
        ;;
    "app")
        run_app
        ;;
    *)
        if [ ! -z "$CMD" ]; then
            echo "Unrecognized command: $CMD"
        else
            echo "No command specified"
        fi
        ;;
esac
