# article_13778_convert_optical_and_sar
日本発の衛星データプラットフォーム Tellus のオウンドメディア「宙畑」の記事、https://sorabatake.jp/13778 で利用しているコードです。
光学画像→SAR画像変換、及びSAR画像→光学画像変換をペア画像を必要としない教師なし学習で実現します

なお、SARデータの取得にはTellusの開発環境を申し込む必要があります。

## ソースコード(./src/配下を参照)
- 00.py
  - ALOS-2のSAR画像ダウンロード
- 01.py
  - 投影方式の変換
- 02.py
  - ASNARO-1の光学画像ダウンロード
- 03.py
  - 光学画像、SAR画像のマッチング処理(マッチング後画像はrootフォルダのa.png, b.png参照)
- cyclegan/cyclegan_1.py
  - Sentinel-1/2の相互変換
- cyclegan/cyclegan_2.py
  - ALOS-2/ASNAROの相互変換
- cyclegan/data_loader.py
  - cycleganのデータローダ
- pix2pix/pix2pix_1_1.py
  - Sentinel-1/2の光学→SAR変換
- pix2pix/pix2pix_1_2.py
  - Sentinel-1/2のSAR→光学変換
- pix2pix/pix2pix_2_1.py
  - ALOS-2/ASNAROの光学→SAR変換
- pix2pix/pix2pix_2_2.py
  - ALOS-2/ASNAROのSAR→光学変換
- pix2pix/data_loader.py
  - pix2pixのデータローダ

## ライセンス、利用規約
ソースコードのライセンスは CC0-1.0（Creative Commons Zero v1.0 Universal）ライセンスです。  
今回コード内で PALSAR-2 データを用いております。利用ポリシーは以下をご参考下さい。
https://www.tellusxdp.com/market/tool_detail/de3c41ac-a8ca-4170-9028-c9e1a39841e1/e364c31c-bfad-49d0-bd6d-f2bc11d67386
※サイトの閲覧にはTellusへのログインが必要です。

## 貢献方法
プルリクエストや Issue はいつでも歓迎します。



by charmegiddo
