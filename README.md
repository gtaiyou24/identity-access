# Identity Access
ユーザーに対するロールベースのセキュアなアクセス管理機能を提供するサービス

 - メール配信 : [SendGrid](https://sendgrid.kke.co.jp/)
 - 決済 : [Stripe](https://stripe.com/jp)

## Domain

| ユビキタス言語 | 説明                                                                                                             |
|:-----------:|:---------------------------------------------------------------------------------------------------------------|
| テナント | テナント（tenant）は、本来は賃貸人のことだが、IT分野ではシステムやサービスの利用範囲を定義する言葉で、**ユーザーの契約単位**を指す。 |

## How To
### Run

```bash
docker-compose up --build
```

## 🔗APPENDIX

 - https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt/
 - https://github.com/VaughnVernon/IDDD_Samples/tree/master/iddd_identityaccess
 - https://github.com/hafizn07/next-auth-v5-advanced-guide-2024/tree/main
