import bcrypt


# 원본 비밀번호를 해싱하는 함수
def hash_password(plain_password: str) -> str:
    # bcrypt 함수에 1) bytes 형식의 비밀번호 2) salt 값을 전달
    hashed_password = bcrypt.hashpw(
        plain_password.encode(), bcrypt.gensalt()
    )
    # 해싱 값(bytes)을 str으로 변환해서 반환
    return hashed_password.decode()

# 해시된 값을 검증하는 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # hashed_pw가 plain_pw로부터 만들어진 값이 맞는지 확인하는 함수(결과: True/False) 
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )
