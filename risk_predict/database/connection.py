from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///risk_predict.db"

async_engine = create_async_engine(DATABASE_URL)

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()
