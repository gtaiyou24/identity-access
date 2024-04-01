from fastapi import APIRouter


router = APIRouter(
    prefix='/health',
    tags=['Health']
)


@router.get('/check', name='ヘルスチェック用のエンドポイント')
def check() -> str:
    return 'OK'
