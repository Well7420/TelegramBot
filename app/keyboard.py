from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Кошик')],
                                     [KeyboardButton(text='Контакти'),
                                     KeyboardButton(text='Про нас')]],
                                     resize_keyboard=True, input_field_placeholder='Оберіть пункт меню...')


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}")) 
        # callback_data=f"category_ щоб "ловити" усі колбеки, які починаються зі слова "category", а потім діставати з нього category.id
        keyboard.add(InlineKeyboardButton(text='На головну', callback_data='to_main'))
        return keyboard.adjust(2).as_markup()
        # adjust = регулювання клавіатури за шириною adjust(2) - ширина в дві кнопки
        # .as_markup() потрібно використовувати завжди, коли використовується from aiogram.utils.keyboard import InlineKeyboardBuilder для створення клавіатури

async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}")) 
        keyboard.add(InlineKeyboardButton(text='На головну', callback_data='to_main'))
        return keyboard.adjust(2).as_markup()
    
get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Надіслати свій номер', request_contact=True)]], resize_keyboard=True)