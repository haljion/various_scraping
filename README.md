# various_scraping

小規模なスクレイピングツールをまとめておくプロジェクト

## paiza_job.py
---

paiza(https://paiza.jp/)の求人から言語と必須要件で絞り込み検索し、
現在のランクや業務経験で受けることが可能な求人の情報を抽出するツール 

データは以下項目を持つcsvファイルとしてoutputディレクトリ配下に出力される　
- 会社名
- 求人タイトル
- 必須要件
- 通過ランク
- 求人ページへのリンク
