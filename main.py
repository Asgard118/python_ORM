import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime


from model import create_table, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:2467@localhost:5432/postgres'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)

# тут заполняются данные 
def populate_data(session):
    # Создаем издателей
    publisher1 = Publisher(name='Manga Publishing Co.')
    publisher2 = Publisher(name='Manga Central')
    
    # Создаем книги
    book1 = Book(title='Ninja Adventures', publisher=publisher1)
    book2 = Book(title='Magic Chronicles', publisher=publisher1)
    book3 = Book(title='Samurai Legends', publisher=publisher2)
    
    # Создаем магазины
    shop1 = Shop(name='Manga Emporium')
    shop2 = Shop(name='Anime Haven')
    
    # Создаем склады
    stock1 = Stock(book=book1, shop=shop1, count=50)
    stock2 = Stock(book=book2, shop=shop1, count=30)
    stock3 = Stock(book=book3, shop=shop2, count=20)
    
    # Создаем продажи
    sale1 = Sale(stock=stock1, price=9.99, count=10)
    sale2 = Sale(stock=stock2, price=7.99, count=5)
    sale3 = Sale(stock=stock3, price=12.99, count=8, data_sale=datetime(2023, 7, 10))
    
    # Добавляем объекты в сессию
    session.add_all([publisher1, publisher2, book1, book2, book3, shop1, shop2, stock1, stock2, stock3, sale1, sale2, sale3])
    
    # Сохраняем изменения
    session.commit()



#тут код для задания 2, по данным с кода выше
def main2():
    publisher_name = input("Введите имя издателя: ")
    
    publisher = session.query(Publisher).filter_by(name=publisher_name).first()
    if publisher:
        sales = (
            session.query(Sale)
            .join(Stock, Sale.id_stock == Stock.id)
            .join(Book, Stock.id_book == Book.id)
            .join(Publisher, Book.id_publisher == Publisher.id)
            .join(Shop, Stock.id_shop == Shop.id)
            .filter(Publisher.id == publisher.id)
            .all()
        )

        if sales:
            print("Название книги | Название магазина | Стоимость покупки | Дата покупки")
            print("-" * 60)
            for sale in sales:
                print(f"{sale.stock.book.title} | {sale.stock.shop.name} | {sale.price} | {sale.data_sale}")
        else:
            print(f"Нет данных о покупках книг издателя '{publisher_name}'.")
    else:
        print(f"Издатель с именем '{publisher_name}' не найден.")

if __name__ == "__main__":
    session = Session()
    def main():
        create_table(engine)
        populate_data(session)
    main2()
    session.close()






