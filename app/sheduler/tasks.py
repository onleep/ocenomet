import asyncio
import logging
from parser.main import apartPage, listPages

lock = asyncio.Lock()

async def parsing(page=1):
    rooms = [
        '', 'room1', 'room2', 'room3', 'room4',
        'room5', 'room6', 'room7', 'room8', 'room9'
    ]
    sorts = ['', 'creation_date_asc', 'creation_date_desc']

    def process_page(page, sort, room):
        errors = 0
        while errors < 30:
            pglist = listPages(page, sort, room)
            if pglist == 'END':
                logging.info('End of pglist reached')
                break
            data = apartPage(pglist)
            if data == 'END':
                logging.info('End of data reached')
                break
            if not data:
                errors += 1
                logging.info(f'Error parse count: {errors}')
                if errors >= 30:
                    logging.info(f'Error limit {errors} reached')
                    break
            else:
                errors = 0
            page += 1
        logging.info(f'Page: {page}\nRooms: {room}\nSort: {sort}\nEND')

    def theard():
        for room in rooms:
            for sort in sorts:
                process_page(page, sort, room)
                logging.info(f'Finished: Rooms: {room}, Sort: {sort}')
    async with lock:
        await asyncio.to_thread(theard)
