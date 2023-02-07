### NFT Ferma Twitter Promotion

installing with pip

```
!pip install git+https://github.com/zhernosek12/nft-ferma-twitter-promotion.git
```

running the script

```
from zhnftfermatwitter import robot

secret_key = "<your-secret-key>"
chrome_driver = "<your-directory-path>"

fermaTwitter = robot.ZhNFTFermaTwitter(secret_key, chrome_driver)
fermaTwitter.start()
```

__chrome_driver__ - chromedriver-windows-x64.exe download from selenium project, and specify the path
