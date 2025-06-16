# bash autocompletion for openrouter-cli
refresh_openrouter_model_cache_if_needed() {
    local CACHE_FILE="$HOME/.cache/openrouter_models.txt"
    local CACHE_DURATION=86400  # 24 horas
    if [[ ! -f "$CACHE_FILE" || $(( $(date +%s) - $(stat -c %Y "$CACHE_FILE") )) -gt $CACHE_DURATION ]]; then
        mkdir -p "$(dirname \"$CACHE_FILE\")"
        if command -v openrouter &> /dev/null; then
            openrouter list-models 2>/dev/null | cut -d' ' -f 1 | grep '/' > "$CACHE_FILE.tmp" && mv "$CACHE_FILE.tmp" "$CACHE_FILE"
        else
            echo "[failed:P1]"
        fi
    fi
}

_openrouter_cli_autocomplete() {
    local cur prev words cword
    _init_completion || return

    local subcommands="chat list-models"
    local opts="--model -m --stream --no-stream --no-reasoning --save"
    local CACHE_FILE="$HOME/.cache/openrouter_models.txt"

    if [[ $cword -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "$subcommands" -- "$cur") )
        return 0
    fi

    case ${words[1]} in
        chat)
            if [[ $prev == "--model" || $prev == "-m" ]]; then
                refresh_openrouter_model_cache_if_needed
                if [[ -f "$CACHE_FILE" ]]; then
                    mapfile -t models < "$CACHE_FILE"
                    COMPREPLY=( $(compgen -W "${models[*]}" -- "$cur") )
                fi
                return 0
            fi
            COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
            ;;
        *)
            ;;
    esac
}

complete -F _openrouter_cli_autocomplete openrouter

