#!/bin/bash
# Notification handler hook for ProxmoxMCP
# Sends desktop notifications for important events

# Get notification type and message
NOTIFICATION_TYPE=$(echo "$CLAUDE_NOTIFICATION" | jq -r '.type // "info"')
MESSAGE=$(echo "$CLAUDE_NOTIFICATION" | jq -r '.message // "Claude Code notification"')

# Log notification
echo "[$(date +"%Y-%m-%d %H:%M:%S")] $NOTIFICATION_TYPE: $MESSAGE" >> /workspaces/ProxmoxMCP/.claude/logs/notifications.log

# Send desktop notification if available
if command -v notify-send &> /dev/null; then
    case "$NOTIFICATION_TYPE" in
        "error")
            notify-send -u critical "ProxmoxMCP Error" "$MESSAGE" -i error
            ;;
        "warning")
            notify-send -u normal "ProxmoxMCP Warning" "$MESSAGE" -i warning
            ;;
        "success")
            notify-send -u low "ProxmoxMCP Success" "$MESSAGE" -i info
            ;;
        *)
            notify-send -u low "ProxmoxMCP" "$MESSAGE" -i info
            ;;
    esac
fi

# Terminal notification with colors
case "$NOTIFICATION_TYPE" in
    "error")
        echo -e "\033[31m❌ ERROR: $MESSAGE\033[0m"
        ;;
    "warning")
        echo -e "\033[33m⚠️  WARNING: $MESSAGE\033[0m"
        ;;
    "success")
        echo -e "\033[32m✅ SUCCESS: $MESSAGE\033[0m"
        ;;
    *)
        echo "ℹ️  $MESSAGE"
        ;;
esac

exit 0