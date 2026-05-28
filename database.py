import aiosqlite

DB_NAME = "swano.db"


# -------------------------
# INIT DATABASE
# -------------------------
async def init_db():

    async with aiosqlite.connect(DB_NAME) as db:

        # MONEY TABLE (KEEP EXISTING)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id TEXT PRIMARY KEY,
            money INTEGER DEFAULT 0
        )
        """)

        # LEVELS TABLE (NEW)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            user_id TEXT PRIMARY KEY,
            messages INTEGER DEFAULT 0,
            level INTEGER DEFAULT 0,
            last_message TEXT DEFAULT 'never',
            last_levelup TEXT DEFAULT 'never'
        )
        """)

        await db.commit()


# -------------------------
# LEVEL FUNCTIONS
# -------------------------
async def get_level(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        async with db.execute("""
            SELECT messages, level, last_message, last_levelup
            FROM levels
            WHERE user_id = ?
        """, (str(user_id),)) as cursor:

            row = await cursor.fetchone()

            if row is None:
                return 0, 0, "never", "never"

            return row


async def add_message(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT INTO levels (user_id, messages, level, last_message, last_levelup)
            VALUES (?, 0, 0, 'never', 'never')
            ON CONFLICT(user_id) DO NOTHING
        """, (str(user_id),))

        await db.execute("""
            UPDATE levels
            SET messages = messages + 1,
                last_message = datetime('now')
            WHERE user_id = ?
        """, (str(user_id),))

        await db.commit()


async def level_up(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            UPDATE levels
            SET level = level + 1,
                messages = messages - 150,
                last_levelup = datetime('now')
            WHERE user_id = ?
        """, (str(user_id),))

        await db.commit()
