# from email._parseaddr import quote
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine as dbAccess
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import db_config as dbDefaultConfig
import json
from urllib.parse import quote_plus
from sqlalchemy.exc import SQLAlchemyError


class Db:
    # engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
    __dbTypeCon = {
        "postgres": "postgresql+asyncpg://{}:{}@{}:{}/{}",
        "mysql": "mysql+pymysql+aiomysql://{}:{}@{}:{}/{}?charset=utf8mb4"
    }

    def __init__(self, db_config = None):
        if db_config != None :
            self.__host = db_config['host']
            self.__port = db_config['port']
            self.__db = db_config['db']
            self.__username = db_config['username']
            self.__password = quote_plus(db_config['password'])
            self.__dbType = db_config['dbType']
        else:
            self.__host = dbDefaultConfig.db_config["host"]
            self.__db = dbDefaultConfig.db_config["db"]
            self.__username = dbDefaultConfig.db_config["username"]
            self.__password = dbDefaultConfig.db_config["password"]
            self.__dbType = dbDefaultConfig.db_config["dbType"]
            self.__port = dbDefaultConfig.db_config["port"]

        self.__dbExec = dbAccess(self.__setDbConnectString())

    def __setDbConnectString(self):

        if self.__dbType == 'postgres':
            strConnection = self.__dbTypeCon[self.__dbType]
            strConnection = strConnection.format(self.__username, '%s', self.__host, self.__port, self.__db)
            strConnection = strConnection % quote_plus(self.__password)


        if self.__dbType == 'mysql':
            # print("xxxx")
            strConnection = self.__dbTypeCon[self.__dbType]
            strConnection = strConnection.format(self.__username, '%s', self.__host, self.__port, self.__db)
            strConnection = strConnection % quote_plus(self.__password)
        # print(strConnection)
        return strConnection

    def convert_datetime_to_string(self, datetime):
        return str(datetime)

    async def executeQuery(self, sqlString):
        async with self.__dbExec.begin() as conn:
            await conn.execute(text(sqlString))
            await self.__dbExec.dispose()

    async def executeToDict(self, sqlString):
        # print("xxxxxx")
        async with self.__dbExec.connect() as conn:
            result = await conn.execute(text(sqlString))
            await self.__dbExec.dispose()
            return result.mappings().all()

    # async def executeToJSON(self, sqlString):
    #     return json.dumps(await self.executeToDict(sqlString), default=self.convert_datetime_to_string)

    async def executeTrans(self, sqlStringArray:[]):
        Session = async_sessionmaker(self.__dbExec, expire_on_commit=False)
        status=""
        try:
            async with Session() as session:
                for sqlString in sqlStringArray:
                    await session.execute(text(sqlString))
                await session.commit()
                await session.close()
                await self.__dbExec.dispose()
                status = True
        except SQLAlchemyError as e:
            await session.rollback()
            status = False
        finally:
            await session.close()

        return status

    def genStrInsertSingleObject(self, object, table):
        sql = f"insert into {table} "
        field = "("
        values = "values ("
        for key, item in object.items():
            field = field + f""" "{key}","""
            if item == "current_timestamp":
                values = values + f"{item},"
            else:
                if item == None or item =='None':
                    values = values + f"null,"
                else:
                    values = values + f"'{item}',"
        field = field[:-1]+")"
        values = values[:-1]+")"
        sqlString = sql + field + values
        return sqlString

    def genStrInsertArrayObject(self, objectArray, table):
        sql = f"insert into {table} "
        length = len(objectArray)
        values = ""
        i = 0
        fieldx = []

        field = "("
        for key, item in objectArray[i].items():
            field = field + f""" "{key}","""
            fieldx.append(key)
        field = field[:-1] + ")"

        while (i < length):
            value = " ("
            """for key, item in objectArray[i].items():
                field = field + f"{key},"
                if item == "current_timestamp":
                    value = value + f"{item},"
                elif item == None:
                    value = value + f"null,"
                else:
                    value = value + f"'{item}',"""
            for index in range(len(fieldx)):
                if objectArray[i][fieldx[index]] == "current_timestamp":
                    value = value + f"{objectArray[i][fieldx[index]]},"
                elif objectArray[i][fieldx[index]] == None or objectArray[i][fieldx[index]] == 'None':
                    value = value + f"null,"
                else:
                    value = value + f"'{objectArray[i][fieldx[index]]}',"
            values = values + value[:-1] + "),"
            i = i + 1
        sqlString = sql + field + " values " + values[:-1]
        return sqlString

    def genUpdateObject(self, objectSet, objectWhere, table):
        sql = f"update {table} set "
        values = ""
        where = ""
        for key, item in objectSet.items():
            if item == "current_timestamp":
                values = values + f""" "{key}"={item},"""
            else:
                if item == None or item =='None':
                    values = values + f""" "{key}"=null,"""
                else:
                    values = values + f""" "{key}"='{item}',"""
        for key, item in objectWhere.items():
            where = where + f"{key}='{item}' and "
        values = values[:-1]
        sqlString = sql + values +' where '+where[:-4]

        return sqlString

    def genDeleteObject(self, objectWhere, table):
        sql = f"delete from {table} where "
        where = ""
        for key, item in objectWhere.items():
            where = where + f"""  "{key}"='{item}' and"""
        where = where[:-3]
        sqlString = sql +where
        return sqlString
# dbConnect = Db()
