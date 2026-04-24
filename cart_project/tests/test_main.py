import pytest

from main import ShoppingCart
'''''
def test_adding():
    assert adding(2,3) == 5, "2 + 3 should be 5"
    assert adding(-1, 1) == 0, "-1 + 1 should be 0"
    assert adding(0, 0) == 0, "0 + 0 should be 0"


def test_dividing():

    assert dividing(10,2 ) == 5, " 10/2 should be 5"
    assert dividing(10, 20) == 0.5, "10/20 should be 0.5"
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        dividing(10,0)

def test_calculate_age():
    with pytest.raises(TypeError, match="You must be the number!"):
        calculate_age("Hello")

    assert calculate_age(1958), "2026 - 1958 should be 68"



class Test_Simple_mathematic():

    def test_adding(self):
        assert 1 + 1 == 2




class Test_Book:

    def test_get_info(self):
        #Creating our Test Object
        test_book = Book("Testowa", "Ksiazka")
        # Triggering the method and saving the test result
        test_result = test_book.get_info()

        # Creating assertion to check if it meets our expectations

        assert test_result == "Testowa by Ksiazka"


class Test_AudioBook():

    def test_play(self):

        test_audioBook = AudioBook("PSY", "Andrzej Wajda")

        test_result = test_audioBook.play()


        assert test_result == "Playing: PSY"

'''''



class Test_ShoppingCart():



    def test_add_item(self):


        test_cola = ShoppingCart()
        test_cola.add_item("cola", 10, 3)

        assert test_cola.items == {"cola": {"price": 10, "quantity": 3}}



        test_cola.add_item("cola", 10, 10)

        assert test_cola.items == {"cola":{"price": 10, "quantity": 13}}


    def test_remove_item(self):

        test_cola = ShoppingCart()
        test_cola.add_item("cola", 10, 11)
        test_cola.remove_item("cola", 10)

        assert test_cola.items == {"cola":{"price": 10, "quantity": 1}}

        test_cola.add_item("cola", 10, 10)
        test_cola.remove_item("cola", 11)

        assert "cola" not in test_cola.items

        ### Creating a test to check the code behaviour if we will try to remove item that doesn't exist,

        last_test = ShoppingCart()
        last_test.add_item("apple", 3, 10)
        last_test.remove_item("banana", 3)

        assert last_test.items == {"apple": {"price": 3, "quantity": 10}}
        assert "banana" not in last_test.items




    def test_get_total(self):


        test_total = ShoppingCart()
        test_total.add_item("cola", 10, 3)


        test_total.add_item("apple", 4, 7 )

        assert test_total.get_total() == 58









