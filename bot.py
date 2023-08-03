import discord
import sqlite3
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.command()
async def add_user(ctx, *args):
    # WARNING: This code is vulnerable to SQL injection
    username = " ".join(args)
    print(username)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '123');"
        c.execute(query)
        conn.commit()

        # Get the user from the database to confirm the addition
        c.execute(f"SELECT username FROM users WHERE username='{username}';")
        result = c.fetchone()
        conn.close()

        if result:
            await ctx.send(f"User {result[0]} added successfully!")
        else:
            await ctx.send("Failed to add the user.")
    except sqlite3.Error as e:
        await ctx.send(f"An error occurred: {e}")
        conn.rollback()
        conn.close()

@client.command()
async def get_users(ctx):
    # WARNING: This code is vulnerable to SQL injection
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = "SELECT username FROM users;"
    c.execute(query)
    result = c.fetchall()
    conn.close()

    users = [row[0] for row in result]
    await ctx.send(f"Users: {', '.join(users)}")

@client.command()
async def order_by(ctx,*args):
    # WARNING: This code is vulnerable to SQL injection
    orderby_arg = " ".join(args)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT username FROM users ORDER BY {orderby_arg};"
    try:
        c.execute(query)
        result = c.fetchall()
        conn.close()
        users = [row[0] for row in result]
        await ctx.send(f"Users (ordered by ID): {''.join(users)}")
    except sqlite3.Error as e:
        await ctx.send(f"An error occurred: {e}")
        conn.close()

@client.command()
async def where_username(ctx,*args):
    # WARNING: This code is vulnerable to SQL injection
    where_arg = " ".join(args)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = {where_arg};"
    try:
        c.execute(query)
        result = c.fetchall()
        conn.close()
        users = [row[0] for row in result]
        #await ctx.send(f"Got User: {', '.join(str(users))}")
        await ctx.send(result)
    except sqlite3.Error as e:
        await ctx.send(f"An error occurred: {e}")
        conn.close()

@client.command()
async def where_id(ctx, *args):
    where_arg = " ".join(args)

    try:
        # Convert where_arg to an integer (if it's not an integer, this will raise a ValueError)
        user_id = int(where_arg)
    except ValueError:
        await ctx.send("Invalid user ID. Please provide a valid integer.")
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT username FROM users WHERE id = ?;"

    try:
        c.execute(query, (user_id,))
        result = c.fetchone()
        conn.close()

        if result:
            await ctx.send(f"User with ID {user_id}: {result[0]}")
        else:
            await ctx.send("No user found with the given ID.")
    except sqlite3.Error as e:
        await ctx.send(f"An error occurred: {e}")
        conn.close()



client.run('OTg1NTQ3NDU5NzUxMTg2NDMy.GutYPS.jgJU09kfjQ0mfJWtWD8oZ6f_vX-jchG1I6-UzE')
