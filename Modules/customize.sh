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

if "$BOOTMODE" ; then
    ui_print "- Loading"
else
    ui_print "*********************************************************"
    ui_print "! Install from recovery is NOT supported"
    abort "*********************************************************"
fi

if "$KSU" ; then
    ui_print "- Installing from KernelSU app"
    ui_print "- KernelSU version：$KSU_VER"
    ui_print "- KernelSU version code：$KSU_VER_CODE"
else
    ui_print "- Installing from Magisk app"
    ui_print "- Magisk version：$MAGISK_VER"
    ui_print "- Magisk version code：$MAGISK_VER_CODE"
fi

VERSION=$(grep_prop version "${TMPDIR}/module.prop")
ui_print "- LSPosed version ${VERSION}"

extract 'action.sh'

ui_print "- Device platform: $ARCH"

if [ "$SIMPLIFIED_CHINESE" = "true" ] ; then
    am start -a android.intent.action.VIEW -d https://b23.tv/qSgZmj8 > /dev/null 2>&1
else
    am start -a android.intent.action.VIEW -d https://youtu.be/dQw4w9WgXcQ > /dev/null 2>&1
fi

sleep 5

if [ "$SIMPLIFIED_CHINESE" = "true" ] ; then
    ui_print "- 你被骗了，快去坑别人吧！"
    ui_print "- 如果你还意犹未尽，咱给你安排了，点一下操作就行了！"
else
    ui_print "- You've been tricked. Go and trick someone else!"
    ui_print "- If you still haven't had enough, we've got you covered. Just click the operation and it's done!"
fi
