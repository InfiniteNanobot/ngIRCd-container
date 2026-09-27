# ngIRCd コンテナ

このリポジトリでは、AlmaLinux 10 をベースに ngIRCd のコンテナイメージをビルド・実行するためのファイルを管理します。

## ファイル構成

- `Containerfile` — EPEL から ngIRCd をインストールし、非 root ユーザーでフォアグラウンド実行します。
- `config/ngircd.conf` — イメージ内に配置する ngIRCd の設定ファイル。
- `config/ngircd.motd` — 接続したクライアントに表示する MOTD（Message of the Day）。
- `README.md` — 英語版の説明。

## ビルドと実行

設定ファイルを追加した後、Podman でイメージをビルドして起動します。

```sh
podman build -t ngircd-container -f Containerfile .
podman run --rm --name ngircd -p 6667:6667 ngircd-container
```

コンテナを実行しているホストの TCP ポート `6667` に IRC クライアントから接続してください。

設定を変更するには `config/ngircd.conf` を編集してイメージを再ビルドしてください。インターネットに公開する前に、設定内容とアクセス制御を確認してください。

> **注:** `Containerfile` は `config/ngircd.conf` と `config/ngircd.motd` を参照します。これらのファイルはまだ追加されていないため、追加するまではイメージをビルドできません。
