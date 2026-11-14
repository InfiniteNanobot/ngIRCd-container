# ngIRCd-container

このリポジトリでは、AlmaLinux 10 をベースに ngIRCd のコンテナイメージをビルド・実行するためのファイルを管理します。

## ファイル構成

- `Containerfile` — EPEL から ngIRCd をインストールし、非 root ユーザーでフォアグラウンド実行します。
- `config/ngircd.conf` — イメージ内に配置する ngIRCd の設定ファイル。
- `config/ngircd.motd` — 接続したクライアントに表示する MOTD（Message of the Day）。
- `tests/smoke.py` — Podman でイメージをビルドし、IRC 接続をテストします。
- `README.md` — 英語版の説明。

## ビルドと実行

Podman でイメージをビルドして起動します。

```sh
podman build -t ngircd-container -f Containerfile .
podman run --rm --name ngircd -p 127.0.0.1:6667:6667 ngircd-container
```

ホスト上の IRC クライアントから `127.0.0.1:6667` に接続してください。この例ではホストのループバックインターフェースにのみポートを公開します。

サンプル設定には認証も TLS もなく、ローカルテスト用です。リモート接続を受け付ける前に、アクセス制御と TLS を設定し、サーバー名や設定内容を確認して、必要に応じて公開先のホストアドレスを変更してください。TLS がなければ IRC のパスワードは平文で送信されます。

設定や MOTD を変更するには `config/` 内のファイルを編集してイメージを再ビルドしてください。設定ファイルと MOTD は `ngircd` ユーザーから読み取り可能にする必要があります。サーバーはコンテナ外からアクセス可能なアドレスで待ち受け、PID ファイルを設定する場合は `/run/ngircd` 以下に置いてください。

## テスト

Podman と Python 3 があれば `python3 tests/smoke.py` でイメージをビルドし、設定の検証と IRC 接続のテストを実行できます。テストはホストのループバックに一時ポートを割り当て、終了時にコンテナを削除します。`NGIRCD_TEST_IMAGE` でテスト用イメージのタグを変更できます。

> **注:** 現在 EPEL 10 には ngIRCd がないため、AlmaLinux 10 イメージには署名済みの EPEL 9 パッケージをインストールします。
