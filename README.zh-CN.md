# 澶囦唤瑙勫垝宸ュ叿

[English](README.md)

棰勮骞舵墽琛屽畨鍏ㄧ殑澧為噺鏂囦欢澶囦唤锛屾敮鎸?JSON 娓呭崟鍜?SHA-256 鏍￠獙銆?
## 瀹夊叏璁捐

- 榛樿鍙瑙堛€?- 涓嶅垹闄ゆ簮鏂囦欢銆?- 涓嶅垹闄ょ洰鏍囦綅缃腑宸叉湁鐨勯澶栨枃浠躲€?- 鎷掔粷鎶婄洰鏍囩洰褰曟斁鍦ㄦ簮鐩綍鍐呴儴銆?- 鍙娇鐢?SHA-256 鏍￠獙姣忎釜澶嶅埗鏂囦欢銆?
杩欐槸涓€涓畨鍏ㄥ鍒惰緟鍔╁伐鍏凤紝涓嶈兘浠ｆ浛缁忚繃楠岃瘉鐨勫畬鏁寸伨闅炬仮澶嶆柟妗堛€?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/backup-planner.git
cd backup-planner
python -m pip install -e .
```

## 浣跨敤

```bash
backup-plan D:\Documents D:\Backups\Documents
backup-plan D:\Documents D:\Backups\Documents --apply
backup-plan D:\Documents D:\Backups\Documents --hash --apply --verify
backup-plan D:\Documents D:\Backups\Documents --apply --manifest report.json
```

`--hash` 浼氭瘮杈冨凡鏈夋枃浠剁殑瀹為檯鍐呭锛岄€熷害杈冩參锛屼絾鏇村交搴曘€?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT


