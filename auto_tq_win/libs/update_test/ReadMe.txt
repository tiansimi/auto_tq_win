pre_upgrade_test.exe

## Parameters

> [-d]: delete virdb directory file, hwl.db、prop.db、pset.db、troj.db

> [-c]: delete component,HipsMain.exe、HipsTray.exe、HipsLog.exe、uninst.exe

> [-cd]: delete virdb directory file and component
 
 ## Return value
> [0]: program normal exit

> [1]: find virdb directory path fail

> [2]: delete virdb directory fail

> [3]: find install path fail

> [4]: delete component fail

> [10]: input parameter errors

UpdateAssist.exe -h   帮助
D:\HR\hr_ui_front\library\update_test>UpdateAssist.exe -h
使用方法: UpdateAssist.exe [参数].
    参数:
      --product, -p     选择产品名称。不填写此参数时，程序将检测当前安装产品。
        产品名称        HR50    个人版5.0
                        ESS10    企业版1.0
                        ESS20    企业版2.0
      --update, -u      选择升级地址。
        升级地址        intest   开发内测  http://update-dev.huorong.cn/upgrade7
                        vertest  版本测试 http://update-rc.huorong.cn/upgrade7
                        pubtest  发布测试 http://update-test.huorong.cn/upgrade7
                        canary   灰度升级 http://update.huorong.cn/upgrade7fast
                        release  正式升级 http://update.huorong.cn/upgrade7
      --help, -h        显示帮助信息。
使用方法
D:\HR\hr_ui_front\library\update_test>UpdateAssist.exe -p HR50 -u vertest
设置升级地址成功！