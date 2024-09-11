from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboard as kb
import app.database.requests as rq

router = Router()

contact_message = f'Зв\'язок з нами👇\n📲Номер телефону: 044111222333\n📨Email: example@gmail.com'
about_us = f'*Текст, який розповідатиме про команду магазину*🤗'

class Order(StatesGroup):
    name = State()
    size = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привіт!\nЩо Вас зацікавило в нашому магазині?😊', reply_markup=kb.main) # Звичайне повідомлення на реакцію команди /start


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Будь ласка, оберіть категорію товара👀', reply_markup=await kb.categories())
    

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Оберіть бажаний товар', reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.answer(f'Назва: {item_data.name}\nОпис: {item_data.description}\nВартість: {item_data.price}₴', reply_markup=await kb.items(callback.data.split('_')[1]))


@router.message(F.text == 'Контакти')
async def contacts(message: Message):
    await message.answer(contact_message)


@router.message(F.text == 'Про нас')
async def aboutus(message: Message):
    await message.answer(about_us)


@router.message(F.text == 'cake')
async def cake(message: Message):
    await message.answer('The cake is a lie.')


@router.message(Command('order'))
async def order(message: Message, state: FSMContext):
    await state.set_state(Order.name)
    await message.answer('Введіть, будь ласка, Ваше ім\'я')

@router.message(Order.name)
async def order_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order.size)
    await message.answer('Введіть, будь ласка, бажаний розмір')

@router.message(Order.size)
async def order_size(message: Message, state: FSMContext):
    await state.update_data(size=message.text)
    await state.set_state(Order.number)
    await message.answer('Введіть, будь ласка, Ваш контактний номер телефона', reply_markup=kb.get_number)

@router.message(Order.number, F.contact)
async def order_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше ім\'я: {data["name"]}\nОбраний розмір товару: {data["size"]}\nКонтактний номер телефону: {data["number"]}')
    await state.clear()