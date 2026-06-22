import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect('postgresql://postgres:postgres@127.0.0.1:5432/postgres')
    rows = await conn.fetch('SELECT datname FROM pg_database;')
    for r in rows:
        print("DB:", repr(r['datname']))
    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
