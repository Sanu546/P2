def test():
    print("Hello, world!")
    
def original():
    print("Original function")

func = original

func()

func = test

func()

func = None

func()