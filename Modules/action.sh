SIMPLIFIED_CHINESE=false

locale=$(getprop persist.sys.locale 2>/dev/null)
[ -z "$locale" ] && locale=$(settings get system system_locales 2>/dev/null)
[ -z "$locale" ] && locale=$(getprop ro.product.locale 2>/dev/null)
[ -z "$locale" ] && locale=$(getprop ro.product.locale.language 2>/dev/null)

case "$locale" in
    *zh*CN*|*zh-CN*|*zh_CN*|*cn*)
        SIMPLIFIED_CHINESE=true
        ;;
    *zh*)
        SIMPLIFIED_CHINESE=true
        ;;
esac


if [ "$SIMPLIFIED_CHINESE" = "true" ] ; then
    am start -a android.intent.action.VIEW -d https://b23.tv/qSgZmj8 > /dev/null 2>&1
else
    am start -a android.intent.action.VIEW -d https://youtu.be/dQw4w9WgXcQ > /dev/null 2>&1
fi
