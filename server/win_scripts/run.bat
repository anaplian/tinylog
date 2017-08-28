set ENV=DEV
set FLASK_DEBUG=1
set FLASK_APP=..\tinylog_server\app.py
set DATABASE_DSN=sqlite:///..\dev.db
set CAPTCHA_CHALLENGE=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
set CAPTCHA_SECRET=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
flask run --host=0.0.0.0 --port=8000