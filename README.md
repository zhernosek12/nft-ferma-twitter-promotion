### NFT Ferma Twitter Promotion

installing with pip

```
!pip install git+https://github.com/zhernosek12/nft-ferma-twitter-promotion.git
```

running the script

```
secret_key = "<your-secret-key>"
chrome_driver = "<your-directory-path>"

zhFermaTwitter = ZhFermaTwitter(secret_key, chrome_driver)
zhFermaTwitter.start()
```

__chrome_driver__ - chromedriver-windows-x64.exe download from selenium project, and specify the path
